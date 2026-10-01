# Architecture AI Agent — Master Handoff

## Purpose

This document is the durable continuation point for the Architecture AI Agent project. It is intentionally repository-backed so development can continue without Notion.

## Non-negotiable governance

1. Do not redo completed work unless regression evidence requires it.
2. Implement the current stage.
3. Run the **real CI workflow** for the current commit.
4. Verify the actual result and distinguish `success` from queued/running/failed/unobserved.
5. Run required regression checks when applicable.
6. Persist the verified state in the repository.
7. **Green Gate:** a stage is GREEN/PASS only when the relevant real CI run is `completed` with `success` and required verification/regression evidence is confirmed.
8. Do not start the next gated H stage until the current gate has real evidence.
9. **Notion is excluded from governance and execution.** It is neither a source of truth nor a condition for PASS, continuation, persistence, or release.
10. Never convert Logical/Static PASS or unknown evidence into Real Runtime/Visual PASS.

## Architecture principles

- This is not an image editor.
- The controlled-editing pipeline must understand architectural plan logic.
- Source of Truth: PlanModel + ConstraintMap + ApprovedChangePlan.
- Pipeline: prompt → understanding → ChangeRequest → PlanModel → ConstraintMap → ImpactAnalysis → Rules → ChangeProposal → Conflict → Validation → ApprovedChangePlan → Controlled Editing → PostEditDiff → Final Validation → Audit.
- Unknown or insufficient evidence must fail closed.
- Provider selection must remain provider-neutral and deterministic where required.

## MVP scope

### Inputs
JPG / PNG / WEBP / PDF plus user prompt.

### Current real-artifact validation boundary
Native DWG evidence is being used as a test/validation boundary for real architectural drawings.

### Edit classes
- Furniture / Furnishing
- Furniture Layout Change
- Overall Architectural Layout Change

### Locked elements
- Columns C01–C12
- Outer Boundary
- Walls
- Doors
- Windows
- Overall Plan Form

## Repository and test assets

Repository: m30morgh1991-prog/architecture-ai-agent

Golden projects:
- test-assets/golden-projects/bagheri7.dwg
- test-assets/golden-projects/afifiiiii.end.edit3.dwg

These files are intended to remain the stable real-project regression inputs when present in the repository.

## Latest verified repository evidence

Main currently points to:
ef75ce077284a308e9c720b4d20f6b29098f1809

Latest observed successful Runtime Tests:
- Run #223
- branch: feat/real-plan-space-rebuild
- head: 3bd1233e702db681f8ef59fa2647d13a363e9aa5
- conclusion: success
- PR: #5
- commit message: Fix planar face traversal for orthogonal space extraction

Run #222 on the same development line failed before Run #223 succeeded. Do not treat the failed run as the current result; preserve it as historical evidence.

## Current continuation point

Continue from the active real-DWG / plan-space reconstruction work. The latest successful evidence indicates the planar-face traversal fix passed Runtime Tests. The next action must still be determined from the current PR/main state and the project's H-gate evidence, not guessed from a commit message alone.

## Continuation procedure

- Do not stop development because Notion is unavailable or absent.
- Read PROJECT_STATE.md and this file.
- Inspect main and the active feature branch.
- Inspect the latest CI workflow runs.
- Continue only from verified evidence.
- Repository-backed state is the durable continuation record.

## Governance lock — 2026-10-01

The execution rule is permanently recorded as:

**Implement → REAL CI Run/Status → Verify → Regression (when applicable) → Persist State → Continue**

No Notion action is required at any point in this chain.

## Integrity rule

These files are additive. They do not replace, delete, or rewrite historical commits. They exist to make the continuation state recoverable from Git alone.
