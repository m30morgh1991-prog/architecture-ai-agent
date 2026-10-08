# Project State

## **H100 — Golden Understanding Gate — active on main**

**Current verified point:** PR #75 is merged to main at `c056c31ff97db532381c7466388200ff3cb62aeb`. Exact-head PR CI #219, Runtime #506, and Bug Hunt #176 were completed/success on PR #75. Mainline workflows for the merge commit are not exposed by the current PR-run query, so post-merge Green is not claimed.

### H100 historical input-source boundary verification
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

### Current H100 continuation after PR #75

- PR #73 persisted the real Golden DWG SHA-256 evidence from CI-checked-out bytes.
- PR #74 established the provider-neutral AutoCAD-MCP adapter boundary.
- PR #75 merged the persisted SHA-256 values, byte-level mismatch regression, stronger Bug Hunt evidence contract, and a dependency-free read-only CAD inspection adapter.
- Golden SHA-256: `bagheri7.dwg = 865244d69e260d9ad23abed7b3ecaeb4df8b5f7da562c8d0284b466f3da13e6a`.
- Golden SHA-256: `afifiiiii.end.edit3.dwg = 508673cf44661b8b46fbb7f98992fffc99bd7d87531c1011fc5b8139d65a11a5`.
- Both preserved Golden DWGs remain fail-closed for uncertain structural semantics; hashes establish source identity, not semantic truth.
- AutoCAD-MCP remains read-only/adapter-only; no live AutoCAD write is enabled.
- Bug Hunt now requires affected contracts, risk classification, negative tests, and unresolved-findings evidence in addition to reproduction/root-cause/regression/fail-closed/exact-head evidence.

## H100 continuation
PR #66 established the source boundary; PR #68 established semantic/drawing evidence; PR #69 locked Golden Understanding research; PR #70 is the active Golden Understanding Regression implementation; PR #72 adds the standalone CLI E2E verification.
Do not start H101 until UG-01..UG-09 are Green and the verified state is persisted.

Current active sequence:
1. PR #71 standalone Golden Understanding runner is merged at `671133d4ab8941b2a38c79597769d8df2b18269e`; exact-head pre-merge gates were green.
2. PR #72 standalone Golden runner CLI E2E is merged at `b55242becb786fb4f932c671cf98e61c5aa3686d`; exact-head PR CI #204, Bug Hunt #161, and Runtime #491 were green.
3. PR #75 is merged at `c056c31ff97db532381c7466388200ff3cb62aeb`; exact-head gates were green.
4. Golden source SHA-256 values are now persisted and byte-verified by regression.
5. Read-only CAD inspection adapter is implemented behind the provider-neutral contract; live AutoCAD remains blocked.
6. UG-04/UG-06 and full Golden semantic ground truth remain pending; H101 stays locked.
3. Keep dimensions, levels, view markers and vertical circulation UNKNOWN unless source evidence supports them.
4. Apply reconciliation/provenance/fail-closed checks before authoritative PlanModel promotion.
5. Run exact-head REAL CI + Runtime + Bug Hunt + required regression.
6. Persist only verified state, then unlock H101.

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


### H100 mainline checkpoint — PR #76
- PR #76 merged at `8880b1890d5094771662464b48a294c9563a3059`.
- Exact-head PR #76: PR CI #225 SUCCESS, Runtime #512 SUCCESS, Bug Hunt #182 SUCCESS.
- Added executable mainline checkpoint coverage for Golden source binding, UNKNOWN status, fail-closed state documentation, and read-only CAD boundary.
- Mainline post-merge workflow Green is still not claimed because the current workflow-run query exposes PR-triggered runs only.
