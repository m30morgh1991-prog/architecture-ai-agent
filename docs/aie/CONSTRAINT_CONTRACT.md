# AIE Constraint and Change-Safety Contract — v0.1

**Status:** design contract aligned to existing `ConstraintMap` and `ApprovedChangePlanDecision`  
**Purpose:** prevent an uncertain or unauthorized plan change from reaching execution.

## 1. State model

Every canonical PlanElement has exactly one state:
- `LOCKED`: protected; mutation is prohibited.
- `EDITABLE`: mutation may be proposed, subject to approval and validation.
- `CONDITIONAL`: mutation requires explicit preconditions and evidence.
- `UNKNOWN`: permission cannot be established; treat as non-editable.

The existing ConstraintMap stores these states in four mutually exclusive ID buckets. The PlanElement state and ConstraintMap membership must agree. Any mismatch is a conflict and blocks execution.

## 2. MVP protected defaults

Until project-specific evidence and an explicit policy authorize otherwise, treat these as protected:
- columns and other identified structural fixed elements
- external building boundary
- walls
- doors
- windows
- overall plan form

A default protection rule is not proof that an element was correctly detected. If identity or geometry is uncertain, state remains UNKNOWN and the operation is blocked.

## 3. Evidence requirements

- Every element state must be traceable to evidence.
- LOCKED and EDITABLE confidence thresholds already enforced by `PlanElement.validate()` must not be weakened.
- Evidence must belong to the same source SHA as the PlanModel.
- Missing, cross-source, stale, or contradictory evidence blocks state promotion.
- A detector's confidence score alone does not establish structural role or edit permission.

## 4. Change request lifecycle

```text
ChangeRequest
  -> Target Resolution
  -> Constraint Check
  -> Impact Analysis
  -> Conflict Detection
  -> Change Proposal
  -> Explicit User Approval
  -> ApprovedChangePlan
  -> Controlled Execution
  -> Post-edit Diff
  -> Final Validation
  -> Audit
```

Approval is specific to the proposed targets and change type. Any change to targets, geometry, source revision, or material preconditions invalidates the prior approval and requires a new decision.

## 5. Approval contract

Reuse `runtime.approved_change_plan_contract.ApprovedChangePlanDecision` and its existing `APPROVED` / `REJECT` states. Its builder rejects:
- missing target IDs
- uncertainty-blocked requests
- empty targets
- targets not in the editable set

Do not treat a user request as approval. Do not infer approval from a previous request or a UI state. Approval must be captured as an explicit, auditable event before execution.

## 6. Conditional changes

A CONDITIONAL target is not editable by default. It requires:
1. a named precondition,
2. source-bound evidence satisfying that precondition,
3. a deterministic check of the precondition,
4. explicit user approval for the exact proposal.

If any condition is unavailable or ambiguous, return BLOCKED / NEEDS_REVIEW.

## 7. Impact analysis requirements

Before approval, report at least:
- directly targeted elements
- dependent/adjacent elements
- affected spaces and space relations
- affected dimensions/areas where supported by evidence
- potential opening-host changes
- geometry intersections and clearances where supported
- protected/unknown elements touched by the proposed operation
- unresolved assumptions and missing evidence

Impact analysis is advisory and must not mutate PlanModel or grant permission.

## 8. Execution guard

The execution boundary must re-check immediately before mutation:
- exact source/model revision
- approval target set and change type
- current ConstraintMap and PlanElement states
- all conditional preconditions
- absence of unresolved blocking conflicts
- adapter capability and target support

If the model revision or constraints changed after approval, reject as stale approval. If the executor cannot prove it is modifying only approved editable targets, do not execute.

## 9. Required negative tests

- locked target -> rejected
- unknown target state -> rejected
- conditional target without evidence -> rejected
- target absent from PlanModel -> rejected
- ConstraintMap bucket overlap -> rejected
- PlanElement/ConstraintMap mismatch -> rejected
- cross-source evidence -> rejected
- approval for old revision -> rejected
- changed target set after approval -> rejected
- adapter attempts an unapproved mutation -> rejected
- incomplete impact analysis -> no approval promotion

## 10. Audit event minimum

Record request ID, model/source revision, target IDs, constraint snapshot/reference, impact report reference, proposal hash, approval decision and actor/time, adapter identity/version, execution result, post-edit diff, and validation results. Do not store secrets or provider credentials in audit payloads.
