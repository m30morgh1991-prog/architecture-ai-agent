# Architecture AI Agent — Master Progress Checklist

> This file is the persistent cross-chat project checklist. When asked "کجای پروژه هستیم؟" or "مرحله بعد چیست؟", use this file together with GitHub PR/CI status and `PROJECT_STATE.md` as the source of truth.

## Governance Gate — ALWAYS ACTIVE

- [ ] Implement
- [ ] REAL CI run/status
- [ ] Verify exact HEAD
- [ ] Regression when applicable
- [ ] Persist State
- [ ] Continue immediately when Green
- [ ] If Red: Bug Hunt → root cause → fix → REAL CI again
- [ ] Never treat queued/in_progress/no-CI as Green
- [ ] Never bypass Fail-Closed
- [ ] No-Wait Rule: prepare/debug in parallel while CI runs, without bypassing the gate

## Current master sequence

- [x] Architecture Agent feature-to-file matrix defined (PR #65)
- [x] Plan Understanding Semantic Chain defined
- [x] PR #65 — CI + Bug Hunt Green
- [x] PR #65 — Merge (`176bc2ceb330e2987891ef6edbbaf33b73dc77d3`)
- [x] Post-merge main REAL CI Green — Runtime #427, PR CI #140, Bug Hunt #97
- [x] H100 — Input source boundary: engineering-plan vs image input
- [x] H100 — Geometry evidence hierarchy: DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP
- [x] H100 — PDF representation must be evidence-classified; unknown PDF is fail-closed
- [x] H100 — Source profile carried through ExecutionRequest metadata
- [x] 2026-10-08 — GitHub architecture-agent research consolidated
- [x] 2026-10-08 — YQArch/AutoCAD execution adapter direction recorded
- [x] 2026-10-08 — Iranian architectural drawing-language requirements consolidated
- [x] H100 Golden Understanding research lock merged (PR #69, merge `b27ea1f09b6e20c2ed13931177f740e6db93c6d0`)
- [x] H100 Golden Understanding Regression contract foundation implemented (PR #70 branch)
- [x] H100 — Drawing Semantics + Dimension/Annotation Evidence foundation (PR #68)
- [x] H100 — Semantic Chain foundation wired to canonical PlanModel (PR #68)
- [x] H100 — Evidence IDs/provenance bound to semantic facts (PR #68)
- [x] H100 — UNKNOWN / NEEDS_REVIEW / BLOCKED propagation foundation (PR #68)
- [x] H100 — Contradiction detection foundation (PR #68)
- [x] H100 — Missing-evidence detection foundation (PR #68)
- [ ] H100 — Golden Understanding Regression: contract + manifest + fail-closed evaluator
- [ ] H100 — Golden Understanding: real Golden DWG execution + source hashes + ground truth
- [ ] H100 — UG-01..UG-08 Golden Understanding Gate checks Green
- [ ] H100 — UG-09 exact-head REAL CI + Runtime + Bug Hunt Green
- [ ] H100 — UG-10 Green → persist verified state and unlock H101
- [ ] H101 — Architectural Intent + Program + Plan Generation + deterministic geometry/layout
- [ ] H101 — REAL CI + Bug Hunt Green
- [ ] H102 — Architecture IR + lint/diagnostics
- [ ] H103 — Deterministic Drawing Compiler + SVG/DXF
- [ ] H104 — Dimensions/annotations/views + drawing standards
- [ ] H105 — Sections + elevations
- [ ] H106 — Details + schedules + sheets
- [ ] H107 — Multi-output sync + BIM export boundary
- [ ] H108 — Multi-agent roles/orchestration
- [ ] H109 — Iterative propose → inspect → revise
- [ ] H110 — Cross-format round-trip validation
- [ ] H111 — Production documentation/release gate

## H100 — Semantic/Drawing Evidence checklist

### Golden Understanding Gate (UG-01..UG-10)

- [x] UG-01 Golden case manifest exists
- [x] UG-02 Ground-truth schema is source-bound and versioned
- [ ] UG-03 End-to-end Understanding Runner emits a machine-checkable report
- [ ] UG-04 All required semantic domains have expected truth or explicit UNKNOWN
- [x] UG-05 Public benchmark calibration is separated from project acceptance
- [ ] UG-06 Adversarial cases exist for every fail-closed category
- [ ] UG-07 Metrics are computed per domain
- [x] UG-08 False-PASS / unsafe-acceptance checks are hard blockers
- [ ] UG-09 Exact-head REAL CI + Runtime + Bug Hunt Green
- [ ] UG-10 Only after UG-01..UG-09 pass may H101 begin

- [ ] Door/window symbols + opening direction
- [ ] Line type/thickness/weight
- [ ] Layer semantics
- [ ] Dimensions + extension lines
- [ ] Elevation/level codes
- [ ] Room/space labels
- [ ] Section markers + direction lines + cut-plane semantics
- [ ] Elevation markers + direction
- [ ] Hatch semantics
- [ ] Column/structural symbols
- [ ] Element ↔ wall/space relations
- [ ] Floor/level semantics
- [ ] Floor-to-floor relationships
- [ ] Stairs/landings and stair-count inference only with explicit consistent evidence
- [ ] Scale/unit evidence
- [ ] Title-block/drawing metadata evidence
- [x] Input source classification/provenance boundary
- [ ] Evidence IDs/provenance bound to semantic facts
- [ ] UNKNOWN / NEEDS_REVIEW / BLOCKED propagation
- [ ] Contradiction detection
- [ ] Missing-evidence detection
- [ ] Golden DWG regression

## Integrated research findings

### External architecture-agent patterns

- JMU → scene graph / relations
- RedrawAI → raster → wall graph → openings → validation + uncertainty
- Draftly → semantic intent → deterministic geometry + incremental editing
- CraftBot → knowledge/skills + feedback loop
- dwg-bim_AI → CV segmentation → CAD/BIM/IFC

Transfer rule: use these as patterns only; keep one canonical PlanModel/evidence graph.

### YQArch / AutoCAD

- YQArch is an Execution Adapter candidate, not the project brain.
- Use Capability Registry + controlled adapter boundary.
- No arbitrary LISP execution path.
- No direct LLM → AutoCAD geometry authority.
- PlanModel + ApprovedChangePlan remain authoritative.

### Input-source boundary

**DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP**

Engineering-plan and image inputs remain distinct. Raster evidence may inform candidates but cannot silently become authoritative geometry.

### Iranian drawing-language additions

Treat the following as semantic evidence, not decoration:

- conventional symbols and orientation;
- line types/weights/layers;
- dimensions and extension lines;
- level/elevation codes;
- floor relationships and vertical circulation;
- stairs/landings/riser evidence;
- section markers, direction lines and cut planes;
- elevation markers/direction;
- hatch;
- title block;
- scale/unit;
- space labels and element relations.

## Plan Understanding — target semantic chain

Source Evidence
→ Element Identity
→ Geometry
→ Topology
→ Spatial Relation
→ Architectural Semantics
→ BIM Semantics
→ Rule Context

Rule: Detection is not Understanding. Do not create a second PlanModel or second BIM evidence graph. Preserve provenance continuity into the existing canonical model.

## H101 — Plan Generation checklist

- [ ] Architectural Intent contract
- [ ] Program/room requirements
- [ ] Prompt → plan proposal
- [ ] Deterministic layout/geometry
- [ ] Adjacency + circulation
- [ ] Opening connectivity
- [ ] Structural/regulatory constraints
- [ ] ConstraintMap integration
- [ ] Generated PlanModel
- [ ] Validation + conflict handling
- [ ] Fail-closed behavior
- [ ] Normal + ambiguous/failure tests
- [ ] Golden/regression coverage
- [ ] Exact-head REAL CI Green

## Feature-to-file matrix milestones

- F01–F02 → Intent + Program (H101)
- F03–F04 → Plan Generation + deterministic geometry (H101)
- F05–F06 → Architecture IR + validation (H102)
- F07–F10 → Drawing compiler/backends (H103–H104)
- F11–F18 → Phase-2 documentation (H104–H106)
- F19–F20 → Output sync + BIM export (H107)
- F21–F23 → Multi-agent + iterative design (H108–H109)
- F24–F26 → Semantic/BIM/evidence continuity (H100+ continuous)
- F27–F28 → Iran/architectural drawing standards + symbols/layers (H100/H104+)
- F29 → Round-trip (H110)
- F30 → Production readiness (H111)

## Status rules

- **PLANNED** = listed in matrix, not implemented.
- **IMPLEMENTED** = code exists, but exact-head REAL CI is not Green.
- **IMPLEMENTED + GREEN** = code + exact-head REAL CI success.
- **MERGED + VERIFIED** = merged to main + required post-merge verification Green.

## Source of truth

1. GitHub main/PR state and exact-head REAL CI
2. `PROJECT_STATE.md`
3. `MASTER_HANDOFF.md`
4. This checklist
5. Feature-to-file matrix / research docs as supporting planning documents

Notion is not a governance or Green-Gate source of truth.
