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

## Evaluated upstream implementation — U-C4N/Autocad-MCP

Research reference: https://github.com/U-C4N/Autocad-MCP (README and repository LICENSE reviewed 2026-11-13; upstream declares MIT).

This is a candidate implementation/reference for the existing adapter boundary, not a new core dependency. Its README describes two execution paths: live AutoCAD automation through Windows COM, and headless DXF processing through ezdxf. DWG conversion depends on external tooling. It also describes typed MCP tools, drawing/entity/layer inspection, guarded operations, dry-run/checkpoint patterns and QA workflows. These are upstream-described capabilities, not independently reproduced compatibility evidence for our project.

### Adopt as design requirements (not wholesale code)

- Capability discovery reports host, backend, version, read/write scope and unsupported operations before tools are exposed.
- Read-only inspection tools are separately allow-listed from mutation tools.
- Mutations require a source-bound ApprovedChangePlan, explicit target identity, preconditions and bounded scope.
- Dry-run returns a machine-readable proposed diff and is never reported as execution success.
- Every write is followed by independent readback, deterministic requested-vs-actual diff, source/output hashes and audit record.
- Checkpoint/rollback is adopted only after recovery guarantees are tested on disposable copies.
- MCP tool descriptions and model-generated arguments are untrusted input and must be validated against our own typed contracts.

### Staged evaluation

**CAD-MCP-PILOT-01 — read-only DXF (host-independent):**
1. Pin an exact upstream commit and archive its license/dependency manifest.
2. Use only a generated disposable DXF fixture (never Golden DWGs).
3. Compare entity, layer, block, dimension and unit observations against ezdxf and our current read-only adapter.
4. Record source hash, backend/version, tool name, raw response hash and normalized evidence.
5. Missing or ambiguous fields remain UNKNOWN or NEEDS_REVIEW.

**CAD-MCP-PILOT-02 — live AutoCAD (Windows, deferred):**
1. Run only when a Windows host with the exact target AutoCAD version is available.
2. Use a disposable drawing copy and verify document identity before and after every operation.
3. Keep all mutation tools disabled until ApprovedChangePlan, readback, diff and recovery gates pass.
4. Record AutoCAD version, COM/backend details, input/output hashes and unsupported capabilities.

No upstream implementation is considered integrated until a separate implementation PR passes exact-head CI and adapter tests.
