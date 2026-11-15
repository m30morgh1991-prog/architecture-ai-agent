## Runtime remediation chain update — 2026-11-15

This is the newest inventory snapshot and supersedes prior PR-count notes.

- Current open PR count: **19** — the 16 PRs retained after cleanup plus #150, #151, and #152.
- PR #150 exact head `b50ade91cd1e9c771f7e81500dc9fbf6f1a23c3a`: Bug Hunt #43740147040, Runtime #43740147034, PR CI #43740147064 completed/success; 429 tests passed. Draft.
- PR #151 exact head `d52e9c1a92f58f4a1a629dbf413a2746f627491e`: Bug Hunt #43741176591, Runtime #43741176576, PR CI #43741176603 completed/success; 432 tests passed. Draft, stacked on #150.
- PR #152 exact head `2b7b7d08269893aebf6b612dcd19b4f42667dbbc`: Bug Hunt #43741879578, Runtime #43741879584, PR CI #43741879589 completed/success; 433 tests passed. Draft, stacked on #151.
- Dependency order is strictly #150 → #151 → #152. Do not merge later PRs independently or before their base PRs.
- #150 fixes the false EXECUTE PASS audit event on rejected requests.
- #151 binds idempotency replay to a canonical request fingerprint and rejects changed payloads using the same execution ID.
- #152 makes Handler._json serialize nested dataclass values through dataclasses.asdict while still rejecting arbitrary unsupported objects.
- A remaining P0 API/runtime backlog: strict HTTP request schema validation and body-size caps; localhost-only binding/authentication before network deployment; durable execution/audit/idempotency storage; canonical PlanModel/ConstraintMap runtime integration; in-flight idempotency reservation for concurrent execution; and real controlled CAD writer implementation.
- PR #151's initial valid-request test also identified that successful HTTP responses previously failed serialization; this is fixed by #152 and covered by its regression test.
- No PR was merged, approved, or closed in this update. All three remediation PRs remain Draft; explicit user authorization is required for each merge.

The current PR #147 head before this addendum was `8c4bbbc66795a536ad7e83e14c9c50b655f2ae68`, with Bug Hunt #43741582623, Runtime #43741582593, and PR CI #43741582627 completed/success. This addendum changes PR #147's head, so those results are historical and must be rerun on the new exact head. Mainline CI remains UNKNOWN; Windows/AutoCAD/ODA host tests remain NOT_RUN.

---

## Current PR queue and runtime blocker update — 2026-11-15

This update supersedes the prior open-PR count above.

- Current open PR count: **18** — the 16 PRs remaining after the two cleanup closures, plus #150 and #151.
- PR #150 current head `b50ade91cd1e9c771f7e81500dc9fbf6f1a23c3a`: Bug Hunt #43740147040, Runtime #43740147034, PR CI #43740147064 all completed/success; 429 tests passed. Draft, not merged.
- PR #151 current head `d52e9c1a92f58f4a1a629dbf413a2746f627491e`, stacked on PR #150: Bug Hunt #43741176591, Runtime #43741176576, PR CI #43741176603 all completed/success; 432 tests passed. Draft, not independently mergeable or merged.
- PR #151 TDD RED was observed on corrected test-only head `0e973e4a80d03c4ec3fcba62ad958743b10f9fa0`: the HTTP handler returned 200 for a different payload using the same execution ID; the regression expected 409. The implementation binds the idempotency cache to canonical request fingerprints and rejects mismatches.
- PR #151 also updates WorkflowGuard to use execution identity with the shared idempotency guard; a cross-execution key-reuse test passes.
- A separate P0 API defect was discovered while building the integration test: valid successful HTTP execution responses can fail JSON serialization because the response includes an ApprovedChangePlan containing a ChangeRequest dataclass, while the legacy handler uses plain `json.dumps`. This remains UNRESOLVED and must be fixed separately with a successful-request HTTP regression test.
- Other P0 items remain: HTTP body/schema validation and size limits, localhost/network binding, persistent execution/audit state, canonical runtime pipeline integration, and in-flight idempotency reservation for any future concurrent server.
- No PR was merged, approved, or closed in this update. PR #150 and #151 remain drafts; explicit user authorization is still required before each merge.

All listed CI evidence applies only to the exact heads named above. Mainline CI remains UNKNOWN because the fresh main SHA query returned no workflow/status records. Windows/AutoCAD/ODA host tests remain NOT_RUN.

---

## Post-cleanup implementation update — 2026-11-15

This addendum follows the repository cleanup snapshot above and records the first implementation PR opened after that snapshot.

- PR #150 — `fix(runtime): keep rejected executions out of PASS audit` — remains open as a draft, current exact head `b50ade91cd1e9c771f7e81500dc9fbf6f1a23c3a`.
- TDD RED evidence: on test-only head `d83fa8982c524e5b8f7f6f38e5adf8c74715316a`, Runtime Tests run #43739863627 ran 429 tests and failed exactly one: the new regression test observed the false `PASS` audit event.
- TDD GREEN evidence: on implementation head `95f1b993f8ddc6df655d24a60207e7255ad0d1ff`, Bug Hunt #43740008417, Runtime Tests #43740008362 and PR CI #43740008288 all completed/success; the full 429-test suite passed.
- The PR-150 evidence-only final head `b50ade91cd1e9c771f7e81500dc9fbf6f1a23c3a` was then rechecked: Bug Hunt #43740147040, Runtime Tests #43740147034 and PR CI #43740147064 all completed/success. The final full suite ran 429 tests; the new regression test passed.
- The fix records EXECUTE STARTED before validation, BLOCKED on rejection paths, and PASS only after validation, controlled-editing, and approval gates succeed. Rejected results expose audit_complete=false, audit_ok=false, and runtime_ok=false.
- The open PR count is now **17**, adding PR #150 to the 16-PR cleanup inventory above. No PR was merged or approved.
- This does not resolve the other P0 runtime issues: payload-bound idempotency, HTTP request validation/body limits, safe network binding, persistent execution/audit records, and canonical PlanModel pipeline integration remain open.

All statuses above apply only to their stated exact heads. Windows/AutoCAD/ODA runtime checks remain NOT_RUN. The owner-controlled merge policy is unchanged.

---

## Latest cleanup and exact-state audit — 2026-11-15

This section supersedes any conflicting PR counts, head SHAs, readiness labels, or CI claims in older checkpoint text below.

### Mainline evidence
- Current `main` SHA: `ad60e81cef4335c771fee8df4fad57740d06481b`.
- A fresh query of workflow runs and combined commit statuses returned no records for this main SHA. Mainline Green is therefore **UNKNOWN / NOT independently confirmed** in this audit. PR-head checks are not substitutes for mainline checks.

### Pull-request cleanup
- The live inventory initially contained 18 open PRs.
- PR #133 was closed as superseded by this newer checkpoint. Its discussion and branch are retained.
- PR #131 was closed as a failed, non-production ezdwg conversion experiment. Its data-loss result is retained as a negative regression baseline; neither its branch nor Golden inputs were deleted.
- Current open PR count after those two closures: **16** — #149, #148, #147, #144, #143, #139, #138, #137, #136, #135, #132, #130, #129, #128, #127, #119.
- No other PR or branch was closed or deleted. No PR was merged or approved.

### Exact-head CI evidence checked live
- PR #149, head `465548467b7da20abaf274a718f7c93cfb2dce1a`: Bug Hunt #698, AgentShield #82, PR CI #739, Runtime #1026, and acadrust pilot #18 all completed/success. This is still an isolated pilot; conversion fidelity remains NEEDS_REVIEW, not PASS.
- PR #147, head `4972438078d5fbe1fa6a0a43256a66fea3aa03d7`: Bug Hunt #685, PR CI #726, Runtime #1013 all completed/success. This state-file update creates a new head; all three checks must rerun.
- PR #143, head `2e9a8f5ebf1790471ed892e88aa8c431643d3e80`: Bug Hunt #667, PR CI #708, Runtime #995 all completed/success.
- PR #144, head `569ceffffa6104998b24da163b86c2e38052af1f`: Bug Hunt #631, PR CI #672, Runtime #959 all completed/success.
- PR #148, head `a8faeb44a39a124092587a9e5c0fd3e908a1c8ab`: Bug Hunt #661, PR CI #702, Runtime #989 all completed/success.
- PR #139, head `5cedcffb4c8dbc1e07b98eac640455872be816bd`: Bug Hunt #694, PR CI #735, Runtime #1022 all completed/success.
- PR #138, head `867fb5fee0f3b9a6b8a2957d50ef575a01526355`: Bug Hunt #665, PR CI #706, Runtime #993 all completed/success.
- PR #137, head `63d009f2cd138b1c1a6f7fb2fd66897920d07003`: Bug Hunt #676, PR CI #717, Runtime #1004 all completed/success.
- PR #136, head `9e1b937006001a9790ed1ccd2f3163960fe8f039`: Bug Hunt #682, PR CI #723, Runtime #1010 all completed/success.
- PR #135, head `fb52cc47d1c86104856a8c27f819fe5f5eaf3339`: Bug Hunt #662, PR CI #703, Runtime #990 all completed/success.
- These are exact PR-head workflow results only. They do not establish merge approval, runtime fidelity, or post-merge mainline Green.

### Dependency and backlog triage
- CAD comparator chain: PR #143 → PR #144 → PR #148. PR #144 is based on an older #143 head, and #148 is based on #144. Rebase/synchronize in dependency order and rerun exact-head checks before any merge decision.
- Autodesk evidence chain: PR #129 → PR #130 → PR #132. #130 and #132 are stacked and must not be treated as independently mergeable.
- PRs #127 and #128 are older mainline-based work; re-check their diff overlap and current base before deciding whether to retain, rebase, or close.
- PR #119 remains research-only for Shiraz parking-rule sources and is stale relative to current main; verify source currency and rebase before relying on it.
- PRs #135–#139 contain distinct contract/research corrections. Keep them open pending ordered technical review and integration decisions; green CI alone is not an instruction to merge.
- PR #147's earlier statements that mainline CI is green are superseded by the fresh query above, which returned no mainline run/status records.

### Repository cleanup boundaries
- No source files, runtime contracts, dependencies, Golden DWGs, or branches were deleted in this cleanup pass.
- No feature work was added. The next implementation priority remains the existing runtime/API safety and canonical-contract defects identified in the full audit.
- Windows, AutoCAD, ODA, and real-host tests remain NOT_RUN until the user confirms the Windows environment and software are ready.
- Owner-controlled merge policy remains unchanged: ask for explicit approval for each PR and exact head SHA before merging.

---

## Live repository checkpoint — 2026-11-15 (verified from GitHub)

### Mainline
- Current `main`: `ad60e81cef4335c771fee8df4fad57740d06481b`.
- PR #142 is merged. Its merge commit is the current main HEAD.
- Mainline checks on that exact SHA: `test`, `runtime-tests`, and `Mandatory Bug Hunt` are all `completed/success`.
- PR #142 established the current governance policy: AI performs technical review; the repository owner controls each merge. No PR may be merged without a separate explicit owner authorization for that PR and exact head SHA. No fabricated APPROVE review.

### Open pull requests and current gates
- Live open inventory includes PRs #149, #147, #143, #139, #138, #137, #136, #135 and older PRs #133, #132, #131, #130, #129, #128, #127, #119.
- **READY_FOR_OWNER_DECISION — PRs #135, #136, #137, #138, #139, #143, #147.** Each branch is synchronized with current main `ad60e81cef4335c771fee8df4fad57740d06481b`, GitHub reports mergeable=true, no unresolved review threads were found, and all required checks completed/success on the exact current head. This is technical readiness only; no human approval is fabricated and every merge still requires a separate explicit owner authorization for that PR and exact head SHA.
- **PR #135 — opening/host-wall evidence guard:** exact head `fb52cc47d1c86104856a8c27f819fe5f5eaf3339`; Bug Hunt, PR CI and Runtime Tests all completed/success. Rejects malformed/boolean/non-finite geometry, string wall inventories and invalid top-level inputs. Connected candidates remain UNKNOWN.
- **PR #136 — empty detector evidence and type integrity:** exact head `9e1b937006001a9790ed1ccd2f3163960fe8f039`; all three required checks completed/success. Adds source-bound UNKNOWN detector-gap evidence, rejects conflicting evidence-ID reuse, and requires PlanElement evidence type to match its ElementEvidence type.
- **PR #137 — SpaceModel numeric validation:** exact head `63d009f2cd138b1c1a6f7fb2fd66897920d07003`; all three required checks completed/success. Rejects booleans, non-finite values and numeric strings in bbox, centroid and area.
- **PR #138 — GeometryReference / H101:** exact head `867fb5fee0f3b9a6b8a2957d50ef575a01526355`; all three required checks completed/success. Public dataclass construction validates evidence; coordinate transforms must be affine and nonsingular. No DWG parsing or PlanModel integration is claimed.
- **PR #139 — open-source AEC/CAD research:** exact head `f04d5470c98c94a75bdcbdeb00d61370d3d2dbd3`; all three required checks completed/success. Static research only; no external code or model weights adopted.
- **PR #143 — DXF comparison provenance:** exact head `2e9a8f5ebf1790471ed892e88aa8c431643d3e80`; all three required checks completed/success. Streaming SHA-256 and ezdxf version are retained even on parse-failure reports.
- **PR #147 — durable checkpoint:** exact head `d3a2f1072d51b8251c0f4275d136272eb19db7c4`; all three required checks completed/success. This checkpoint refresh is being updated again with current PR/pilot results, so its current head and checks will change.
- **PR #149 — isolated acadrust DWG→DXF pilot:** draft, exact head `063c4b2547805b08f5264600b482ea504b8e0c48`; all five checks completed/success (PR CI, Runtime Tests, Bug Hunt, AgentShield, dedicated acadrust pilot). It is not production-ready and remains draft.
- **PR #131 — existing ezdwg Golden conversion:** dedicated conversion/reopen gate remains failed. Bagheri7's prior ezdwg output contained only 2 entities versus 8,842 source LINE entities; Afifiiiii output was similarly incomplete. This failure remains valid evidence and is not overridden by the separate acadrust pilot.
- **PR #132** remains stacked on PR #130; do not treat it as independently mergeable. Older PRs not listed as ready still require fresh exact-head review.
- No PR other than the previously authorized PR #142 has been merged. No PR approval is fabricated. No H-stage advancement is claimed.

### CAD conversion research and pilot evidence
- Issue #141 remains open for expansion of the independent read-only DXF comparator: layer/style/layout/entity inventories, units, XData/proxy content, dimensions, nested blocks and adversarial/resource-heavy fixtures.
- Issue #145 is now implemented as an isolated pilot in PR #149. It pins the crates.io release `acadrust = 0.6.8` (MPL-2.0), disables optional Rayon parallelism, and writes directly from `CadDocument` to a temporary DXF candidate through `DxfWriter::write_to_file`, avoiding a full intermediate DXF byte/string buffer.
- On the successful pilot head `a5ee9614835d21aadb34c0826fd4678ae31053ce` (before the final evidence-only commit), both Golden fixtures converted and reopened independently:
  - Bagheri7: 19,268 source entities; 19,268 acadrust DXF-reopen entities; ezdxf 1.4.5 independently found 13,208 modelspace entities, 42 layers and 7 linetypes.
  - Afifiiiii: 74,252 source entities; 74,252 acadrust DXF-reopen entities; ezdxf independently found 72,921 modelspace entities, 33 layers and 6 linetypes.
  - Both input SHA-256 values were unchanged. Rust and ezdxf core inventory checks matched.
  - Both decisions remain NEEDS_REVIEW, never PASS. Per-entity properties, dimensions, XData, proxy graphics, nested block semantics, layouts, fonts and CAD-host visual fidelity remain unresolved.
- Pilot artifact from run `43726067671`, artifact `14166741334`: [download evidence and candidate DXFs](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/43726067671/artifacts/14166741334). ZIP SHA-256: `a9f6f2fcf70193c8c3f18ff1e0c0512bc4b5465b4ed65e727b6765a31d4e0129`. It contains candidate DXFs, JSON reports, generated Cargo.lock and summary. Cargo.lock is not yet committed; it must be pinned before production adoption.
- The converter enforces a 512 MiB input/decompressed-data cap, mesh limits, strict parsing, source-hash immutability, no-overwrite atomic hard-link publication, candidate/report SHA-256, candidate byte size and Linux peak RSS when available. It never emits a production/final output.
- Upstream acadrust main is currently commit `52034a673ff59bf6936ebf01ec794b07a97df246`; comparison shows 581 commits beyond the `v0.6.8` release tag, despite the same package version string. A separate pinned-source comparison is the next experiment; do not silently substitute upstream main for the release.
- No production conversion provider is selected. No acadrust dependency has been added to production runtime manifests.
- CADCraft's reported 4.54 GB peak RSS for a 47.8 MB DWG remains a warning about its intermediate-DXF bridge, not an acadrust benchmark. MLightCAD's optional DWG worker remains GPL-3.0 and is not selected.

### Safety and unresolved evidence
- Golden DWGs remain immutable: `test-assets/golden-projects/bagheri7.dwg` and `test-assets/golden-projects/afifiiiii.end.edit3.dwg`.
- Windows, AutoCAD, and real ODA host tests remain `NOT_RUN` until the user confirms Windows replacement and software installation.
- Conversion fidelity remains UNKNOWN / NEEDS_REVIEW unless independently established. Parser success, a self-comparison, or a successful exit code is not a fidelity PASS.
- PlanModel remains canonical. No research candidate may mutate PlanModel, ConstraintMap, ApprovedChangePlan, BIM semantics, or H101.
- No repository settings, rulesets, branch protection, secrets, or collaborators were changed.
- The daily Architecture Agent Guard, Auto-Runner, and Daily Backup automations were found disabled. Auto-Runner's stored prompt predates the owner-controlled merge policy and must not be re-enabled without first replacing that conflicting instruction. This checkpoint does not claim automated daily monitoring is active.

### Continuation order
1. Complete final exact-head CI verification for PR #149 after its durable evidence update; keep it draft until the release and upstream-main comparison, entity-level fidelity checks, and license review are complete.
2. Run a second isolated acadrust comparison pinned to upstream commit `52034a673ff59bf6936ebf01ec794b07a97df246`; keep the released 0.6.8 result as the stable baseline.
3. Expand fidelity checks for entity-type counts, blocks/INSERTs, dimensions, HATCH boundaries, XData, layouts, units and text/font handling. Any discrepancy remains BLOCKED/NEEDS_REVIEW.
4. PRs #135, #136, #137, #138, #139, #143 and #147 are technically ready for individual owner decisions; merge only after explicit authorization for the exact current PR head.
5. Keep PR #131's ezdwg Golden failure visible; do not weaken its gate or route production conversions to an unproven provider.
6. Windows/AutoCAD/ODA host testing remains NOT_RUN until the user confirms the Windows environment is ready. Preserve fail-closed states and do not advance H-stages without evidence.

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
- Autodesk/G​​olden findings: both preserved Golden DWGs previously exported successfully with source hashes matching the manifest and `source_mutated=false`. Both report `INSUNITS=1` (inches), but scale remains NEEDS_REVIEW. Layer-name evidence supports WALLS and COLUMNS candidates only; the misspelled source layer `COULMN` is not geometric column recognition. DOORS/WINDOWS remain UNKNOWN. Persian text/font recovery is not verified.
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

# Project State

## Live repository checkpoint — 2026-10-11 (after PR #115)

- Verified latest main commit: `3b584b6459fadece28ed8744ca94ed7b0a01e5cf`, created by squash-merging PR #115.
- PR #115 exact pre-merge head `642671abab3dafa00c9ccd56037da1efc610aded` passed PR CI Gate #372, Runtime Tests #659, and Mandatory Bug Hunt #331 (completed/success) before merge.
- **Post-merge mainline Green is verified for `3b584b6459fadece28ed8744ca94ed7b0a01e5cf`:** PR CI Gate run #373, Runtime Tests run #660, and Bug Hunt Gate run #332 were all completed/success on this exact SHA. See [PR CI Gate #373](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38123425938), [Runtime Tests #660](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38123426028), and [Bug Hunt Gate #332](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38123426003).
- Scheduled Governance Health Check run #1 completed/success at [run #38095937202](https://github.com/m30morgh1991-prog/architecture-ai-agent/actions/runs/38095937202), running runtime smoke tests, the complete unittest suite, and Bug Hunt governance contract tests. It occurred before PR #115 merged (event SHA `caa8bdf5d74449ba70e52a699036bd5281a1967b`), so it confirms the scheduled workflow works but does not replace exact-SHA mainline gates.
- Ruleset `Min` (ID `24680937`) requires `runtime-tests`, `test`, and `Mandatory Bug Hunt`. Required approving reviews remain zero by the user's explicit decision; do not change this without explicit authorization.
- No secure AI execution provider has been configured or verified. The independent runner remains a deterministic policy contract, not a live AI execution service. No auto-merge or autonomous H-stage advancement is enabled.
- H100 remains active. H101 remains LOCKED until Golden Understanding acceptance evidence is genuinely green. Both Golden DWG files remain immutable.


## **H100 — Golden Understanding Gate — active on main**

**Current verified point:** PR #75 is merged to main at `c056c31ff97db532381c7466388200ff3cb62aeb`. Exact-head PR CI #219, Runtime #506, and Bug Hunt #176 were completed/success on PR #75. Mainline workflows for the merge commit are not exposed by the current PR-run query, so post-merge Green is not claimed.

### H100 historical input-source boundary verification
- PR: #66
- Branch: feat/h100-input-source-boundary
- PR head before merge: `2b0627c67e039db79749d67c000bc2bc2f84eeb4`
- Merge commit: `4f1363ead6c10378cbf807d29271ae315ae01c36`
- Exact PR-head Bug Hunt Gate #108: completed / success
- Exact PR-head PR CI Gate #151: completed / success
- Exact PR-head Runtime Tests #438: completed / success
- H100 PR Green Gate: satisfied for PR #66
- Post-merge main CI for merge commit `4f1363ead6c10378cbf807d29271ae315ae01c36`: not yet observed; therefore mainline Green Gate is NOT yet claimed.

### H100 implemented boundary
- Engineering Plan Input and Image Input are separate.
- Geometry evidence hierarchy: DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP.
- Unknown PDF representation remains UNKNOWN / SOURCE_REQUIRED until inspection evidence exists.
- Source classification/provenance is carried through execution metadata.
- PlanModel + ConstraintMap + ApprovedChangePlan remain the only Source of Truth.
- Raster/image evidence cannot silently become authoritative geometry.

### Current H100 continuation after PR #75

- PR #73 persisted the real Golden DWG SHA-256 evidence from CI-checked-out bytes.
- PR #74 established the provider-neutral AutoCAD-MCP adapter boundary.
- PR #75 merged the persisted SHA-256 values, byte-level mismatch regression, stronger Bug Hunt evidence contract, and a dependency-free read-only CAD inspection adapter.
- Golden SHA-256: `bagheri7.dwg = 865244d69e260d9ad23abed7b3ecaeb4df8b5f7da562c8d0284b466f3da13e6a`.
- Golden SHA-256: `afifiiiii.end.edit3.dwg = 508673cf44661b8b46fbb7f98992fffc99bd7d87531c1011fc5b8139d65a11a5`.
- Both preserved Golden DWGs remain fail-closed for uncertain structural semantics; hashes establish source identity, not semantic truth.
- AutoCAD-MCP remains read-only/adapter-only; no live AutoCAD write is enabled.
- Bug Hunt now requires affected contracts, risk classification, negative tests, and unresolved-findings evidence in addition to reproduction/root-cause/regression/fail-closed/exact-head evidence.

## H100 continuation
PR #66 established the source boundary; PR #68 established semantic/drawing evidence; PR #69 locked Golden Understanding research; PR #70 is the active Golden Understanding Regression implementation; PR #72 adds the standalone CLI E2E verification.
Do not start H101 until UG-01..UG-09 are Green and the verified state is persisted.

Current active sequence:
1. PR #71 standalone Golden Understanding runner is merged at `671133d4ab8941b2a38c79597769d8df2b18269e`; exact-head pre-merge gates were green.
2. PR #72 standalone Golden runner CLI E2E is merged at `b55242becb786fb4f932c671cf98e61c5aa3686d`; exact-head PR CI #204, Bug Hunt #161, and Runtime #491 were green.
3. PR #75 is merged at `c056c31ff97db532381c7466388200ff3cb62aeb`; exact-head gates were green.
4. Golden source SHA-256 values are now persisted and byte-verified by regression.
5. Read-only CAD inspection adapter is implemented behind the provider-neutral contract; live AutoCAD remains blocked.
6. UG-04/UG-06 and full Golden semantic ground truth remain pending; H101 stays locked.
3. Keep dimensions, levels, view markers and vertical circulation UNKNOWN unless source evidence supports them.
4. Apply reconciliation/provenance/fail-closed checks before authoritative PlanModel promotion.
5. Run exact-head REAL CI + Runtime + Bug Hunt + required regression.
6. Persist only verified state, then unlock H101.

## Integrated research checkpoint — 2026-10-08

### Newly consolidated decisions
- External architecture-agent research is part of the project knowledge layer; it does not create a second semantic graph.
- Useful patterns include scene graph/relations, raster-to-wall/opening reconstruction with uncertainty, semantic intent → deterministic geometry, knowledge/skills + feedback, and CV → CAD/BIM/IFC bridging.
- YQArch/AutoCAD is a future Execution Adapter capability, not the project brain.
- No arbitrary LISP path and no direct LLM → AutoCAD geometry authority.
- Iranian architectural drawing language is a first-class semantic evidence layer.
- Level/stair/section inferences remain fail-closed and require explicit consistent evidence.
- Standards and knowledge sources feed traceable Rule/Validation layers.
- Core invariant: **understand the plan before generating or editing the plan**.

### H100 continuation priorities
1. Bind evidence IDs/provenance to semantic facts.
2. Wire contradiction/missing-evidence handling and fail-closed propagation.
3. Complete drawing semantics/dimensions/annotations/markers/scale/unit coverage.
4. Integrate architectural relations into the canonical PlanModel/ConstraintMap.
5. Apply Golden DWG regression where applicable.
6. Run exact-head REAL CI + Bug Hunt + required regression; persist only verified state.
7. Continue to H101 only after Green Gate.

## Durable governance

- Required cycle: Implement → REAL CI → Verify → Regression → Persist State → Continue.
- Green Gate requires exact-head real CI completed/success plus required verification/regression evidence.
- queued/in_progress/cancelled/failure/missing/unobserved is never GREEN.
- Bug Hunting is mandatory after red tests.
- Notion is excluded from governance.
- Golden DWG assets remain preserved.
- “بکاپ بگیر” means additive checkpoint; never destructive reset.


### H100 mainline checkpoint — PR #76
- PR #76 merged at `8880b1890d5094771662464b48a294c9563a3059`.
- Exact-head PR #76: PR CI #225 SUCCESS, Runtime #512 SUCCESS, Bug Hunt #182 SUCCESS.
- Added executable mainline checkpoint coverage for Golden source binding, UNKNOWN status, fail-closed state documentation, and read-only CAD boundary.
- Mainline post-merge workflow Green is still not claimed because the current workflow-run query exposes PR-triggered runs only.


### H100 UG-04 checkpoint — PR #78
- PR #78 merged at `79790fce10ec89b64dfbe613e5dbb1b321eadb76`.
- Exact-head PR CI #229, Runtime #516, Bug Hunt #186 = SUCCESS.
- Every required Golden semantic domain now has explicit machine-readable `expected_domain_status`; current truth is explicitly UNKNOWN.
- UG-04 is implementation-complete; semantic truth remains unresolved and fail-closed.


### H100 UG-06 checkpoint — PR #80
- PR #80 merged at `d0f40f2fac5f1df20c3bbfbd96eaeab966002e03`.
- Exact-head PR CI #233, Runtime #520, Bug Hunt #190 = SUCCESS.
- A machine-checkable adversarial manifest now covers every current fail-closed category with explicit non-PASS expected decisions.
- These are contract-level adversarial fixtures; real-world image/DWG adversarial fixtures remain a follow-up and H101 remains locked.


## H100 mainline checkpoint — PR #82

PR #82 merged at `a08750765c19aadce02003e6fa221532d073992f`. Exact-head `3ea24d659490c7f809bb8579b3ea1e3efbe627fb` had PR CI #244 SUCCESS, Runtime #531 SUCCESS, Bug Hunt #201 SUCCESS. The PR closed the evaluator gap so `expected_domain_status` is actually consumed; current Golden semantic truth remains explicitly UNKNOWN, so this does not claim semantic understanding. Post-merge workflow runs for the merge commit are not exposed by the current workflow-run query; therefore mainline post-merge Green is not claimed.

### Next H100 priority
- Build actual semantic Golden truth from read-only DWG/CAD evidence, not guessed labels or VLM-only interpretation.
- Expand contract-level adversarial fixtures into real-world transformed/defective drawing fixtures.
- Keep H101 locked until the remaining Golden Understanding gates have real evidence.

### H100 PR #83 checkpoint — read-only DWG semantic evidence
- PR #83 merged to main at `d92eb9d3f63819e744b1c901504d447508cd9cab`.
- Exact PR head `ce3a2298495f579f37b51c17961d03dbd467f4d8`: PR CI #252 SUCCESS, Runtime #539 SUCCESS, Bug Hunt #209 SUCCESS.
- Added conservative `ezdwg` read-only semantic evidence extraction for the preserved Golden DWGs.
- Evidence includes source identity, entity/layer/block evidence, text, dimensions, and only explicit direct semantic candidates. Generic geometry is not promoted to architectural truth.
- Semantic authority remains false; unsupported semantic domains remain UNKNOWN/fail-closed.
- Post-merge workflow query for merge commit returned no exposed runs, so post-merge Green is NOT claimed.
- Next priority: reconcile extracted CAD evidence into provenance-bound semantic facts and build real-world adversarial Golden fixtures before unlocking H101.


### H100 PR #84 checkpoint — DWG evidence reconciliation bridge
- PR #84 merged to main at `2038ea392fcaeccafc67f8d5ea695a16ff34a918` after repaired exact head `bd86bb20141fba44cc25c1c93aee44b00645125d` passed PR CI #258, Runtime #545, and Bug Hunt #215.
- The bridge normalizes source-bound read-only DWG candidates, text, and dimensions into the existing `DrawingEvidence` contract; it does not create a second PlanModel and ignores generic geometry as architectural truth.
- The first Bug Hunt failure was a governance-format defect in `PR-84.md`; the exact required headings were restored and all three REAL CI gates then passed at the repaired exact head.
- Semantic Golden truth remains unresolved. Real-world adversarial DWG/image fixtures remain pending. H101 remains locked.
- Post-merge workflow query for merge commit `2038ea392fcaeccafc67f8d5ea695a16ff34a918` returned no exposed runs; therefore post-merge Green is NOT claimed.
- Next priority: bind reconciled evidence to CandidateFacts/provenance, add contradiction/negative-evidence checks, then build real-world adversarial Golden fixtures before any H101 unlock.


### H100 PR #86 checkpoint — CandidateFact provenance

- PR #86 merged to `main` at `117e6f52cbe02bedc59dfbf73810a821d7a70765`.
- Exact fixed PR head `e9804928523e0f3ed3b6c8a9847fbc400247ab32` passed PR CI #264, Runtime #551, and Bug Hunt #221.
- PR #86 binds source-bound DWG evidence to deterministic CandidateFacts and validates evidence-reference/source-SHA continuity; contradiction handling is preserved rather than silently discarded.
- The first Bug Hunt failure was governance-only (`## Bug Hunt` heading missing); it was fixed and re-run successfully at the exact fixed head.
- Current main post-merge workflow query returns no runs for the merge SHA, so post-merge Green is NOT claimed.
- Open PRs: none at checkpoint time.
- H100 remains active; H101 remains locked.

### Immediate next H100 execution
1. Strengthen contradiction and negative-evidence handling at the DWG evidence boundary.
2. Add conservative level/elevation, section marker/cut-plane/direction, scale/unit, and Iranian drawing-language semantics.
3. Expand contract-level adversarial coverage into real-world transformed/defective Golden fixtures.
4. Run exact-head PR CI + Runtime + Bug Hunt + required Golden regression.
5. Persist only verified state; do not unlock H101 without Green Gate evidence.



### H100 PR #88 checkpoint — negative evidence hardening

- PR #88 merged at `a6ae2d3273dc97face2fbb3e3190dd7a333f7bdb`.
- Exact verified PR head `b465b5951c27f1df4164ef02adf854d14f4dd15a`: PR CI #269 SUCCESS, Runtime #556 SUCCESS, Bug Hunt #226 SUCCESS.
- PR #88 hardens contradiction/required-evidence references to the same source-bound DrawingEvidenceSet and rejects missing/cross-source references plus support/contradiction overlap.
- PR #88 first exact-head attempt failed because an existing contradiction test used an unbound fixture; the fixture was repaired with independent source-bound evidence and all gates passed.
- PR #87 checkpoint merged at `e520aaf91063cb45a424b76a1960b804b9b56852`; its final exact head `719ae231390e3cdbbe66de0230cdceb1d058b547` passed PR CI #270, Runtime #557, Bug Hunt #227.
- Post-merge workflow query for PR #88 merge SHA currently exposes no runs; post-merge Green is NOT claimed.
- H101 remains locked.

### Next H100 execution
1. Add conservative level/elevation semantics.
2. Add section-marker/cut-plane/direction semantics.
3. Add scale/unit semantics.
4. Integrate Iranian drawing-language conventions without promoting unsupported raster/vector inference.
5. Build real-world transformed/defective Golden fixtures and evaluate fail-closed decisions.


### H100 PR #90 checkpoint — level/elevation evidence

- PR #90 merged at `c4011e0a8b67b3da41b755dfb485c1f2b60a71a0`.
- Exact head `5ab500c72151e64f8a63c80c211c3d5522ed7cb3`: PR CI #276, Runtime #563, Bug Hunt #233 all SUCCESS.
- Added conservative direct DWG level/elevation evidence extraction. Explicit level context/unit is supported; arbitrary numeric text remains UNKNOWN.
- No floor relation or stair-count inference is promoted yet.
- H101 remains locked.
- Post-merge workflow runs for `c4011e0...` are not claimed until exposed.

Next: section marker/cut-plane/direction semantics, then scale/unit semantics.


## H100 PR #91 checkpoint — persisted after PR #90

- PR #91 merged to main at \`2dfcd893ed97028f69982477dc7d9d6741eff9ca\`.
- Exact PR #91 head \`1d6eb08b16abaf60b2c2bd5ed390db962c38b864\`: PR CI #287, Runtime #574, Bug Hunt #244 = SUCCESS.
- This is a documentation/state checkpoint only; it does not claim new runtime semantics or post-merge mainline Green.
- H100 remains active and H101 remains locked.

## H100 PR #93 — section-marker evidence implementation in progress

- Branch: \`feature/h100-section-marker-semantics\`.
- Adds conservative read-only DWG evidence for explicitly contextualized section/cut-plane/elevation/detail markers and explicitly named marker blocks.
- Marker evidence is bound to source SHA-256 and DIRECT provenance.
- Bare labels such as \`A-A\` remain unpromoted without context.
- Direction and cut-plane geometry remain UNKNOWN even when marker presence is supported; arrow glyphs do not establish direction.
- Exact-head PR CI, Runtime Tests, Bug Hunt, and required Golden regression are pending verification. This branch is NOT Green until all required gates are completed/success.


## Research checkpoint — architectural books evidence map (clean branch, 2026-10-09)

- Added `docs/research/architectural-books-evidence-map.md` from the cleaned research content on an isolated branch created directly from `main`.
- This checkpoint contains architecture-only source mapping: Iranian drawing vocabulary; dimension/scale evidence; plan-section-elevation-roof-detail relations; phase-2 completeness; stair/level evidence; cross-view coordination; traceability; ambiguity and missing-evidence tests.
- The two 31-page phase-2 references are retained separately until page-image/content comparison proves duplication.
- This is initial text/index research, not a full visual audit or implementation claim. No runtime code or acceptance criteria changed.
- H100 remains active; H101 remains locked. Exact-head PR CI, Runtime Tests, and Bug Hunt must all pass before merge.


## H100 research checkpoint — educational drawing references (mainline refresh, 2026-10-09)

- Prepared from current main commit `5aa7b31c446a0aacbbc49fdc0b40e08390768f97`, preserving the merged PR #96 architectural-books evidence map.
- Carries forward the educational drawing-reading reference summary, candidate comparison, Jorjani candidate record, and Architecture Understanding Core documentation integration.
- Candidate catalog entries remain `CATALOG-VERIFIED / NOT YET STUDIED` until the actual legal edition is inspected. Educational references do not override current official regulations; uncertain claims remain source-required/review-only.
- Documentation-only scope: no runtime code, PlanModel, ConstraintMap, ApprovedChangePlan, or Golden DWG assets are modified by this checkpoint.
- Exact-head PR CI, Runtime Tests, Mandatory Bug Hunt, and any applicable regression gates are required before merge. No Green claim is made until those checks complete successfully.
- H100 remains active; H101 remains locked.


## H100 integration checkpoint — scale/unit fail-closed contract queued after PR #101 (2026-10-09)

- PR #101 merged into main at `e6b0283551b75862787376f9a5d8a54d17f80c87`; educational drawing-reference documentation and the PR-specific Bug Hunt record are now on main.
- PR #98 scale/unit fail-closed changes are being refreshed onto this exact mainline in a clean integration branch. This contract is a prerequisite for PR #99's DWG metadata bridge.
- Intended safety invariant: unknown, unsupported, malformed, or conflicting unit evidence cannot become PASS. Native unit declaration alone does not prove scale or dimension-to-geometry correspondence.
- This integration changes runtime code and tests; it is not documentation-only. Exact-head PR CI, Runtime Tests, Mandatory Bug Hunt, and applicable Golden regression must complete successfully before merge.
- Golden DWG inputs remain immutable. H100 active; H101 locked.


## Plan-understanding research checkpoint — 2026-10-10

- Research record: `docs/research/plan-understanding-research-and-revit-ai-review-2026-10-10.md`; capability mapping: `docs/research/ARCHITECTURE_AGENT_FEATURE_FILE_MATRIX.md`.
- Highest-value additions are evaluation patterns from fpvec-lab/ResPlan-FP (separate wall/room/opening metrics, topology, correction cost), AEC-Geometric-Bench (external geometric validation subject to non-commercial data terms), and ConstructDrawingAI CIR (vector-first ingestion, explicit connectivity, provenance/confidence, perception/reasoning separation).
- Raster-to-Graph, FloorPlan2IFC, FloorPlanCAD, and PerDAW are recorded as follow-up research candidates; their dependencies, dataset access, and artifact-specific licenses must be reviewed before use.
- Revit product review distinguishes Drafted in Revit (new schematic single-storey house-plan generator) from WiseBIM AI (existing 2D plan-to-Revit reconstruction) and Autodesk Assistant/Generative Design (model/documentation actions and constrained alternatives). None proves Iranian code compliance or the project's required understanding of levels, stairs, section direction, and local drafting language.
- No external code or dataset was imported. No new runtime provider/dependency was added. The research record does not change the Source of Truth or authorize a parallel semantic model.
- Licensing guardrail: AEC-Geometric-Bench data and FloorPlanCAD material have non-commercial restrictions described by their maintainers; ConstructDrawingAI code is PolyForm Noncommercial. Verify each artifact's terms before reuse.
- Acceptance remains fail-closed: external scores do not replace source-bound Golden semantic ground truth. Golden DWGs are immutable. H100 remains active and H101 remains locked until actual semantic acceptance evidence and all exact-head gates are green.


## Post-merge checkpoint — PR #113 and independent runner (2026-10-10)

- PR #113 (plan-understanding research and Revit AI review) was merged using squash at `caa8bdf5d74449ba70e52a699036bd5281a1967b`. Research findings and file mappings are now on main; no external code, packages, or datasets were imported.
- Exact PR-head `36e73894c43b96ff4454b8367e7c182dd4c40307`: PR CI Gate run #363, Runtime Tests run #650, and Mandatory Bug Hunt run #322 all completed/success. These are PR-head results, not post-merge mainline verification.
- Post-merge mainline workflow evidence for `caa8bdf5d74449ba70e52a699036bd5281a1967b` has not been observed through the available workflow query. Mainline Green is therefore NOT claimed.
- Independent runner remains design + deterministic fail-closed policy only. The scheduled read-only health-check workflow exists, but its first successful post-merge manual/scheduled run is not yet verified. No AI execution provider or credentials are configured/verified; autonomous editing remains disabled.
- Next non-conflicting steps: verify a health-check run from GitHub Actions; research/select an allowed provider/execution backend without committing secrets; then implement a bounded, event-driven canary in an isolated branch with strict concurrency, budgets, exact-SHA checks, and failure recovery.
- H100 remains active and H101 locked. Golden DWGs remain immutable. Human-controlled merge and stage advancement remain mandatory.
