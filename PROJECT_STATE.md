# Project State

## Current Stage

**H100 — input-source boundary implementation — merged; post-merge mainline verification pending**

### H100 PR #66 verification
- PR: #66
- Branch: feat/h100-input-source-boundary
- PR head before merge: `2b0627c67e039db79749d67c000bc2bc2f84eeb4`
- Merge commit: `4f1363ead6c10378cbf807d29271ae315ae01c36`
- Exact PR-head Bug Hunt Gate #108: completed / success
- Exact PR-head PR CI Gate #151: completed / success
- Exact PR-head Runtime Tests #438: completed / success
- H100 PR Green Gate: satisfied for PR #66
- Post-merge main CI for merge commit `4f1363ead6c10378cbf807d29271ae315ae01c36`: not yet observed; therefore mainline Green Gate is NOT yet claimed.

### H100 implemented boundary
- Engineering Plan Input and Image Input are separate.
- Geometry evidence hierarchy: DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP.
- Unknown PDF representation remains UNKNOWN / SOURCE_REQUIRED until inspection evidence exists.
- Source classification/provenance is carried through execution metadata.
- PlanModel + ConstraintMap + ApprovedChangePlan remain the only Source of Truth.
- Raster/image evidence cannot silently become authoritative geometry.

### H100 continuation
Do not redo H95–H99. Do not treat the PR merge alone as final H100 completion until post-merge main verification is observed.

Next sequence:
1. Observe main CI for merge commit `4f1363ead6c10378cbf807d29271ae315ae01c36` and the current state-persistence main commit.
2. If main CI is GREEN, persist the verified H100 checkpoint and continue.
3. If main CI is RED, perform mandatory Bug Hunt → patch → rerun → verify.
4. Continue H100 semantic/drawing evidence strengthening only after the current mainline gate is verified.

## Integrated research checkpoint — 2026-10-08

### Newly consolidated decisions
- External architecture-agent research is part of the project knowledge layer; it does not create a second semantic graph.
- Useful patterns include scene graph/relations, raster-to-wall/opening reconstruction with uncertainty, semantic intent → deterministic geometry, knowledge/skills + feedback, CV → CAD/BIM/IFC bridging, deterministic BIM verification, typed CAD/BIM capabilities, and measurement provenance.
- HarnessBIM is a reference for verification/checker architecture, not an MVP multi-agent dependency.
- IFC_AGENTS is a reference for deterministic IFC operations, issue/evidence lifecycle, and human-approved correction.
- Floor-plan vision systems are references for Evidence Extraction/Semantic Candidates, not authoritative geometry sources.
- CAD/BIM agent bridges are references for capability discovery and deterministic execution boundaries.
- YQArch/AutoCAD is a future Execution Adapter capability, not the project brain.
- No arbitrary LISP path and no direct LLM → AutoCAD geometry authority.
- Iranian architectural drawing language is a first-class semantic evidence layer.
- Level/stair/section inferences remain fail-closed and require explicit consistent evidence.
- Standards and knowledge sources feed traceable Rule/Validation layers.
- Core invariant: **understand the plan before generating or editing the plan**.

### H101–H110 roadmap decisions

**H101 — Evidence & Provenance**
- Evidence IDs bound to semantic facts.
- Source/evidence strength and measurement provenance.
- Contradiction and missing-evidence propagation.
- No authoritative semantic fact without traceable evidence.

**H102 — Relations & Topology**
- Wall ↔ Door ↔ Window ↔ Space relations.
- Adjacency, containment, connectivity.
- Geometry/semantic consistency.
- Canonical PlanModel/ConstraintMap only; no duplicate semantic graph.

**H103 — Drawing Set Graph**
- Sheet, floor/storey, plan, section, elevation, detail identity.
- Continuation/reference links and cross-sheet provenance.
- No cross-sheet inference without evidence.

**H104 — Vertical Circulation**
- Level/elevation codes, storey heights, riser/tread, landing, flight count and direction.
- Plan/section consistency.
- Stair/level inference remains fail-closed.

**H105 — Architectural Capability Registry**
- Semantic capability IDs, operation/object type, backend/provider, required evidence, risk, approval requirement and refusal defaults.
- Example: DOOR.WIDTH.UPDATE.
- Model requests semantic operations; capability validation controls execution.

**H106 — Controlled Editing**
- Transactions, rollback, execution lifecycle and provider-neutral adapters.
- No direct LLM → AutoCAD authority.
- Only approved semantic operations reach backend adapters.

**H107 — Post-Edit Verification**
- Drawing diff, reopen/parity, geometry validation, semantic validation and before/after evidence.
- Execution success requires post-edit verification.

**H108 — Rule & Compliance Layer**
- Traceable/testable rule packs.
- Iran/local architectural rules, drafting standards, accessibility/MEP/structural checks where evidence supports them.
- Rule results must cite their rule definition and required evidence.

**H109 — End-to-End Plan Understanding**
- Evidence → Semantic Candidates → PlanModel → Relations/Topology → ConstraintMap → Validation → Understanding Result.
- System must expose supported understanding and remaining UNKNOWN/NEEDS_REVIEW/BLOCKED states.

**H110 — Controlled Plan Generation**
- Starts only after H109 Green.
- Understanding → Design Intent → ChangeRequest → ImpactAnalysis → ApprovedChangePlan → Controlled Generation → Validation.
- Generation never becomes an alternative Source of Truth.

### Research artifact
- Consolidated comparative analysis and roadmap: `docs/research/external-agent-gap-analysis-2026-10-08.md`
- This artifact records adoption boundaries and acceptance criteria; it is research/design state, not a Green implementation claim.

## Durable governance

- Required cycle: Implement → REAL CI → Verify → Regression → Persist State → Continue.
- Green Gate requires exact-head real CI completed/success plus required verification/regression evidence.
- queued/in_progress/cancelled/failure/missing/unobserved is never GREEN.
- Bug Hunting is mandatory after red tests.
- Notion is excluded from governance.
- Golden DWG assets remain preserved.
- “بکاپ بگیر” means additive checkpoint; never destructive reset.
