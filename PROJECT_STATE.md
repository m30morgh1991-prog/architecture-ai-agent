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

## Current verified state — H78 / H79 checkpoint
- H77 BIM-ready PlanModel integration: **GREEN / MERGED**
- H77 PR #24 merge commit: edc1900a33d9310f7e81f7dd32384782208dd6ea
- H77 Runtime Tests #288: completed / success.
- H78 BIM-to-Constraint binding: **GREEN / MERGED**
- H78 PR #25 merge commit: 0ca7fd0fc1265e8170e89945138ed47087913d07
- H78 Runtime Tests #293: completed / success.
- H78 PR CI Gate #6: completed / success.
- H79 evidence-backed BIM ConstraintMap: implementation complete, PR #26 open.
- H79 head: 429f4ef5bd51cecbd06a238a797bb8b5cf974366
- H79 Runtime Tests #295: **in_progress**; not GREEN until completed/success.
- H79 PR CI Gate #8: **in_progress**; not GREEN until completed/success.
- Current gated continuation: PR #26 / H79.
- No H80 merge or GREEN claim is permitted until H79's current real CI gates complete successfully.
- Parallel preparation is allowed only when it does not alter the active H79 head or invalidate its CI gate.

## Backup checkpoint
- Repository-only recovery checkpoint recorded for continuation if Notion or auxiliary tools are unavailable.
- Active continuation branch: feat/h79-evidence-backed-bim-constraintmap via PR #26.
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
