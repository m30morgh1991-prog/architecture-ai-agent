# H101 — GeometryReference Contract

Status: implementation proposal in PR; not yet merged or integrated into the drawing-ingestion pipeline.

## Purpose

GeometryReference records how coordinate values may be interpreted. It is evidence/provenance metadata, not a geometry converter and not an approval signal. It remains attached to the original source SHA-256 and does not create a parallel PlanModel.

## Separate evidence domains

| Domain | What it means | What it does not mean |
|---|---|---|
| Linear unit | The unit represented by model coordinates: MM, CM, M, IN, FT, or UNKNOWN | Paper scale or proof that an INSUNITS header matches actual geometry |
| Coordinate frame | WCS, OCS, PDF_PAGE, IMAGE_PIXELS, IFC_LOCAL, or UNKNOWN | Proof that all entity transforms have been applied |
| Sheet scale | Ratio such as 1:100 for paper representation | A conversion factor for model-space coordinates |
| Raster calibration | Evidence-backed 3x3 pixel-to-world affine transform | A license to infer scale from image dimensions |
| Dimension reconciliation | Whether dimension evidence has been reconciled to measured geometry | Annotation text alone or dimension self-consistency |

## Fail-closed rules

- Every referenced evidence ID resolves to a typed evidence record with the same source SHA-256 and expected evidence domain.
- Every SUPPORTED state requires one or more matching evidence records whose own status is SUPPORTED.
- UNKNOWN, UNCERTAIN, and CONTRADICTED never authorize conversion.
- A paper scale ratio never changes model-space coordinates or establishes model units.
- A unit label or INSUNITS value without a matching source-hash-bound UNIT evidence record in SUPPORTED state cannot authorize metric area reporting.
- Area remains in raw coordinate-units-squared until a recognized linear unit is SUPPORTED.
- Raster calibration requires a finite, non-singular affine transform and transform evidence.
- Coordinate transforms are recorded only with evidence; this contract does not yet implement OCS/WCS or nested INSERT transform resolution.
- Dimension reconciliation remains a separate evidence domain. A supported dimension must reference actual dimension evidence.
- No geometry is normalized, edited, or promoted to LOCKED/EDITABLE by this contract.

## Integration boundary

The first implementation is intentionally a standalone runtime contract and unit-test suite. It is not yet wired into SpaceModel, PlanModel reconstruction, the Golden Understanding report, CAD extraction, PDF parsing, or IFC ingestion. Those integrations require explicit source evidence adapters and regression coverage.

## Next implementation slices

1. Add source-specific evidence adapters for DWG header/unit metadata, entity OCS/WCS and INSERT transforms, PDF page geometry, and raster calibration.
2. Bind GeometryReference to the canonical PlanModel and SpaceModel while preserving source-hash identity.
3. Extend typed dimension evidence with definition points and conservative dimension-to-geometry reconciliation.
4. Add golden regression assertions; do not change the immutable Golden DWG files.
5. Keep Windows/AutoCAD host tests NOT_RUN until a compatible user Windows host is available.
