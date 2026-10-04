# Architecture AI Agent — Project State

> Durable project-state record. Repository-backed continuation state.

## Authority model
- **Technical source of truth:** Git repository, commits, CI results, runtime tests, release gates.
- **Architecture source of truth:** PlanModel + ConstraintMap + ApprovedChangePlan.
- **Notion:** removed from project execution/governance. Never a source of truth or Green Gate.
- **Rule:** never claim CI green from assumptions.

## Continuation rule
**Implement → REAL CI Run/Status → Verify → Regression (when applicable) → Persist State → Continue**

## No-Wait / Forward-Motion Rule
- **Never wait idle when a solvable path exists.** If blocked by a tool, workflow, dependency, or environment limitation, immediately investigate the root cause and pursue a technically valid solution or a compatible alternative path.
- Prefer parallelizable, non-conflicting preparation while a gated CI run is active, provided it does not invalidate the active gate or violate stage dependencies.
- Do not bypass Green Gate evidence: alternatives may accelerate preparation and verification, but a gated stage still requires real `completed / success` CI evidence before it is declared GREEN/PASS.
- Stop only when there is a genuine external blocker or an unavoidable human decision; otherwise keep the project moving toward the next verifiable milestone.

## Current verified state — H97 checkpoint
- **H95 — Idempotent Execution Recovery:** merged and verified.
- **H96 — Evidence-based Release Gate:** merged as PR #56; merge commit `75117399336135f654a99a805977a93251be0946`.
- **H97 — Runtime Evidence Integration:** PR #57 merged on 2026-10-04.
- H97 head: `b52474cce806fc096d4ad92a64598714f39a70a9`.
- H97 exact-head CI: Bug Hunt Gate #66, PR CI Gate #109, Runtime Tests #396 — all `completed / success`.
- H97 merge commit / current main: `ce972970d12f3a93e7bbcfc72c28243a74b7dd0d`.
- H97 wires audit completeness, idempotency completion, and runtime PASS evidence into the hardened H96 release gate and persists the enriched result for replay.
- **Post-merge Main CI is currently unobserved** on `ce972970d12f3a93e7bbcfc72c28243a74b7dd0d`; combined status and commit-associated workflow lookup returned no runs. This is **not GREEN evidence** and must not be inferred as success.
- Next action: synchronize durable state, then define/implement the next gated hardening stage from the current mainline rather than redoing completed H95–H97 work.

## Backup checkpoint
- Repository-only recovery checkpoint recorded for continuation if Notion or auxiliary tools are unavailable.
- Active continuation branch: feat/h77-bim-planmodel-integration via PR #24.
- Important changes since prior documented checkpoint: H76 rule engine, H76 BIM-ready PlanModel core, H77 BIM-ready PlanModel integration, PR CI gate workflow.
- No destructive deletion or overwrite was performed.
- Recovery order: inspect main, active PR head, latest real CI, then continue from latest verified green stage.

## Current technical direction
Reconstruct a deterministic, evidence-backed PlanModel from real DWG architectural detection and space extraction. Preserve conservative/fail-closed behavior: insufficient or contradictory evidence remains unresolved/UNKNOWN and cannot be promoted to PASS.

## Golden DWG test assets
- test-assets/golden-projects/bagheri7.dwg
- test-assets/golden-projects/afifiiiii.end.edit3.dwg

## Constraints
- MVP inputs: JPG/PNG/WEBP/PDF + prompt; native DWG is the real-artifact validation/test boundary.
- Locked MVP elements: columns, outer boundary, walls, doors, windows, overall plan form.
- Constraint states: LOCKED / EDITABLE / CONDITIONAL.
- Fail-closed: UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW / ABSTAIN / BLOCKED.
- No PASS on uncertainty.
- This is not an image editor; Source of Truth is structured plan/constraint/change data.
- Real Visual Runtime remains a separate gate; Logical/Static PASS is not Visual PASS.

## Backup / recovery
Repository state is the durable recovery mechanism. Manual «بکاپ بگیر» checkpoints preserve the current continuation point and never restart from zero.

## Green Gate
A stage is GREEN/PASS only when its relevant real CI run for the current commit is `completed` with `success`, with required verification/regression evidence confirmed. queued/in_progress/cancelled/failure/missing/unobserved is not GREEN.

## Update protocol
After meaningful milestones, persist exact stage, commit, CI evidence, verification/regression evidence, blockers, and continuation point before starting the next gated H.

## Automation — Project Auto-Runner
- **Automation:** Architecture Auto-Runner
- **Purpose:** automatically monitor the project continuation cycle and advance gated H stages without requiring a manual “check CI” prompt.
- **Execution policy:** Implement → REAL CI Run/Status → Verify → Regression (when applicable) → Persist State → Continue.
- **CI rule:** never treat queued/in_progress/cancelled/failure/missing/unobserved as GREEN.
- **Safety:** do not create unnecessary commits while a required CI gate is running if they would invalidate that gate.
- **Failure path:** inspect CI logs → identify root cause → patch → rerun CI → verify.
- **Success path:** verify → regression when required → merge when ready → persist PROJECT_STATE/MASTER_HANDOFF → verify persistence CI → continue to next gated H.
- **Human intervention:** stop only for genuine external blockers such as required access, CAPTCHA, missing files, or an unavoidable human decision.
- **Notion:** never used as an execution/governance gate.


## Daily Backup — 2026-10-04
- Additive checkpoint after H97 merge.
- Current main: `ce972970d12f3a93e7bbcfc72c28243a74b7dd0d`.
- H97 exact-head evidence: Bug Hunt #66, PR CI #109, Runtime #396 — completed/success.
- No destructive reset/rewrite performed; Golden DWG assets and historical commits remain intact.

## Historical verification — H93 / H94
- H93 and H94 were previously merged and verified on main.
- H94 mainline CI was Runtime Tests #377, Bug Hunt Gate #47, PR CI Gate #90 — all completed/success.
- The H94 DWG polygonization performance root cause was fixed and regression-verified.

## Current continuation
- Mainline continuation commit: `ce972970d12f3a93e7bbcfc72c28243a74b7dd0d`.
- H97 is merged and its exact-head gate is green.
- Main post-merge CI is unobserved; do not declare the merge GREEN solely from PR evidence.
- Continue with repository-backed hardening and persist each verified milestone before advancing. 
