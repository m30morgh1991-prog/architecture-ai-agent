## Live repository checkpoint — 2026-11-12 (refreshed after PR review and regression fixes)

- Current `main` SHA: `4e7ede9bd3267ac2440ab55e1cdd4cba2fcd04f5`. Exact-main combined-status and workflow-run queries returned no records. **Mainline Green remains UNKNOWN.**
- Open PR inventory: #119, #127, #128, #129, #130, #131, #132, #133. PR #126 is merged. No PR has been merged or approved in this continuation.
- PR #133 documentation checkpoint head `bafe2ebc5eff9c691f5dc10744ba864addf1e471` passed PR CI Gate #43275277286, Runtime Tests #43275277323, and Bug Hunt Gate #43275277283. This checkpoint refresh changes the PR head; those runs are historical for the old head and must be rerun.
- PR #127 (read-only Golden DWG geometry coordinates) remains open at `4a3642bc88314af58c56a628ce40c058fd8dd2a6`; its PR CI #38382657911, Runtime #38382657906, Bug Hunt #38382657885, and Golden export #38382658040 passed on that historical head. OCS/WCS and INSERT transforms remain UNKNOWN. PR #127 and PR #129 both modify `runtime/dwg_semantic_evidence.py`; a review comment documents the required conflict-resolved combination. Do not merge either stale branch without preserving both feature sets and rerunning exact-head gates.
- PR #128 (review report, input completeness, PlanModel revision diff) now includes a fail-closed fix: placeholder scale/unit values no longer count as PASS; malformed or zero scale ratios, unitless labels, and unknown unit tokens require review. Regression tests were added. Head `655f656a7fa84a7a07377cdf37d2ddb93b8f7290` passed PR CI #43292183863, Runtime #43292183993, and Bug Hunt #43292183899. The Bug Hunt report was then updated at head `182ede7df04e71188232cda4175bdc2e03df4889`; at checkpoint time Bug Hunt was success while PR CI and Runtime were still in_progress. These helpers remain additive and are not wired into the runtime pipeline. Review comments also require explicit coordinate-frame **and unit** attestation for revision diffs; a bare boolean is insufficient.
- PR #129 (AIE v0.1 and Autodesk read-only evidence) now fixes level-text parsing. `LEVEL 2 FFL +3.20 m` resolves to 3.20 m; `LEVEL 2` and uncontextualized numbers remain UNKNOWN with no promoted elevation; conflicting elevation values remain UNKNOWN. Regression cases include Persian `تراز`, FFL, T.O., missing units, floor-index-only text, and multiple values. Head `9a4bfedf18c84a570191936a20cb7ba2ac185525` passed PR CI #43292093376, Runtime #43292093364, Bug Hunt #43292093328, Golden export #43292093345, and AgentShield #43292093331. The Bug Hunt report was subsequently updated to head `85f1a55b35698d0d1c61e09e543c8b8c30ef29b0`; no check runs were yet visible for that latest documentation-only head at checkpoint time. Review state is COMMENTED, not APPROVED. The adapter remains read-only evidence, not architectural semantics or regulatory authority.
- PR #130 (fail-closed AutoCAD snapshot binding) remains stacked on #129 at `925fdbf843b6bb9ab3cd82e93be5b09f6d340eab`. Against the latest #129 head `85f1a55b35698d0d1c61e09e543c8b8c30ef29b0`, comparison is diverged (3 commits ahead / 10 behind from #130's side); GitHub reports #130 not mergeable. Rebase/reapply #130 only after #129 is accepted, then rerun all exact-head gates.
- PR #131 (DWG-to-DXF fidelity experiment) remains open and BLOCKED as a lossless conversion path. Golden DWG to DXF Fidelity Test #43270191429 failed: Afifiiiii lost 72,447 LINE entities plus other data; native writer is BLOCKED by XDATA, preview and extension-dictionary preservation. Source hashes before/after match; Golden originals were not modified.
- PR #132 (AutoCAD 2020 target) remains stacked on #130. All six exact-head checks on `94f506e0b5d87c9fa01565e960e6de866f0dd2b4` completed/success: PR CI #43274718737, Runtime #43274718636, AutoCAD 2020 Host Compatibility Contract #43274718725, Bug Hunt #43274718809, Golden export #43274718850, AgentShield #43274718600. **Real Windows/AutoCAD build and NETLOAD are deliberately deferred at the user's request** until laptop Windows and required software are reinstalled. Record host tests as NOT_RUN, not as PASS or failure.
- PR #119 Shiraz parking-rule audit remains research-only. The 1383 transcription is secondary-source evidence; the 2025 report referencing letter 176814/99/1399 appears in a municipal-fee adjustment resolution and does not itself prove the current parking-design rule or its dimensions. No numerical local rule may be enforced until the actual applicable approved text and amendments are obtained.
- Golden DWGs `bagheri7.dwg` and `afifiiiii.end.edit3.dwg` remain immutable. INSUNITS=1 is declared inches metadata, not proof of effective geometry scale. No unit conversion, dimension-to-geometry association, semantic promotion, or compliance PASS is authorized without independent evidence.
- Autodesk snapshot binding remains NEEDS_REVIEW until active in-memory database identity is independently bound to disk bytes. H100 remains active; H101 remains LOCKED until Golden Understanding acceptance evidence is complete.

### Immediate continuation order
1. Finish exact-head PR CI and Runtime checks for latest PR #128 and #129 documentation heads; inspect any failure logs and fix only evidenced issues.
2. Obtain required human review/approval for #128 and #129; do not bypass repository protections.
3. After #129 acceptance, resolve the #127/#129 shared-file overlap and refresh/reapply #130 onto the final #129 head. Then refresh #132 onto the final #130 head.
4. Keep #131 blocked; investigate a different converter/export route only with entity-by-entity fidelity checks and immutable-source hashes.
5. Keep #119 research-only until primary official Shiraz rule text, amendments, jurisdiction and effective date are verified.
6. Defer all Windows/AutoCAD host testing until the user's laptop reinstall is complete. Meanwhile continue source-level tests, CI, evidence contracts and documentation.
7. Recheck mainline CI after any future merge; absent/queued/running evidence is UNKNOWN, not Green.

---
---
---

## Live repository checkpoint — 2026-11-11 (refreshed from live GitHub)

- Current `main` ref: `30e141bfb644d120e53c57070cd200df8fdbeeae` (PR #121 merge commit; PR #125's `711c085508ab563d347c5c3918263317b08325f2` is its parent, not the current main head).
- Mainline CI evidence for `30e141bfb644d120e53c57070cd200df8fdbeeae`: the available workflow-run and combined-status queries returned no records. **Post-merge mainline Green is not claimed.**
- Live open PR inventory checked 2026-11-11: #119, #126, #127, #128, #129, #130. No PR was merged, approved, or closed as part of this checkpoint.
- PR #127 (read-only Golden DWG geometry coordinates) is based on current main, exact head `4a3642bc88314af58c56a628ce40c058fd8dd2a6`; PR CI #38382657911, Runtime #38382657906, Bug Hunt #38382657885, Golden export #38382658040 all completed/success. Coordinate-frame reconciliation remains UNKNOWN for unresolved OCS/WCS and INSERT transforms. Review comment requested entity-specific CSV fields; the PR body reports these fields and a regression test were added and the thread resolved. PR remains open.
- PR #128 (review findings, input completeness, PlanModel revision diff) is based on current main, exact head `3af9328a90909191ce494287f59f95f8a48d2650`; PR CI #40281675282, Runtime #40281675235, Bug Hunt #40281675279 all completed/success. Its 46 tests cover additive deterministic contracts; these helpers are not yet wired into the runtime pipeline. PR remains open.
- PR #129 (AIE v0.1 + Autodesk read-only evidence extractor) is based on current main, exact head `4924622886aa00d7f1c039e010269b7d47f7c359`; PR CI #42915700762, Runtime #42915700788, Bug Hunt #42915700846, Golden export #42915700723, AgentShield #42915700735 all completed/success. Review state is COMMENTED, not APPROVED. AIE remains read-only; no semantic or compliance authority is granted.
- PR #130 (fail-closed snapshot-binding correction) is stacked on PR #129, exact head `925fdbf843b6bb9ab3cd82e93be5b09f6d340eab`; PR CI #42918732550, Runtime #42918732442, Bug Hunt #42918732385, Golden export #42918732429 all completed/success. It ignores an exporter-supplied `snapshot_binding_status=VERIFIED` claim and keeps unproven in-memory-to-disk binding at NEEDS_REVIEW. It must not be merged ahead of its parent PR #129.
- PR #126 (this durable-state repair) was previously green on head `5980ced03478e5164a3ff1b0eb56838445cd260c`: PR CI #38393586659, Runtime #38393586450, Bug Hunt #38393586341 all completed/success. The branch was synchronized with current main `30e141bfb644d120e53c57070cd200df8fdbeeae` on 2026-11-11 (compare: ahead 38, behind 0). The refreshed checkpoint changed its exact head; rerun all required gates before claiming Green.
- PR #119 (Shiraz parking-rule/source audit) is research-only and based on old `4c167caace10afe2806439f0f260bb544f95b7d0`; its branch is diverged from current main (4 commits ahead, 5 behind). Its old-head PR CI #38393757098, Runtime #38393756952, Bug Hunt #38393757050 succeeded, but these do not replace rebase/refresh and exact-head checks. Secondary-source values remain unverified; no current regulatory threshold is asserted.
- Autodesk/Golden findings: both preserved Golden DWGs previously exported successfully with source hashes matching the manifest and `source_mutated=false`. Both report `INSUNITS=1` (inches), but scale remains NEEDS_REVIEW. Layer-name evidence supports WALLS and COLUMNS candidates only; the misspelled source layer `COULMN` is not geometric column recognition. DOORS/WINDOWS remain UNKNOWN. Persian text/font recovery is not verified.
- Dimension boundary: the current C# exporter emits dimension type/text/measurement but not typed definition points. The earlier 67/68 result is annotation-point self-consistency only, not dimension-to-entity geometric association. Full reconciliation remains pending.
- Real AutoCAD 2025/2026 build and in-host smoke test remain NOT_RUN. They require a Windows host with matching AutoCAD managed assemblies and a disposable DWG; Golden sources must not be used for this test.
- No unit conversion, geometric association, semantic promotion, compliance PASS, H-stage advancement, approval bypass, or merge is authorized by this checkpoint. H100 remains active; H101 remains LOCKED. Golden DWGs remain immutable.

### Immediate continuation order
1. Verify this refreshed durable-state PR on its new exact head (PR CI, Runtime Tests, Mandatory Bug Hunt).
2. Complete human review of PR #127/#128 and review PR #129; keep PR #130 dependent on acceptance of #129.
3. Run the AutoCAD host build/smoke test on a disposable drawing when a compatible Windows/AutoCAD host is available.
4. Add typed dimension definition-point evidence and a conservative dimension-to-geometry reconciliation contract; keep ambiguous matches NEEDS_REVIEW.
5. Continue Persian font/encoding provenance and block/geometry-based door/window evidence; unsupported cases stay UNKNOWN.
6. Refresh stale PR #119 against current main before any merge decision. Keep H101 locked until H100 semantic acceptance evidence is genuinely complete.

---

## Historical checkpoint — 2026-10-12 (superseded by the live checkpoint above)

- Latest verified main checkpoint is PR #125 merge commit `711c085508ab563d347c5c3918263317b08325f2` (PR #125 is merged). PR #121 merge commit `30e141bfb644d120e53c57070cd200df8fdbeeae` is a prior historical milestone, not the latest main checkpoint.
- PR #124 fixed a real Bug Hunt false-pass: headings/tokens inside fenced Markdown code previously could satisfy required evidence. The validator now ignores fenced blocks and fails closed on an unclosed fence. Regression coverage was added; post-merge checks on PR #124 merge commit `8cb2fe258f5dad3984f91492502630f4a6e28da6` were completed/success (PR CI #38164505118, Runtime #38164505129, Bug Hunt #38164505253).
- PR #125 is merged at `711c085508ab563d347c5c3918263317b08325f2`, persisting PR #124's verified state. This new checkpoint refresh corrects the stale top-level live checkpoint, which still pointed at PR #115 while later PR #124/#125 evidence had been appended lower in the files.
- Live PR checkpoint checked on 2026-10-13: PR #119 (Shiraz parking-rule/source audit), PR #126 (durable-state checkpoint repair), and PR #127 (clean mainline geometry-evidence replacement) are open. PR #121 was merged at `30e141bfb644d120e53c57070cd200df8fdbeeae`; PR #125 merge `711c085508ab563d347c5c3918263317b08325f2` remains the latest verified main checkpoint. PR #123 was re-opened by repository activity, then explicitly closed unmerged again on 2026-10-13 as superseded by PR #127. PR #127 current head `4a3642bc88314af58c56a628ce40c058fd8dd2a6` is based directly on main and all four exact-head workflows are completed/success: PR CI #38382657911, Runtime Tests #38382657906, Bug Hunt #38382657885, and read-only Golden DWG Evidence Export #38382658040. ECC found incomplete entity-specific geometry fields in `geometry.csv`; those fields are now exported, a regression test was added, and the review thread is resolved after all gates passed. `coordinate_frame_status=UNKNOWN` remains fail-closed until OCS/WCS semantics and INSERT transforms are reconciled. PR #127 remains unmerged pending required human approval. PR #126 exact-head gates all passed at `62d37e0a2fbf95c9ad7ad5db4c021ad54ec86f08`, but any new state-doc commit requires fresh exact-head checks. PR #119 remains research-only; verify the current official rule edition and applicability before any compliance claim.
- Durable-state rule: the top-level live checkpoint must name the latest verified main SHA, while historical H-stage notes must be explicitly labeled historical. Never infer latest state from appended sections alone.
- H100 remains active; H101 remains LOCKED until Golden Understanding acceptance evidence is green. Golden DWG fixtures remain immutable. No auto-merge, no bypass, no stage advancement from documentation work.

---

## Post-merge checkpoint — PR #124 / ECC-inspired TDD Bug Hunt validator hardening (2026-10-11)

- PR #124 was squash-merged into `main` as `8cb2fe258f5dad3984f91492502630f4a6e28da6`.
- The defect was reproduced during the test-only RED phase: required Markdown headings/tokens inside fenced code could be mistaken for valid Bug Hunt evidence.
- Minimal fix: validate exact heading lines and required tokens only outside fenced code blocks; an unclosed fence fails closed. Regression tests cover fenced-code headings and tokens.
- Post-merge required checks on the exact merge commit are completed/success:
  - PR CI Gate [#38164505118](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38164505118)
  - Runtime Tests [#38164505129](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38164505129)
  - Bug Hunt Gate [#38164505253](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38164505253)
- Scope was limited to Bug Hunt evidence validation and regression tests. No PlanModel, ConstraintMap, ApprovedChangePlan, BIM, architectural-understanding logic, runtime architecture editing, or Golden DWG assets were changed.
- H100 remains active; H101 remains LOCKED until Golden Understanding acceptance evidence is green. Golden DWG fixtures remain immutable.
- Next: create a separate documentation-only checkpoint PR to persist this verified state. Then pilot ECC Code Review independently, with concrete file/line and reproducible findings only. No full-toolkit installation, auto-merge, approval bypass, or autonomous H-stage advancement.

## Post-merge checkpoint — PR #120 / ECC workflow evaluation queued (2026-10-11)

- PR #120 merged to `main` as commit `8f6052e9f692a8247924c9b532ccb116c03be928`.
- Exact pre-merge head `22916262e0882164d904342af1be559d78f51c31` passed Bug Hunt Gate run [#38144467841](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38144467841), PR CI Gate run [#38144467815](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38144467815), and Runtime Tests run [#38144467813](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38144467813).
- Post-merge mainline checks on exact commit `8f6052e9f692a8247924c9b532ccb116c03be928` are all completed/success:
  - PR CI Gate [#38144634836](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38144634836)
  - Runtime Tests [#38144634842](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38144634842)
  - Bug Hunt Gate [#38144634816](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38144634816)
- PR #120 adds a durable checkpoint for the already-merged ECC AgentShield pilot; it does not modify runtime logic.
- ECC TDD and Code Review remain research/pilot candidates, not installed or adopted. Next pilot must be isolated and evidence-based; no whole-toolkit install.
- H100 remains active; H101 remains LOCKED pending green Golden Understanding acceptance evidence. Golden DWG fixtures remain immutable.
- No auto-merge, approval bypass, or autonomous stage advancement.
## Post-merge checkpoint — PR #118 / ECC AgentShield pilot (2026-10-11)

- PR #118 was squash-merged into `main`; post-merge commit: `4c167caace10afe2806439f0f260bb544f95b7d0`.
- PR #117 was closed as superseded; no checks or protections were bypassed.
- Exact pre-merge PR #118 head `fb0a568336ca98aa7e468fdde2cdd41d7d91def7` passed required PR gates and the advisory AgentShield scan (Grade A, 100/100, zero findings).
- Post-merge mainline gates on exact commit `4c167caace10afe2806439f0f260bb544f95b7d0` are verified completed/success:
  - PR CI Gate run [#38143697507](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38143697507)
  - Runtime Tests run [#38143697485](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38143697485)
  - Bug Hunt Gate run [#38143697482](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38143697482)
- AgentShield is advisory only. Workflow success must not be interpreted as proof the scanner itself passed; it does not replace CI, Runtime Tests, or Bug Hunt.
- Scope is limited to coding-agent configuration scanning. No architecture understanding, PlanModel, ConstraintMap, Golden DWG, runtime-validation, or source-of-truth behavior changed.
- H100 remains active; H101 remains LOCKED until Golden Understanding acceptance evidence is genuinely green. Golden DWG files remain immutable.
- Next: pilot ECC TDD workflow and Code Review workflow independently on isolated changes; inspect outputs and licensing/security implications; adopt only useful coding-workflow helpers. No whole-toolkit installation, auto-merge, approval bypass, or autonomous H-stage advancement.
- This checkpoint was prepared only after all three post-merge gates completed successfully on the exact main SHA above.

# Architecture AI Agent — Master Handoff

## Live repository checkpoint — 2026-10-11 (after PR #115)

- Verified latest main commit: `3b584b6459fadece28ed8744ca94ed7b0a01e5cf`, created by squash-merging PR #115.
- PR #115 exact pre-merge head `642671abab3dafa00c9ccd56037da1efc610aded` passed PR CI Gate #372, Runtime Tests #659, and Mandatory Bug Hunt #331 (completed/success) before merge.
- **Post-merge mainline Green is verified for `3b584b6459fadece28ed8744ca94ed7b0a01e5cf`:** PR CI Gate run #373, Runtime Tests run #660, and Bug Hunt Gate run #332 were all completed/success on this exact SHA. See [PR CI Gate #373](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38123425938), [Runtime Tests #660](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38123426028), and [Bug Hunt Gate #332](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38123426003).
- Scheduled Governance Health Check run #1 completed/success at [run #38095937202](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38095937202), running runtime smoke tests, the complete unittest suite, and Bug Hunt governance contract tests. It occurred before PR #115 merged (event SHA `caa8bdf5d74449ba70e52a699036bd5281a1967b`), so it confirms the scheduled workflow works but does not replace exact-SHA mainline gates.
- Ruleset `Min` (ID `24680937`) requires `runtime-tests`, `test`, and `Mandatory Bug Hunt`. Required approving reviews remain zero by the user's explicit decision; do not change this without explicit authorization.
- No secure AI execution provider has been configured or verified. The independent runner remains a deterministic policy contract, not a live AI execution service. No auto-merge or autonomous H-stage advancement is enabled.
- H100 remains active. H101 remains LOCKED until Golden Understanding acceptance evidence is genuinely green. Both Golden DWG files remain immutable.


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

- H99 — Architectural Relations is merged on main: `2344e1083937e5d91857ba24b6a0f077414f06ca`.
- PR #65 Feature-to-File Matrix + semantic-chain research is merged: `176bc2ceb330e2987891ef6edbbaf33b73dc77d3`.
- PR #65 pre-merge gates: PR CI #138, Runtime #425, Bug Hunt #96 — completed/success.
- Post-merge main gates on `176bc2c`: Runtime #427, PR CI #140, Bug Hunt #97 — completed/success.
- H100 source-boundary work is historical; active H100 work is PR #70 on `research/h100-golden-understanding-lock`.
- Implemented boundary: Image Input remains supported but is separate from Engineering Plan Input.
- Geometry evidence hierarchy: **DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP**.
- PDF must be classified by evidence as vector or raster; unknown representation remains fail-closed.
- `runtime/input_source_contract.py` defines the source classes and trust ordering.
- `runtime/request_contract.py` carries optional `source_profile` metadata.
- H100 is **not complete yet**; PR #70, #71, #72, #73, #74 and #75 are merged. PR #75 merge is `c056c31ff97db532381c7466388200ff3cb62aeb`. Exact-head PR #75 gates: PR CI #219, Runtime #506, Bug Hunt #176 — completed/success. Golden source SHA-256 values are now persisted and byte-verified. A dependency-free read-only CAD inspection adapter is merged behind the provider-neutral boundary. Full Golden semantic ground truth, adversarial coverage, and the remaining UG gates are still incomplete; H101 remains locked.

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

## Continuation after H99 / PR #65

1. H99 is complete and post-merge main CI is GREEN.
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

### Current H100 work
Finish source provenance/evidence binding, drawing-language semantics, contradiction/missing-evidence handling, fail-closed propagation, adversarial Golden coverage, and semantic ground truth. The persisted Golden hashes prove source identity only; they do not promote uncertain understanding to PASS. H101 remains locked until UG-01..UG-09 are actually Green.


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

## H100 PR #93 — current implementation branch

- Branch: \`feature/h100-section-marker-semantics\`.
- Scope: typed, source-bound, read-only section/cut-plane/elevation/detail marker candidates from explicit contextual text or explicitly named marker blocks.
- False-positive boundary: bare \`A-A\` is not enough; section marker presence does not prove direction, cut-plane endpoints, or view geometry.
- Source SHA-256 and DIRECT provenance are carried into each emitted candidate.
- Tests cover Persian section context, bare-label rejection, named marker blocks, and fail-closed direction/cut-plane status.
- Run exact-head PR CI + Runtime + Bug Hunt and preserve Golden regression before merge. H101 stays locked.


## Plan-understanding research checkpoint — 2026-10-10

- Research record: `docs/research/plan-understanding-research-and-revit-ai-review-2026-10-10.md`; capability mapping: `docs/research/ARCHITECTURE_AGENT_FEATURE_FILE_MATRIX.md`.
- Highest-value additions are evaluation patterns from fpvec-lab/ResPlan-FP (separate wall/room/opening metrics, topology, correction cost), AEC-Geometric-Bench (external geometric validation subject to non-commercial data terms), and ConstructDrawingAI CIR (vector-first ingestion, explicit connectivity, provenance/confidence, perception/reasoning separation).
- Raster-to-Graph, FloorPlan2IFC, FloorPlanCAD, and PerDAW are recorded as follow-up research candidates; their dependencies, dataset access, and artifact-specific licenses must be reviewed before use.
- Revit product review distinguishes Drafted in Revit (new schematic single-storey house-plan generator) from WiseBIM AI (existing 2D plan-to-Revit reconstruction) and Autodesk Assistant/Generative Design (model/documentation actions and constrained alternatives). None proves Iranian code compliance or the project's required understanding of levels, stairs, section direction, and local drafting language.
- No external code or dataset was imported. No new runtime provider/dependency was added. The research record does not change the Source of Truth or authorize a parallel semantic model.
- Licensing guardrail: AEC-Geometric-Bench data and FloorPlanCAD material have non-commercial restrictions described by their maintainers; ConstructDrawingAI code is PolyForm Noncommercial. Verify each artifact's terms before reuse.
- Acceptance remains fail-closed: external scores do not replace source-bound Golden semantic ground truth. Golden DWGs are immutable. H100 remains active and H101 remains locked until actual semantic acceptance evidence and all exact-head gates are green.


## Post-merge checkpoint — PR #113 and independent runner (2026-10-10)

- PR #113 merged via squash at `caa8bdf5d74449ba70e52a699036bd5281a1967b`.
- Exact PR-head `36e73894c43b96ff4454b8367e7c182dd4c40307`: PR CI #363, Runtime Tests #650, Mandatory Bug Hunt #322 completed/success. These are PR-head results, not post-merge mainline checks.
- Post-merge mainline workflows for the squash SHA have not been observed; mainline Green is not claimed.
- Runner remains a deterministic policy contract, not an autonomous coding service. No provider/execution backend is configured or verified, and the first successful health-check run remains unobserved.
- Next: verify a real scheduled/manual health-check run; configure an execution backend securely; then implement a bounded event-driven canary on an isolated branch. No automatic merge or H-stage advancement.
- H100 active; H101 locked; Golden DWGs immutable.
