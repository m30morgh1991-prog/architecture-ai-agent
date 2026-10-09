# Project State

## **H100 — Golden Understanding Gate — active on main**

**Current verified point (2026-10-09):** `main` is `2842cf2523fb9140b72f03a2311addf06c468af2` (PR #93 merged). PR #93 exact head `26f1a0c9c0f47b3d8fa5f419f4a659c57b6e9d5e` passed PR CI #289, Runtime #576, and Bug Hunt #246. The merge commit has no exposed post-merge workflow runs/statuses through the available read path, so mainline post-merge Green is NOT claimed.

**Open H100 PRs (all still require review; no submitted reviews are recorded):**
- PR #96 book evidence map — head `1df773883036525e20c972815ac3a3410c00d7da`; PR CI #300, Runtime #587, Bug Hunt #257 = SUCCESS.
- PR #97 educational drawing references — head `25d57ef7e6b18f49228f9194b3991a92387cd04b`; PR CI #305, Runtime #592, Bug Hunt #262 = SUCCESS.
- PR #98 scale/unit fail-closed contract — head `7092f3cba6fc5b3f8747bbe78ff2e2976111ae1b`; PR CI #303, Runtime #590, Bug Hunt #260 = SUCCESS. Required prerequisite for #99.
- PR #99 scale/unit Golden bridge — head `c472396d5a3a984c8c134bb7f55d068326c4fc14`; PR CI #313, Runtime #600, Bug Hunt #272 = SUCCESS. Do not merge before #98; after #98 merges, rebase/retarget to updated main and rerun every gate on the final exact head.

**Governance blockers:** H100 remains active and H101 remains LOCKED. Golden semantic ground truth and real-world transformed/defective fixtures are incomplete. Repository ruleset `Min` (ID `24680937`) is `disabled`, targets no branches, and has no required status checks configured; the intended protections therefore do not currently enforce review or CI. Enable/configure it for `refs/heads/main` before treating branch protections as active.

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

## H100 foundation established through PR #75 (historical checkpoint)

- PR #66 established the input-source boundary; PR #68 added the semantic/drawing evidence foundation; PR #69 locked the Golden Understanding research direction.
- PRs #71 and #72 introduced the standalone Golden Understanding runner and CLI E2E; PR #75 persisted Golden source hashes, byte-level mismatch regression, and the read-only CAD inspection adapter.
- These are historical implementation milestones, not the current acceptance head. Current status, open PRs, and latest exact-head gates are recorded at the top of this file and in the pre-phase audit.
- H100 remains incomplete: authoritative Golden semantic ground truth, real-world transformed/defective fixtures, remaining drawing-language semantics, and UG-10 are pending. H101 remains locked.
- Preserve dimensions, levels, view markers, scale, and vertical-circulation claims as UNKNOWN/NEEDS_REVIEW unless independent source evidence supports them.
- Required cycle remains: implement → exact-head REAL CI → verify → regression → persist state → continue. Persist only verified state.

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

## H100 PR #93 checkpoint — merged

- PR #93 merged into main at `2842cf2523fb9140b72f03a2311addf06c468af2`.
- Exact PR head `26f1a0c9c0f47b3d8fa5f419f4a659c57b6e9d5e`: PR CI #289, Runtime #576, Bug Hunt #246 = SUCCESS.
- Contextual section/cut-plane/elevation/detail marker candidates are source-bound and read-only; bare labels such as `A-A` are rejected without context.
- Marker presence does NOT establish direction, cut-plane endpoints, or view geometry; these remain UNKNOWN without independent evidence.
- No post-merge mainline Green is claimed because no mainline workflow runs/statuses were exposed for the merge commit.

**Current verified point (2026-10-09):** `main` is `2842cf2523fb9140b72f03a2311addf06c468af2` (PR #93 merged). PR #93 exact head `26f1a0c9c0f47b3d8fa5f419f4a659c57b6e9d5e` passed PR CI #289, Runtime #576, and Bug Hunt #246. The merge commit has no exposed post-merge workflow runs/statuses through the available read path, so mainline post-merge Green is NOT claimed.

**Open H100 PRs (all still require review; no submitted reviews are recorded):**
- PR #96 book evidence map — head `1df773883036525e20c972815ac3a3410c00d7da`; PR CI #300, Runtime #587, Bug Hunt #257 = SUCCESS.
- PR #97 educational drawing references — head `25d57ef7e6b18f49228f9194b3991a92387cd04b`; PR CI #305, Runtime #592, Bug Hunt #262 = SUCCESS.
- PR #98 scale/unit fail-closed contract — head `7092f3cba6fc5b3f8747bbe78ff2e2976111ae1b`; PR CI #303, Runtime #590, Bug Hunt #260 = SUCCESS. Required prerequisite for #99.
- PR #99 scale/unit Golden bridge — head `c472396d5a3a984c8c134bb7f55d068326c4fc14`; PR CI #313, Runtime #600, Bug Hunt #272 = SUCCESS. Do not merge before #98; after #98 merges, rebase/retarget to updated main and rerun every gate on the final exact head.

**Governance blockers:** H100 remains active and H101 remains LOCKED. Golden semantic ground truth and real-world transformed/defective fixtures are incomplete. Repository ruleset `Min` (ID `24680937`) is `disabled`, targets no branches, and has no required status checks configured; the intended protections therefore do not currently enforce review or CI. Enable/configure it for `refs/heads/main` before treating branch protections as active.
