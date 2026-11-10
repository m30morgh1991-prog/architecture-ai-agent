# Autodesk AutoCAD Read-only Extractor Contract — v0.1

## Ownership

Autodesk is an evidence adapter only. AIE owns the canonical PlanModel, ConstraintMap, approval lifecycle, validation policy, and audit. The adapter must not create a parallel semantic graph or mutate canonical state. This is a local AutoCAD .NET integration, not the Autodesk Product Help connector and not a mandatory APS cloud dependency.

## Host implementation

The initial plug-in targets AutoCAD 2025+ / .NET 8 and runs inside the AutoCAD process using the matching managed assemblies. AIEEXPORTREADONLY requires a named, unmodified active drawing; reads Model Space entities and layer records with OpenMode.ForRead; exports entity handles/types/layers, extents, supported primitive geometry, text, dimensions, block-reference identity/transforms, drawing version, and INSUNITS; hashes the source before and after; and writes a separate JSON evidence file. It never saves the DWG.

## Python validation boundary

runtime.autodesk_dwg_evidence_adapter.inspect_autodesk_export verifies schema, entity identity, source SHA before/after/export/current disk, source_mutated=false, read_only=true, semantic_authority=false, and compliance_assessed=false. Any mismatch or malformed envelope is BLOCKED. Unknown units and unverified active-database snapshot identity remain NEEDS_REVIEW.

## Evidence and limits

V1 supports Model Space, layer state, WCS extents, Line/Circle/Arc/Polyline geometry, DBText/MText, dimension displayed text/measurement, and block-reference name/position/rotation/scale. Polyline vertices are OCS and labelled as such; no silent coordinate conversion occurs.

Paper Space, recursive block expansion, xrefs, proxy/custom objects, full associative-dimension resolution, hatch topology, architectural recognition, structural classification, and code compliance are not implemented. INSUNITS is only a declared unit, not proof of drawing scale. The active in-memory database cannot be cryptographically proven byte-identical to the disk DWG by this plug-in, so the export is not promoted beyond NEEDS_REVIEW.

## Verification

Generic CI tests the Python contract only. The C# plug-in must be built against an installed AutoCAD 2025+ managed API and smoke-tested on a disposable DWG copy. Golden DWGs remain immutable; no host test may save or overwrite them.
