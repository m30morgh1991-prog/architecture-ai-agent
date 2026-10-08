# Project State

## Current Stage

**H100 — input-source boundary implementation — merged**

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
1. Observe main CI for merge commit `4f1363ead6c10378cbf807d29271ae315ae01c36`.
2. If main CI is GREEN, persist the verified H100 checkpoint and continue.
3. If main CI is RED, perform mandatory Bug Hunt → patch → rerun → verify.
4. Continue H100 semantic/drawing evidence strengthening only after the current mainline gate is verified.

## Integrated research checkpoint — 2026-10-08

### Newly consolidated decisions
- External architecture-agent research is part of the project knowledge layer; it does not create a second semantic graph.
- Useful patterns include scene graph/relations, raster-to-wall/opening reconstruction with uncertainty, semantic intent → deterministic geometry, knowledge/skills + feedback, and CV → CAD/BIM/IFC bridging.
- YQArch/AutoCAD is a future Execution Adapter capability, not the project brain.
- No arbitrary LISP path and no direct LLM → AutoCAD geometry authority.
- Iranian architectural drawing language is a first-class semantic evidence layer.
- Level/stair/section inferences remain fail-closed and require explicit consistent evidence.
- Standards and knowledge sources feed traceable Rule/Validation layers.
- Core invariant: **understand the plan before generating or editing the plan**.

### H100 continuation priorities
1. Bind evidence IDs/provenance to semantic facts.
2. Wire contradiction/missing-evidence handling and fail-closed propagation.
3. Complete drawing semantics/dimensions/annotations/markers/scale/unit coverage.
4. Integrate architectural relations into the canonical PlanModel/ConstraintMap.
5. Apply Golden DWG regression where applicable.
6. Run exact-head REAL CI + Bug Hunt + required regression; persist only verified state.
7. Continue to H101 only after Green Gate.

## Durable governance

- Required cycle: Implement → REAL CI → Verify → Regression → Persist State → Continue.
- Green Gate requires exact-head real CI completed/success plus required verification/regression evidence.
- queued/in_progress/cancelled/failure/missing/unobserved is never GREEN.
- Bug Hunting is mandatory after red tests.
- Notion is excluded from governance.
- Golden DWG assets remain preserved.
- “بکاپ بگیر” means additive checkpoint; never destructive reset.
