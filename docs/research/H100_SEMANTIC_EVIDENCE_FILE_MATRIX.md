# H100 — Semantic & Drawing Evidence: Feature → File → Contract → Test

## Canonical rule

**Understanding the plan comes before generating or editing the plan.**

No feature below creates a second PlanModel. Each module emits source-bound
evidence or a deterministic reconciliation result consumed by the existing
PlanModel/ConstraintMap chain.

| Stage | Evidence / responsibility | Canonical file | Contract | Test boundary |
|---|---|---|---|---|
| Source boundary | DWG/DXF vs vector/raster PDF vs image | `runtime/input_source_contract.py` | `SourceProfile` | `tests/test_input_source_contract.py` |
| Element identity | protected architectural element candidates | `runtime/locked_element_detection.py` | existing detection/evidence contract | existing locked-element regression |
| Geometry | geometry candidates and reconstruction | `runtime/plan_model_reconstruction.py` | `PlanModel` + `ElementEvidenceBundle` | reconstruction tests |
| Topology | space boundaries/relations | `runtime/spatial_topology.py` | relation evidence | topology + H99 relation tests |
| Relations | element/space relationships | `runtime/architectural_relations.py` | `ArchitecturalRelationSet` | relation tests |
| Symbols | conventional symbols/orientation | `runtime/drawing_semantic_evidence.py` | `DrawingEvidence(domain=SYMBOL)` | H100 semantic tests |
| Linework/layers | line type/weight/layer evidence | `runtime/drawing_semantic_evidence.py` | `DrawingEvidence(domain=LINEWORK)` | semantic tests |
| Text/OCR | labels, notes, Persian annotations | `runtime/drawing_semantic_evidence.py` | `DrawingEvidence(domain=TEXT)` | provenance + unknown tests |
| Dimensions | dimension line + extension + measured geometry | `runtime/drawing_semantic_evidence.py` | `DimensionEvidence` | geometry-link tests |
| Levels | level/elevation codes and floor mapping | `runtime/drawing_semantic_evidence.py` | `LevelEvidence` | explicit-elevation tests |
| Sections | marker + direction + cut plane + references | `runtime/drawing_semantic_evidence.py` | `ViewMarkerEvidence` | fail-closed section tests |
| Elevations | elevation marker + direction + references | `runtime/drawing_semantic_evidence.py` | `ViewMarkerEvidence` | marker tests |
| Hatch | material/semantic hatch evidence | `runtime/drawing_semantic_evidence.py` | `DrawingEvidence(domain=HATCH)` | provenance/status tests |
| Structure | columns/fixed elements | `runtime/element_evidence_contract.py` | existing fixed-element evidence | golden DWG regression |
| Scale/unit | scale + units | `runtime/scale_unit_evidence.py` | existing `ScaleEvidence` | scale runtime gate |
| Title block | sheet metadata / title block | `runtime/drawing_metadata_extractor.py` + `runtime/native_drawing_evidence.py` | native evidence payload | native extraction regression |
| Provenance | source SHA + evidence reference | `runtime/drawing_semantic_evidence.py` | every evidence requires source_ref | H100 semantic tests |
| Contradiction | conflicting candidate facts | `runtime/evidence_reconciliation.py` | `ReconciliationResult` | contradiction test |
| Missing evidence | incomplete required evidence | `runtime/evidence_reconciliation.py` | `NEEDS_REVIEW` | missing-evidence test |
| BIM mapping | semantic identity/relations | `runtime/bim_ready_contract.py` | BIM-ready identity graph | existing BIM tests |
| Canonical model | final validated semantic state | `runtime/plan_model_contract.py` | `PlanModel` + `ConstraintMap` | plan-model tests |
| Golden regression | real DWG behavior | `runtime/golden_dwg_regression.py` | regression boundary | Golden DWG workflow |

## Evidence decision rule

`SUPPORTED` is allowed only when required evidence is present and no
contradiction is recorded.

`UNKNOWN` means there is not enough evidence to decide.

`NEEDS_REVIEW` means a required evidence item is missing.

`CONTRADICTED` blocks promotion to authoritative state.

The reconciliation layer never changes a fact to PASS by confidence alone.

## Iranian drawing-language coverage

The contract explicitly reserves semantic evidence for:
- conventional symbols and orientation;
- line types, thickness/weight and layers;
- room/space labels;
- dimensions and extension lines;
- level/elevation codes;
- floor-to-floor and vertical circulation;
- stair/landing/riser evidence;
- section direction and cut-plane;
- elevation markers/direction;
- hatch;
- column/structural symbols;
- scale/unit;
- title-block metadata.
