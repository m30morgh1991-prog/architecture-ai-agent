# GitHub Research — Floor-Plan Understanding Core
Date: 2026-11-13
Status: Research inventory; no external model or dataset is adopted by this document.

## Executive decision

Keep the product core vector-first, evidence-backed, graph-based, and provider-neutral. Do not import a monolithic floor-plan model or any non-commercial pretrained weights. Use external repositories as bounded components or research references only after reproducible tests on our own licensed drawings.

The strongest near-term candidates are:
1. HAWP and DeepLSD for image-derived line/junction proposals only.
2. CubiCasa5k-Next as an optional raster segmentation research baseline, trained on data we are allowed to use commercially.
3. ResPlan's MIT-licensed graph utilities and typed edge vocabulary as a reference for topology QA, not as an authority for our connectivity decisions.
4. IfcOpenShell as a later optional, read-only IFC evidence adapter; it is not a floor-plan recognition model.

No candidate in this inventory is approved for direct production integration.

## Research method and caveat

The public plan-extract catalogue (research snapshot dated 2026-10-07) indexes roughly 120 implementations across raster segmentation, vectorisation, graph reconstruction, CAD primitive classification, OCR, multimodal parsing, and datasets:
https://github.com/bbl-dres/plan-extract/blob/main/docs/solutions-open.md

Its methodology explicitly says the cataloguer did not download, clone, or run the listed projects. We therefore use it as a discovery index, then independently inspect the selected repositories' README and LICENSE files. This document records static repository review only; it does not claim runtime, accuracy, or security validation.

## Candidate review

| Candidate | Verified code licence / input | Useful contribution | Limits and decision |
|---|---|---|---|
| HAWP — https://github.com/cherubicXN/hawp | MIT; image line/junction detection | Propose line segments and junction candidates in raster plans | Generic wireframe detector, not architectural semantics. Research baseline only; retrain/evaluate on our own permitted plan renders. |
| DeepLSD — https://github.com/cvg/DeepLSD | MIT; image line detection/refinement | Improve line proposals and geometric line consistency | Generic line detector; repository reports older Python/CUDA toolchain. Optional image-lane experiment, not required runtime. |
| CubiCasa5k-Next — https://github.com/Lqm1/CubiCasa5k-Next | Apache-2.0 code; raster to junction heatmaps, room/icon logits and post-processed geometry | Modern clean-room implementation of a multi-task floor-plan parsing approach | README requires Python 3.13 and PyTorch 2.x; no pretrained weights are released. The code licence does not grant rights to external datasets. Candidate for isolated experiments with our own licensed training data. |
| Floor Plan Document Intelligence — https://github.com/alifarzadjamali/floor-plan-document-intelligence | MIT code; raster + SVG annotations | Reproducible segmentation/OCR/polygon pipeline and review-aware JSON output | Its documented experiments use CubiCasa5K. Do not use CubiCasa-derived data or weights commercially; inspect code-only reuse separately. |
| Raster-to-Vector — https://github.com/art-programmer/FloorplanTransformation | MIT code; raster-to-vector structural graph | Junction/segment constraints and integer-programming formulation for closed room loops and openings on walls | Original implementation is Torch7-era and low-resolution/Manhattan-oriented; its PyTorch port is described as not well-tested. Reuse the formulation as a design reference, not the old runtime or weights. |
| RoomFormer — https://github.com/ywyue/RoomFormer | MIT code; top-down density maps from 3D scans to room polygons | Structured polygon prediction and multi-room reasoning | Its primary input is density maps from 3D scans, not ordinary 2D DWG/PDF plan sheets. Not selected for the MVP recognition pipeline. |
| ResPlan — https://github.com/m-agour/ResPlan | MIT code; graph utilities; dataset separately CC BY 4.0 | Room graph vocabulary and graph QA ideas, including via-door, adjacency, via-window and direct relations | Residential listing-derived data is not representative of Iranian engineering drawings. Use code/reference only after reviewing individual functions; never use heuristic graph edges as approval-grade connectivity. |
| IfcOpenShell — https://github.com/IfcOpenShell/IfcOpenShell | LGPL-3.0-or-later core library; IFC parsing and geometry support | Read IFC entities, spatial decomposition, containment, properties, placements and relationships | Large optional dependency; not a 2D raster/CAD recognition engine. Future isolated read-only IFC adapter only; keep BIM evidence separate from geometric truth until reconciled. |
| FloorPlanMaster — https://github.com/TheGingeros/floorplanmaster | Blender plugin | Structural graph / room graph concepts | Blender authoring plugin, not a suitable dependency for our read-only plan-understanding core. |

## Licensing boundary

- CubiCasa5K repository/data: CC BY-NC 4.0. Treat it as non-commercial; do not train, ship, or validate a commercial product using its weights/data without separate permission.
- FloorPlanCAD and ArchCAD sources listed in the research catalogue are also non-commercial or research-restricted. Do not assume a permissive code licence makes the dataset or trained weights commercially usable.
- Floor Plan Document Intelligence's MIT licence covers its code, not CubiCasa5K source annotations or derivatives.
- CubiCasa5k-Next's Apache-2.0 code licence does not license third-party training data or guarantee that its model weights exist.
- ResPlan explicitly separates MIT code from CC BY 4.0 dataset terms. The dataset's underlying source drawings are not included; do not treat its data licence as a blanket licence over original plans.
- IfcOpenShell is LGPL-3.0-or-later; any distribution/integration needs the usual LGPL compliance review. Bonsai is GPL-3.0-or-later and is not required by our product.
- The selected code repositories' current LICENSE files were inspected during this review. This is not a substitute for legal review of future versions, model cards, fonts, submodules, and data provenance.

## Recommended architecture for our core

The literature and implementations converge on a structural representation:
- typed junctions;
- wall/structural segments connecting junctions;
- openings attached to host walls;
- spaces represented as closed cycles/faces of the structural graph;
- a dual spatial graph whose nodes are spaces and whose edges encode evidence-backed relations.

This is compatible with our existing PlanModel + ConstraintMap + SpaceModel direction. It is not a reason to create a second semantic graph.

### Source lanes

1. Vector engineering input: preserve native entity identity, geometry, layer/block/text/dimension evidence, drawing units, OCS/WCS, INSERT transforms, source hash, and view/sheet context.
2. Raster/vector-PDF input: crop the actual plan view first; detect line/junction proposals; extract OCR and dimensions; vectorize only as candidate geometry. Keep image-model outputs as evidence, never direct edit permissions.
3. BIM input: read IFC semantic entities and relationships into source-bound evidence; do not generate or edit a 3D model. Reconcile IFC identities against the 2D drawing rather than assuming they match.
4. Reconciliation: combine independent signals (native CAD entity, layer/block name, geometry/topology, OCR label, dimensions, schedule, BIM relationship). Contradictions remain explicit.
5. Canonical output: PlanModel, ConstraintMap, SpaceModel and ApprovedChangePlan remain the only authoritative project contracts.

### Graph rules

- Shared boundary is not the same as walkable connectivity.
- A door/window insertion point alone never creates a connection.
- A connected-by-opening candidate requires a verified native opening span, a verified host wall, two distinct space boundaries, and source-bound evidence IDs.
- Even a complete candidate remains UNKNOWN/NEEDS_REVIEW until a downstream contract validates semantics.
- Never add a nearest-neighbour fallback edge merely to make the room graph connected.
- Preserve disconnected, blocked, unknown and contradictory relations; do not force a connected graph.

## Gaps confirmed in our current repository

1. DWG geometry extraction is read-only and evidence-oriented, but coordinate-frame/OCS/WCS/INSERT reconciliation is still incomplete.
2. Door/window semantics are still UNKNOWN in the Golden DWG evidence export.
3. Dimension-to-geometry reconciliation and full associative dimension resolution remain pending.
4. The existing SpaceModel records raw numeric geometry but does not explicitly carry a validated coordinate-frame/unit/scale contract. Area and length must not be presented as metric or compliance-grade until this is addressed.
5. The BIM contracts represent identity/relations and constraint bindings, but an IFC ingestion adapter is not yet implemented.
6. Raster recognition lacks a licence-clean, project-owned training corpus and a benchmark covering Iranian drafting styles.
7. Empty detector output currently exposes a core contract gap: PlanModel reconstruction can have unresolved required element types but no evidence records; PlanUnderstandingCore then has no evidence IDs to place in ConstraintMap. This PR adds explicit source-bound UNKNOWN detector-gap records without claiming that the element is absent.
8. Opening connectivity previously treated a non-empty host_wall_id as verified when the wall inventory was absent; PR #135 adds the missing inventory/evidence guard.

## Evaluation plan

Every candidate must be evaluated separately on:
- wall/column/door/window precision and recall;
- junction and segment F1 at declared geometric tolerances;
- room polygon IoU and room-count error;
- adjacency and via-door graph precision/recall;
- geometric closure and topology consistency;
- OCR character error and label-to-space association;
- dimension-to-geometry residual;
- scale/unit correctness and coordinate-frame correctness;
- performance by drawing style, source type, rotation, line weight, language, and complexity;
- false-PASS count (target: zero).

Keep Golden DWGs immutable. Add a separately versioned, source-hash-bound annotated benchmark with explicit rights to use each sample commercially. Split by source/project to prevent near-duplicate leakage. Record model code licence, weight licence, training-data licence, and dependency licences independently.

## Adoption decisions

- Adopt now: evidence-first typed geometry and dual-graph architecture; retain the existing canonical contracts.
- Prototype next: optional HAWP/DeepLSD line proposals and CubiCasa5k-Next segmentation using only our own commercially usable synthetic or authorized drawings.
- Reuse selectively: ResPlan graph QA concepts and Raster-to-Vector constraint formulation after independent tests and code review.
- Defer: RoomFormer as its native input is 3D scan density; full IfcOpenShell adapter until the 2D evidence contracts are stable.
- Reject for commercial training: CubiCasa5K, FloorPlanCAD and other non-commercial/research-only datasets unless separate written commercial permission is obtained.

## Research status

STATIC_REPOSITORY_REVIEW_ONLY
NOT_RUNTIME_TESTED
NO_EXTERNAL_MODEL_ADOPTED
NO_DATASET_IMPORTED
NO_GOLDEN_DWG_MODIFIED
