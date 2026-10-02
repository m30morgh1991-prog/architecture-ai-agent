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

## Current verified continuation point

### H75 — Impact Analysis
- Status: **GREEN / PASS**
- PR #20 merged.
- PR head: c64a56017a0813eab8d3c232e5ecd9b3531a5b23
- Merge commit: f2ae155ed14ad24c5bb71f5539692af75538d221
- Runtime Tests #274: **completed / success** on the H75 PR head.
- Verification: deterministic source/model-bound impact analysis, fail-closed target/constraint handling, and overall-layout review gating passed.

### Next
Begin **H76 — Architecture Rule Engine** after this persistence checkpoint is CI-verified.

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
