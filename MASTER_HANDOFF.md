# Architecture AI Agent — Master Handoff

## Purpose
Durable repository-backed continuation point for Architecture AI Agent.

## Non-negotiable governance
1. Do not redo completed work unless regression evidence requires it.
2. Implement the current stage.
3. Run the **real CI workflow** for the current commit.
4. Verify actual status/conclusion; queued/running/failed/unobserved is not green.
5. Run required regression checks when applicable.
6. Persist verified state in the repository.
7. Green Gate requires real CI completed / success plus required verification/regression evidence.
8. Do not start the next gated H until the current gate has real evidence.
9. **Notion is excluded from governance and execution.**
10. Never convert Logical/Static PASS or UNKNOWN evidence into Real Runtime/Visual PASS.
11. **No-Wait / Forward-Motion Rule:** investigate blockers immediately; safe parallel preparation is allowed only when it does not invalidate the active gate or violate dependencies.

## Architecture principles
- This is not an image editor.
- Controlled editing must understand architectural plan logic.
- Source of Truth: PlanModel + ConstraintMap + ApprovedChangePlan.
- Pipeline: prompt → understanding → ChangeRequest → PlanModel → ConstraintMap → ImpactAnalysis → Rules → ChangeProposal → Conflict → Validation → ApprovedChangePlan → Controlled Editing → PostEditDiff → Final Validation → Audit.
- Unknown/insufficient evidence fails closed.

## Current continuation point — H100 input-source boundary

- H99 — Architectural Relations is merged on main: `2344e1083937e5d91857ba24b6a0f077414f06ca`.
- PR #65 Feature-to-File Matrix + semantic-chain research is merged: `176bc2ceb330e2987891ef6edbbaf33b73dc77d3`.
- PR #65 pre-merge gates: PR CI #138, Runtime #425, Bug Hunt #96 — completed/success.
- Post-merge main gates on `176bc2c`: Runtime #427, PR CI #140, Bug Hunt #97 — completed/success.
- H100 PR #66 is merged.
- H100 PR-head gates: Bug Hunt #108, PR CI #151, Runtime #438 — completed/success.
- H100 merge commit: `4f1363ead6c10378cbf807d29271ae315ae01c36`.
- The current state-persistence commit is `7474396ca33c09dc3ac50666cb0491e954a567fa`.
- Post-merge main CI has not yet been observed; H100 mainline Green is therefore not claimed.
- Implemented boundary: Image Input remains supported but is separate from Engineering Plan Input.
- Geometry evidence hierarchy: **DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP**.
- PDF must be classified by evidence as vector or raster; unknown representation remains fail-closed.
- `runtime/input_source_contract.py` defines source classes/trust ordering.
- `runtime/request_contract.py` carries optional `source_profile` metadata.

## Consolidated architecture baseline

### Product
- Architecture AI Agent MVP; provider-neutral, low-cost/open-source oriented, Iran-friendly, tablet/PWA friendly.
- MVP supports image/document inputs, but distinguishes Engineering Plan Input from Image Input.
- Native DWG/DXF editing remains outside the current MVP editing boundary; Golden DWGs remain regression assets.
- Golden DWGs: `bagheri7.dwg`, `afifiiiii.end.edit3.dwg`.

### Source of Truth and pipeline
- Source of Truth: PlanModel + ConstraintMap + ApprovedChangePlan.
- Pipeline: Prompt → Understanding → ChangeRequest → PlanModel → ConstraintMap → Impact → Rules → Proposal → Conflict → Validation → ApprovedChangePlan → Controlled Editing → Diff → Final Validation → Audit.

### Safety / fail-closed
- LOCKED / EDITABLE / CONDITIONAL / UNKNOWN.
- UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW / ABSTAIN / BLOCKED.
- No uncertainty may become PASS.
- Logical, Runtime, and Visual PASS are separate.
- Protected MVP elements: columns, outer boundary, walls, doors, windows, overall plan form.

### BIM and plan understanding
- H98 is the deterministic Detection → PlanModel Reconstruction → ConstraintMap integration boundary.
- PlanModel remains evidence-backed and source-bound.
- BIM-ready semantic contracts provide identity and validated relations without making full IFC/BIM a runtime dependency.
- BIM must remain provider/software neutral and fail-closed.

### Knowledge / rules
- Future Rule/Validation layers should incorporate traceable Iran building regulations, Engineering Organization/local rules, relevant نشریه 55/246/256, accessibility/façade/MEP rules, ISO 128/129-1/5457/7200, Neufert, Metric Handbook, Time-Saver, vocational drafting references, and CAD/BIM/Revit conventions.
- Keep rule sources separate from raw detection and make rules explicit/testable.

## Research-derived decisions — 2026-10-08

The comparative research is consolidated in `docs/research/external-agent-gap-analysis-2026-10-08.md`.

- HarnessBIM: reference for BIM verification/checker architecture, not an MVP multi-agent dependency.
- IFC_AGENTS: reference for deterministic IFC operations, issue/evidence lifecycle, and human-approved correction.
- Floor-plan vision systems: reference for Evidence Extraction/Semantic Candidates, not authoritative geometry.
- CAD/BIM agent bridges: reference for capability discovery and deterministic execution.
- OpenTakeoff-style patterns: reference for scale gates and measurement provenance.
- YQArch/AutoCAD: future Execution Adapter behind a Capability Registry, never the semantic authority.
- No arbitrary LISP path and no direct LLM → AutoCAD geometry authority.
- Iranian architectural drawing language is first-class semantic evidence.
- Level/stair/section inference is fail-closed and requires explicit consistent evidence.
- Core invariant: **understand the plan before generating or editing the plan**.

## H101–H110 roadmap

1. **H101 — Evidence & Provenance:** Evidence IDs, source binding, evidence strength, measurement provenance, contradiction/missing-evidence propagation.
2. **H102 — Relations & Topology:** canonical Wall/Door/Window/Space relations, adjacency, containment, connectivity, geometry/semantic consistency.
3. **H103 — Drawing Set Graph:** sheet/floor/plan/section/elevation/detail identity, continuation/reference links, cross-sheet provenance.
4. **H104 — Vertical Circulation:** levels, storey heights, riser/tread, landings, flights, direction, plan/section consistency.
5. **H105 — Architectural Capability Registry:** semantic capabilities, backend/provider, evidence requirements, risk, approval, refusal defaults.
6. **H106 — Controlled Editing:** transaction, rollback, lifecycle, provider-neutral adapters.
7. **H107 — Post-Edit Verification:** diff, reopen/parity, geometry/semantic validation, before/after evidence.
8. **H108 — Rule & Compliance:** traceable/testable Iran/local/drafting/accessibility/MEP/structural rules.
9. **H109 — End-to-End Plan Understanding:** Evidence → Semantic Candidates → PlanModel → Relations/Topology → ConstraintMap → Validation → Understanding Result.
10. **H110 — Controlled Plan Generation:** only after H109 Green; Design Intent → ChangeRequest → ImpactAnalysis → ApprovedChangePlan → Controlled Generation → Validation.

### Acceptance invariant
No stage may make generation an alternative Source of Truth. Understanding, provenance, relations, topology and validation precede increased execution power.

## Golden / regression integrity
- Golden DWG assets must remain preserved.
- No destructive history reset.
- Real DWG regression remains a validation boundary.
- Visual Runtime remains separate from logical/static reconstruction.

## Immediate next sequence

1. Observe main CI for H100 merge/state commits.
2. If GREEN, persist the verified H100 mainline checkpoint.
3. If RED, mandatory Bug Hunt → patch → rerun → verify.
4. Only after H100 mainline Green, derive the exact implementation/files for H101 from repository contracts and tests.
5. Run exact-head REAL CI + Bug Hunt + required regression before each Green Gate.
