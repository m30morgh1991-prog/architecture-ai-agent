# Architecture AI Agent — Master Progress Checklist

## Live repository checkpoint — 2026-10-10

- Verified `main`: `ccd8c2d8762597bf06b4873c623eb35271994a6a` (PR #103 merged).
- PR #101 and #102 are merged; PR #103 is merged. PR #99 is closed as superseded. PR #100 remains open but is stale and must not merge without being rebuilt/reconciled against current `main`.
- Post-merge `Mandatory Bug Hunt` is SUCCESS. Post-merge `test` and `runtime-tests` are still running at last observation; post-merge Green is NOT yet established.
- Ruleset `Min` (ID `24680937`) is active on the default branch and requires `runtime-tests`, `test`, and `Mandatory Bug Hunt`. It currently requires zero approving reviews; do not describe it as requiring one approval.
- H100 remains active. H101 remains locked until final H100 acceptance gates and evidence are green. Golden DWGs remain immutable.


> This file is the persistent cross-chat project checklist. When asked "کجای پروژه هستیم؟" or "مرحله بعد چیست؟", use this file together with GitHub PR/CI status and `PROJECT_STATE.md` as the source of truth.

## Governance Gate — ALWAYS ACTIVE

- [ ] Implement
- [ ] REAL CI run/status
- [ ] Verify exact HEAD
- [ ] Regression when applicable
- [ ] Persist State
- [ ] Continue immediately when Green
- [ ] If Red: Bug Hunt → root cause → fix → REAL CI again
- [ ] Never treat queued/in_progress/no-CI as Green
- [ ] Never bypass Fail-Closed
- [ ] No-Wait Rule: prepare/debug in parallel while CI runs, without bypassing the gate

## Current master sequence

- [x] Architecture Agent feature-to-file matrix defined (PR #65)
- [x] Plan Understanding Semantic Chain defined
- [x] PR #65 — CI + Bug Hunt Green
- [x] PR #65 — Merge (`176bc2ceb330e2987891ef6edbbaf33b73dc77d3`)
- [x] Post-merge main REAL CI Green — Runtime #427, PR CI #140, Bug Hunt #97
- [x] H100 — Input source boundary: engineering-plan vs image input
- [x] H100 — Geometry evidence hierarchy: DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP
- [x] H100 — PDF representation must be evidence-classified; unknown PDF is fail-closed
- [x] H100 — Source profile carried through ExecutionRequest metadata
- [x] 2026-10-08 — GitHub architecture-agent research consolidated
- [x] 2026-10-08 — YQArch/AutoCAD execution adapter direction recorded
- [x] 2026-10-08 — Iranian architectural drawing-language requirements consolidated
- [x] H100 Golden Understanding research lock merged (PR #69, merge `b27ea1f09b6e20c2ed13931177f740e6db93c6d0`)
- [x] H100 Golden Understanding Regression contract foundation implemented (PR #70 branch; not Green)
- [x] H100 — Drawing Semantics + Dimension/Annotation Evidence foundation (PR #68)
- [x] H100 — Semantic Chain foundation wired to canonical PlanModel (PR #68)
- [x] H100 — Evidence IDs/provenance bound to semantic facts (PR #68)
- [x] H100 — UNKNOWN / NEEDS_REVIEW / BLOCKED propagation foundation (PR #68)
- [x] H100 — Contradiction detection foundation (PR #68)
- [x] H100 — Missing-evidence detection foundation (PR #68)
- [x] H100 — Golden Understanding Regression: contract + manifest + fail-closed evaluator implemented; exact-head Green still required
- [x] H100 — Golden DWG source execution/identity + real SHA-256 persistence
- [ ] H100 — Golden semantic ground truth and authoritative understanding
- [ ] H100 — UG-01..UG-08 Golden Understanding Gate checks Green
- [x] H100 — PR #70 exact-head PR CI + Runtime + Bug Hunt Green (pre-merge); post-merge mainline verification remains pending
- [ ] H100 — UG-10 Green → persist verified state and unlock H101
- [ ] H101 — Architectural Intent + Program + Plan Generation + deterministic geometry/layout
- [ ] H101 — REAL CI + Bug Hunt Green
- [ ] H102 — Architecture IR + lint/diagnostics
- [ ] H103 — Deterministic Drawing Compiler + SVG/DXF
- [ ] H104 — Dimensions/annotations/views + drawing standards
- [ ] H105 — Sections + elevations
- [ ] H106 — Details + schedules + sheets
- [ ] H107 — Multi-output sync + BIM export boundary
- [ ] H108 — Multi-agent roles/orchestration
- [ ] H109 — Iterative propose → inspect → revise
- [ ] H110 — Cross-format round-trip validation
- [ ] H111 — Production documentation/release gate

## H100 — Semantic/Drawing Evidence checklist

### Golden Understanding Gate (UG-01..UG-10)

- [x] UG-01 Golden case manifest exists
- [x] UG-02 Ground-truth schema is source-bound and versioned
- [x] UG-03 End-to-end Understanding Runner emits a machine-checkable report
- [x] UG-04 All required semantic domains have expected truth or explicit UNKNOWN (machine-checked; current truth explicitly UNKNOWN)
- [x] UG-05 Public benchmark calibration is separated from project acceptance
- [x] UG-06 Contract-level adversarial cases exist for every current fail-closed category (real-world DWG/image expansion pending)
- [x] UG-07 Metrics are computed per domain (implementation); Green evidence still required
- [x] UG-08 False-PASS / unsafe-acceptance checks are hard blockers
- [x] UG-09 PR #75 exact-head REAL CI #219 + Runtime #506 + Bug Hunt #176 Green
- [ ] UG-10 Only after UG-01..UG-09 pass may H101 begin

- [ ] Door/window symbols + opening direction
- [ ] Line type/thickness/weight
- [ ] Layer semantics
- [ ] Dimensions + extension lines
- [ ] Elevation/level codes
- [ ] Room/space labels
- [ ] Section markers + direction lines + cut-plane semantics
- [ ] Elevation markers + direction
- [ ] Hatch semantics
- [ ] Column/structural symbols
- [ ] Element ↔ wall/space relations
- [ ] Floor/level semantics
- [ ] Floor-to-floor relationships
- [ ] Stairs/landings and stair-count inference only with explicit consistent evidence
- [ ] Scale/unit evidence
- [ ] Title-block/drawing metadata evidence
- [x] Input source classification/provenance boundary
- [x] Evidence IDs/provenance bound to semantic facts (foundation; authoritative promotion remains fail-closed)
- [x] UNKNOWN / NEEDS_REVIEW / BLOCKED propagation (foundation; end-to-end Golden Gate still pending)
- [x] Contradiction detection (foundation; adversarial coverage pending)
- [x] Missing-evidence detection (foundation; adversarial coverage pending)
- [x] Golden DWG regression — real source hashes persisted and byte-verified
- [ ] Golden DWG regression — semantic ground truth / adversarial acceptance pending

## Integrated research findings

### External architecture-agent patterns

- JMU → scene graph / relations
- RedrawAI → raster → wall graph → openings → validation + uncertainty
- Draftly → semantic intent → deterministic geometry + incremental editing
- CraftBot → knowledge/skills + feedback loop
- dwg-bim_AI → CV segmentation → CAD/BIM/IFC

Transfer rule: use these as patterns only; keep one canonical PlanModel/evidence graph.

### YQArch / AutoCAD

- YQArch is an Execution Adapter candidate, not the project brain.
- Use Capability Registry + controlled adapter boundary.
- No arbitrary LISP execution path.
- No direct LLM → AutoCAD geometry authority.
- PlanModel + ApprovedChangePlan remain authoritative.

### Input-source boundary

**DWG/DXF → Vector PDF → Raster PDF → JPG/PNG/WEBP**

Engineering-plan and image inputs remain distinct. Raster evidence may inform candidates but cannot silently become authoritative geometry.

### Iranian drawing-language additions

Treat the following as semantic evidence, not decoration:

- conventional symbols and orientation;
- line types/weights/layers;
- dimensions and extension lines;
- level/elevation codes;
- floor relationships and vertical circulation;
- stairs/landings/riser evidence;
- section markers, direction lines and cut planes;
- elevation markers/direction;
- hatch;
- title block;
- scale/unit;
- space labels and element relations.

## Plan Understanding — target semantic chain

Source Evidence
→ Element Identity
→ Geometry
→ Topology
→ Spatial Relation
→ Architectural Semantics
→ BIM Semantics
→ Rule Context

Rule: Detection is not Understanding. Do not create a second PlanModel or second BIM evidence graph. Preserve provenance continuity into the existing canonical model.

## H100 architectural decisions carried forward

- SourceProfile must remain traceable through evidence into the canonical PlanModel; no duplicate UnderstandingModel is introduced.
- Dimensions, levels, section/elevation markers and vertical circulation are semantic evidence domains, not mere OCR/annotation text.
- Stair/floor/section facts may be DIRECT or validated DERIVED only; incomplete or conflicting evidence remains UNKNOWN/NEEDS_REVIEW/BLOCKED.
- BIM mapping remains a semantic mapping layer and must remain evidence-backed; IFC does not replace PlanModel.
- H101 generation is locked behind the Golden Understanding Gate; unresolved understanding cannot become authoritative generation input.

## H101 — Plan Generation checklist

- [ ] Architectural Intent contract
- [ ] Program/room requirements
- [ ] Prompt → plan proposal
- [ ] Deterministic layout/geometry
- [ ] Adjacency + circulation
- [ ] Opening connectivity
- [ ] Structural/regulatory constraints
- [ ] ConstraintMap integration
- [ ] Generated PlanModel
- [ ] Validation + conflict handling
- [ ] Fail-closed behavior
- [ ] Normal + ambiguous/failure tests
- [ ] Golden/regression coverage
- [ ] Exact-head REAL CI Green

## Feature-to-file matrix milestones

- F01–F02 → Intent + Program (H101)
- F03–F04 → Plan Generation + deterministic geometry (H101)
- F05–F06 → Architecture IR + validation (H102)
- F07–F10 → Drawing compiler/backends (H103–H104)
- F11–F18 → Phase-2 documentation (H104–H106)
- F19–F20 → Output sync + BIM export (H107)
- F21–F23 → Multi-agent + iterative design (H108–H109)
- F24–F26 → Semantic/BIM/evidence continuity (H100+ continuous)
- F27–F28 → Iran/architectural drawing standards + symbols/layers (H100/H104+)
- F29 → Round-trip (H110)
- F30 → Production readiness (H111)

## Status rules

- **PLANNED** = listed in matrix, not implemented.
- **IMPLEMENTED** = code exists, but exact-head REAL CI is not Green.
- **IMPLEMENTED + GREEN** = code + exact-head REAL CI success.
- **MERGED + VERIFIED** = merged to main + required post-merge verification Green.

## Source of truth

1. GitHub main/PR state and exact-head REAL CI
2. `PROJECT_STATE.md`
3. `MASTER_HANDOFF.md`
4. This checklist
5. Feature-to-file matrix / research docs as supporting planning documents

Notion is not a governance or Green-Gate source of truth.

## 2026-10-08 verified checkpoint — PR #75

- Merge: `c056c31ff97db532381c7466388200ff3cb62aeb`
- Exact-head PR CI #219: success
- Exact-head Runtime #506: success
- Exact-head Bug Hunt #176: success
- Golden SHA-256: `bagheri7.dwg = 865244d69e260d9ad23abed7b3ecaeb4df8b5f7da562c8d0284b466f3da13e6a`
- Golden SHA-256: `afifiiiii.end.edit3.dwg = 508673cf44661b8b46fbb7f98992fffc99bd7d87531c1011fc5b8139d65a11a5`
- AutoCAD-MCP: provider-neutral boundary + read-only source-identity adapter merged; live write remains blocked.
- Bug Hunt evidence contract now requires affected contracts, risk classification, negative tests, unresolved findings, plus existing fail-closed/exact-head evidence.
- H101 remains locked until remaining Golden semantic/adversarial gates are Green.


## 2026-10-08 — H100 PR #76 checkpoint
- PR #76 merged: `8880b1890d5094771662464b48a294c9563a3059`
- Exact-head gates: PR CI #225 / Runtime #512 / Bug Hunt #182 = SUCCESS
- Mainline checkpoint regression coverage is merged.
- Semantic Golden ground truth and remaining adversarial gates remain pending.


## 2026-10-08 — H100 UG-04 checkpoint
- PR #78 merged: `79790fce10ec89b64dfbe613e5dbb1b321eadb76`
- Exact-head gates: PR CI #229 / Runtime #516 / Bug Hunt #186 = SUCCESS
- UG-04 per-domain explicit status contract implemented; all current statuses are UNKNOWN.
- UG-06 adversarial coverage and semantic ground truth remain pending.


## 2026-10-08 — H100 UG-06 checkpoint
- PR #80 merged: `d0f40f2fac5f1df20c3bbfbd96eaeab966002e03`
- Exact-head gates: PR CI #233 / Runtime #520 / Bug Hunt #190 = SUCCESS
- Contract-level adversarial coverage exists for every current fail-closed category.
- Real-world DWG/image adversarial fixtures and semantic ground truth remain pending.


## 2026-10-08 — H100 PR #82 checkpoint

- PR #82 merged: `a08750765c19aadce02003e6fa221532d073992f`
- Exact-head `3ea24d659490c7f809bb8579b3ea1e3efbe627fb`: PR CI #244 / Runtime #531 / Bug Hunt #201 = SUCCESS
- Evaluator now enforces `expected_domain_status`; explicit UNKNOWN truth no longer incorrectly demands element inventory.
- Current semantic Golden truth remains UNKNOWN; this is contract correctness, not semantic PASS.
- Post-merge workflow runs for `a08750765c19aadce02003e6fa221532d073992f` are not exposed by the current query; post-merge Green is therefore not claimed.
- Next: authoritative DWG evidence → reconciliation/provenance → real-world adversarial fixtures → remaining H100 gates.


## 2026-10-08 — H100 PR #83 checkpoint

- PR #83 merged: `d92eb9d3f63819e744b1c901504d447508cd9cab`
- Exact-head `ce3a2298495f579f37b51c17961d03dbd467f4d8`: PR CI #252 / Runtime #539 / Bug Hunt #209 = SUCCESS
- Read-only `ezdwg` DWG semantic evidence extraction is merged; source identity, entity/layer/block evidence, text and dimensions are captured conservatively.
- Generic geometry is explicitly prevented from becoming architectural truth; semantic authority remains false.
- Post-merge workflow runs are not exposed for the merge commit, so post-merge Green is not claimed.
- Next: evidence reconciliation/provenance → real-world adversarial Golden fixtures → remaining H100 gates.


## 2026-10-08 — H100 PR #84 checkpoint

- [x] PR #84 merged: `2038ea392fcaeccafc67f8d5ea695a16ff34a918`
- [x] Repaired exact head `bd86bb20141fba44cc25c1c93aee44b00645125d` — PR CI #258 / Runtime #545 / Bug Hunt #215 = SUCCESS
- [x] DWG evidence normalization bridge is source-bound and read-only; generic geometry does not become architectural truth
- [x] Bug Hunt governance-format defect fixed and re-verified at exact head
- [ ] H100 semantic Golden ground truth / authoritative understanding
- [ ] H100 real-world adversarial DWG/image fixtures
- [ ] H100 UG-10 Green and H101 unlock
- Post-merge workflows for merge commit `2038ea392fcaeccafc67f8d5ea695a16ff34a918` are not exposed by the current workflow-run query, so post-merge Green is NOT claimed.
- Next: CandidateFacts/provenance binding → contradiction/negative evidence → drawing-language/level/section semantics → real-world adversarial Golden fixtures → exact-head gates.


## 2026-10-08 — H100 PR #86 checkpoint

- [x] PR #86 merged: `117e6f52cbe02bedc59dfbf73810a821d7a70765`
- [x] Fixed exact head `e9804928523e0f3ed3b6c8a9847fbc400247ab32` — PR CI #264 / Runtime #551 / Bug Hunt #221 = SUCCESS
- [x] DWG evidence → CandidateFact provenance binding and source-SHA continuity validation merged
- [x] Contradictions are preserved through reconciliation; they are not silently discarded
- [x] Bug Hunt governance-only failure fixed and re-verified
- [ ] H100 contradiction/negative-evidence hardening
- [ ] H100 level/elevation + section/cut-plane/direction + scale/unit semantics
- [ ] H100 Iranian drawing-language semantic coverage
- [ ] H100 real-world transformed/defective Golden fixtures
- [ ] H100 semantic Golden ground truth / authoritative understanding
- [ ] H100 UG-10 Green and H101 unlock
- Post-merge workflows for `117e6f52cbe02bedc59dfbf73810a821d7a70765` are not exposed by the current commit workflow-run query, so post-merge Green is NOT claimed.



## 2026-10-09 — H100 PR #88 checkpoint

- [x] PR #87 merged: `e520aaf91063cb45a424b76a1960b804b9b56852`
- [x] PR #88 merged: `a6ae2d3273dc97face2fbb3e3190dd7a333f7bdb`
- [x] PR #88 exact head `b465b5951c27f1df4164ef02adf854d14f4dd15a` — PR CI #269 / Runtime #556 / Bug Hunt #226 = SUCCESS
- [x] Contradiction and negative-evidence source fencing
- [x] Missing/cross-source/overlap negative evidence tests
- [ ] H100 level/elevation semantics
- [ ] H100 section marker/cut-plane/direction semantics
- [ ] H100 scale/unit semantics
- [ ] H100 Iranian drawing-language semantic coverage
- [ ] H100 real-world transformed/defective Golden fixtures
- [ ] H100 semantic Golden ground truth / authoritative understanding
- [ ] H100 UG-10 Green and H101 unlock
- Post-merge workflows for `a6ae2d3273dc97face2fbb3e3190dd7a333f7bdb` are not exposed; post-merge Green is not claimed.


## 2026-10-09 — H100 PR #90 checkpoint

- [x] PR #90 merged: `c4011e0a8b67b3da41b755dfb485c1f2b60a71a0`
- [x] Exact head `5ab500c72151e64f8a63c80c211c3d5522ed7cb3` — PR CI #276 / Runtime #563 / Bug Hunt #233 = SUCCESS
- [x] Conservative level/elevation evidence extraction
- [x] Uncontextualized numeric annotations remain UNKNOWN
- [ ] Section marker/cut-plane/direction semantics
- [ ] Scale/unit semantics
- [ ] Iranian drawing-language semantic coverage
- [ ] Real-world transformed/defective Golden fixtures
- [ ] H100 semantic Golden ground truth / authoritative understanding
- [ ] H100 UG-10 Green and H101 unlock
- Post-merge workflow evidence for PR #90 is not currently exposed.


## 2026-10-09 — H100 section-marker evidence continuation

- [x] PR #91 merged at \`2dfcd893ed97028f69982477dc7d9d6741eff9ca\`; exact-head PR CI #287 / Runtime #574 / Bug Hunt #244 = SUCCESS.
- [ ] PR #93 — explicit section/cut-plane/elevation/detail marker evidence implementation (branch in progress; gates not yet verified)
- [ ] Reject bare section-like labels without contextual evidence
- [ ] Keep marker direction and cut-plane geometry UNKNOWN until geometric/source evidence supports them
- [ ] Scale/unit evidence
- [ ] Iranian drawing-language semantic coverage
- [ ] Real-world transformed/defective Golden fixtures
- [ ] H100 semantic Golden ground truth / authoritative understanding
- [ ] H100 UG-10 Green and H101 unlock
