# AutoCAD-MCP Integration Boundary

## Decision

Integrate AutoCAD-MCP as an external CAD Execution / Inspection Adapter, not as the Architecture AI Agent semantic brain or source of truth.

Canonical flow:

DWG/DXF -> AutoCAD-MCP inspection/evidence -> DrawingEvidence -> Reconciliation -> PlanModel -> ConstraintMap -> ImpactAnalysis -> Rules -> ApprovedChangePlan -> AutoCAD-MCP controlled execution -> PostEditDiff -> Final Validation -> Audit

AutoCAD-MCP evidence must never bypass the existing evidence/reconciliation contracts.

## Integration rules

1. Read-only first. The first adapter milestone is inspection/evidence only.
2. No arbitrary AutoCAD commands. The Architecture Core may send only typed, allow-listed operations represented by an ApprovedChangePlan.
3. No direct PlanModel mutation. Adapter responses are evidence; reconciliation remains authoritative.
4. Source fencing. Every operation binds to source SHA-256 and, for live AutoCAD, document identity/revision where available.
5. Fail closed. Missing capability, stale revision, wrong document, unsupported operation, uncertain geometry, or missing postcondition produces BLOCKED or NEEDS_REVIEW, never PASS.
6. Postcondition readback is mandatory. A successful command is not evidence that intended geometry was produced.
7. Original Golden DWGs remain immutable. Execution tests use copies and retain source/output hashes.
8. Headless CI first. Linux CI exercises the adapter contract with deterministic DXF fixtures. Real AutoCAD smoke tests remain a separate Windows evidence layer.
9. Provider neutrality. AutoCAD-MCP is one adapter implementation; core contracts do not depend on its package or proprietary AutoCAD APIs.
10. Execution remains behind ApprovedChangePlan. No prompt, VLM output, or raw MCP response can directly trigger a write.

## Capability mapping

| AutoCAD-MCP capability | Architecture AI Agent use |
|---|---|
| entity/layer/block/annotation inspection | source-bound DrawingEvidence |
| dimensions / topology audit | dimension + topology evidence |
| document identity/revision | execution fencing |
| checked writes / readback | controlled editing + PostEditDiff |
| transactions / idempotency | recovery + execution safety |
| headless DXF backend | CI adapter tests |
| DWG/AutoCAD backend | future real runtime |
| delivery manifest / SHA-256 | audit + release validation |
| preview / fixed-camera evidence | Visual Runtime, never semantic authority |

## Acceptance gates before real write integration

- Adapter contract tests pass.
- Headless DXF inspection produces source-bound evidence.
- Evidence source SHA matches the input.
- Unsupported capability returns a machine-readable blocked result.
- Stale source/document revision blocks mutation.
- ApprovedChangePlan is required.
- Postcondition readback is required.
- Requested/actual diff is deterministic.
- Original source is unchanged.
- Golden regression remains fail-closed.
- Real Windows AutoCAD smoke test passes independently before enabling live execution.

## Current scope

This change introduces the provider-neutral boundary and acceptance contract only. It does not claim that live AutoCAD is connected, that AutoCAD-MCP is installed in ChatGPT, or that DWG mutation is currently production-ready.
