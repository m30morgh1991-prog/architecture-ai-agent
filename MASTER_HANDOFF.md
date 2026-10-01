# Architecture AI Agent — Master Handoff

## Purpose

This document is the durable continuation point for the Architecture AI Agent project. It is intentionally repository-backed so development can continue without Notion.

## Non-negotiable governance

1. Do not redo completed work unless regression evidence requires it.
2. Implement the current stage.
3. Run the real CI workflow.
4. Verify the actual result and distinguish success from queued/running/failed.
5. Persist the state in the repository.
6. Sync Notion when available; if unavailable, continue without blocking.
7. Do not start the next gated H stage until the current gate has real evidence.

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

## Notion outage/fallback procedure

If Notion cannot be opened:
- Do not stop development.
- Read PROJECT_STATE.md and this file.
- Inspect main and the active feature branch.
- Inspect the latest CI workflow runs.
- Continue only from verified evidence.
- When Notion returns, mirror the repository state back into the Notion project page.
- Never make Notion the sole copy of project state.

## Integrity rule

These files are additive. They do not replace, delete, or rewrite historical commits. They exist to make the continuation state recoverable from Git alone.
