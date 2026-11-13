# AIE — Architecture Intelligence Engine (Architecture v0.1)

**Status:** proposed architecture baseline; documentation only  
**Scope:** offline-first orchestration around the repository's existing architectural contracts  
**Non-goal:** replacing the current PlanModel, ConstraintMap, ApprovedChangePlan, H100 understanding work, or Golden DWG evidence pipeline.

## 1. Product decision

AIE is the modular coordination layer for understanding, validating, and safely changing architectural plans. It is not an image editor and it must not become a second semantic source of truth.

The existing repository contracts remain authoritative:
- `runtime.plan_model_contract.PlanModel` and `PlanElement`
- `runtime.plan_model_contract.ConstraintMap`
- source-bound element and drawing evidence contracts
- `runtime.space_model_contract.SpaceModel`
- `runtime.approved_change_plan_contract.ApprovedChangePlanDecision`
- existing request, input-source, controlled-editing, and validation contracts

AIE may add orchestration and adapter boundaries around these contracts. It must reuse or extend them through reviewed migrations; it must not create a parallel PlanModel or duplicate semantic graph.

## 2. Priorities

### MVP — in this order
1. Plan understanding and source/evidence reconciliation.
2. Canonical PlanModel and spatial relationships.
3. ConstraintMap and protected-element enforcement.
4. Impact analysis before any proposed change.
5. Explicit approval and controlled editing.
6. Independent validation, post-edit diff, and audit.
7. Portable local execution and replaceable integrations.

### Explicitly deferred
- Full BIM workflows, IFC import/export, authoring, and BIM coordination.
- Revit authoring or synchronization.
- Autonomous structural classification or code-compliance claims without authoritative evidence.
- Mandatory cloud AI/provider dependency.
- Native DWG/DXF editing as an assumed MVP capability.

The current code already contains optional BIM-ready identity/relation fields. Preserve those compatibility points, but do not expand BIM functionality as part of this AIE MVP.

## 3. Logical architecture

```text
Inputs
  |-- Engineering plan evidence (DWG/DXF, inspected vector PDF)
  |-- Image/document evidence (raster PDF, JPG/PNG/WEBP)
  |-- User request and supplied dimensions
  v
Input Classification + Provenance
  v
Understanding / Detection Adapters
  v
Evidence Reconciliation
  v
Existing PlanModel + SpaceModel
  v
Existing ConstraintMap
  v
Impact Analysis + Rule Evaluation
  v
Change Proposal
  v
Explicit Approval -> ApprovedChangePlan
  v
Controlled Execution Adapter
  v
Post-edit Diff -> Independent Validation -> Audit / Export
```

The actual pipeline must preserve the repository's established ordering and source trust boundaries. Image evidence must not silently become authoritative engineering geometry. PDF representation must be inspected; an unclassified PDF remains UNKNOWN.

## 4. Module boundaries

| Module | Responsibility | Authority |
|---|---|---|
| Input Boundary | classify source, capture hash, page/frame metadata, units evidence | source metadata only |
| Understanding | detect geometric and drawing-language candidates | candidate evidence only |
| Reconciliation | bind evidence, provenance, contradictions, unresolved facts | may promote only under existing contracts |
| PlanModel Facade | expose the canonical model and its revisions | existing PlanModel contract |
| Constraint Facade | protected/editable/conditional/unknown state | existing ConstraintMap contract |
| Impact Analysis | calculate affected elements, spaces, dimensions and dependencies | advisory proposal; no edit authority |
| Change Orchestrator | request, proposal, approval, execution hand-off | ApprovedChangePlan required |
| Validation | static, runtime, visual, domain checks | reports separate outcomes |
| Audit / Export | immutable trace, diff, generated artifacts | no semantic authority |

Each module has a narrow input/output contract. Dependencies point inward to shared contracts; adapters must not import or mutate core state directly.

## 5. Adapter strategy

Adapters are optional ports:
- **HZplan adapter:** optional remote extraction/reconstruction capability. It may return candidate geometry and metadata, never authoritative semantics by itself.
- **ArchLang adapter:** optional deterministic plan compilation/lint/geometry-validation capability. Its result is one validation signal, not the sole validator.
- **Local visual/CAD adapters:** use existing local runtime paths where available. Keep read-only CAD evidence distinct from write/edit capability.

No adapter is required to construct, validate, or inspect the core data model. Adapter absence or outage must not corrupt state. If an operation cannot be completed safely without an unavailable adapter, return a typed blocked/needs-review result.

## 6. Offline-first design

The core contracts, state transitions, deterministic geometry checks, impact analysis, audit, and supported local input processing should run without network access once dependencies and models are present locally.

Network adapters must be capability-detected and optional. Never download or execute unpinned code/models during a plan operation. Cache provenance and model/version metadata where applicable. A local mode is not considered verified merely because the code has no explicit HTTP call; dependency availability and actual offline tests are required.

## 7. Safety invariants

- Source of Truth remains PlanModel + ConstraintMap + ApprovedChangePlan.
- Every promoted element is source-bound and evidence-backed.
- Unknown, conflicting, or insufficient evidence stays unresolved.
- LOCKED elements cannot be edited by an adapter or execution backend.
- Impact analysis precedes approval; approval precedes execution.
- No LLM, adapter, plugin, or generated file can bypass deterministic validation.
- Logical/static, runtime, and visual results remain distinct.
- Golden DWG fixtures remain immutable regression inputs.
- No stage is declared complete from documentation or a design diagram alone.

## 8. Proposed package layout

This is a target boundary, not a directive to duplicate or move current runtime modules:

```text
runtime/
  aie/
    orchestration/
    ports/
    adapters/
      hzplan/
      archlang/
    impact/
    audit/
```

Before introducing packages, map existing files and tests to these responsibilities. Prefer a thin facade over a large refactor.

## 9. Delivery sequence

1. Inventory current contracts and map them to AIE responsibilities.
2. Freeze adapter request/response contracts and error taxonomy.
3. Implement a read-only AIE facade over existing PlanModel/evidence.
4. Add deterministic impact-analysis contract and tests.
5. Add change orchestration without new editing capability.
6. Connect optional adapters behind capability flags.
7. Verify exact-head CI, Runtime Tests, Bug Hunt, and applicable Golden regression.
8. Add true offline integration tests before claiming offline support.

## 10. Acceptance for this document

This document establishes design intent only. It does not claim implementation, runtime capability, offline verification, or H100 completion. Any implementation PR must identify reused contracts, changed files, migration risks, negative tests, and exact-head CI evidence.
