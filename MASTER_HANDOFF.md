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

## Current verified continuation point — H100 Golden Understanding Gate

**Current verified point (2026-10-09):** `main` is `2842cf2523fb9140b72f03a2311addf06c468af2` (PR #93 merged). PR #93 exact head `26f1a0c9c0f47b3d8fa5f419f4a659c57b6e9d5e` passed PR CI #289, Runtime #576, and Bug Hunt #246. The merge commit has no exposed post-merge workflow runs/statuses through the available read path, so mainline post-merge Green is NOT claimed.

**Open H100 PRs (all still require review; no submitted reviews are recorded):**
- PR #96 book evidence map — head `1df773883036525e20c972815ac3a3410c00d7da`; PR CI #300, Runtime #587, Bug Hunt #257 = SUCCESS.
- PR #97 educational drawing references — head `25d57ef7e6b18f49228f9194b3991a92387cd04b`; current exact-head workflow-run query and combined status both returned no evidence. Status = UNOBSERVED, not GREEN. Re-run/verify PR CI, Runtime Tests, and Bug Hunt on this exact head before merge.
- PR #98 scale/unit fail-closed contract — head `7092f3cba6fc5b3f8747bbe78ff2e2976111ae1b`; PR CI #303, Runtime #590, Bug Hunt #260 = SUCCESS. Required prerequisite for #99.
- PR #99 scale/unit Golden bridge — head `c472396d5a3a984c8c134bb7f55d068326c4fc14`; PR CI #313, Runtime #600, Bug Hunt #272 = SUCCESS. Do not merge before #98; after #98 merges, rebase/retarget to updated main and rerun every gate on the final exact head.

**Governance blockers:** H100 remains active and H101 remains LOCKED. Golden semantic ground truth and real-world transformed/defective fixtures are incomplete. Repository ruleset `Min` (ID `24680937`) is `disabled`, targets no branches, and has no required status checks configured; the intended protections therefore do not currently enforce review or CI. Enable/configure it for `refs/heads/main` before treating branch protections as active.

- H100 implementation continues only within the existing canonical evidence/PlanModel path; do not create a parallel semantic graph.
- Geometry input hierarchy remains DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP; unknown source representation remains fail-closed.
- PlanModel + ConstraintMap + ApprovedChangePlan remain the Source of Truth.
- Scale/unit metadata alone is not verified scale: recognized DWG units remain NEEDS_REVIEW; missing/unsupported/conflicting evidence remains UNKNOWN/BLOCKED as appropriate. Dimensions remain UNKNOWN absent verified dimension-to-geometry correspondence.
- Preserve both Golden DWGs and their established SHA-256 identities; never rewrite or use them as output fixtures.
- Continue the required cycle: implement → exact-head REAL CI → verify → regression → persist state → continue. Any red result requires Bug Hunt/root cause/fix/re-run.

## Consolidated architecture baseline
### Product
- Architecture AI Agent MVP; provider-neutral, low-cost/open-source oriented, Iran-friendly, tablet/PWA friendly.
- MVP supports image/document inputs, but the architecture now distinguishes Engineering Plan Input from Image Input.
- Source hierarchy for geometry reconstruction: DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP.
- Native DWG/DXF editing remains outside the current MVP editing boundary; Golden DWGs remain regression assets.
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

## Historical continuation baseline after H99 / PR #65

1. H99 was complete at that historical checkpoint; this does not imply current post-merge Green for later main commits.
2. Finish H100 from the actual repository contracts and tests.
3. Keep PDF representation evidence-driven; never guess vector/raster.
4. Preserve one canonical PlanModel/evidence chain; do not create duplicate semantic graphs.
5. Run REAL CI + Bug Hunt + required regression on the H100 head.
6. Persist verified state, then continue to H101 only after Green Gate evidence.


## Integrated research checkpoint — 2026-10-08

The project now carries forward the latest research without changing the Source of Truth.

### Research-derived architecture rules
- Use JMU-style explicit relations, RedrawAI-style staged raster reconstruction/uncertainty, Draftly-style semantic-intent-to-deterministic-geometry separation, CraftBot-style knowledge/feedback loops, and dwg-bim_AI-style CV→CAD/BIM bridging only as implementation patterns.
- YQArch/AutoCAD belongs behind a future Capability Registry / Execution Adapter. It is not the semantic authority.
- Do not allow arbitrary LISP or direct LLM-generated AutoCAD geometry to bypass PlanModel, ApprovedChangePlan and validation.
- Treat Iranian drawing conventions as semantic evidence: symbols, orientation, line weights/layers, dimensions, level codes, floor/stair relations, section/elevation markers and directions, cut planes, hatch, scale/unit and title-block metadata.
- Section markers/direction are semantic relations; level codes can constrain floor and vertical-circulation reasoning when evidence is complete and consistent.

### Current invariant
**Understanding the plan comes before generating or editing the plan.**

### H100 acceptance criteria still open
- Finish drawing-language semantics, contradiction/missing-evidence adversarial coverage, real-world transformed/defective Golden fixtures, and authoritative semantic Golden ground truth.
- The persisted Golden hashes prove source identity only; they do not promote uncertain understanding to PASS.
- Historical PR #75 gates do not substitute for exact-head verification of the final H100 acceptance head.
- H101 remains locked until UG-10 and all required current-head CI/regression/review/governance evidence are satisfied.


### H100 PR #76 checkpoint
PR #76 merged at `8880b1890d5094771662464b48a294c9563a3059`. Exact-head PR CI #225, Runtime #512, and Bug Hunt #182 were successful. Mainline post-merge Green remains unclaimed. H100 semantic ground truth/adversarial gates remain pending; H101 remains locked.


### H100 UG-04 checkpoint
PR #78 merged at `79790fce10ec89b64dfbe613e5dbb1b321eadb76`; exact-head PR CI #229, Runtime #516, Bug Hunt #186 succeeded. UG-04 explicit per-domain status is implemented; current statuses remain UNKNOWN. UG-06 and semantic ground truth remain pending.


### H100 UG-06 checkpoint
PR #80 merged at `d0f40f2fac5f1df20c3bbfbd96eaeab966002e03`; exact-head PR CI #233, Runtime #520, Bug Hunt #190 succeeded. Contract-level adversarial coverage now enumerates all current fail-closed categories. Real-world DWG/image adversarial fixtures and semantic ground truth remain pending.


## H100 PR #82 checkpoint

PR #82 merged at `a08750765c19aadce02003e6fa221532d073992f` after exact-head `3ea24d659490c7f809bb8579b3ea1e3efbe627fb` passed PR CI #244, Runtime #531, and Bug Hunt #201. The evaluator now consumes `expected_domain_status` and correctly treats explicit UNKNOWN truth as unresolved rather than requiring populated element inventories. Current Golden semantic truth remains UNKNOWN. Post-merge workflow runs are not exposed by the current query, so no post-merge Green claim is made.

### Immediate continuation
1. Obtain authoritative/read-only structured evidence from the preserved Golden DWGs.
2. Reconcile CAD evidence into semantic facts with provenance and source binding.
3. Populate only verified DIRECT/validated DERIVED Golden truth; leave unsupported domains UNKNOWN.
4. Add real-world adversarial fixtures and corresponding fail-closed expected decisions.
5. Run exact-head REAL CI + Runtime + Bug Hunt + Golden regression before each gate transition.
6. Persist verified state; H101 remains locked.

## H100 PR #83 checkpoint

PR #83 merged at `d92eb9d3f63819e744b1c901504d447508cd9cab` after exact head `ce3a2298495f579f37b51c17961d03dbd467f4d8` passed PR CI #252, Runtime #539, and Bug Hunt #209. The merged extractor is read-only and conservative: it captures CAD/source evidence and direct semantic candidates without treating generic geometry as architectural truth. Semantic authority remains false and unresolved domains remain UNKNOWN. Post-merge workflow runs for the merge commit were not exposed, so post-merge Green is not claimed.

### Immediate continuation after PR #83
1. Reconcile DWG evidence into source-bound CandidateFacts with DIRECT/DERIVED/INFERRED provenance.
2. Add contradiction/negative-evidence handling at the CAD-evidence boundary.
3. Build real-world transformed/defective Golden DWG fixtures and expected fail-closed outcomes.
4. Expand layer/block/text/dimension/level/section semantics without allowing unsupported inference to PASS.
5. Run exact-head REAL CI + Runtime + Bug Hunt + Golden regression before every gate transition.
6. Persist only verified state; H101 remains locked.


## H100 PR #84 checkpoint — DWG evidence reconciliation

PR #84 merged at `2038ea392fcaeccafc67f8d5ea695a16ff34a918` after repaired exact head `bd86bb20141fba44cc25c1c93aee44b00645125d` passed PR CI #258, Runtime #545, and Bug Hunt #215. The bridge is source-bound and read-only: it normalizes DWG semantic candidates, text, and dimensions into the existing DrawingEvidence contract, while generic geometry remains non-authoritative and no second PlanModel is introduced. The first Bug Hunt failure was governance-format-only and was fixed before merge. Semantic Golden truth is still unresolved; real-world adversarial fixtures are still pending; H101 remains locked. Post-merge workflows for `2038ea392fcaeccafc67f8d5ea695a16ff34a918` are not exposed, so post-merge Green is not claimed.

### Next execution order
1. Bind normalized evidence to CandidateFacts with explicit DIRECT/DERIVED/INFERRED provenance and source SHA continuity.
2. Add contradiction/negative-evidence handling at the DWG evidence boundary.
3. Expand conservative level/section/scale/unit/drawing-language semantics.
4. Build real-world transformed/defective Golden fixtures and expected fail-closed outcomes.
5. Run exact-head REAL CI + Runtime + Bug Hunt + required Golden regression before each gate transition.
6. Persist only verified state; keep H101 locked until H100 Green evidence is complete.


## H100 PR #86 checkpoint — CandidateFact provenance

PR #86 merged at `117e6f52cbe02bedc59dfbf73810a821d7a70765`. Fixed exact head `e9804928523e0f3ed3b6c8a9847fbc400247ab32` passed PR CI #264, Runtime #551, and Bug Hunt #221. The implementation binds normalized DWG evidence to source-bound CandidateFacts with deterministic fact IDs and validates evidence references/source SHA continuity; contradictions are preserved and routed through the canonical reconciliation path.

The initial Bug Hunt #220 failure was governance-format-only (missing `## Bug Hunt` heading); it was corrected in `e980492...`, then all three gates passed. No open PRs remain at this checkpoint. Workflow runs for merge commit `117e6f...` are not exposed by the current commit workflow-run query, so post-merge Green is not claimed.

### Next execution order
1. Implement contradiction/negative-evidence hardening at the DWG boundary.
2. Add conservative level/elevation, section-marker/cut-plane/direction, scale/unit and Iranian drawing-language semantics.
3. Build real-world transformed/defective Golden fixtures with fail-closed expected decisions.
4. Run exact-head REAL CI + Runtime + Bug Hunt + required Golden regression.
5. Persist verified state; H101 remains locked until H100 Green evidence is complete.



## H100 PR #88 checkpoint — negative evidence hardening

PR #88 merged at `a6ae2d3273dc97face2fbb3e3190dd7a333f7bdb`. Exact verified head `b465b5951c27f1df4164ef02adf854d14f4dd15a` passed PR CI #269, Runtime #556 and Bug Hunt #226. The implementation fences contradiction and required-evidence references to the same source-bound DrawingEvidenceSet and rejects missing/cross-source/overlap cases.

PR #87 documentation checkpoint also merged at `e520aaf91063cb45a424b76a1960b804b9b56852`, with exact head `719ae231390e3cdbbe66de0230cdceb1d058b547` passing PR CI #270, Runtime #557 and Bug Hunt #227.

No post-merge workflow run is currently exposed for PR #88 merge SHA, so no post-merge Green claim is made.

Next: level/elevation → section marker/cut-plane/direction → scale/unit → Iranian drawing language → real-world adversarial Golden fixtures. H101 stays locked.


## H100 PR #90 checkpoint — level/elevation evidence

PR #90 merged at `c4011e0a8b67b3da41b755dfb485c1f2b60a71a0`. Exact head `5ab500c72151e64f8a63c80c211c3d5522ed7cb3` passed PR CI #276, Runtime #563 and Bug Hunt #233. Level extraction remains conservative and source-bound; numeric text alone is not promoted, and stair/floor inference remains pending.

Next: section marker/cut-plane/direction → scale/unit → Iranian drawing language → real-world adversarial Golden fixtures.


## H100 PR #91 checkpoint — merged state

PR #91 was merged at \`2dfcd893ed97028f69982477dc7d9d6741eff9ca\` after exact-head \`1d6eb08b16abaf60b2c2bd5ed390db962c38b864\` passed PR CI #287, Runtime #574, and Bug Hunt #244. It is a documentation checkpoint only; it does not close H100 or unlock H101. No post-merge mainline Green is claimed.

## H100 PR #93 checkpoint — merged

PR #93 merged into main at `2842cf2523fb9140b72f03a2311addf06c468af2`. Its exact head `26f1a0c9c0f47b3d8fa5f419f4a659c57b6e9d5e` passed PR CI #289, Runtime #576, and Bug Hunt #246. The implementation accepts only contextual/source-bound marker evidence; direction and cut-plane geometry remain UNKNOWN. H100 is not complete and H101 remains locked.

## Pre-phase audit checkpoint — 2026-10-09

**Current verified point (2026-10-09):** `main` is `2842cf2523fb9140b72f03a2311addf06c468af2` (PR #93 merged). PR #93 exact head `26f1a0c9c0f47b3d8fa5f419f4a659c57b6e9d5e` passed PR CI #289, Runtime #576, and Bug Hunt #246. The merge commit has no exposed post-merge workflow runs/statuses through the available read path, so mainline post-merge Green is NOT claimed.

**Open H100 PRs (all still require review; no submitted reviews are recorded):**
- PR #96 book evidence map — head `1df773883036525e20c972815ac3a3410c00d7da`; PR CI #300, Runtime #587, Bug Hunt #257 = SUCCESS.
- PR #97 educational drawing references — head `25d57ef7e6b18f49228f9194b3991a92387cd04b`; current exact-head workflow-run query and combined status both returned no evidence. Status = UNOBSERVED, not GREEN. Re-run/verify PR CI, Runtime Tests, and Bug Hunt on this exact head before merge.
- PR #98 scale/unit fail-closed contract — head `7092f3cba6fc5b3f8747bbe78ff2e2976111ae1b`; PR CI #303, Runtime #590, Bug Hunt #260 = SUCCESS. Required prerequisite for #99.
- PR #99 scale/unit Golden bridge — head `c472396d5a3a984c8c134bb7f55d068326c4fc14`; PR CI #313, Runtime #600, Bug Hunt #272 = SUCCESS. Do not merge before #98; after #98 merges, rebase/retarget to updated main and rerun every gate on the final exact head.

**Governance blockers:** H100 remains active and H101 remains LOCKED. Golden semantic ground truth and real-world transformed/defective fixtures are incomplete. Repository ruleset `Min` (ID `24680937`) is `disabled`, targets no branches, and has no required status checks configured; the intended protections therefore do not currently enforce review or CI. Enable/configure it for `refs/heads/main` before treating branch protections as active.
