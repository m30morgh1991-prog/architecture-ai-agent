# AIE Adapter Contract — v0.1

**Status:** proposed port/adapter boundary; no live HZplan or ArchLang integration is claimed.

## 1. Design rules

1. Adapters are replaceable capabilities, not authorities.
2. The canonical PlanModel and ConstraintMap remain owned by the repository.
3. An adapter may emit evidence or a validation report; it cannot silently promote evidence or change permissions.
4. All adapter inputs/outputs must be versioned, validated, and traceable.
5. Adapter failure, timeout, unavailable credentials, unsupported geometry, or schema mismatch must fail closed for the requested operation.
6. Core workflows must remain usable without optional network adapters.

## 2. Common envelope

Every adapter request/response should carry:
- `contract_version`
- `operation_id`
- `project_id`
- `source_sha256` or exact PlanModel revision
- `adapter_id` and adapter version
- declared capability and requested operation
- coordinate frame and units, when geometry is involved
- provenance/evidence references
- typed status and diagnostics

Never accept an adapter response if its source hash, model revision, coordinate frame, or contract version does not match the request.

## 3. Capability discovery

An adapter should expose capabilities before it is selected, for example:
- image-to-candidate-geometry
- drawing-page splitting
- scale calibration support
- plan compilation
- geometry lint/validation
- supported entity types
- supported coordinate frames and units
- online/offline requirement

Capability discovery is descriptive, not proof that a particular input can be processed successfully.

## 4. HZplan adapter

### Intended role
Optional extraction/reconstruction assistant for image-based floor plans and structured geometry. Its result is candidate evidence.

### Required behavior
- Preserve original source identity and page/storey selection.
- Return raw and normalized geometry separately.
- Report scale-calibration status explicitly.
- Never assume an uncalibrated model is dimensionally authoritative.
- Return entity IDs as external references, mapped to canonical AIE IDs only by a deterministic reconciliation step.
- Preserve unsupported/ambiguous elements as unresolved.
- Do not write directly into the canonical PlanModel or ConstraintMap.

### Error/status mapping
- service unavailable -> `ADAPTER_UNAVAILABLE`
- quota/entitlement failure -> `CAPABILITY_UNAVAILABLE`
- scale not calibrated -> `SOURCE_REQUIRED` / `NEEDS_REVIEW`
- incomplete/ambiguous extraction -> `PARTIAL` with unresolved references
- source mismatch -> `BLOCKED`

## 5. ArchLang adapter

### Intended role
Optional deterministic plan representation, compilation, linting, and geometry validation.

### Required behavior
- Convert only an approved, normalized model snapshot into ArchLang input.
- Preserve canonical IDs through a reversible mapping table.
- Return compiler version, diagnostics, warnings, and validation scope.
- Report unsupported model features explicitly.
- Never infer architectural compliance from successful compilation.
- Never become the only geometry validator.
- Never apply generated output back to the canonical model without a reviewed import/reconciliation step.

### Error/status mapping
- compile failure -> `VALIDATION_FAILED`
- unsupported entity -> `UNSUPPORTED_CAPABILITY`
- coordinate/unit ambiguity -> `BLOCKED`
- lint warning -> non-PASS diagnostic; disposition depends on severity policy

## 6. Local adapter and offline operation

Local processing should be preferred where reliable and supported. AIE must record dependency versions and capability availability. If a local dependency is absent, report a typed unavailable status; do not silently fall back to an unverified cloud provider.

A network adapter must be opt-in and must disclose that the source drawing or derived geometry leaves the local environment. Do not transmit files or personal/project data without explicit user authorization and a configured privacy policy.

## 7. Minimal interface sketch

```python
class PlanAdapter:
    def capabilities(self) -> dict:
        ...

    def inspect(self, request: dict) -> dict:
        ...

    def validate(self, request: dict) -> dict:
        ...
```

This is an interface sketch only. Concrete Python protocols, serialization, retries, cancellation, and timeout policy must be specified against the repository's existing runtime conventions before implementation.

## 8. Adapter acceptance tests

- exact source SHA is echoed and verified
- wrong source SHA is rejected
- unsupported contract version is rejected
- units/frame absent or mismatched is not normalized by guessing
- partial extraction preserves unresolved IDs
- adapter outage does not corrupt canonical state
- adapter cannot mutate LOCKED or unapproved targets
- ArchLang compile PASS is not represented as code-compliance PASS
- HZplan uncalibrated scale is never reported as calibrated
- no network adapter is invoked in offline-only mode
