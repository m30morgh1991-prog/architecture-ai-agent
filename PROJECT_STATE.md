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

## Current verified state — H68
- Stage: **H68 — Architectural Element Detection**
- Status: **GREEN / PASS**
- PR: **#12**
- Head: `65327be27fcb5187eebcec04e91af6efa5df3f10`
- Merge commit on main: `8a63761ad665da5564468a3b0a0b902db95bf365`
- CI: **Runtime Tests #252 — completed / success**
- Verification: Golden DWG regression coverage passed for conservative architectural element candidate detection, deterministic evidence, allowed element types/statuses, and fail-closed uncertainty handling on both golden projects.
- H62–H67 remain GREEN/PASS.
- Next gated stage: **H69 — Element Evidence Contract**.

## Current technical direction
Extend real-DWG evidence toward reliable architectural space reconstruction. Preserve conservative/fail-closed behavior: insufficient evidence remains UNKNOWN.

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
