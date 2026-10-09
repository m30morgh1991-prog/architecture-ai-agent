# Project State

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
