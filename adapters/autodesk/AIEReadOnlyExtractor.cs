using System.Security.Cryptography;
#if NETFRAMEWORK
using System.Web.Script.Serialization;
#else
using System.Text.Json;
#endif
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.Geometry;
using Autodesk.AutoCAD.Runtime;

[assembly: CommandClass(typeof(AIE.Autodesk.ReadOnlyExtractor.Commands))]

namespace AIE.Autodesk.ReadOnlyExtractor;

public sealed class Commands
{
    private const string Schema = "autodesk-autocad-readonly-evidence-v1";

    [CommandMethod("AIEEXPORTREADONLY", CommandFlags.Session)]
    public void ExportReadOnly()
    {
        Document? doc = Application.DocumentManager.MdiActiveDocument;
        if (doc is null) return;
        Editor ed = doc.Editor;
        Database db = doc.Database;
        string source = db.Filename;

        if (string.IsNullOrWhiteSpace(source) || !File.Exists(source))
        {
            ed.WriteMessage("\nAIE: SOURCE_REQUIRED — save a named DWG first.");
            return;
        }
        if (doc.IsModified)
        {
            ed.WriteMessage("\nAIE: NEEDS_REVIEW — save or discard unsaved changes, then rerun.");
            return;
        }

        var options = new PromptStringOptions("\nJSON output path (must differ from source DWG): ") { AllowSpaces = true };
        PromptResult answer = ed.GetString(options);
        if (answer.Status != PromptStatus.OK || string.IsNullOrWhiteSpace(answer.StringResult)) return;
        string output = Path.GetFullPath(answer.StringResult.Trim().Trim('"'));
        if (string.Equals(Path.GetFullPath(source), output, StringComparison.OrdinalIgnoreCase))
        {
            ed.WriteMessage("\nAIE: BLOCKED — output cannot overwrite source.");
            return;
        }

        try
        {
            string before = HashFile(source);
            Dictionary<string, object?> result = ReadDatabase(db, source, before);
            string after = HashFile(source);
            if (before != after) throw new InvalidOperationException("SOURCE_CHANGED_DURING_READ");

            result["source_integrity"] = new Dictionary<string, object?>
            {
                ["sha256_before"] = before, ["sha256_after"] = after,
                ["source_mutated"] = false, ["snapshot_binding_status"] = "NEEDS_REVIEW",
                ["snapshot_binding_note"] = "Disk hash continuity is verified; in-memory database identity is not cryptographically proven."
            };
            File.WriteAllText(output, SerializeJson(result), new System.Text.UTF8Encoding(false));
            ed.WriteMessage($"\nAIE: exported read-only evidence to {output}; source DWG was not saved or modified.");
        }
        catch (System.Exception ex)
        {
            ed.WriteMessage($"\nAIE: BLOCKED — {ex.GetType().Name}: {ex.Message}");
        }
    }

    private static Dictionary<string, object?> ReadDatabase(Database db, string source, string sha)
    {
        var layers = new List<Dictionary<string, object?>>();
        var entities = new List<Dictionary<string, object?>>();
        var counts = new SortedDictionary<string, int>(StringComparer.Ordinal);

        using (Transaction tr = db.TransactionManager.StartTransaction())
        {
            var lt = (LayerTable)tr.GetObject(db.LayerTableId, OpenMode.ForRead);
            foreach (ObjectId id in lt)
            {
                var layer = (LayerTableRecord)tr.GetObject(id, OpenMode.ForRead);
                layers.Add(new Dictionary<string, object?>
                {
                    ["name"] = layer.Name, ["is_off"] = layer.IsOff,
                    ["is_frozen"] = layer.IsFrozen, ["is_locked"] = layer.IsLocked,
                    ["line_weight"] = layer.LineWeight.ToString(),
                    ["color_index"] = layer.Color?.ColorIndex
                });
            }

            var bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);
            var ms = (BlockTableRecord)tr.GetObject(bt[BlockTableRecord.ModelSpace], OpenMode.ForRead);
            foreach (ObjectId id in ms)
            {
                if (!id.ObjectClass.IsDerivedFrom(RXObject.GetClass(typeof(Entity)))) continue;
                if (tr.GetObject(id, OpenMode.ForRead, false) is not Entity e) continue;
                string type = e.GetType().Name;
                counts[type] = counts.TryGetValue(type, out int n) ? n + 1 : 1;

                var row = new Dictionary<string, object?>
                {
                    ["handle"] = e.Handle.ToString(), ["object_id"] = id.ToString(),
                    ["type"] = type, ["dxf_name"] = e.GetRXClass().DxfName,
                    ["layer"] = e.Layer, ["owner_space"] = "MODEL",
                    ["extents_wcs"] = Extents(e)
                };
                switch (e)
                {
                    case Line x:
                        row["geometry"] = new { kind = "LINE", start_wcs = Point(x.StartPoint), end_wcs = Point(x.EndPoint) };
                        break;
                    case Circle x:
                        row["geometry"] = new { kind = "CIRCLE", center_wcs = Point(x.Center), radius = x.Radius };
                        break;
                    case Arc x:
                        row["geometry"] = new { kind = "ARC", center_wcs = Point(x.Center), radius = x.Radius, start_angle_radians = x.StartAngle, end_angle_radians = x.EndAngle };
                        break;
                    case Polyline x:
                        var vertices = new List<object>();
                        for (int i = 0; i < x.NumberOfVertices; i++)
                        {
                            Point2d p = x.GetPoint2dAt(i);
                            vertices.Add(new { x = p.X, y = p.Y, bulge = x.GetBulgeAt(i) });
                        }
                        row["geometry"] = new { kind = "LWPOLYLINE", vertices_ocs = vertices, closed = x.Closed, normal = Vector(x.Normal), elevation = x.Elevation };
                        break;
                    case DBText x:
                        row["text"] = x.TextString; row["position_wcs"] = Point(x.Position); row["rotation_radians"] = x.Rotation;
                        break;
                    case MText x:
                        row["text"] = x.Contents; row["position_wcs"] = Point(x.Location); row["rotation_radians"] = x.Rotation;
                        break;
                    case Dimension x:
                        row["dimension"] = new { dimension_text_override = x.DimensionText, measurement = Measurement(x), dimension_type = x.GetType().Name };
                        break;
                    case BlockReference x:
                        string name = "";
                        try { name = ((BlockTableRecord)tr.GetObject(x.BlockTableRecord, OpenMode.ForRead)).Name; } catch { }
                        row["block_reference"] = new { name, position_wcs = Point(x.Position), rotation_radians = x.Rotation, scale = new[] { x.ScaleFactors.X, x.ScaleFactors.Y, x.ScaleFactors.Z } };
                        break;
                }
                entities.Add(row);
            }
        }

        return new Dictionary<string, object?>
        {
            ["schema"] = Schema,
            ["adapter"] = new { adapter_id = "autodesk-autocad-dotnet-readonly-v1", host_product = "AutoCAD", host_version = Convert.ToString(Application.GetSystemVariable("ACADVER")), read_only = true },
            ["source_profile"] = new { path = source, sha256 = sha, drawing_version = db.OriginalFileVersion.ToString(), insunits = db.Insunits.ToString(), coordinate_frame = "WCS_WITH_POLYLINE_OCS_DECLARED", source_class = "ENGINEERING_PLAN" },
            ["scope"] = new { space = "MODEL", entity_count = entities.Count, entity_type_counts = counts, paper_space_included = false, nested_block_definitions_expanded = false, xref_contents_expanded = false },
            ["layers"] = layers, ["entities"] = entities,
            ["authority"] = new { read_only = true, semantic_authority = false, compliance_assessed = false, generic_geometry_is_not_architectural_truth = true }
        };
    }

    private static string SerializeJson(Dictionary<string, object?> result)
    {
#if NETFRAMEWORK
        var serializer = new JavaScriptSerializer { MaxJsonLength = int.MaxValue, RecursionLimit = 256 };
        return serializer.Serialize(result);
#else
        return JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true });
#endif
    }

    private static string HashFile(string path)
    {
        using var stream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite | FileShare.Delete);
        using var sha = SHA256.Create();
        return BitConverter.ToString(sha.ComputeHash(stream)).Replace("-", "").ToLowerInvariant();
    }

    private static Dictionary<string, double> Point(Point3d p) => new() { ["x"] = p.X, ["y"] = p.Y, ["z"] = p.Z };
    private static Dictionary<string, double> Vector(Vector3d v) => new() { ["x"] = v.X, ["y"] = v.Y, ["z"] = v.Z };

    private static object? Extents(Entity e)
    {
        try
        {
            Extents3d x = e.GeometricExtents;
            return new { min = Point(x.MinPoint), max = Point(x.MaxPoint), coordinate_frame = "WCS" };
        }
        catch { return null; }
    }

    private static object? Measurement(Dimension d)
    {
        try { return d.Measurement; } catch { return null; }
    }
}
