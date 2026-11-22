# IFC / BIM Adapter Boundary

## Decision

IfcOpenShell and buildingSMART IDS/IfcTester are optional candidate implementations for a provider-neutral IFC/BIM evidence adapter. They are not part of the mandatory runtime and do not replace PlanModel.

Canonical flow:

IFC / ifcJSON → IFC adapter → source-bound BIM evidence → reconciliation → existing BIM-ready contracts / PlanModel consumers → rules and validation

IFC schema validity, IDS information conformance, geometry/topology validity, architectural understanding and local regulatory compliance are distinct outcomes.

## Responsibilities

- Inspect IFC schema and file-level metadata.
- Preserve explicit length/area/angle units and coordinate/georeferencing metadata.
- Extract project/site/building/storey spatial hierarchy and containment.
- Extract typed entities, stable GlobalIds, placements, properties and relationships.
- Report unsupported entities/properties and lossy mappings explicitly.
- Optionally run IDS checks through a separately versioned ruleset.
- Optionally compare two IFC snapshots and report additions, removals and property/placement changes.

## Prohibited behavior

- No direct mutation of PlanModel, ConstraintMap or ApprovedChangePlan.
- No inference that an IFC entity is architecturally correct merely because it is schema-valid.
- No inference that IDS pass proves geometric or regulatory correctness.
- No silent unit conversion, coordinate transform, entity dropping or property coercion.
- No mandatory IfcOpenShell dependency in the core.
- No GPL/Bonsai component bundling without package-specific license review.

## Read-only pilot BIM-IFC-PILOT-01

Use a synthetic, self-authored IFC fixture. Record:
1. Exact IfcOpenShell and IfcTester versions/commits and package licenses.
2. IFC schema identifier and unit assignments.
3. Spatial hierarchy and containment.
4. Entity counts, GlobalId uniqueness and unresolved references.
5. Placements, coordinate context and unsupported geometry.
6. IDS specification/version and each requirement result.
7. Input SHA-256, normalized evidence hash and deterministic repeatability.

Acceptance requires reproducible results, explicit unsupported-field reporting, correct unit handling, no mutation of canonical state and tests in an optional isolated environment. The pilot does not authorize a production dependency or claim BIM compliance.

## License and distribution

IfcOpenShell is a multi-component ecosystem with differing licenses. Inspect the exact Python package, native libraries, bundled dependencies and distribution model before shipping. Bonsai is a separate GPL-licensed application and is not required for this adapter. This note is engineering triage, not legal advice.

## Research references

- https://github.com/IfcOpenShell/IfcOpenShell
- https://docs.ifcopenshell.org/introduction
- https://github.com/buildingSMART/ifctester
- https://www.buildingsmart.org/standards/bsi-standards/ids/
- Research review: `docs/research/open-source-aec-cad-agent-review-2026-11-13.md`
