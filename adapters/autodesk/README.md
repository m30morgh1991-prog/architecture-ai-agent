# Autodesk AutoCAD Read-only Extractor

This is a host-side AutoCAD .NET plug-in plus a provider-neutral Python evidence validator.

## Supported host targets

| AutoCAD host | Target framework | Default managed API directory |
|---|---|---|
| AutoCAD 2020 | .NET Framework 4.7 (net47) | C:\Program Files\Autodesk\AutoCAD 2020 |
| AutoCAD 2025/2026 | .NET 8 Windows (net8.0-windows) | C:\Program Files\Autodesk\AutoCAD 2025 |

The two targets compile the same read-only extractor source against the host's own managed API assemblies. AutoCAD 2020 requires the .NET Framework 4.7 Developer/Targeting Pack on the build machine. Its JSON output uses the framework-provided System.Web.Extensions serializer, so no third-party JSON DLL is added to AutoCAD's process. The matching AutoCAD installation must provide AcCoreMgd.dll, AcDbMgd.dll, and AcMgd.dll.

## Build and run on Windows

For AutoCAD 2020:

    dotnet build adapters/autodesk/AIE.Autodesk.ReadOnlyExtractor.csproj -f net47 -p:AutoCADManagedDir="C:\Program Files\Autodesk\AutoCAD 2020"

For AutoCAD 2025:

    dotnet build adapters/autodesk/AIE.Autodesk.ReadOnlyExtractor.csproj -f net8.0-windows -p:AutoCADManagedDir="C:\Program Files\Autodesk\AutoCAD 2025"

Load the resulting DLL from bin\Debug\net47\ or bin\Debug\net8.0-windows\ with AutoCAD's NETLOAD command, then run AIEEXPORTREADONLY. Enter a JSON output path outside the source drawing. Validate it from the repository root:

    python -c "from runtime.autodesk_dwg_evidence_adapter import inspect_autodesk_export; print(inspect_autodesk_export('evidence.json', 'source.dwg'))"

If AutoCAD blocks the assembly, use a dedicated trusted folder configured through AutoCAD's trusted-path settings; do not weaken SECURELOAD globally.

## Safety and limits

- Requires a named, unmodified active drawing. Opens database records ForRead only.
- Writes a separate JSON file; never saves, edits, purges, explodes, binds, or overwrites the DWG.
- V1 exports Model Space entities, layers, extents, Line/Circle/Arc/Polyline geometry, DBText/MText, dimension values, and block-reference identity/transforms.
- Paper Space, recursive block definitions, xrefs, proxy/custom objects, hatch topology, and full associative-dimension resolution are out of scope.
- INSUNITS is a unit declaration, not proof of drawing scale.
- Disk hash continuity is verified, but equality between AutoCAD's in-memory database and on-disk bytes is not cryptographically proven. The Python adapter therefore keeps the result NEEDS_REVIEW.
- Generic CI validates the Python contract only. A host build and in-AutoCAD smoke test must be completed separately for each target; neither is claimed by a Python test pass.
