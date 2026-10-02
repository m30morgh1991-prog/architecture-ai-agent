# Architecture AI Agent — Research Integration Roadmap

## Purpose
Durable implementation memory for research findings that must be applied at the relevant H stage. These are project requirements/inputs, not claims that external projects are standards.

## Autodesk / OAS findings — MUST APPLY
Source: Autodesk Platform Services, Open Architecture Standards for 2D Floor Plans (OAS).

### Canonical architecture rule
- PlanModel remains the canonical internal source of truth.
- OAS is an interoperability/schema adapter, never a replacement for PlanModel.
- Keep file-format adapters outside the deterministic core.

### When to apply
**H77–H80 (Change Proposal → ApprovedChangePlan → Controlled Editing):**
- Carry explicit units and coordinate-system metadata through proposals/plans where geometry is involved.
- Represent rooms/spaces, walls, openings and furniture as explicit semantic entities where evidence supports them.
- Preserve the distinction between resolved layout and design intent.
- Keep render/image representation separate from semantic architectural data.
- Make target/region references inspectable before execution.

**H81–H84 (DWG controlled editing + post-edit + E2E):**
- Add/validate an OAS interoperability adapter only where useful; do not couple the core to OAS.
- Map OAS concepts into PlanModel with deterministic, loss-aware conversion.
- Never silently discard unsupported fields; preserve them as extensions or mark them UNKNOWN.
- Validate units, coordinate system, geometry, topology and element identity during conversion.
- Use real Golden DWGs as regression evidence.

**Future IFC/OpenBIM work:**
- Maintain the same adapter boundary for IFC/IDS.
- IDS is an information-validation layer; geometry validation remains separate.

## Research findings that reinforce the same architecture
- SALI-FP: evidence-gated parsing and revision → preserve source evidence, derived geometry, semantic interpretation and edit authorization as distinct layers.
- PolarSym: geometry-aware CAD parsing → capture orientation, distance, alignment, symmetry where evidenced, topology and connectivity as validation/invariant inputs.
- RePlan: plan-then-execute and region-aligned guidance → ApprovedChangePlan remains the execution authorization boundary.
- PhysEdit: physically consistent editing → post-edit validation must protect physical/structural invariants.
- buildingSMART IDS / IfcOpenShell → future IFC adapter + deterministic information validation + provenance; do not embed IFC assumptions in the core.
- AFPlan / dwg-bim_AI → keep raster, vector and CAD evidence paths distinct.

## Mandatory integration rule
Before implementing any stage listed above, inspect this roadmap and the related research document:
docs/research/2026-10-02-architecture-ai-research-update.md

Then implement only the subset appropriate to that stage and prove it with:
Implement -> REAL CI -> Verify -> Regression -> Persist -> Continue.

No external research source can override fail-closed governance or authorize regulatory compliance claims without authoritative evidence.
