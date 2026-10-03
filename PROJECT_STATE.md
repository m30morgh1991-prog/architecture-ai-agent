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

## Current verified state — H75 / H76 / H77 checkpoint
- Main verified baseline: **H75 — Impact Analysis**
- H75 status: **GREEN / PASS**
- H75 PR #20 merged; merge commit: f2ae155ed14ad24c5bb71f5539692af75538d221
- H75 CI: Runtime Tests #274 — completed / success.
- H76 Architecture Rule Engine PR #21: open, mergeable=false, head 9611c96eada263109d516ca3f97c2a0688d90e4b.
- H76 CI: Runtime Tests #282 — completed / success.
- H76 BIM-ready PlanModel core PR #22: open, mergeable=false, head ee7169c8e65e2faadb9b1446816a95d412d74ccf.
- H76 BIM-ready core CI: Runtime Tests #283 — completed / success.
- H77 BIM-ready PlanModel integration PR #24: open, mergeable=true, head b0f97dfae71e2ba44c782f4eea4275566f3aac4e.
- H77 CI: Runtime Tests #288 — in_progress; not GREEN until completed/success.
- Latest observed repository checkpoint commit: a706d0ede1c7fdd683fe2c219a13d7cbf825d815 (chore: enable PR CI gate).
- Safe continuation: preserve H77 active CI; do not merge until real CI completes/succeeds and PR is verified.

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


## Daily Backup — 2026-10-03
- Backup checkpoint verified against GitHub Repository.
- Active continuation branch: `feat/h92-final-validation-bypass-guard`.
- Active head: `41f18f2f6d616b7e2809feb0e8027d71b86ef03b`.
- Main baseline: `2d1271de8c1dc0a23e11c6b1216d937386ffe3b0` (H91 v2).
- Active branch is 15 commits ahead of main; no destructive reset/rewrite performed.
- H92 / PR #52 CI evidence on current head: Runtime Tests #362 = completed/success; Bug Hunt Gate #32 = completed/success; PR CI Gate #75 = completed/success.
- H92 is therefore CI-green on its current head; PR #52 remains the active continuation point unless/ until merged and post-merge main CI is verified.
- Important changes since the previous durable state checkpoint include H91 final-validation fail-closed hardening and H92 final-validation bypass-guard changes, including runtime/e2e/final-validation and regression-test updates plus `docs/bug-hunting/PR-52.md`.
- Recovery rule: use Repository + this file + MASTER_HANDOFF.md + real CI evidence only; auxiliary tools such as Notion are non-authoritative.
- Backup is additive and non-destructive. Historical commits and Golden DWG assets remain untouched.
