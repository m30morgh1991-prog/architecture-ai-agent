# Autodesk AutoCAD Read-only Extractor

This is a host-side AutoCAD .NET plug-in plus a provider-neutral Python evidence validator.

## Build and run

The first host target is AutoCAD 2025/2026 / .NET 8. Install AutoCAD and its managed API assemblies, then build on Windows:

    dotnet build AIE.Autodesk.ReadOnlyExtractor.csproj -p:AutoCADManagedDir="C:\Program Files\Autodesk\AutoCAD 2025"

Load the DLL with NETLOAD and run AIEEXPORTREADONLY. Enter a JSON output path outside the source drawing. Validate it from the repository root:

    python -c "from runtime.autodesk_dwg_evidence_adapter import inspect_autodesk_export; print(inspect_autodesk_export('evidence.json', 'source.dwg'))"

## Safety and limits

- Requires a named, unmodified active drawing. Opens database records ForRead only.
- Writes a separate JSON file; never saves, edits, purges, explodes, binds, or overwrites the DWG.
- V1 exports Model Space entities, layers, extents, Line/Circle/Arc/Polyline geometry, DBText/MText, dimension values, and block-reference identity/transforms.
- Paper Space, recursive block definitions, xrefs, proxy/custom objects, hatch topology, and full associative-dimension resolution are out of scope.
- INSUNITS is a unit declaration, not proof of drawing scale.
- Disk hash continuity is verified, but equality between AutoCAD's in-memory database and on-disk bytes is not cryptographically proven. The Python adapter therefore keeps the result NEEDS_REVIEW.
- Generic CI cannot compile or execute the host plug-in without AutoCAD's managed assemblies. AutoCAD 2027 uses .NET 10 and needs a separately retargeted build. A real host build and smoke test are required before operational acceptance.
