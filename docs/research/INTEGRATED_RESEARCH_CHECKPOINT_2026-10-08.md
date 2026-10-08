# Integrated Research Checkpoint — 2026-10-08

## Purpose

Consolidate the architecture-agent research completed on 2026-10-07/08 into the repository so future implementation stages use one canonical project direction.

## 1. External architecture-agent findings

The reviewed projects reinforce a common architecture:

- **JMU** — scene-graph / relation-oriented representation; useful for explicit element and relationship modeling.
- **RedrawAI** — raster → wall graph → openings → validation; useful for image evidence, uncertainty handling, and staged reconstruction.
- **Draftly** — semantic intent → deterministic geometry; useful for keeping language/intent separate from deterministic geometric construction and for incremental edits.
- **CraftBot** — knowledge/skills + feedback loop; useful for structured architectural knowledge and iterative inspection/revision.
- **dwg-bim_AI** — CV segmentation → CAD/BIM/IFC; useful as a bridge pattern between visual detection and BIM-ready semantics.

### Transfer rule

These projects are references, not sources of truth. Their useful capabilities must enter the existing canonical chain:

**Source Evidence → Element Identity → Geometry → Topology → Spatial Relation → Architectural Semantics → BIM Semantics → Rule Context → PlanModel/ConstraintMap → Impact/Validation → ApprovedChangePlan**

No second PlanModel and no duplicate BIM/evidence graph should be introduced.

## 2. YQArch / AutoCAD execution research

YQArch was reviewed as an **Execution Adapter candidate**, not as the project brain.

Observed useful capabilities:

- large AutoCAD command/tool surface;
- architectural primitives and drafting-oriented operations;
- command registry/capability discovery;
- calculation/listing helpers;
- potential future MCP/AutoCAD execution integration.

Architecture decision:

- **PlanModel remains Source of Truth.**
- YQArch/autocad-MCP capabilities belong behind a **Capability Registry / Execution Adapter**.
- LLM must not directly emit arbitrary AutoCAD operations.
- Arbitrary LISP is not an approved execution path.
- Layer semantics may be used as evidence, but must not silently override stronger source evidence.
- Runtime execution states must remain fail-closed until verified.
- Controlled Editing remains gated by ConstraintMap + ImpactAnalysis + Rules + ApprovedChangePlan + validation.

Target future shape:

**PlanModel → ApprovedChangePlan → Capability Registry → Execution Adapter → AutoCAD/YQArch → PostEditDiff → Validation**

## 3. Engineering Plan Input vs Image Input

The H100 boundary is now a first-class architecture rule.

Geometry-evidence hierarchy:

**DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP**

Source classes:

- ENGINEERING_VECTOR: DWG/DXF
- DOCUMENT_VECTOR: confirmed vector PDF
- DOCUMENT_RASTER: confirmed raster PDF
- IMAGE_RASTER: JPG/PNG/WEBP
- UNKNOWN: insufficient source evidence

PDF must never be classified by extension alone:

- PDF + confirmed vector evidence → ENGINEERING_PLAN
- PDF + confirmed raster evidence → IMAGE
- PDF + unknown representation → UNKNOWN / SOURCE_REQUIRED

Image Input remains supported, but raster evidence cannot silently become authoritative engineering geometry.

## 4. Iranian architectural drawing language

The project must understand architectural drawings as a language, not only as pixels or line segments.

The semantic evidence set includes:

- conventional architectural symbols and their shape/orientation;
- line types, thickness/weight and layer semantics;
- doors/windows and opening direction;
- dimensions and extension lines;
- level/elevation codes and their relation to floors;
- floor-to-floor and vertical-circulation relationships;
- stairs, landings, risers and evidence-based stair-count inference;
- room/space labels and space relationships;
- section markers, section direction lines and cut-plane semantics;
- elevation markers and direction;
- hatch semantics;
- column/structural symbols;
- title block and drawing metadata;
- scale and unit evidence;
- floor/level semantics and inter-floor relations;
- architectural drafting conventions from Iran plus relevant international CAD/drawing standards.

Important rule: section lines are not merely graphics. Their marker, direction and cut-plane meaning must become semantic evidence.

Level codes are also not merely annotations. They can constrain floor relationships and, when evidence is complete and consistent, support vertical-circulation/stair-count reasoning. Such inferences remain evidence-gated and fail-closed.

## 5. Standards / knowledge integration

The knowledge layer should preserve traceability to:

- Iran National Building Regulations and Engineering Organization/local rules;
- relevant Shiraz/local requirements;
- نشریه 55, 246 and 256 where applicable;
- accessibility, façade, MEP and architectural provisions;
- ISO 128, ISO 129-1, ISO 5457, ISO 7200;
- Neufert, Metric Handbook, Time-Saver;
- پایه 10 ترسیم فنی و نقشه‌کشی;
- پایه 11 نقشه‌کشی معماری;
- AutoCAD/CAD/BIM/Revit drafting and layer conventions.

These references feed Rule/Validation and semantic interpretation. They must not be mixed into raw detection as undocumented model assumptions.

## 6. Current integration priorities

Priority order after the H100 input boundary:

1. Finish H100 semantic/drawing evidence integration.
2. Bind source provenance/evidence IDs to semantic facts.
3. Strengthen UNKNOWN / NEEDS_REVIEW / BLOCKED propagation.
4. Add contradiction and missing-evidence handling.
5. Integrate architectural relations with the existing PlanModel/ConstraintMap rather than creating parallel graphs.
6. Add Golden DWG regression coverage where the evidence contract is applicable.
7. Keep YQArch/AutoCAD as a future controlled execution adapter, not as a replacement for PlanModel.
8. Only after H100 Green Gate, continue to H101 plan-generation work.

## 7. Architectural invariant

**Understanding the plan comes before generating or editing the plan.**

The system should first establish what the drawing says, what evidence supports it, what remains unknown, and how elements relate. Generation/editing may only consume validated semantic state.

## Verification status

This document records research/architecture decisions only. It does not declare H100 Green. H100 remains subject to exact-head REAL CI, Bug Hunt, required regression and persisted state evidence.
