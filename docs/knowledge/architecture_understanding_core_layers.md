# Architecture Understanding Core — Unified Layer Model (BIM-ready)

**Status:** SPECIFICATION INTEGRATION — implementation/CI status must be verified separately.

## Canonical pipeline
RAW SOURCE → EVIDENCE → ELEMENT IDENTITY → GEOMETRY → TOPOLOGY → SPATIAL/ARCHITECTURAL RELATIONS → ARCHITECTURAL SEMANTICS → BIM-READY ELEMENT/SPACE MODEL → CONSTRAINTS → RULE CONTEXT → IMPACT → CONTROLLED EDITING → POST-EDIT DIFF → VALIDATION/AUDIT

The AI Agent may interpret requests and evidence, but deterministic contracts remain the source of truth for geometry, identity, relationships, architectural semantics, constraints, rules and validation. Detection is not understanding: a detector candidate, symbol, layer, text label, or BIM mapping is evidence until its semantic meaning is explicitly supported.

## 1. Source & Evidence Layer
- Source identity and immutable source hash.
- Native entity provenance (DWG/Revit/IFC/visual/external detector).
- Evidence bundles with typed evidence IDs.
- Source/version/provider metadata.
- Contradiction and missing-evidence states remain fail-closed.

## 2. Drawing Representation Layer
Software-neutral representation evidence before semantic interpretation.
- AutoCAD: Layer, Entity, Block/Attribute, Linetype, Lineweight, Color, Dimension, Hatch, XREF, Model/Paper Space, Layout, Viewport, Units.
- Revit: Category/Subcategory, Family/Type, Parameter, Level, Room/Space, View, View Template, Object Style, Filter, Tag, Annotation Symbol.
- Future IFC: IFC entity/property/relationship.
- Sheet/title-block/annotation geometry is kept separate from model geometry.
- Layer/color/linetype/block/symbol is evidence, never semantic truth alone.

## 3. Geometry Layer
- Native geometry, closed boundaries, curves, arcs, insertion points, extents and scale/units.
- Geometry identity must remain traceable to source evidence.
- BBox overlap is only candidate evidence, never architectural adjacency by itself.
- Dimensions are evidence objects; dimension text alone does not prove an associated edge.

## 4. Architectural Semantic Layer
Canonical candidate types include:
Boundary, Wall, Column, Door, Window, Opening, Stair, Furniture, Fixture, Space/Room, Grid/Axis, Level, Annotation and Documentation objects.
- Detector order: structural fixed → walls/doors/windows → furniture → spaces/relations.
- Candidate ≠ approved semantic truth.
- Fixed/critical semantics require corroborated evidence; contradiction → BLOCKED; insufficient evidence → UNKNOWN.

## 5. BIM-Ready Element Layer
Every architectural element/space is modeled with:
- stable unique ID;
- canonical category/type;
- optional IFC class mapping;
- name/label;
- parent/container/level;
- geometry reference;
- native/external reference;
- extensible properties/parameters;
- evidence/provenance;
- permission/constraint state;
- version/change history.

BIM-ready means the core can carry structured element identity, properties, hierarchy and relationships; it does not mean full BIM authoring/compliance is part of the MVP.

## 6. Space Model Layer
Spaces are first-class objects, not just polygons:
- stable space ID;
- boundary references;
- area/geometry evidence;
- level/context;
- optional room/space classification/name;
- evidence and confidence state;
- relations to bounding elements and openings.
Uncertain closure or semantics remains UNKNOWN.

## 7. Topology & Relationship Layer
Relationships are explicit, typed and evidence-backed:
- CONTAINS / CONTAINED_BY
- BOUNDED_BY
- SHARED_BOUNDARY
- ADJACENCY_CANDIDATE
- CONNECTED_BY_OPENING
- HOSTED_BY
- SUPPORTS
- INTERSECTS / OVERLAPS
- DISCONNECTED
A relationship must never be fabricated from proximity alone. Opening connectivity requires native geometry/host-boundary evidence.

## 8. Constraint & Permission Layer
LOCKED / EDITABLE / CONDITIONAL / UNKNOWN
- Locked elements cannot be changed without explicit authorization.
- Constraints attach to elements, spaces and relationships.
- Evidence and source identity are mandatory for approval-grade constraints.
- UNKNOWN is not PASS.

## 9. Rules / BIM + Regulatory Context Layer
Rules consume structured context rather than raw drawing cues:
- project type, jurisdiction, phase/version;
- binding regulations > official standards > technical sources > reference books > educational material;
- BIM properties can provide evidence/context but cannot override authoritative regulatory evidence.
- Missing source/version/context → SOURCE_REQUIRED/UNKNOWN.

## 10. Change / Impact / Controlled Editing Layer
Request → ImpactAnalysis → ChangeProposal → Conflict → Validation → ApprovedChangePlan → Controlled Editing.
The editor consumes approved decisions and guard data; it does not decide editability.

## 11. Validation / Diff / Audit Layer
- PlanModel↔ConstraintMap identity and evidence binding.
- source/evidence hashes.
- PostEditDiff for unauthorized deltas.
- Final Validation and Audit.
- Release remains blocked on unresolved critical UNKNOWN/BLOCKED states.

## Cross-platform mapping
AutoCAD → Drawing Representation → Common BIM-ready Element Model
Revit → Drawing Representation → Common BIM-ready Element Model
IFC (future) → Common BIM-ready Element Model

The common model is upstream of PlanModel consumers and provider-neutral.

## Architectural invariant
PlanModel + SpaceModel + ElementEvidenceBundle + ConstraintMap + ApprovedChangePlan are the logical source of truth.

Forbidden:
Prompt → Image Editor → Final Plan

Required:
Request → Evidence/Understanding → PlanModel → Constraints/Relations → Rules/Impact → ApprovedChangePlan → Controlled Editing → PostEditDiff → Final Validation → Audit

## Integration status
This document consolidates the BIM-ready H76 direction with the 2026-10-02 Drawing Representation standards boundary. It does not claim CI green until the repository workflow is actually observed as successful.


## 12. Research refinement — semantic understanding chain

The current research adds an explicit interpretation chain inside the existing architecture:

**Source Evidence → Element Identity → Geometry → Topology → Spatial Relation → Architectural Semantics → BIM Semantics → Rule Context**

This does not introduce another canonical model. It clarifies how existing contracts compose.

### Drawing-language evidence

The semantic layer must be able to consume, with provenance:

- door/window symbols and opening direction;
- layer, linetype and lineweight;
- dimensions and extension lines;
- level/elevation codes;
- room/space names and identifiers;
- section/elevation markers and direction;
- hatch/pattern evidence;
- columns and structural symbols;
- stairs/landings and level relationships;
- grid/axis symbols;
- title block, scale and unit evidence.

No single cue is sufficient when corroboration is required.

### BIM/IFC boundary

IFC and ifcJSON are interoperability representations, not the MVP Source of Truth. The existing PlanModel/BIM-ready contracts remain canonical upstream.

Stable identity, level, parent/container, placement, properties and typed relationships should be mappable to IFC-style semantics. Approval-grade relation provenance should remain traceable to the existing ArchitecturalRelation evidence rather than creating a second BIM evidence graph.

### Fail-closed semantic interpretation

- Missing referenced geometry → UNKNOWN.
- Contradictory explicit evidence → BLOCKED.
- Incomplete host/opening relation → NEEDS_REVIEW.
- Unsupported symbol/layer inference → UNKNOWN/NEEDS_REVIEW.
- Incomplete IFC mapping → unresolved downstream export; never mutate PlanModel truth.
- Stair-count inference from level codes is permitted only when the relevant level/rise/run evidence is explicit and internally consistent.

See `docs/research/PLAN_UNDERSTANDING_SEMANTIC_CHAIN.md` for the implementation mapping and H sequencing.


## Educational reference integration — architectural drawing language

The reference `docs/knowledge/uas1_plan_drawing_reading_reference.md` is part of the educational knowledge base. It records conventional Iranian architectural/structural drawing vocabulary, including plan symbols, section markers and view relations, stair/landing/level evidence, ramp slope and level consistency, dimension chains, hatching, title/scale evidence, and structural grid/axis vocabulary.

These are educational evidence and interpretation rules, not current regulatory authority. They must feed the existing fail-closed evidence model and must not override official regulations or project-approved documents.

The full source PDF is intentionally not redistributed in this public repository. The user-provided PDF remains the source material for study.
