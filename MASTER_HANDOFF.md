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

## Architecture principles
- This is not an image editor.
- Controlled editing must understand architectural plan logic.
- Source of Truth: PlanModel + ConstraintMap + ApprovedChangePlan.
- Pipeline: prompt → understanding → ChangeRequest → PlanModel → ConstraintMap → ImpactAnalysis → Rules → ChangeProposal → Conflict → Validation → ApprovedChangePlan → Controlled Editing → PostEditDiff → Final Validation → Audit.
- Unknown/insufficient evidence fails closed.

## Current verified continuation point

### H64 — Space Extraction Evidence Contract
- Status: **GREEN / PASS**
- PR #8 merged.
- Head: `d34195e3745eb7ad00bb9b3a94da8f0ae80a1155`
- Merge commit: `f14fa94e41c8640d3298e1b0db02a3cce198bffb`
- Runtime Tests #234: **completed / success**
- Verification: extraction-result contract tests passed, including evidence identity, unresolved relation tracking, typed SpaceModel normalization, and UNKNOWN preservation.

### Persistence checkpoint
- PROJECT_STATE.md persistence commit: `a428bd8762a07ad5e246a1318eaa649a2b905677`
- This checkpoint must receive its own real CI verification before H65 begins.

### Next
After the persistence commit is CI-green, begin **H65** based on current repository evidence, focusing on real-DWG space extraction integration/precedence and avoiding false space selection when explicit closed polylines and line-derived planar faces coexist.

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
