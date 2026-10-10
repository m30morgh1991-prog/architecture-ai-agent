# Architecture Agent — Feature-to-File Matrix

> Baseline: `main` at `2344e1083937e5d91857ba24b6a0f077414f06ca` (H99 merge).
>
> Purpose: turn the comparison of Higharc, SketchPro, CraftBot, ArchLang, and Trace-BIM into an implementation map for this repository.
>
> This document is planning/governance evidence. It does **not** authorize bypassing CI, changing the Source of Truth, or importing external architecture wholesale.

## 1. Non-negotiable architecture

- Source of Truth remains **PlanModel + ConstraintMap + ApprovedChangePlan**.
- Images, LLM output, DXF, SVG, PDF, IFC, or Revit are representations/adapters, never the authoritative architectural state.
- Fail-closed states remain: UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW / ABSTAIN / BLOCKED.
- Constraint states remain: LOCKED / EDITABLE / CONDITIONAL / UNKNOWN.
- Logical/Static PASS, Real Runtime PASS, and Visual Runtime PASS remain distinct.
- Golden DWG files remain regression assets; native DWG/DXF editing remains outside MVP.
- Every implementation follows: **Implement → REAL CI → Verify → Regression when applicable → Persist State → Continue**.
- No external project's code, schema, or license is copied without explicit compatibility review.

## 2. Reference projects

| Reference | Primary contribution to our design |
|---|---|
| Higharc | live canonical building/BIM model; prompt-to-production workflow; synchronized downstream outputs |
| SketchPro | Revit-centric construction documentation: dimensions, tags, views, sheets, schedules, QA |
| CraftBot | multi-agent design/build/inspect/revise loop and iterative geometry generation |
| ArchLang | declarative architectural IR/compiler; deterministic SVG/DXF/PDF generation; lint/diagnostics |
| Trace-BIM | raster-to-semantic/BIM package; canonical JSON; evidence/placement/validation discipline |

## 3. Feature-to-file matrix

| ID | Feature | Reference | Existing anchor | New module/file | Dependencies | Tests / evidence | Target H | Priority |
|---|---|---|---|---|---|---|---|---|
| F01 | Architectural Intent / Brief | Higharc, CraftBot | `request_contract.py`, `ai_router.py`, `space_model_contract.py` | `architectural_intent_contract.py`, `architectural_intent.py` | request, provider policy, SpaceModel | contract + fail-closed intent tests | H100+ | P0 |
| F02 | Program / room requirements | Higharc, CraftBot | `space_model_contract.py`, `space_extraction.py` | extend SpaceModel or add `program_contract.py` only if needed | intent, room identity | explicit/scheduled room mapping regression | H100+ | P0 |
| F03 | Prompt → generative plan proposal | Higharc, CraftBot, Draftly pattern | `plan_model_contract.py`, `architectural_relations.py` | `plan_generation_contract.py`, `plan_generation.py` | intent, SpaceModel, relations, rules | deterministic fixtures + invalid/ambiguous prompt tests | H101+ | P0 |
| F04 | Deterministic geometry/layout engine | CraftBot, ArchLang, Draftly pattern | `geometry_topology_validation.py`, `spatial_topology.py` | `geometry_generation.py`, `layout_solver.py` | PlanModel, topology, constraints | topology invariants, overlap, closure, connectivity | H101+ | P0 |
| F05 | Architecture IR | ArchLang | `plan_model_contract.py`, `bim_ready_contract.py` | `architecture_ir_contract.py`, `architecture_ir.py` | PlanModel, BIM identities, relations | round-trip semantic equality + fail-closed diagnostics | H102 | P0 |
| F06 | IR validation/lint | ArchLang | `rule_engine.py`, `final_validation.py` | `architecture_ir_validation.py` | Architecture IR, RuleContext | rule/lint fixtures, UNKNOWN propagation | H102 | P0 |
| F07 | Deterministic drawing compiler | ArchLang | `drawing_standards_validation.py`, `drawing_metadata_extractor.py` | `drawing_compiler.py` + backend package | IR, standards | golden drawing fixtures + geometry checksum | H103 | P0 |
| F08 | SVG backend | ArchLang | none | `drawing_backends/svg_backend.py` | drawing IR | deterministic SVG snapshot/semantic tests | H103 | P1 |
| F09 | DXF backend | ArchLang, Trace-BIM | `golden_dwg_regression.py`, `native_dwg_structural_detection.py` | `drawing_backends/dxf_backend.py` | IR, layer standards | DXF structure/layer regression; golden assets unchanged | H103+ | P0 |
| F10 | PDF drawing-set backend | Higharc, SketchPro, ArchLang | `drawing_standards_validation.py` | `drawing_backends/pdf_backend.py` | sheet model, annotations | PDF semantic checks; page/view/title consistency | H104 | P1 |
| F11 | Dimensions generation | SketchPro | `drawing_standards_validation.py`, `scale_unit_evidence.py` | `dimension_generation.py` | scale evidence, IR, standards | dimension evidence + scale fail-closed tests | H100/H104 | P0 |
| F12 | Annotation/tag generation | SketchPro | `drawing_metadata_extractor.py`, `element_evidence_contract.py` | `annotation_generation.py` | evidence, semantic elements | annotation-to-PlanModel linkage + UNKNOWN tests | H100/H104 | P0 |
| F13 | View generation | SketchPro, Higharc | `visual_orchestration.py`, `drawing_standards_validation.py` | `view_generation.py` | IR, section/elevation semantics | view completeness + cross-view identity tests | H104 | P0 |
| F14 | Section generation | Higharc, SketchPro, CraftBot | `architectural_relations.py`, `geometry_topology_validation.py` | `section_generation.py` | cut-plane model, levels, geometry | section topology + cut-element evidence | H105 | P0 |
| F15 | Elevation generation | Higharc, SketchPro, CraftBot | `geometry_topology_validation.py` | `elevation_generation.py` | exterior boundary, openings, levels | façade/opening correspondence | H105 | P0 |
| F16 | Detail generation | SketchPro | `drawing_standards_validation.py`, knowledge/rules | `detail_generation.py` | standards, element types, IR | detail applicability + source traceability | H106 | P1 |
| F17 | Schedules | Higharc, SketchPro, Floorra pattern | `plan_model_contract.py`, `space_model_contract.py`, `bim_ready_contract.py` | `schedule_generation.py` | semantic elements, identity, properties | schedule ↔ model reconciliation | H106 | P0 |
| F18 | Sheet composition/title blocks | SketchPro | `drawing_standards_validation.py` | `sheet_composition.py` | views, annotations, schedules | sheet completeness + title metadata | H106 | P1 |
| F19 | Canonical multi-output synchronization | Higharc | `plan_model_contract.py`, `approved_change_plan_contract.py`, `post_edit_diff.py` | `output_sync.py` | PlanModel, IR, outputs | same semantic IDs across outputs; change propagation | H107 | P0 |
| F20 | BIM semantic export boundary | Higharc, Trace-BIM, buildingSMART IFC/ifcJSON | `bim_ready_contract.py`, `bim_constraint_contract.py`, `bim_constraintmap_contract.py` | `bim_export_contract.py` + IFC/ifcJSON adapters | semantic identities, relations, placement, properties | provider-neutral round trip; provenance preserved | H107 | P0 |
| F21 | Multi-agent orchestration | CraftBot | `execution_orchestrator.py`, `visual_orchestration.py`, `workflow_guard.py` | `architecture_agent_orchestrator.py`, role contracts | intent, generator, rules, inspector | deterministic role handoff + blocked-state tests | H108 | P0 |
| F22 | Designer/Researcher/Builder/Inspector roles | CraftBot | `rule_engine.py`, `final_validation.py`, `decision_trace.py` | role prompts/contracts under `runtime/agents/` | orchestrator, evidence | role isolation + evidence trace | H108 | P1 |
| F23 | Iterative propose → inspect → revise loop | CraftBot | `change_request_contract.py`, `impact_analysis.py`, `controlled_editing_runtime.py`, `bug_hunting_gate.py` | `design_iteration.py` | approved change plan, validation | bounded iterations, no silent mutation, fail-closed stop | H109 | P0 |
| F24 | Raster → semantic canonical package | Trace-BIM, Raster2Seq | `element_evidence_contract.py`, `plan_model_reconstruction.py`, `plan_understanding_core.py` | extend existing contracts; avoid duplicate canonical model; explicit Evidence→Identity→Geometry boundary | detection, geometry, scale, topology, relations | reconstruction + provenance + ambiguity regressions | H100+ | P0 |
| F25 | Placement/hosting semantics | Trace-BIM | `architectural_relations.py`, `opening_connectivity.py`, `bim_ready_contract.py` | `placement_rules.py` or RuleEngine extension | relations, BIM identities | host/opening/level consistency | H102+ | P1 |
| F26 | Evidence-backed diagnostics | Trace-BIM, ArchLang | `element_evidence_contract.py`, `architectural_relations.py`, `decision_trace.py`, `final_validation.py` | extend existing evidence/relation contracts; preserve one provenance chain | all semantic stages | provenance, confidence, contradiction and UNKNOWN propagation | continuous | P0 |
| F27 | Firm / Iran drawing standards | SketchPro + project research | `drawing_standards_validation.py`, `docs/knowledge/drawing_standards/*` | versioned rule packs under `docs/knowledge/drawing_standards/` | RuleContext, source traceability | rule fixture suite; source/version trace | H104+ | P0 |
| F28 | Architectural symbol/line/layer semantics | ArchLang/SketchPro + project research | `drawing_metadata_extractor.py`, `drawing_standards_validation.py`, `scale_unit_evidence.py` | extend H100 semantics; add `architectural_semantics_contract.py` only if required | evidence, geometry, topology, relations, PlanModel | symbol/line/layer/hatch/marker evidence + UNKNOWN propagation | H100/H102 | P0 |
| F29 | Cross-format round trip | Trace-BIM, ArchLang | `golden_dwg_regression.py`, `post_edit_diff_validation.py` | `format_roundtrip_validation.py` | DXF/SVG/PDF/BIM adapters | semantic equivalence, no geometry drift | H110 | P0 |
| F30 | Production documentation gate | SketchPro, Higharc | `production_readiness_gate.py`, `release_gate.py`, `runtime_release_gate.py` | extend existing gates | drawing set, validation, evidence | exact-head REAL CI + drawing regression | H111 | P0 |

## 4. What must NOT be duplicated

### Existing foundations to extend, not replace

- `plan_model_contract.py` — canonical semantic plan model.
- `plan_model_reconstruction.py` — reconstruction boundary.
- `plan_understanding_core.py` — detection → reconstruction → ConstraintMap.
- `architectural_relations.py` — relation boundary established by H99.
- `geometry_topology_validation.py` / `spatial_topology.py` — topology validation.
- `element_evidence_contract.py` — evidence/provenance.
- `rule_engine.py` / `rule_context.py` — rule execution boundary.
- `impact_analysis.py` — change impact.
- `approved_change_plan_contract.py` — controlled approval boundary.
- `controlled_editing_runtime.py` — controlled mutation.
- `post_edit_diff*.py` — post-change verification.
- `final_validation*.py` — final validation.
- `drawing_standards_validation.py` — drawing compliance validation.
- `bim_*_contract.py` — BIM semantic boundary.
- `bug_hunting_gate.py` / `release_gate.py` — governance gates.

Do **not** create parallel PlanModel, evidence, ConstraintMap, or release-gate systems just because an external project uses different names.

## 5. Semantic understanding chain\n\nThe architecture-understanding research adds an explicit chain that must sit inside the existing canonical pipeline:\n\n`Source Evidence → Element Identity → Geometry → Topology → Spatial Relation → Architectural Semantics → BIM Semantics → Rule Context`\n\nThe chain is an integration boundary, not a new Source of Truth. Existing evidence, PlanModel, relation, BIM, and rule contracts remain authoritative. See `docs/research/PLAN_UNDERSTANDING_SEMANTIC_CHAIN.md`.\n\n## 6. Dependency order

### Track A — generation foundation

`ArchitecturalIntent → Program → PlanGeneration → GeometryGeneration → PlanModel`

### Track B — deterministic drawing

`PlanModel → ArchitectureIR → IR Validation → DrawingCompiler → SVG/DXF/PDF`

### Track C — Phase 2

`IR → Dimensions/Annotations/Views → Sections/Elevations → Details/Schedules → Sheets`

### Track D — BIM

`PlanModel → BIM semantic layer → provider-neutral export adapters`

### Track E — agent loop

`Intent → Designer → Generator → Rule/Impact → Proposal → Inspector → Revision`

The tracks may be prepared in parallel, but implementation must respect dependency boundaries and Green Gates.

## 7. Recommended H sequencing

| Stage | Scope | Exit evidence |
|---|---|---|
| H100 | Drawing semantics + dimension/annotation evidence boundary | contract tests + fail-closed evidence |
| H101 | Generative plan/geometry boundary | deterministic generation + topology regression |
| H102 | Architecture IR + lint/diagnostics | semantic round-trip + validation |
| H103 | Drawing compiler + DXF/SVG backend foundation | deterministic output + drawing regression |
| H104 | Dimensions/annotations/views + standards integration | drawing-set semantic validation |
| H105 | Sections + elevations | cross-view geometry/identity regression |
| H106 | Details + schedules + sheets | model ↔ documentation reconciliation |
| H107 | Canonical multi-output synchronization + BIM export boundary | change propagation + BIM semantic regression |
| H108 | Multi-agent architecture roles | role trace + bounded/fail-closed handoffs |
| H109 | Iterative design/revision loop | bounded iterations + no silent mutation |
| H110 | Cross-format round-trip | semantic equivalence across representations |
| H111 | Production documentation/release gate | exact-head REAL CI + required regressions |

> H100 is treated as the immediate drawing-semantics boundary only if/when its implementation is actually present on a branch/main. This matrix does not claim a stage is green merely because it is planned.

## 8. Priority rule

P0 items are required for the core product direction. P1 items improve completeness but must not block the semantic/validation backbone.

The first implementation wave should therefore prioritize:

1. F01 Architectural Intent
2. F03/F04 Generative Plan + deterministic geometry
3. F05/F06 Architecture IR + validation
4. F07/F09 Drawing compiler + DXF
5. F11/F12/F13 documentation semantics
6. F14/F15 sections/elevations
7. F17 schedules
8. F19/F20 synchronization + BIM boundary
9. F21/F23 agent orchestration + bounded iteration

## 9. External-project lessons mapped to our architecture

### Higharc
Adopt the **canonical live model + synchronized downstream outputs** idea.

Do not adopt a proprietary/provider-bound source of truth.

### SketchPro
Adopt **documentation automation as a first-class subsystem**, not merely a renderer.

### CraftBot
Adopt **role separation and inspect/revise loops**, while keeping our deterministic gates between roles.

### ArchLang
Adopt **declarative IR + compiler + lint/diagnostics**. This is the strongest architectural pattern for deterministic drawing generation.

### Trace-BIM
Adopt **canonical semantic exchange + evidence/placement validation**, while reusing our existing PlanModel and evidence contracts.

## 10. Definition of Done for this matrix

A matrix item is not considered implemented because a file exists.

It is complete only when:

1. Contract is defined.
2. Implementation is wired to the existing canonical architecture.
3. Tests cover normal and ambiguous/failure cases.
4. Fail-closed behavior is proven where uncertainty exists.
5. Required regression is run.
6. Exact-head REAL CI is `completed / success`.
7. State is persisted in repository-backed project state.
8. No duplicate Source of Truth was introduced.

## 11. Current repository baseline

- Main head: `2344e1083937e5d91857ba24b6a0f077414f06ca`
- Current merged feature: H99 — Architectural Relations integrated with PlanModel.
- H99 merge commit: `2344e1083937e5d91857ba24b6a0f077414f06ca`.
- H99 should be treated as the current architectural-relations boundary.
- This document is a planning artifact and does not declare any future H green.


## 12. New plan-understanding research additions — 2026-10-10

Research record: `docs/research/plan-understanding-research-and-revit-ai-review-2026-10-10.md`

| Reference | Adopted lesson | Existing integration boundary | Next evidence before implementation | Priority |
|---|---|---|---|---|
| fpvec-lab / ResPlan-FP | Compare graph/junction readout, sequence reconstruction, wall/room/opening metrics, and correction cost | `plan_model_reconstruction.py`, `plan_understanding_core.py`, `geometry_topology_validation.py`, `golden_understanding_regression.py` | Reproducible scorer protocol; source/license audit per artifact; wall/room/opening fixture metrics | P0 research |
| AEC-Geometric-Bench | Separate object, wall-mask, area-mask, and area-instance scores | Golden runner/evaluator and optional benchmark adapter | Confirm exact public data terms; do not bundle CC BY-NC data; document 15-sheet public GT limitation | P0 validation |
| ConstructDrawingAI CIR | Vector-first input, canonical representation, connectivity, provenance/confidence, perception/reasoning separation | `drawing_semantic_evidence.py`, `evidence_reconciliation.py`, `plan_model_reconstruction.py`, existing PlanModel | Map concepts to current contracts; no second IR/PlanModel; no code copying under PolyForm Noncommercial | P0 architecture study |
| Raster-to-Graph | Junction and wall-segment graph as a topology reconstruction candidate | `spatial_topology.py`, `architectural_relations.py`, `geometry_topology_validation.py` | Verify dependency age, data access and licenses; benchmark against existing contract | P1 |
| FloorPlan2IFC | Segmentation → skeleton/junction graph → walls/openings → IFC pipeline | Existing PlanModel/BIM contracts and future provider-neutral export adapter | Reproduce claims independently; semantic reconciliation must precede export PASS | P1 |
| FloorPlanCAD / PerDAW | CAD line-grained symbols; door/window representations across plan/elevation | Drawing semantic evidence and Iranian drawing-language fixture suite | Rights/license, label mapping, source drawing provenance and non-commercial restrictions | P1 research |
| Drafted in Revit | Multi-option native BIM schematic generator for narrow single-storey residential use | Future H101+ generation comparator only; not an understanding core | Compare outputs and input constraints only if test environment exists; not a substitute for Iranian code validation | Comparator |
| WiseBIM AI | Existing-plan conversion to Revit objects with staged detection and user verification | Raster/vector evidence, reconstruction, opening connectivity, uncertainty handling | Measure on permitted independent plans; check scale assumptions, connection/alignment correction and privacy terms | P1 comparator |
| Autodesk Assistant / Revit Generative Design | Natural-language model/documentation actions and constrained design alternatives | Future execution adapter / design exploration only | Separate supported actions from plan-understanding claims; region and account availability checks | Context only |

### Added evaluation rules

- Never collapse wall, room, opening, symbols, topology, and Iranian-drafting semantics into a single opaque score.
- External benchmark results are research evidence only; they do not replace source-bound Golden Understanding ground truth.
- BIM/Revit/IFC export success does not prove that the source plan was correctly understood.
- Dataset/code licenses must be reviewed per artifact. Public availability does not grant commercial reuse rights.
- No H101 unlock, new provider, third-party package, dataset import, or Golden DWG modification is authorized by this research entry.
