# AIE PlanModel Contract Mapping — v0.1

**Status:** design mapping to existing contracts; not a new runtime schema  
**Canonical implementation:** `runtime/plan_model_contract.py`

## 1. Non-duplication rule

AIE must use the existing `PlanModel`, `PlanElement`, `ConstraintMap`, `SpaceModel`, `ElementEvidenceBundle`, and `DrawingEvidenceSet` contracts. This document describes their role and the additional metadata that may be proposed later. It does not authorize a second PlanModel class or a second semantic graph.

## 2. Existing canonical fields

### PlanModel

Current dataclass fields:
- `model_id`
- `source_sha256`
- `drawing_count`
- `elements`
- `unresolved`
- `space_model`
- `element_evidence`
- `drawing_evidence`
- `bim_relations` (optional compatibility surface; BIM expansion deferred)

Current validation includes source hash shape, positive drawing count, unique element IDs, element validation, evidence source continuity, drawing evidence validation, and SpaceModel source continuity.

### PlanElement

Current dataclass fields:
- `element_id`
- `element_type`
- `state` — LOCKED / EDITABLE / CONDITIONAL / UNKNOWN
- `geometry` — current open dictionary; do not assume a unit or coordinate frame unless evidence explicitly supplies it
- `evidence_ids`
- `confidence`
- `bim_identity` — optional compatibility field; not an MVP workstream

The existing validator requires evidence references and confidence in [0, 1]. LOCKED elements require confidence >= 0.95; EDITABLE elements require confidence >= 0.90. AIE must not weaken these thresholds or invent evidence to satisfy them.

### ConstraintMap

Current fields:
- `map_id`
- `model_id`
- `protected_element_ids`
- `editable_element_ids`
- `conditional_element_ids`
- `unknown_element_ids`
- `evidence_ids`

Current validation requires non-empty IDs/evidence and mutually exclusive state buckets. Additional checks for complete coverage and references to actual PlanModel IDs should be considered only as a separately tested contract extension.

## 3. Space model

Spaces and their relations remain owned by the existing `SpaceModel` contract. AIE should reference its spaces and relations rather than creating a competing room graph. The source SHA must remain continuous with the containing PlanModel.

## 4. Canonical identity

Use stable, model-scoped IDs for elements. Human-readable prefixes may be used as display conventions, not as semantic proof:
- `W-...` wall
- `C-...` column
- `D-...` door
- `WN-...` window
- `SP-...` space

IDs must be unique within a model revision. When external tools use their own IDs (for example `wall1`), store them as adapter-local external references mapped to canonical IDs. Never use an external ID as the sole durable identity.

## 5. Geometry metadata — proposed extension, not current enforcement

The current `PlanElement.geometry` is a dictionary. Before standardizing its content, inspect all producers and consumers. The target representation should make these concepts explicit:
- geometry type and coordinates
- coordinate-frame identifier
- unit (prefer mm for normalized architectural geometry)
- source geometry reference
- transformation/calibration record
- geometry validity status

Do not silently add a default unit. Missing/contradictory units or coordinate frame must remain UNKNOWN / SOURCE_REQUIRED. A known measurement may calibrate scale only through an explicit, auditable calibration operation.

## 6. Evidence and provenance

Each element must reference evidence IDs from the source-bound evidence contracts. Evidence records should preserve:
- source file SHA-256
- source class and input mode
- page/view/entity locator where available
- extraction method and version
- provenance (DIRECT / DERIVED / INFERRED where supported by the current contract)
- confidence and unresolved/contradictory state

A file hash proves source identity, not semantic correctness. A CAD line, layer name, text label, or visual detector output is not automatically an architectural fact.

## 7. Revision and diff

PlanModel revisions should be immutable snapshots or otherwise have explicit version identity. A revision comparison should report:
- added/removed/changed canonical IDs
- geometry changes with coordinate-frame compatibility checks
- state/permission changes
- evidence additions/removals
- unresolved and conflict changes

A comparison across different or unknown coordinate frames must not claim geometric equivalence. Do not overwrite the source snapshot during controlled editing.

## 8. Example — conceptual only

```json
{
  "model_id": "plan-rev-0001",
  "source_sha256": "<64-character-source-hash>",
  "drawing_count": 1,
  "elements": [
    {
      "element_id": "W-001",
      "element_type": "wall",
      "state": "UNKNOWN",
      "geometry": {},
      "evidence_ids": ["EV-001"],
      "confidence": 0.0,
      "bim_identity": null
    }
  ],
  "unresolved": ["W-001:GEOMETRY_AND_CLASSIFICATION_REQUIRE_REVIEW"]
}
```

This is an explanatory payload, not a valid fixture by itself: the evidence bundle and referenced evidence must exist and pass their own validators. The example intentionally does not assign a unit, structural role, or editable state.

## 9. BIM policy

The current PlanModel has optional BIM-ready fields. Keep them backward compatible, but do not add IFC, BIM authoring, or expanded relationship semantics in this MVP. BIM remains a later capability that must reuse canonical element identity and evidence lineage.
