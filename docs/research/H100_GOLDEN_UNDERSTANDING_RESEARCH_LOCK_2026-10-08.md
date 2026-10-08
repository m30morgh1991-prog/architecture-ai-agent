# H100 — Golden Understanding Research Lock (2026-10-08)

## Decision

Do not treat Golden Understanding Regression as a simple image-to-label regression. The authoritative unit is a source-bound understanding report evaluated across source classification, element identity, geometry, topology, spatial/architectural relations, drawing-language semantics, OCR/text, dimensions, levels/elevations, section/elevation markers, vertical circulation, BIM mapping, provenance, contradiction handling, uncertainty and fail-closed behavior.

Understanding remains a prerequisite for generation/editing.

## Research findings

### Public benchmarks
- CubiCasa5K: 5,000 raster/SVG floorplans with 80+ object categories and dense polygon annotations. Useful for raster semantic/geometry calibration, but not sufficient for engineering drawing language.
- ResPlan: 17,000 vector residential plans with metric coordinates, walls, doors, windows, rooms and four typed connectivity relations. Useful for semantic labeling, topology and relation regression. It also reports regional limitations and near-duplicate leakage.
- MLStructFP: 954 large-scale multi-unit plans with wall polygons; useful for larger/complex layouts.
- MSD: more than 5.3K medium/large building-complex floorplans with image, geometry and graph modalities; useful for escaping an apartment-only benchmark.

### Recent AEC benchmarks
AECV-Bench (2026) evaluates realistic AEC drawings through object counting and drawing-grounded QA covering OCR, counting and spatial reasoning. Its results show that symbol-centric understanding remains much harder than text/OCR.

ArchPlanVQA (2026) reports only about 33–38% semantic understanding accuracy for current general VLMs on architectural CAD drawings. Therefore VLM answers cannot be accepted as authoritative without structured evidence and geometric checks.

ArchSpatialBench separates basic semantics, single-drawing spatial reasoning, cross-drawing plan/section/elevation coordination and geometric precision. This maps directly to our required understanding layers.

### Graph/topology
ResPlan evaluates graph nodes and typed edges using precision, recall and F1. Recent floorplan vectorization work also supports separating perception from deterministic/reconciled geometric readout.

Therefore Golden Understanding must score node detection, relation detection, relation type, topology validity, room closure and opening-to-wall attachment separately.

### Engineering validity
Recent vectorization research evaluates structural validity separately from IoU/F1. A visually plausible overlap can still be an invalid engineering topology.

Our regression therefore needs hard checks for closed room boundaries, wall connectivity, opening attachment, impossible intersections, coordinate consistency, units/scale when claimed, valid relation endpoints and provenance.

### Evidence-gated workflows
Recent evidence-gated floorplan parsing research explicitly retains semantic objects, vectors, relations and review/recovery traces. This supports our rule that residual uncertainty and review states must remain explicit instead of being silently discarded.

## Golden truth model

A Golden case should contain:

- source_profile
- expected_elements
- expected_geometry
- expected_topology
- expected_relations
- expected_drawing_evidence
- expected_text
- expected_dimensions
- expected_levels
- expected_view_markers
- expected_vertical_circulation
- expected_bim_mapping
- expected_uncertainties
- expected_contradictions
- expected_missing_evidence
- expected_fail_closed_decision

Every expected fact needs a provenance class:
- DIRECT: explicitly present in the source;
- DERIVED: deterministic derivation from validated evidence;
- INFERRED: multi-evidence inference;
- UNKNOWN: intentionally not asserted.

Only DIRECT and validated DERIVED facts may become authoritative without review.

## Evaluation model

Use a multi-axis scorecard, not one aggregate accuracy:

1. Source correctness: exact source-classification accuracy.
2. Element detection: precision/recall/F1 with class-aware matching.
3. Geometry: boundary IoU plus boundary/centerline F1 and tolerance checks.
4. Topology: graph validity, connected components, room closure and wall-junction validity.
5. Relations: per-relation precision/recall/F1 and relation-type accuracy.
6. Semantic labels: macro-F1 so rare/safety-critical classes are not hidden by micro accuracy.
7. OCR/text: exact match where appropriate plus normalized semantic match.
8. Dimensions: line detection, value, unit and measured-geometry association.
9. Levels/elevations: label/elevation correctness and floor association.
10. Section/elevation markers: marker, direction/cut-plane, target/reference correctness.
11. BIM semantics: class mapping and relation consistency.
12. Evidence provenance: every authoritative fact must point to source evidence.
13. Contradiction detection: false acceptance of contradictory facts is a hard failure.
14. Abstention/fail-closed: correct abstention rate, unsafe acceptance rate and false-PASS rate.

False-PASS is more important than maximizing raw recall.

## Dataset strategy

### Tier 1 — Public calibration
CubiCasa5K, ResPlan, MLStructFP, MSD and relevant architectural symbol/drawing datasets.

### Tier 2 — Architecture AI Agent Golden Set
Use preserved Golden DWGs, engineering/vector PDFs, raster PDFs, JPG/PNG/WEBP, Iranian architectural drawings, and coordinated plan + section + elevation cases.

### Tier 3 — Adversarial
Low resolution, skew/rotation, thick/thin walls, curved/slanted walls, furniture-heavy plans, dense dimensions, unreadable OCR, contradictory dimensions, missing scale, ambiguous level codes, section lines crossing plans, multiple floors, incomplete openings and unusual Iranian conventions.

### Tier 4 — Cross-source generalization
Where possible, represent the same semantic case through different source modalities to detect source-specific overfitting.

## Benchmark hygiene

Public benchmark scores must not automatically become project acceptance thresholds. Known dataset issues include regional bias, annotation assumptions, normalized wall thickness, duplicate/near-duplicate plans and limited multi-floor coverage.

Golden cases must be independently versioned and provenance-controlled. Train/test contamination must be prevented with content fingerprints and source-level separation.

## Hard blockers

A Golden Understanding release is not green if any of these occur:

1. false PASS on contradictory evidence;
2. authoritative fact without provenance;
3. source-bound evidence mismatch;
4. invalid topology marked understood;
5. unsupported dimension/level/section semantics marked SUPPORTED;
6. UNKNOWN or NEEDS_REVIEW silently accepted;
7. missing regression coverage for a required semantic domain;
8. test-set contamination or duplicate leakage.

## Proposed Understanding Gate

UG-01 Golden case manifest exists.
UG-02 Ground-truth schema is source-bound and versioned.
UG-03 End-to-end Understanding Runner emits a machine-checkable report.
UG-04 All required semantic domains have expected truth or explicit UNKNOWN.
UG-05 Public benchmark calibration is separated from project acceptance.
UG-06 Adversarial cases exist for every fail-closed category.
UG-07 Metrics are computed per domain, not only globally.
UG-08 False-PASS and unsafe-acceptance checks are hard blockers.
UG-09 Exact-head REAL CI + Runtime + Bug Hunt are required.
UG-10 Only after UG-01..UG-09 pass may H101/generation begin.

## Research conclusion

The research does not justify a single giant Understanding model.

It supports the architecture already chosen:

Source → Evidence Extraction → Element Identity → Geometry → Topology → Relations → Architectural Semantics → BIM Semantics → Reconciliation → Provenance/Confidence → Contradiction/Missing Evidence → PlanModel

The next implementation step is Golden Understanding Regression, specifically as an Understanding Gate around the canonical PlanModel, not as another model or semantic graph.

## External evidence used

CubiCasa5K; ResPlan; MLStructFP; MSD; AECV-Bench; ArchPlanVQA; ArchSpatialBench; recent evidence-gated floorplan parsing/vectorization research; recent floorplan vectorization work on geometry emission versus graph readout/reconciliation.

All external datasets are calibration inputs. None replaces the project's own source-bound Golden Understanding truth.
