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

## Open-source AEC/CAD agent integration — 2026-11-13

Research record: `docs/research/open-source-aec-cad-agent-review-2026-11-13.md`.

### Adopted patterns and stage placement

| Upstream project | Adopted subset | Existing boundary / stage | Explicit non-adoption |
|---|---|---|---|
| U-C4N/Autocad-MCP (MIT) | capability discovery, read/write separation, dry-run, source fencing, checked execution, readback, diff and recovery test patterns | Existing `docs/integrations/AUTOCAD_MCP_ADAPTER.md`; H81–H84 controlled CAD editing and post-edit validation | No wholesale server import, arbitrary command execution or live writes before Windows evidence |
| IfcOpenShell / IfcTester / IDS | optional read-only IFC parsing, spatial hierarchy/property extraction, schema and IDS checks, IFC diff | New `docs/integrations/IFC_BIM_ADAPTER.md`; future BIM/IFC adapter work after core semantics are stable | IFC/IDS validity is not geometry, plan-understanding or regulatory compliance PASS |
| bbl-dres/plan-extract (MIT code; demo/data caveats) | staged extraction/evaluation concepts for rooms, walls, openings, stairs and graph reconstruction | Existing DrawingEvidence, CandidateFact, PlanModel reconstruction and topology validation | No second canonical graph, no demo dependency stack, no dataset import without artifact-level rights audit |
| Agent-CAD (MIT) | typed intermediate representation, immutable revisions, measured geometry checks | Existing ApprovedChangePlan, PostEditDiff and Audit design | No mechanical/3D stack or Linux-only worker in architecture MVP |
| awesome-cad-agent | discovery index only | Research process | Not an engine or trusted compatibility source |

### Implementation sequence

1. **Now:** research and integration contracts only; keep H101 and geometry PR gates unchanged.
2. **CAD-MCP-PILOT-01:** read-only, synthetic DXF comparison; no Golden files and no mutation.
3. **BIM-IFC-PILOT-01:** optional isolated IfcOpenShell read-only inspection of a synthetic IFC fixture; report schema, units, spatial containment, element/property counts and IDS results separately.
4. **PLAN-EXTRACT-EVAL-01:** benchmark candidate extraction concepts against our own synthetic/adversarial fixtures, with per-class precision/recall, topology validity, uncertainty and human correction cost.
5. **Adoption gate:** require reproducibility, license/dependency audit, offline/local viability, resource measurements, no semantic regression and green exact-head CI. Only then propose narrowly scoped code integration.

### Non-negotiable interpretation

PlanModel remains canonical. External CAD/IFC/vision outputs are source-bound evidence or optional interchange representations. They cannot directly mutate PlanModel, ConstraintMap or ApprovedChangePlan. Preserve UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW / ABSTAIN / BLOCKED. No H-stage becomes PASS from an external benchmark or an upstream README claim.
