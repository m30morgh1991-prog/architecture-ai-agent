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
