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

## Current verified state — H100 active checkpoint
- **H95 — Idempotent Execution Recovery:** merged and verified.
- **H96 — Evidence-based Release Gate:** merged as PR #56; merge commit `75117399336135f654a99a805977a93251be0946`.
- **H97 — Runtime Evidence Integration:** PR #57 merged on 2026-10-04.
- H97 exact-head CI: Bug Hunt Gate #66, PR CI Gate #109, Runtime Tests #396 — all `completed / success`.
- H97 merge commit: `ce972970d12f3a93e7bbcfc72c28243a74b7dd0d`.
- H97 wires audit completeness, idempotency completion, and runtime PASS evidence into the hardened H96 release gate and persists the enriched result for replay.
- **H98 — Plan Understanding Core:** merged as PR #59; merge commit `e0bf66e46a6963b7561a458c7fcc046d2e5ae24a`.
- H98 exact-head: `754331041aa67625c5e78b4ac83e16d718dfb149`; Bug Hunt #72, PR CI #115, Runtime Tests #402 — all `completed / success`.
- H98 composes Detection → PlanModel Reconstruction → ConstraintMap and preserves UNKNOWN/NEEDS_REVIEW/BLOCKED fail-closed.
- **Post-merge Main CI for H98 is currently unobserved**. This is not GREEN evidence.
- PR #60 is the active durable-state synchronization checkpoint for H98.

## Integrated project knowledge checkpoint — 2026-10-04
This section is the consolidated continuation baseline from the recent project conversations and repository state.

### Product / architecture direction
- Product: **Architecture AI Agent — MVP**, provider-neutral, low-cost/open-source oriented, Iran-friendly, tablet/PWA friendly.
- It is **not an image editor**.
- Source of Truth: **PlanModel + ConstraintMap + ApprovedChangePlan**.
- Core pipeline:
  Prompt → Understanding → ChangeRequest → PlanModel → ConstraintMap → ImpactAnalysis → Rules → ChangeProposal → Conflict → Validation → ApprovedChangePlan → Controlled Editing → PostEditDiff → Final Validation → Audit.
- MVP inputs: JPG / PNG / WEBP / PDF + prompt.
- Native DWG/DXF editing is excluded from MVP; Golden DWG assets are retained as real-artifact regression boundaries.
- Golden assets:
  - `test-assets/golden-projects/bagheri7.dwg`
  - `test-assets/golden-projects/afifiiiii.end.edit3.dwg`

### Fail-closed and constraint semantics
- Constraint states: LOCKED / EDITABLE / CONDITIONAL / UNKNOWN.
- Fail-closed states: UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW / ABSTAIN / BLOCKED.
- Uncertain or contradictory evidence must never become PASS.
- Logical/Static PASS, Real Runtime PASS, and Visual Runtime PASS remain distinct gates.
- MVP protected elements: columns, outer boundary, walls, doors, windows, overall plan form.
- Detection order: Structural Fixed → Walls/Doors/Windows → Furniture → Spaces.

### Plan understanding / BIM direction
- H98 establishes the deterministic boundary:
  **Detection → PlanModel Reconstruction → ConstraintMap**.
- PlanModel is evidence-backed and source-bound.
- ConstraintMap partitions protected/editable/conditional/unknown elements and requires evidence.
- BIM is integrated as a **BIM-ready semantic layer**, not as a full IFC dependency.
- `BIMElementIdentity` and `BIMElementRelation` provide semantic identity, hierarchy/level/parent/property references, and validated relations.
- BIM must remain provider/software neutral and must not weaken MVP fail-closed behavior.
- Next stages must be derived from actual repository contracts/tests rather than blindly replaying the historical H71–H90 roadmap.

### Architectural knowledge / rules direction
Research gathered in prior conversations is part of the project knowledge direction and should feed future Rule/Validation layers, not be mixed into raw detection:
- Iran: National Building Regulations, Engineering Organization rules, Shiraz/local rules, relevant نشریه 55 / 246 / 256, façade, accessibility, mechanical and electrical provisions.
- International: ISO 128 / 129-1 / 5457 / 7200, Neufert, Metric Handbook, Time-Saver.
- Education/vocational references: پایه 10 ترسیم فنی و نقشه‌کشی and پایه 11 نقشه‌کشی معماری.
- CAD/BIM/Revit/AutoCAD layer, symbol, annotation, and modeling conventions.
- Rule sources must remain traceable and should ultimately become explicit, testable rules rather than undocumented model assumptions.

### Runtime / governance direction
- Mandatory cycle: Implement → REAL CI → Verify → Regression when applicable → Persist → Continue.
- Green Gate: only exact-head real CI with `completed / success` plus required verification/regression evidence.
- queued / in_progress / cancelled / failure / missing / unobserved is never GREEN.
- Bug Hunting is mandatory after red tests; root cause → patch → rerun → verify.
- No-Wait Rule: perform safe, non-conflicting preparation while CI runs, but never bypass a gate.
- “بکاپ بگیر” means an additive checkpoint from the current point; never reset to version zero.
- Repository-backed state is the durable recovery mechanism.
- Notion is excluded from governance.
- Project Auto-Runner should advance the cycle automatically when technically possible, but must respect Green Gate and human/external blockers.

## Golden / validation integrity
- Golden DWG files are preserved and must not be deleted or overwritten destructively.
- Historical verified commits remain immutable.
- Real DWG regression remains important even though native DWG editing is outside MVP.
- Visual Runtime remains a separate gate from logical reconstruction.

## Green Gate
A stage is GREEN/PASS only when its relevant real CI run for the current commit is `completed` with `success`, with required verification/regression evidence confirmed. queued/in_progress/cancelled/failure/missing/unobserved is not GREEN.

## Update protocol
After meaningful milestones, persist exact stage, commit, CI evidence, verification/regression evidence, blockers, and continuation point before starting the next gated H.

## Automation — Project Auto-Runner
- **Automation:** Architecture Auto-Runner.
- Purpose: monitor the continuation cycle and advance gated H stages without requiring a manual “check CI” prompt.
- Failure path: inspect CI logs → root cause → patch → rerun → verify.
- Success path: verify → regression → merge when ready → persist state → verify persistence CI → continue.
- Never invalidate an active gate with unnecessary concurrent commits.
- Stop only for genuine external blockers or unavoidable human decisions.

## Daily Backup — 2026-10-04
- Additive checkpoint after H98 merge.
- H98 merge commit: `e0bf66e46a6963b7561a458c7fcc046d2e5ae24a`.
- H98 exact-head evidence: Bug Hunt #72, PR CI #115, Runtime #402 — completed/success.
- PR #60 persists this checkpoint; its exact-head CI must be re-evaluated after any content update.
- No destructive reset/rewrite performed.

## Historical verification — H93 / H94
- H93 and H94 were previously merged and verified on main.
- H94 mainline CI: Runtime Tests #377, Bug Hunt Gate #47, PR CI Gate #90 — all completed/success.
- H94 DWG polygonization performance root cause was fixed and regression-verified.

## YQArch / AutoCAD execution research — registered
- YQArch is an execution-adapter candidate, not a Plan Understanding engine and never a Source of Truth.
- Adopt the concept of a provider-neutral **Architectural Capability Registry** instead of exposing raw YQArch commands to the model.
- Useful capability families registered for future controlled editing: walls, columns, doors/windows, stairs/elevators, axes/grids, dimensions, section/elevation markers, annotations, layers, area/listing helpers, and controlled move/copy/mirror/repair operations.
- Runtime success must distinguish REQUESTED / DISPATCHED / STARTED / INTERACTIVE / EXECUTING / COMPLETED / VERIFIED / FAILED / UNKNOWN; only VERIFIED can satisfy execution success.
- Arbitrary LISP evaluation and arbitrary command strings are explicitly excluded from the model-facing execution boundary.
- Layer names are evidence only; semantic classification must combine layer + geometry + symbols + text + topology + BIM relations.
- YQArch findings are persisted in `docs/research/yqarch-autocad-execution.md`.
- Future VerticalCirculation work should model storey height, riser, tread, flight count, landing, direction, required step count, and plan/section representation.

## Current continuation
- H100 is active in PR #64 (`feat/h100-drawing-semantics`).
- H100 establishes evidence-backed architectural drawing annotations and deterministic dimension semantics.
- YQArch research has been registered as a supporting execution/drawing capability boundary; it does not claim a future stage GREEN.
- After H100 exact-head CI and required Bug Hunt/Runtime verification succeed, persist state, verify the resulting main commit, then derive H101 from actual repository contracts/tests.
