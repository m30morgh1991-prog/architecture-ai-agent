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

## Current verified state — H100 input-source boundary checkpoint

- **H99 — Architectural Relations:** merged on main as commit `2344e1083937e5d91857ba24b6a0f077414f06ca`.
- **PR #65 — Feature-to-File Matrix + semantic-chain research:** merged as commit `176bc2ceb330e2987891ef6edbbaf33b73dc77d3`.
- PR #65 exact-head gates were GREEN before merge: PR CI #138, Runtime #425, Bug Hunt #96.
- Post-merge main GREEN evidence is now confirmed on merge commit `176bc2ceb330e2987891ef6edbbaf33b73dc77d3`: Runtime Tests #427 and PR CI Gate #140 completed/success; Bug Hunt Gate #97 completed/success.
- Repository is currently at **H100 implementation**, with the first H100 boundary implemented on branch `feat/h100-input-source-boundary`.
- H100 input boundary: Image Input remains supported, but is explicitly separated from Engineering Plan Input.
- Geometry-evidence trust hierarchy: **DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP**.
- PDF representation is evidence-classified; unknown PDF representation remains UNKNOWN and requires inspection rather than being guessed.
- Source classification is carried through execution metadata via `source_profile`.
- Current H100 branch implementation must pass exact-head REAL CI + Bug Hunt before merge.
- Do not declare H100 complete yet: drawing semantics, dimensions/annotations, markers, hatch, scale/unit, provenance, contradiction/missing-evidence coverage and Golden DWG regression remain gated work.

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

## Current continuation
- Current durable continuation is **H100 — input-source boundary implementation**.
- Do not redo H95–H99.
- H99 and PR #65 are already merged and post-merge main CI is GREEN.
- Finish H100 from actual repository contracts/tests: drawing-language evidence, source provenance, PDF/vector-vs-raster evidence, dimensions/annotations, markers, scale/unit and regression coverage.
- Required cycle remains: Implement → REAL CI → Verify → Regression → Persist State → Continue.


## Integrated research checkpoint — 2026-10-08

### Newly consolidated decisions
- External architecture-agent research is now part of the project knowledge layer; it does not create a second semantic graph.
- Useful patterns: scene graph/relations (JMU), raster-to-wall/opening reconstruction + uncertainty (RedrawAI), semantic intent → deterministic geometry (Draftly), knowledge/skills + feedback (CraftBot), and CV → CAD/BIM/IFC bridging (dwg-bim_AI).
- YQArch/AutoCAD is classified as a future **Execution Adapter** capability, not the project brain. PlanModel + ConstraintMap + ApprovedChangePlan remain authoritative.
- No arbitrary LISP path and no direct LLM → AutoCAD geometry authority.
- Engineering Plan Input and Image Input are separate. Geometry evidence hierarchy is DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP.
- PDF representation must be evidence-classified; unknown PDF remains UNKNOWN/SOURCE_REQUIRED.
- Iranian architectural drawing language is a first-class semantic evidence layer: symbols/orientation, line types/weights/layers, dimensions, level codes, room labels, section markers/direction/cut plane, elevation markers, hatch, structural symbols, scale/unit, title-block metadata, floor relationships and evidence-based stair/vertical-circulation reasoning.
- Level/stair/section inferences remain fail-closed and require explicit consistent evidence.
- Standards and knowledge sources feed traceable Rule/Validation layers rather than undocumented detection assumptions.
- Core invariant: **understand the plan before generating or editing the plan**.

### H100 continuation priorities
1. Bind evidence IDs/provenance to semantic facts.
2. Wire contradiction/missing-evidence handling and fail-closed propagation.
3. Complete drawing semantics/dimensions/annotations/markers/scale/unit coverage.
4. Integrate architectural relations into the canonical PlanModel/ConstraintMap.
5. Apply Golden DWG regression where applicable.
6. Run exact-head REAL CI + Bug Hunt + required regression; persist only verified state.
7. Continue to H101 only after Green Gate.
