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
7. Green Gate requires real CI `completed / success` plus required verification/regression evidence.
8. Do not start the next gated H until the current gate has real evidence.
9. **Notion is excluded from governance and execution.**
10. Never convert Logical/Static PASS or UNKNOWN evidence into Real Runtime/Visual PASS.
11. **No-Wait / Forward-Motion Rule:** never remain idle when a solvable path exists; investigate blockers immediately and use a technically valid solution or compatible alternative. Parallel preparation is allowed while CI runs only when it does not invalidate the active gate or violate stage dependencies. Alternatives may accelerate progress but never replace required real CI evidence. Stop only for a genuine external blocker or unavoidable human decision.

## Architecture principles
- This is not an image editor.
- Controlled editing must understand architectural plan logic.
- Source of Truth: PlanModel + ConstraintMap + ApprovedChangePlan.
- Pipeline: prompt → understanding → ChangeRequest → PlanModel → ConstraintMap → ImpactAnalysis → Rules → ChangeProposal → Conflict → Validation → ApprovedChangePlan → Controlled Editing → PostEditDiff → Final Validation → Audit.
- Unknown/insufficient evidence fails closed.

## Current verified continuation point — H97 complete
- **H97 — Runtime Evidence Integration:** merged as PR #57.
- H97 exact head: `b52474cce806fc096d4ad92a64598714f39a70a9`.
- Exact-head gates: Bug Hunt Gate #66, PR CI Gate #109, Runtime Tests #396 — all completed/success.
- Merge commit / current main: `ce972970d12f3a93e7bbcfc72c28243a74b7dd0d`.
- H97 integrates audit completeness, idempotency completion, and runtime PASS evidence into the H96 release gate and persists enriched evidence for replay.
- **Important:** post-merge main CI for `ce972970d12f3a93e7bbcfc72c28243a74b7dd0d` is currently unobserved. Missing/unobserved main CI is not GREEN.
- Do not redo H95–H97. Continue from current main with the next verifiable hardening stage after durable state synchronization.

## Backup checkpoint
- Additive and non-destructive.
- No files were deleted or destructively overwritten.
- This checkpoint records the latest known stage, branches, PRs, heads, CI state, and recovery order.
- After H77 completes, persist the verified merge and CI result here before starting H78.

## MVP
Inputs: JPG / PNG / WEBP / PDF + prompt.
Native DWG evidence is the real-artifact validation/test boundary.
Edit classes: Furniture/Furnishing; Furniture Layout Change; Overall Architectural Layout Change.
Locked elements: Columns C01–C12, Outer Boundary, Walls, Doors, Windows, Overall Plan Form.

## Golden projects
- test-assets/golden-projects/bagheri7.dwg
- test-assets/golden-projects/afifiiiii.end.edit3.dwg

## Integrity
Golden assets are additive and historical commits remain immutable.

## Automation — Project Auto-Runner
- **Automation:** Architecture Auto-Runner is enabled for the project.
- It follows the repository governance loop: **Implement → REAL CI → Verify → Regression → Persist State → Continue**.
- It must not claim GREEN without `completed / success` evidence for the relevant current commit.
- It must not invalidate an active CI gate with unnecessary concurrent commits.
- On CI failure it inspects evidence, patches the root cause, reruns CI, and continues only after verification.
- On success it verifies, merges when appropriate, persists durable state, verifies the persistence checkpoint, and advances to the next gated H.
- It stops only when a genuine human/external action is required.
- Notion is excluded from this automation and from all Green Gates.


## Daily Backup — 2026-10-04
- Additive checkpoint after H97 merge.
- Main: `ce972970d12f3a93e7bbcfc72c28243a74b7dd0d`.
- H97 exact-head CI: Bug Hunt #66, PR CI #109, Runtime #396 — completed/success.
- No destructive reset/rewrite performed.

## Historical verification — H94 complete
- H93/H94 were previously merged and mainline-verified.
- H94 mainline CI: Runtime Tests #377, Bug Hunt Gate #47, PR CI Gate #90 — completed/success.

## Continuation rule after H97
- Inspect current main and any active PRs.
- Treat only exact-head completed/success CI as GREEN.
- If main post-merge CI is unavailable, record it as unobserved rather than inferring success.
- Advance only after implementing and verifying the next gated milestone; persist state again at the milestone.
