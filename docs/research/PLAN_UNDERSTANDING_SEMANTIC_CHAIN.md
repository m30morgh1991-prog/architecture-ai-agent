# Plan Understanding Semantic Chain — Research Integration

## Status

Planning/integration specification. This document does not claim implementation or CI GREEN.

## Why this exists

The latest architecture-agent research adds a stronger distinction between **detection** and **understanding**. The project must not treat raster/CAD recognition, BIM metadata, or drawing symbols as architectural truth by themselves.

The required semantic progression is:

**Source Evidence → Element Identity → Geometry → Topology → Spatial Relation → Architectural Semantics → BIM Semantics → Rule Context**

This is compatible with the repository's existing fail-closed architecture, but it exposes several integration boundaries that must be made explicit.

## 1. What already exists

| Chain stage | Existing repository boundary | Current assessment |
|---|---|---|
| Source Evidence | `element_evidence_contract.py`, `native_drawing_evidence.py`, `drawing_metadata_extractor.py` | Strong foundation |
| Element Identity | `plan_model_contract.py`, optional `BIMElementIdentity` | Partial; identity is present but not yet a dedicated evidence-backed semantic identity boundary |
| Geometry | `PlanElement.geometry`, `geometry_topology_validation.py`, `spatial_topology.py`, native drawing evidence | Partial; reconstruction currently carries a conservative bbox/candidate geometry representation |
| Topology | `geometry_topology_validation.py`, `spatial_topology.py` | Existing |
| Spatial Relation | `architectural_relations.py`, `opening_connectivity.py`, SpaceModel relations | Existing, but relation integration should become a first-class downstream input |
| Architectural Semantics | drawing/space/element contracts and H100 annotation semantics | Partial; no single contract currently binds evidence + geometry + topology + relation into semantic interpretation |
| BIM Semantics | `bim_ready_contract.py`, `bim_constraint_contract.py`, `bim_constraintmap_contract.py` | Strong foundation; not full IFC authoring |
| Rule Context | `rule_context.py`, `rule_engine.py`, drawing standards rule packs | Existing and fail-closed |

## 2. Critical architectural finding

The repository should **not** add another PlanModel or another evidence system.

Instead, the missing capability should be an explicit semantic binding boundary that consumes existing evidence/geometry/topology/relation contracts and produces validated architectural semantics.

Proposed future boundary:

`EvidenceBundle + ElementIdentity + Geometry + Topology + ArchitecturalRelationSet + DrawingSemantics → ArchitecturalSemanticModel → BIM mapping → RuleContext`

This is a contract/integration layer, not a second source of truth.

## 3. Required semantic distinctions

### Detection is not understanding

A detector may produce:

- a line candidate;
- a block candidate;
- a text label;
- a hatch;
- a dimension;
- a door/window symbol candidate;
- a level/elevation marker candidate.

None of these alone proves architectural meaning.

The semantic layer must require explicit evidence binding and may return:

- `SUPPORTED`
- `UNKNOWN`
- `NEEDS_REVIEW`
- `BLOCKED`

No uncertain interpretation may become an approval-grade semantic fact.

### Drawing language is evidence

The following should be represented as typed drawing evidence and interpreted through the semantic layer:

- door/window symbol and opening direction;
- line weight, linetype and layer;
- dimensions and extension lines;
- level/elevation codes;
- room/space labels;
- section/elevation markers and direction;
- hatch/pattern evidence;
- structural column symbols;
- stair/landing information;
- grid/axis symbols;
- title block and scale/unit information.

The semantic layer must not treat layer name, color, linetype, text, or symbol shape as sufficient proof in isolation.

## 4. BIM/IFC integration rule

The buildingSMART/IFC research should be used as a **semantic interoperability reference**, not as a new MVP source of truth.

Useful concepts to carry through the existing BIM-ready boundary include:

- stable identity;
- category/type;
- attributes/properties;
- level/floor context;
- parent/container relationships;
- placement/geometry references;
- typed relationships;
- external references;
- machine-readable exchange.

IFC/ifcJSON should be adapters/round-trip representations of the canonical semantic model.

### Important current gap

`BIMElementRelation` is currently an evidence-free graph edge. That is acceptable for a derived graph only if provenance remains recoverable elsewhere, but approval-grade semantic relationships should ultimately be traceable to the existing `ArchitecturalRelation` evidence IDs.

Do not create a second relationship/evidence graph. Prefer extending the existing relation/BIM boundary when implementation begins.

## 5. Recommended implementation boundary

### H100 — Drawing semantics

Keep H100 focused on the existing evidence-backed annotation/dimension boundary.

It should establish the vocabulary and provenance for:

- DIMENSION
- LEVEL
- ELEVATION
- SECTION_MARKER
- GRID
- ROOM_LABEL
- NORTH_ARROW
- SCALE
- TITLE_BLOCK
- DETAIL_MARKER

The current H100 PR already introduces `ArchitecturalAnnotation` and deterministic `DimensionSemantic`. These should become inputs to later semantic interpretation, not a replacement for PlanModel.

### H101+ — Semantic plan generation

When generative planning starts, it must consume the semantic model rather than raw drawing cues.

### H102 — Architecture IR

Architecture IR should be the deterministic representation used to compile validated semantics into drawings and downstream formats.

### H107 — BIM boundary

BIM export should map canonical semantic identities/relations to IFC/ifcJSON-style representations without making IFC the source of truth.

## 6. Concrete file mapping

Prefer these existing anchors:

- `runtime/element_evidence_contract.py` — provenance/evidence.
- `runtime/plan_model_contract.py` — canonical element/space model.
- `runtime/plan_model_reconstruction.py` — evidence → PlanModel reconstruction.
- `runtime/geometry_topology_validation.py` / `runtime/spatial_topology.py` — geometric/topological validation.
- `runtime/architectural_relations.py` — typed spatial/architectural relations.
- `runtime/opening_connectivity.py` — door/window/opening connectivity.
- `runtime/drawing_metadata_extractor.py` — drawing representation evidence.
- `runtime/scale_unit_evidence.py` — scale/unit evidence.
- `runtime/drawing_standards_validation.py` — drawing-standard validation.
- `runtime/bim_ready_contract.py` — BIM identity/property/relation boundary.
- `runtime/rule_context.py` / `runtime/rule_engine.py` — regulatory/rule context.

Potential new file, only if implementation proves necessary:

- `runtime/architectural_semantics_contract.py`

That file must bind existing contracts; it must **not** contain a second PlanModel, evidence store, relation graph, or ConstraintMap.

## 7. Missing capabilities to track

1. Rich geometry identity beyond conservative bbox/candidate geometry.
2. Explicit evidence-backed element identity independent of detector status.
3. First-class integration of ArchitecturalRelationSet into downstream semantic consumers.
4. Evidence/provenance continuity from architectural relations into BIM relationships.
5. Typed representation of Iranian drawing-language semantics.
6. Level/elevation/stair semantics, including deriving stair requirements only when elevation evidence is explicit and consistent.
7. Section/elevation marker direction and cut-plane semantics.
8. Layer/linetype/lineweight/hatch semantics with source evidence.
9. Semantic cross-checks between drawing annotations and geometric/model evidence.
10. IFC/ifcJSON round-trip validation at the adapter boundary.

## 8. Fail-closed examples

- Dimension text exists but referenced geometry is unknown → `UNKNOWN`.
- Door symbol exists but host wall/opening relationship is uncertain → `NEEDS_REVIEW`.
- Level code conflicts with another explicit level code → `BLOCKED`.
- Section marker exists without reliable direction/cut-plane evidence → `UNKNOWN`.
- Layer says WALL but geometry/evidence contradicts it → `NEEDS_REVIEW` or `BLOCKED`, never automatic WALL truth.
- IFC mapping is incomplete → BIM export remains unresolved; it does not alter PlanModel.
- Stair count is inferred from a level code only when the relevant level/rise/run evidence is explicit and internally consistent.

## 9. Updated canonical flow

The existing pipeline remains authoritative, but the understanding core should be read as:

**Source → Evidence → Identity → Geometry → Topology → Spatial/Architectural Relations → Architectural Semantics → PlanModel/BIM Semantics → ConstraintMap → Impact/Rules → ApprovedChangePlan → Controlled Editing → PostEditDiff → Final Validation → Audit**

This is a refinement of the existing architecture, not a replacement.

## 10. Acceptance criteria for implementation

Before this research is promoted from planning to implementation:

1. Existing PlanModel/evidence/relations remain the only canonical semantic stores.
2. New semantic contracts reference existing evidence IDs and source hashes.
3. Ambiguous drawing language remains UNKNOWN/NEEDS_REVIEW/BLOCKED.
4. Geometry/topology evidence cannot be silently replaced by LLM interpretation.
5. BIM/IFC remains provider-neutral and downstream of canonical semantics.
6. Golden DWG regression remains intact.
7. Normal + adversarial tests cover each new semantic boundary.
8. Exact-head REAL CI completes successfully.
9. Project state is updated only after the Green Gate.
