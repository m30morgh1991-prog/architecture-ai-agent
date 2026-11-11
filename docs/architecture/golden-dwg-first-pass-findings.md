# Golden DWG Read-only Evidence — First-pass Findings

Date: 2026-10-12
Scope: read-only inspection of the two immutable Golden DWG inputs using the CI evidence artifact. This is an evidence inventory, not a plan interpretation or regulatory compliance assessment.

## Source integrity

| Case | Source | SHA-256 | Extractor source mutated |
|---|---|---|---|
| GOLDEN-DWG-BAGHERI7 | `test-assets/golden-projects/bagheri7.dwg` | `865244d69e260d9ad23abed7b3ecaeb4df8b5f7da562c8d0284b466f3da13e6a` | No |
| GOLDEN-DWG-AFIFIIIII | `test-assets/golden-projects/afifiiiii.end.edit3.dwg` | `508673cf44661b8b46fbb7f98992fffc99bd7d87531c1011fc5b8139d65a11a5` | No |

## Evidence inventory

| Metric | bagheri7.dwg | afifiiiii.end.edit3.dwg |
|---|---:|---:|
| Model-space entity total | 13,205 | 72,922 |
| Direct geometry rows preserved | 9,737 | 72,520 |
| DIMENSION entities | 60 | 8 |
| TEXT/MTEXT rows | 801 | 100 |
| Distinct block names reported | 55 | 23 |
| Parser layer-count entries | 0 | 0 |
| Raw `$INSUNITS` | 1 | 1 |
| Header declared units | inches | inches |
| Parser-reported units | inches | inches |
| Declared metadata status | SUPPORTED | SUPPORTED |
| Effective geometry units | NEEDS_REVIEW | NEEDS_REVIEW |
| Plot scale | UNKNOWN | UNKNOWN |
| Compliance verdict | NOT_ASSESSED | NOT_ASSESSED |

Autodesk defines INSUNITS for automatic scaling of inserted blocks, images, and xrefs; it is not proof that all existing model-space geometry was drawn at the corresponding physical scale. See https://help.autodesk.com/cloudhelp/2025/ENG/AutoCAD-Core/files/GUID-A58A87BB-482B-4042-A00A-EEF55A2B4FD8.htm

## Dimension evidence requiring review

The extracted dimension actual-measurement values are coordinate-unit numbers with blank displayed dimension text in the current parser output; all are marked `NEEDS_REVIEW`. Examples:
- bagheri7: 1.0, 1.2, 1.9, 2.2, 3.3, 4.9, 6.4, 10.1, 15.18, 18.16, 25.75, 30.01, 38.96, plus fractional/irregular values.
- afifiiiii: 0.8, 1.2, 3.18, 21.14 (repeated dimension sets).

These values must not be called meters, centimeters, inches, parking widths, or parking lengths without associating each dimension to its displayed text/style, geometry endpoints, view/layout, and an independently confirmed reference.

## Text evidence

The afifiiiii file contains repeated text candidates `EXPANSION JOINT=8` and `CM`; these are useful clues but do not establish global drawing units or parking geometry. The bagheri7 text contains many `ROOM` and `EXPANSION JOINT` labels and a `TYPICAL FRAMING PLAN` label. Text may belong to repeated blocks or non-parking details. No semantic classification is authorized from these strings alone.

## Risks and gaps

1. The extractor's layer-count map is empty despite geometry rows containing entity types. Layer metadata extraction needs investigation before layer-based reasoning can be trusted.
2. Entity evidence is primarily model-space; block INSERT contents, paper-space layouts, viewport scales, plot settings, dimension styles/overrides, and block unit declarations are not yet comprehensively reconciled.
3. Geometry extents are not plan extents until unrelated details, repeated drawings, non-plan content, and Z/elevation effects are separated. The bagheri7 header bounds span X≈69.94..1974.14, Y≈−314.66..363.33, Z≈−10.8..1500.872; afifiiiii spans X≈37.76..126.86, Y≈5.86..51.95, Z=0. These are raw bounds only.
4. Current extraction does not prove which geometry belongs to parking stalls, ramps, columns, walls, or a particular plan view.
5. Current official Shiraz local requirements and applicable approval date have not been verified in this artifact; no compliance result should be produced.

## Next controlled steps

1. Keep both Golden DWGs immutable and verify hashes before/after every read.
2. Extend evidence to include entity layer names directly, layer-table metadata, block INSERT transform/scale and block contents, dimension-style fields/overrides, and layout/viewport/plot scale metadata where the parser supports them.
3. Add a read-only geometry clustering/index report (coordinates, extents, repeated groups) without naming clusters as rooms/parking/walls.
4. Produce candidate reference dimensions with source handle, actual measurement, dimension definition points, associated text/style, and nearby geometry; label all associations as candidates until reviewed.
5. Ask the user to confirm unusual measurements with plan context before interpreting them.
6. Verify the current official Shiraz rules and edition/amendments before any rule-based parking assessment.
7. Keep effective units, semantic labels, and compliance fail-closed until independent evidence is available.

Status: `EVIDENCE_INVENTORY_COMPLETE; SEMANTIC_INTERPRETATION_NOT_APPROVED; COMPLIANCE_NOT_ASSESSED`.
