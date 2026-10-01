# Architecture AI Agent — Project State

> Durable project-state record. Repository-backed continuation state.

## Authority model
- **Technical source of truth:** Git repository, commits, CI results, runtime tests, release gates.
- **Architecture source of truth:** PlanModel + ConstraintMap + ApprovedChangePlan.
- **Notion:** removed from project execution/governance. Never a source of truth or Green Gate.
- **Rule:** never claim CI green from assumptions.

## Continuation rule
**Implement → REAL CI Run/Status → Verify → Regression (when applicable) → Persist State → Continue**

## Current verified state — H64
- Stage: **H64 — Space Extraction Evidence Contract**
- Status: **GREEN / PASS**
- PR: **#8**
- Head: `d34195e3745eb7ad00bb9b3a94da8f0ae80a1155`
- Merge commit on main: `f14fa94e41c8640d3298e1b0db02a3cce198bffb`
- CI: **Runtime Tests #234 — completed / success**
- Verification: H64 evidence-backed extraction result contract tests passed.
- Coverage: detector/source identity, space/relation evidence, unresolved-relation tracking, typed SpaceModel normalization, UNKNOWN preservation.
- H62 and H63 remain GREEN/PASS.
- Next gated stage: **H65**, after this persistence commit is itself verified by real CI.

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
