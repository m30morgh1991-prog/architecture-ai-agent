# AIE Validation and Evidence Policy — v0.1

**Status:** proposed policy aligned with repository fail-closed governance.

## 1. Validation is layered

AIE reports separate outcomes. No layer can substitute for another.

| Layer | What it establishes | What it does not establish |
|---|---|---|
| Contract/static | schema, references, IDs, state buckets, deterministic geometry invariants | successful runtime operation or visual correctness |
| Runtime | actual operation completed in the target runtime and produced expected state | visual equivalence or regulatory compliance |
| Visual | rendered before/after comparison and detected visual differences | semantic correctness hidden in the image |
| Domain/rules | explicit rules evaluated against sufficient, traceable inputs | truth of missing source data |

A final report must show each applicable layer as PASS, FAIL, UNKNOWN, BLOCKED, or NOT_RUN. Do not collapse them into a single green badge.

## 2. Evidence states

Use the repository's established fail-closed vocabulary:
- `UNKNOWN`
- `SOURCE_REQUIRED`
- `NEEDS_REVIEW`
- `ABSTAIN`
- `BLOCKED`

A missing check is NOT_RUN, not PASS. A timeout or unavailable dependency is not PASS. A warning cannot be silently discarded. Contradictory evidence must be preserved and resolved through the canonical reconciliation path.

## 3. Input-source policy

Reuse `runtime.input_source_contract`:
- DWG/DXF: engineering-plan input class, subject to parser capability and source evidence.
- vector PDF: engineering-plan input only after vector representation is established.
- raster PDF: image input.
- JPG/JPEG/PNG/WEBP: image input.
- uninspected PDF or unsupported source: UNKNOWN.

The trust rank is a reconstruction ordering, not a correctness guarantee. Extension alone is insufficient to classify a PDF. The source SHA-256 establishes byte identity, not geometry or semantics.

## 4. Units and coordinate frames

No implicit unit or coordinate-frame defaults are permitted. Geometry comparisons and edits require compatible frames. If source units are unknown, mixed, or contradictory, scale-sensitive operations are blocked until a trustworthy measurement or source declaration is supplied and recorded.

A calibration operation must record:
- measured reference and value
- source of the measurement
- original and target unit/frame
- transformation applied
- actor and timestamp
- resulting validation evidence

Never repair an inch/mm/cm ambiguity by silently scaling geometry.

## 5. Golden regression policy

The Golden DWG fixtures remain immutable:
- `test-assets/golden-projects/bagheri7.dwg`
- `test-assets/golden-projects/afifiiiii.end.edit3.dwg`

Their hashes and extracted evidence may be used for regression, but neither hash identity nor generic CAD geometry proves architectural semantics. Regression outputs must be reproducible and must not modify the source fixtures.

## 6. Visual comparison

A visual comparison should record source and output artifact hashes, rendering settings, page/storey selection, scale/viewport, alignment transform, and comparison method. If alignment is uncertain, report comparison as inconclusive rather than treating pixel similarity/difference as semantic truth.

## 7. Change acceptance

A change may be accepted only when:
1. target identity is source-bound,
2. ConstraintMap allows the exact targets,
3. impact analysis has no unresolved blocking conflict,
4. explicit approval matches the exact model revision and proposal,
5. execution is limited to approved targets,
6. post-edit diff is generated,
7. all required static/runtime/visual/domain checks have completed successfully,
8. applicable regression evidence is preserved.

If a required check is missing, failed, cancelled, stale, or unobserved, the change is not GREEN.

## 8. CI and delivery gate

For implementation PRs, require exact-head evidence from the repository's required workflows. A result on an earlier SHA does not validate a later head. At minimum, observe the configured PR CI Gate, Runtime Tests, and Mandatory Bug Hunt; run Golden regression when the change affects source understanding, CAD evidence, geometry, or protected-element behavior.

Do not merge, approve on behalf of the user, bypass branch protection, or advance an H-stage based only on a design document.

## 9. Offline claim

Offline-first is a design requirement, not a current verified runtime claim. It can be marked verified only after a controlled test that:
- disables network access,
- uses a documented local dependency/model set,
- processes supported local inputs,
- executes deterministic checks and audit,
- confirms optional network adapters are not called,
- records exact environment and test result.

## 10. BIM deferral

Optional BIM-ready fields already present in PlanModel remain compatibility fields. IFC, BIM authoring, federated coordination, and BIM-specific validation are deferred and are not part of AIE MVP acceptance.
