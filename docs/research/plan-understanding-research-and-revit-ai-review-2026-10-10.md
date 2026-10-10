# Plan-understanding research additions and Revit AI plan-design review — 2026-10-10

## Decision summary

This is a research-to-file decision record, not a claim that the core has learned to understand these inputs. The best additions are **evaluation methods and architectural patterns**, not wholesale imports of third-party code or datasets.

1. **P0 research/evaluation: fpvec-lab / ResPlan-FP** — investigate graph-readout vs sequence reconstruction, output-level fusion, and edit-cost alongside wall/room/opening F1. Use the paper's reported results as hypotheses, not as verified results for our system.
2. **P0 external validation candidate: AEC-Geometric-Bench** — design an optional benchmark adapter for object, wall-mask, and room/area segmentation metrics. The public ground-truth subset is small and data is non-commercial; do not bundle its data into our product.
3. **P0 architecture pattern: ConstructDrawingAI CIR** — adopt the general principles of vector-first ingestion, canonical intermediate representation, per-entity provenance/confidence, explicit connectivity, and separation of perception from reasoning. Do not copy its code; repository license is PolyForm Noncommercial 1.0.0.
4. **P1 topology reference: Raster-to-Graph** — compare its junction/wall graph representation with our existing PlanModel and topology contracts; no second graph/source of truth.
5. **P1 BIM bridge reference: FloorPlan2IFC** — study its image → segmentation → skeleton/junction graph → wall/opening → IFC sequence. Treat reported metrics as author claims until independently reproduced.
6. **P1 symbol dataset candidates: FloorPlanCAD and PerDAW** — evaluate for line-grained CAD symbols and door/window depictions only after licensing, provenance, and compatibility checks.
7. **Revit product study: Drafted in Revit** — useful as a plan-generation product comparator, not a plan-understanding solution. It creates schematic single-storey single-family residential layouts from a room list and optional footprint; it does not validate Iranian code or infer semantics from an existing plan.

## Existing architecture to extend

Do not create a parallel semantic model. Keep the existing chain:

`Source Evidence → Element Identity → Geometry → Topology → Spatial Relation → Architectural Semantics → BIM Semantics → Rule Context`

Extend these current boundaries:
- `runtime/locked_element_detection.py`: preserve conservative source-modality handling and fixed-element detection; don't pretend this is a learned raster semantic model.
- `runtime/plan_model_reconstruction.py`: receive evidence-backed candidates and keep source SHA/provenance continuity.
- `runtime/drawing_semantic_evidence.py` and `runtime/evidence_reconciliation.py`: reconcile candidates, contradictions, missing evidence, and source-bound facts.
- `runtime/plan_model_contract.py`, `runtime/architectural_relations.py`, `runtime/geometry_topology_validation.py`, and `runtime/spatial_topology.py`: preserve one canonical PlanModel and validated relations/topology.
- `runtime/golden_understanding_regression.py` and the Golden runner: turn benchmark metrics into observable evidence, never into an unearned PASS.

No source in this report justifies bypassing `UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW / ABSTAIN / BLOCKED`, promoting image-only guesses to authoritative geometry, or unlocking H101. H100 remains active; H101 remains locked pending real Golden semantic ground truth and exact-head gates.

## Findings and intended integration

### A. fpvec-lab / ResPlan-FP — highest-value research direction

Source: https://github.com/Cyprinus12138/fpvec-lab  
Paper: https://arxiv.org/abs/2608.25608

**What is useful**
- It compares sequence-based reconstruction with graph readout from junction/centerline heatmaps and output-level fusion.
- Its evaluation considers walls, rooms, and openings separately, plus an edit-cost metric representing human correction effort.
- The reported ResPlan-FP benchmark has 16,998 plans with fixed/fingerprinted splits.

**What to adopt**
- Add a benchmark protocol that scores wall, room, and opening errors separately rather than one opaque plan score.
- Track topology validity and correction burden alongside pixel/instance scores.
- Evaluate graph/junction-based reconstruction as a candidate backend behind the current evidence/PlanModel boundary, not as a replacement source of truth.

**Caveats**
- Published scores are author-reported and need independent reproduction.
- The project code and its datasets have different licenses. README indicates MIT for `fpeval/` and `fpgen/`, CC BY 4.0 for ResPlan-FP, and CC BY-NC-SA 4.0 for the `skv4` derivative of CubiCasa5K. Check each artifact's actual license before use. Do not copy data or code into the product merely because the repository is public.
- This is not evidence of understanding Iranian drafting symbols, level codes, section markers, or DWG semantics.

### B. AEC-Geometric-Bench — useful external validation, with strict data boundary

Source: https://github.com/KamaiEnterprises/aec-geometric-bench

The project describes a real-construction-drawing corpus of 312 sheets, 24,771 annotated object instances, 59,328 wall shapes, and 16,112 area shapes; only 15 sheets have publicly released ground truth and a runnable scorer.

**What to adopt**
- A separate optional benchmark adapter that reports object detection F1, wall-mask quality, area-mask quality, and area-instance quality independently.
- Keep external benchmark scores separate from Golden DWG acceptance and Iranian-language acceptance.
- Use a reproducible benchmark report with dataset version, input hash, scorer version, and explicit missing-data state.

**Caveats**
- Code is Apache-2.0; data is CC BY-NC 4.0, so do not ship the dataset or rely on it for commercial product training without separate permission.
- The public subset is small, and annotations are reported as single-annotator; this is a research cross-check, not a sole acceptance gate.

### C. ConstructDrawingAI CIR — architecture pattern only

Source: https://github.com/A-SHOJAEI/ConstructDrawingAI  
Architecture: https://github.com/A-SHOJAEI/ConstructDrawingAI/blob/main/docs/ARCHITECTURE.md  
CIR: https://github.com/A-SHOJAEI/ConstructDrawingAI/blob/main/docs/CIR.md

Useful ideas:
- vector-first ingestion with raster fallback and tiling;
- a canonical drawing representation with explicit drawing-set/sheet/view/entity and connection relationships;
- per-entity confidence and provenance;
- specialist perception and connectivity before a separate reasoning layer;
- grounding to BIM/IFC concepts without collapsing perception and semantic authority.

**Integration decision:** map these concepts to the existing DrawingEvidence → CandidateFact → PlanModel → relations/BIM path. Do not import its CIR as a second canonical schema or copy code: repository license is PolyForm Noncommercial 1.0.0.

### D. Raster-to-Graph — topology comparison

Source: https://github.com/SizheHu/Raster-to-Graph

Useful as a reference for junctions, wall segments, and graph prediction from raster floor plans. Before implementation, inspect current dependency compatibility, dataset access, and licenses. Only take the representation/evaluation lesson if it improves existing topology contracts; do not create a parallel graph authority.

### E. FloorPlan2IFC — perception-to-BIM adapter study

Source: https://github.com/pj1840/floorplan2ifc

The described pipeline is image → semantic segmentation → skeleton/junction graph → wall centerlines/openings → IFC entities. The README's reported wall/door/window IoUs and geometry-verification figures are author claims, not independently verified by this project.

**Integration decision:** use as a design reference for a future provider-neutral BIM adapter and end-to-end benchmark. Do not treat IFC export as proof that the input plan was correctly understood.

### F. FloorPlanCAD and PerDAW — targeted symbol datasets

- FloorPlanCAD: https://floorplancad.github.io/
- PerDAW: https://github.com/alexandru-filip/perdaw-dataset

Potential value:
- FloorPlanCAD: vector CAD drawings and line-grained symbol annotations.
- PerDAW: door/window representations across plan and elevation views.

Before any use, verify license, source-drawing rights, redistribution rules, dataset download terms, and whether labels match Iranian conventions. FloorPlanCAD annotations are described as CC BY-NC 4.0 and source drawing rights are not owned by the authors; do not use it as a commercial training corpus without permission. Dataset availability does not equal permission to bundle it.

## Revit AI plan-design software review

### 1. Drafted in Revit — likely the plan generator previously mentioned

Official product: https://www.drafted.ai/revit  
Autodesk App Store: https://apps.autodesk.com/en/Detail/Index?id=543d8db6-6f0c-4bbe-88f6-15778b5dc58a  
Requirements/scope: https://www.drafted.ai/learn/docs/revit/requirements-and-scope

The vendor says it returns five editable native Revit schematic designs in roughly 45 seconds from a room list and optional traced footprint. Its generated elements include walls, doors, windows, floors, roofs, Revit Rooms and some dimensions/finishes. The official scope is single-family, single-storey residential; multi-storey, multi-family, and commercial design are outside the current scope. Stairs, structural framing, MEP, ceilings, and schedules remain manual. It requires Windows 10/11 64-bit, Revit 2025–2027, a free Drafted account, and internet access during generation. The vendor states that it sends the created design inputs (room list, footprint, settings), not the existing Revit model or its file paths. Confirm the current privacy terms directly before sending sensitive project data.

**Strengths for comparison**
- Produces editable BIM objects rather than a flat concept image.
- Generates several alternatives quickly and supports early schematic exploration.
- Lets a designer continue in the native Revit workflow and export through Revit.

**Important limitations**
- It is a generator, not an interpreter of existing Iranian plans.
- It explicitly does not check building-code compliance.
- It is not suitable evidence for multi-storey circulation, stair counts, section/elevation semantics, Iranian drafting conventions, or preservation of existing locked geometry.
- Internet and account requirements mean it should not be treated as a provider-neutral/offline core for our product.

### 2. WiseBIM AI — different task: convert existing 2D plans into Revit

Official listing: https://marketplace.autodesk.com/apps/ecaecc60-e0de-452d-8ccf-88c96dbe6486  
Help: https://apps.autodesk.com/en/Detail/HelpDoc?appId=7792821748025964445&appLang=en&os=Win64

WiseBIM is a closer comparator for *plan interpretation*: it takes DWG/DXF/PDF/JPEG/TIFF/PNG plan inputs, asks the user to set scale, then detects walls, openings, slabs and spaces in server-side stages. Its own instructions tell the user to check wall connections/alignment and adjust geometry/families after detection. It requires internet access. This makes it a useful workflow comparator for perception plus human verification, but not proof of accuracy on Iranian plans or of semantic understanding of section markers, levels, and local code.

### 3. Autodesk Assistant and Generative Design — adjacent capabilities, not equivalent products

Official Assistant help: https://help.autodesk.com/cloudhelp/2027/ENU/Revit-Assistant/files/GUID-620ECD98-53F7-47F1-B700-EEE84F15EBF7.html  
Autodesk AI overview: https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/What-AI-features-are-available-in-Revit.html

Autodesk Assistant supports natural-language help, querying a model, and supported model/documentation actions such as creating a floor-plan view or schedules. Revit Generative Design explores alternatives based on supplied goals and constraints. Neither should be conflated with an independently validated engine for understanding arbitrary existing plans.

### Relevance to our product

| Capability | Drafted | WiseBIM | Architecture AI Agent target |
|---|---|---|---|
| Generate new schematic house options | Yes, narrow residential scope | No; primarily conversion | Later, after understanding/rules/gates |
| Interpret existing 2D plan | Not its main task | Yes, object reconstruction workflow | Core priority |
| Native editable BIM output | Yes, Revit-native | Yes, Revit elements | Provider-neutral PlanModel first; BIM adapters later |
| Prove Iranian code compliance | No | Not established | Rules need sourced, versioned validation |
| Understand levels/stairs/section directions | Not established; stairs excluded | Not established by public docs | Explicit evidence domains, fail-closed |
| Work without internet | No for generation | No for detection | Provider-neutral; offline/local path where feasible |
| Preserve locked existing geometry with audit | Not its stated use case | Requires post-detection checking | Mandatory controlled-change contract |

## Proposed measurable acceptance criteria (for future implementation PRs)

1. **Separate metrics:** report wall, room/area, opening, and symbol metrics separately; no aggregate score may hide a failing domain.
2. **Topology:** measure connected components, open/closed wall junctions, room-boundary closure, door-to-wall hosting, and opening/wall consistency.
3. **Provenance:** each promoted semantic fact references source hash, source modality, evidence ID, method, and confidence/uncertainty state.
4. **Fail-closed:** absent, conflicting, malformed, or unsupported evidence remains UNKNOWN/SOURCE_REQUIRED/NEEDS_REVIEW/ABSTAIN/BLOCKED; tests must assert no unsafe PASS.
5. **Human correction burden:** track edits needed to correct a reconstruction when reliable ground truth exists; keep this separate from detection F1.
6. **Iranian drawing language:** a distinct locally authored/verified fixture suite is required for level codes, stair/landing elevations, section markers and direction, dimensions/scale, room tags, and line/layer conventions. Generic foreign datasets cannot satisfy this criterion.
7. **BIM semantics:** IFC/Revit export success is not semantic PASS; reconcile identities, hosts, levels, spaces, and opening relationships after export.
8. **Golden gate:** never modify the preserved Golden DWG assets. Use additional derivative/adversarial fixtures and source-bound expected evidence. H101 stays locked until H100 acceptance is supported by actual semantic ground truth and exact-head required checks.

## Licensing and implementation guardrails

- Public GitHub access is not blanket permission to copy code or data.
- Prefer reproducing general ideas in our own provider-neutral contracts and writing adapters; keep non-commercial datasets out of product artifacts unless permission is obtained.
- Pin source URL, access date, version/commit where known, license per artifact, intended use, restrictions, and evidence status in future dataset records.
- Do not download or commit benchmark datasets until a separate licensing review approves the exact files.
- No new package, model, runtime provider, or external dataset is introduced by this document.
