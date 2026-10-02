# Architecture AI Agent — Research Update (2026-10-02)

## High-signal findings

### 1. Autodesk Open Architecture Standards (OAS)
Autodesk's public `open-architecture-standards-2d-floor-plans` repository describes a lightweight JSON schema for architectural layouts in millimetre coordinates, covering rooms, walls, openings, program, layout, render, and extensions. It explicitly positions the schema as an approach rather than an industry standard.

**Project implication:** keep our PlanModel as the canonical internal source of truth, but add an optional interoperability adapter inspired by OAS concepts:
- explicit units/coordinate system
- rooms/spaces
- walls/openings/furniture
- program constraints and adjacency
- resolved layout vs design intent
- render representation separated from semantic model

Do not replace PlanModel with OAS.

### 2. Evidence-gated floor-plan parsing
A September 2026 research paper, SALI-FP, describes an evidence-gated multimodal pipeline that produces semantic maps, objects, vectors, and relation records and constrains local revisions by image evidence.

**Project implication:** this strongly supports our existing evidence-first architecture. Add a formal distinction between:
- source evidence
- derived geometry
- semantic interpretation
- edit authorization

A visual detector result should never become an editable architectural fact without traceable evidence.

### 3. Geometry-aware CAD floor-plan parsing
PolarSym (2026) reports geometry-aware CAD floor-plan parsing using direction and distance constraints for stronger structural consistency.

**Project implication:** future detection/regression should capture geometric invariants such as:
- orientation
- distance
- alignment
- symmetry where evidenced
- topology
- connectivity

These should feed ConstraintMap/ImpactAnalysis rather than remain only model-internal features.

### 4. Controlled editing research
RePlan (ECCV 2026) uses a Plan-then-Execute pattern with region-aligned guidance and editable intermediate region plans. PhysEdit (ECCV 2026) explicitly targets physically consistent editing.

**Project implication:** our Controlled Editing path should preserve the same conceptual separation:
`request -> explicit plan -> reviewable regions/targets -> constrained execution -> post-edit verification`

This reinforces ApprovedChangePlan as the authorization boundary rather than allowing a model/editor to mutate the source directly.

### 5. IFC / IDS validation
buildingSMART identifies IDS 1.0 as an official standard for machine-interpretable information requirements and automated IFC compliance checking. Its current 2026 survey reports strong demand for better API support, LOIN alignment, richer applicability/relations, documentation, and software certification.

IfcOpenShell currently provides IFC parsing/geometry plus IDS/BCF tooling, including `ifctester`.

**Project implication:** when IFC support becomes active, create an interoperability validation layer rather than embedding IFC assumptions into the core:
- IFC adapter
- IDS rule adapter
- deterministic validation
- evidence/provenance
- versioned schema adapters
- model-vs-model diff

### 6. Existing open-source floor-plan pipelines
Repositories such as AFPlan and dwg-bim_AI demonstrate practical image/vector floor-plan parsing and DWG/IFC-oriented export. Their existence reinforces keeping raster, vector and CAD evidence paths separate instead of forcing one detector to handle all source types.

## Structural update proposed for the roadmap

Add these cross-cutting requirements to the existing H76-H90 work:

1. **Interoperability boundary**
   - PlanModel remains canonical.
   - OAS/IFC/DWG/PDF are adapters, not competing sources of truth.

2. **Evidence lineage**
   - Every architectural fact used for a rule or edit should be traceable to evidence IDs and source identity.

3. **Geometry invariants**
   - Store and validate orientation, distance/alignment, topology and connectivity where available.

4. **Rule provenance**
   - Every rule carries source tier, locator, version and evidence requirements.
   - No legal/regulatory compliance claim without authoritative evidence.

5. **Reviewable edit plan**
   - Controlled editing consumes ApprovedChangePlan only.
   - Region/target guidance remains inspectable before execution.

6. **Post-edit diff**
   - Compare semantic, geometric and protected-element invariants, not only pixels.

7. **OpenBIM adapter path**
   - Treat IDS as an information-validation layer for future IFC workflows.
   - Keep geometry validation separate because IDS itself does not cover geometry.

## Sources

- Autodesk OAS: https://github.com/autodesk-platform-services/open-architecture-standards-2d-floor-plans
- SALI-FP: https://arxiv.org/abs/2609.25615
- PolarSym: https://arxiv.org/abs/2608.11793
- RePlan: https://github.com/JIA-Lab-research/RePlan
- PhysEdit: https://github.com/HiDream-ai/PhysEdit
- buildingSMART IDS: https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/
- buildingSMART standards server: https://standards.buildingsmart.org/
- IfcOpenShell: https://github.com/IfcOpenShell/IfcOpenShell
- AFPlan: https://github.com/cansik/architectural-floor-plan
- dwg-bim_AI: https://github.com/newva/dwg-bim_AI

## Governance note

These findings are research inputs, not automatic changes to the core architecture. Any implementation change must pass:

`Implement -> REAL CI -> Verify -> Regression -> Persist -> Continue`

No research source overrides project fail-closed governance.
