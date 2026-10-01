# Architecture AI Agent — Master Handoff

## Purpose

This document is the durable continuation point for the Architecture AI Agent project. It is repository-backed so development can continue without Notion.

## Non-negotiable governance

1. Do not redo completed work unless regression evidence requires it.
2. Implement the current stage.
3. Run the **real CI workflow** for the current commit.
4. Verify the actual result and distinguish success from queued/running/failed/unobserved.
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

## Current verified continuation point

### H62 — Space Model Contract
- Status: **GREEN / PASS**
- PR #6 merged to main.
- Head: `523781daefcbb2f2c971803994df4ab4ffdf92e0`
- Merge commit: `364307fb25d8e4149ee001dd0cc8b3416e6a939d`
- Runtime Tests #228: **completed / success**
- Verification: H62 contract tests passed for evidence-backed spaces and relations, including fail-closed unresolved opening connectivity.

### Next
Continue with **H63** only after selecting its scope from the current repository implementation and evidence. Do not infer PASS from static code alone.

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

## Integrity rule

These files are additive. They do not replace, delete, or rewrite historical commits. They exist to make the continuation state recoverable from Git alone.
