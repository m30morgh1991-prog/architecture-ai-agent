# Architecture AI Agent — Project State

> Durable project-state record. This file is repository-backed and remains usable when Notion is unavailable.

## Authority model

- **Technical source of truth:** Git repository, commits, CI results, runtime tests, and release gates.
- **Architecture source of truth:** PlanModel + ConstraintMap + ApprovedChangePlan.
- **Notion:** removed from the project execution/governance loop. It is not a source of truth, not a Green Gate, and its availability must never affect implementation, CI, verification, persistence, or continuation.
- **Rule:** never claim CI green from assumptions. A stage becomes PASS only from observable evidence.

## Continuation rule

**Implement → REAL CI Run/Status → Verify → Regression (when applicable) → Persist State → Continue**

Notion is not part of the continuation protocol. Continue using repository + CI + this file + MASTER_HANDOFF.md.

## Current verified state — H62

- Stage: **H62 — Space Model Contract**
- Status: **GREEN / PASS**
- PR: **#6**
- Head commit: `523781daefcbb2f2c971803994df4ab4ffdf92e0`
- Merge commit on main: `364307fb25d8e4149ee001dd0cc8b3416e6a939d`
- CI workflow: **Runtime Tests**
- CI run: **#228**
- CI conclusion: **completed / success**
- Verification: evidence-backed SpaceModel contract and H62 tests passed.
- Contract coverage: typed SpaceRecord, SpaceRelation, SpaceModel; evidence requirements; relation endpoint integrity; unresolved opening relations remain UNKNOWN/null endpoints; duplicate IDs blocked.
- Next gated stage: **H63**, to be selected from current repository evidence.

## Current technical direction

The current work extends real-DWG evidence and rebuilds real plan spaces from native wall linework. The system remains conservative/fail-closed: unresolved evidence stays UNKNOWN rather than being promoted to PASS.

## Golden DWG test assets

- test-assets/golden-projects/bagheri7.dwg
- test-assets/golden-projects/afifiiiii.end.edit3.dwg

## Existing architecture constraints to preserve

- MVP input: JPG/PNG/WEBP/PDF plus user prompt; native DWG evidence is used for the real-artifact validation/test boundary.
- Locked MVP elements: columns, outer boundary, walls, doors, windows, overall plan form.
- Constraint states: LOCKED / EDITABLE / CONDITIONAL.
- Fail-closed states: UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW / ABSTAIN / BLOCKED.
- No PASS on uncertainty.
- Controlled Architectural Editing remains distinct from generic image editing.
- Source of Truth remains structured plan/constraint/change data, not an output image.

## Visual/runtime status

Real Visual Runtime remains a separate verification gate. Visual blockers must not be silently converted into PASS. Continue to distinguish Logical/Simulation/Static PASS from Real Runtime/Visual PASS.

## Backup / recovery

Repository-backed state is the durable recovery mechanism. Daily backup automation is configured separately; manual checkpoint requests such as «بکاپ بگیر» must preserve the current continuation point rather than restarting from version zero.

## Green Gate — mandatory

A stage is **GREEN/PASS** only when the relevant real CI run for the current commit is `completed` with `success`, and the required verification/regression evidence is confirmed. queued, in_progress, cancelled, failure, missing, or unobserved CI is not GREEN.

## Update protocol

After every meaningful milestone:
- update this file with exact evidence;
- update MASTER_HANDOFF.md when the continuation point changes materially;
- record commit SHA;
- record CI workflow/run/status/conclusion;
- record verification/regression evidence;
- record unresolved blockers;
- only then continue to the next gated stage.
