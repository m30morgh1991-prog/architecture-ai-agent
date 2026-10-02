# Architecture Understanding Core — Unified Layer Model (BIM-ready)

**Status:** SPECIFICATION INTEGRATION — implementation/CI status must be verified separately.

## Canonical pipeline
RAW SOURCE → NATIVE/EXTERNAL EXTRACTION → DRAWING REPRESENTATION → GEOMETRY → ARCHITECTURAL SEMANTICS → BIM-READY ELEMENT/SPACE MODEL → TOPOLOGY & RELATIONS → CONSTRAINTS → RULES/IMPACT → CONTROLLED EDITING → POST-EDIT DIFF → VALIDATION/AUDIT

The AI Agent may interpret requests and evidence, but deterministic contracts remain the source of truth for geometry, identity, relationships, constraints, rules and validation.

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
