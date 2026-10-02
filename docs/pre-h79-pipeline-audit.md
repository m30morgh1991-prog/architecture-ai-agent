# Pre-H79 Pipeline Audit

## Scope
Audit of the architecture understanding path before H79 completion:
DWG Pipeline -> BIM/ConstraintMap -> Golden DWG Regression -> Controlled Editing -> Impact Analysis -> Visual Runtime.

## Findings

### 1. DWG Pipeline
- Native DWG ingestion and entity inventory already exist.
- Architectural candidate detection is conservative and evidence-backed.
- Candidates remain UNKNOWN unless approval-grade semantics are proven.
- Geometry, layer, entity and derived evidence are traceable by source hash/handles.
- Existing space extraction and topology validation are reusable.
- Main remaining gap: native DWG semantics for doors/windows/columns/walls must be corroborated before LOCKED promotion.

### 2. BIM <-> ConstraintMap
- BIMElementIdentity and BIM graph validation are present.
- BIM categories map deterministically to LOCKED/EDITABLE/CONDITIONAL/UNKNOWN.
- Contradictions fail closed.
- H79 adds evidence-backed ConstraintMap construction.
- Main integration rule: PlanModel remains Source of Truth; BIM is semantic evidence, not authority.

### 3. Golden DWG Regression
- Existing real-DWG infrastructure and regression history were found in repository.
- Golden files are part of the project workflow.
- Regression should assert: source identity, entity inventory, architectural candidates, evidence provenance, PlanModel validity, relation topology, and fail-closed uncertainty.
- No approval-grade PASS should be inferred merely from successful parsing.

### 4. Controlled Editing
- ControlledEditingDecision, runtime mapping, and ApprovedChangePlan already exist.
- LOCKED targets block execution unless an explicit authorized state is supported by the contract.
- CONDITIONAL targets require conditions.
- UNKNOWN/uncertainty remains blocking.
- No geometry mutation should occur before approval.

### 5. Impact Analysis
- ImpactDependency is already represented in the controlled-editing contract.
- Impact analysis must consume ConstraintMap + architectural relations and classify affected elements before approval.
- Any affected LOCKED/UNKNOWN/CONDITIONAL-without-resolution path must fail closed.
- Impact results must retain evidence and source/model identity.

### 6. Visual Runtime
- Real visual ingestion exists for JPG/PNG/WEBP/PDF/DWG.
- Real visual runtime builds PlanModel and ConstraintMap conservatively.
- Current DWG visual path intentionally reports UNKNOWN for approval-grade fixed-element identification.
- Visual readiness is distinct from visual PASS.
- Existing blockers include detection uncertainty, scale uncertainty, locked-element uncertainty, editor guard verification and post-edit detection.

## Integration Contract
The safe end-to-end invariant is:

SOURCE -> EVIDENCE -> DETECTION -> PLANMODEL -> BIM SEMANTICS -> CONSTRAINTMAP -> IMPACT -> APPROVED CHANGE PLAN -> CONTROLLED EDIT -> POST-EDIT DIFF -> FINAL VALIDATION -> AUDIT

Any missing source, evidence, semantic identity, scale, locked-element proof, editor guard, or post-edit detection must remain fail-closed.

## Gate
This audit branch is preparatory only. It does not modify the active H79 PR/head and must not be treated as H79 completion.
