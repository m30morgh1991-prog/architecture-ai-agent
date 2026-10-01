# Architecture AI Agent — Project State

> Durable project-state record. This file is repository-backed and remains usable when Notion is unavailable.

## Authority model

- **Technical source of truth:** Git repository, commits, CI results, runtime tests, and release gates.
- **Architecture source of truth:** PlanModel + ConstraintMap + ApprovedChangePlan.
- **Notion:** documentation/dashboard mirror only; Notion availability must never block implementation, CI, verification, or continuation.
- **Rule:** never claim CI green from assumptions. A stage becomes PASS only from observable evidence.

## Continuation rule

**Implement → CI Run/Status → Verify → Persist State → Continue**

If Notion is unavailable:
1. Continue using repository + CI + this file + MASTER_HANDOFF.md.
2. Record the exact commit SHA and CI run/status.
3. Sync Notion later when access returns; do not rewrite history.

## Current repository baseline

- Repository: m30morgh1991-prog/architecture-ai-agent
- Default branch: main
- Current main baseline: ef75ce077284a308e9c720b4d20f6b29098f1809
- Latest merged change on main: native DWG drawing evidence boundary.
- Active development line observed: feat/real-plan-space-rebuild
- Latest observed successful Runtime Tests run: #223
- Successful run head: 3bd1233e702db681f8ef59fa2647d13a363e9aa5
- That run is on the active feature branch / PR #5; it is **not** the same thing as main being updated.

## Current technical direction

The current work is extending real-DWG evidence and rebuilding real plan spaces from native wall linework. The system remains conservative/fail-closed: unresolved evidence stays UNKNOWN rather than being promoted to PASS.

Golden DWG test assets:
- test-assets/golden-projects/bagheri7.dwg
- test-assets/golden-projects/afifiiiii.end.edit3.dwg

## Existing architecture constraints to preserve

- MVP input: JPG/PNG/WEBP/PDF plus user prompt; native DWG evidence is being used for the real-artifact validation/test boundary.
- Locked MVP elements: columns, outer boundary, walls, doors, windows, overall plan form.
- Constraint states: LOCKED / EDITABLE / CONDITIONAL.
- Fail-closed states: UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW / ABSTAIN / BLOCKED.
- No PASS on uncertainty.
- Controlled Architectural Editing remains distinct from generic image editing.
- Source of Truth remains structured plan/constraint/change data, not an output image.

## Visual/runtime status

Real Visual Runtime has historically remained a separate verification gate. Visual blockers must not be silently converted into PASS. Continue to distinguish:
- Logical/Simulation/Static PASS
- Real Runtime/Visual PASS

## Notion fallback status

Notion is currently treated as a mirror. No existing PROJECT_STATE.md or MASTER_HANDOFF.md was found before this fallback layer was added.

## Update protocol

After every meaningful milestone:
- update this file with exact evidence;
- update MASTER_HANDOFF.md when the continuation point changes materially;
- record commit SHA;
- record CI workflow/run/conclusion;
- record unresolved blockers;
- only then continue to the next gated stage.
