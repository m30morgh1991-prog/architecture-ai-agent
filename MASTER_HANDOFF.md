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
11. **No-Wait / Forward-Motion Rule:** investigate blockers immediately; safe parallel preparation is allowed only when it does not invalidate the active gate or violate dependencies.

## Architecture principles
- This is not an image editor.
- Controlled editing must understand architectural plan logic.
- Source of Truth: PlanModel + ConstraintMap + ApprovedChangePlan.
- Pipeline: prompt → understanding → ChangeRequest → PlanModel → ConstraintMap → ImpactAnalysis → Rules → ChangeProposal → Conflict → Validation → ApprovedChangePlan → Controlled Editing → PostEditDiff → Final Validation → Audit.
- Unknown/insufficient evidence fails closed.

## Current verified continuation point — H99 complete
- H97 merged as PR #57; exact-head CI: Bug Hunt #66, PR CI #109, Runtime #396 — completed/success.
- H97 merge: `ce972970d12f3a93e7bbcfc72c28243a74b7dd0d`.
- H98 — Plan Understanding Core merged as PR #59.
- H98 exact head: `754331041aa67625c5e78b4ac83e16d718dfb149`.
- H98 gates: Bug Hunt #72, PR CI #115, Runtime #402 — completed/success.
- H98 merge: `e0bf66e46a6963b7561a458c7fcc046d2e5ae24a`.
- H98 composes Detection → PlanModel Reconstruction → ConstraintMap and preserves fail-closed UNKNOWN propagation.
- H99 merged as PR #61; merge commit `2344e1083937e5d91857ba24b6a0f077414f06ca`.
- H99 exact head: `09f75ee5de2319e51d1fbabdce62c864b427de42`.
- H99 gates: Bug Hunt #85, PR CI #128, Runtime #415 — completed/success.
- H99 adds evidence-backed architectural relations, fail-closed unresolved opening relations, stronger SpaceModel identity semantics, and Plan Understanding Core integration.
- Post-merge CI on the H99 merge commit is unobserved and therefore not GREEN.

## Consolidated architecture baseline
### Product
- Architecture AI Agent MVP; provider-neutral, low-cost/open-source oriented, Iran-friendly, tablet/PWA friendly.
- MVP input: JPG / PNG / WEBP / PDF + prompt.
- Native DWG/DXF editing is outside MVP; Golden DWGs remain regression assets.
- Golden DWGs: `bagheri7.dwg`, `afifiiiii.end.edit3.dwg`.

### Source of Truth and pipeline
- Source of Truth: PlanModel + ConstraintMap + ApprovedChangePlan.
- Pipeline: Prompt → Understanding → ChangeRequest → PlanModel → ConstraintMap → Impact → Rules → Proposal → Conflict → Validation → ApprovedChangePlan → Controlled Editing → Diff → Final Validation → Audit.

### Safety / fail-closed
- LOCKED / EDITABLE / CONDITIONAL / UNKNOWN.
- UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW / ABSTAIN / BLOCKED.
- No uncertainty may become PASS.
- Logical, Runtime, and Visual PASS are separate.
- Protected MVP elements: columns, outer boundary, walls, doors, windows, overall plan form.

### BIM and plan understanding
- H98 is the deterministic Detection → PlanModel Reconstruction → ConstraintMap integration boundary.
- PlanModel remains evidence-backed and source-bound.
- BIM-ready semantic contracts provide identity and validated relations without making full IFC/BIM a runtime dependency.
- BIM must remain provider/software neutral and fail-closed.
- Future H stages must be derived from actual repository contracts, tests, and dependencies.

### Knowledge / rules
- Future Rule/Validation layers should incorporate traceable Iran building regulations, Engineering Organization/local rules, relevant نشریه 55/246/256, accessibility/façade/MEP rules, ISO 128/129-1/5457/7200, Neufert, Metric Handbook, Time-Saver, vocational drafting references, and CAD/BIM/Revit conventions.
- Keep rule sources separate from raw detection and make rules explicit/testable.

### Governance
- Implement → REAL CI → Verify → Regression → Persist → Continue.
- Exact-head `completed / success` is required for GREEN.
- Bug Hunting is mandatory after red tests.
- No-Wait Rule permits safe parallel preparation but never bypasses a gate.
- “بکاپ بگیر” is additive from the current point and never resets the project.
- Repository is durable recovery state; Notion is not governance.
- Auto-Runner should keep forward motion while respecting all gates.

## Golden / regression integrity
- Golden DWG assets must remain preserved.
- No destructive history reset.
- Real DWG regression remains a validation boundary.
- Visual Runtime remains separate from logical/static reconstruction.

## Continuation after H99
1. Verify this H99 state-sync commit with real CI.
2. Merge the state-sync checkpoint only after required gates are completed/success.
3. Verify the resulting main commit; unobserved CI remains explicitly unobserved.
4. Inspect repository contracts/tests/active PRs.
5. Define the next stage from actual code/dependencies.
6. Implement → real CI → verify → regression → persist → continue.
