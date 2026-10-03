# Architecture AI Agent — Research Integration Checklist

## Purpose
Durable checklist for **all external research performed for this project**, with special priority for Autodesk OAS findings. This file prevents research from being forgotten and turns research into explicit implementation/regression gates.

## Status vocabulary
- [ ] DISCOVERED — source/findings recorded
- [ ] MAPPED — mapped to one or more H stages
- [ ] IMPLEMENTED — code/contract changed
- [ ] CI-VERIFIED — real GitHub Actions CI is green for the implementation
- [ ] REGRESSION-VERIFIED — relevant golden/runtime/adversarial regression passed
- [ ] PERSISTED — state/handoff records updated
- [ ] DEFERRED — intentionally postponed with a reason

## Cross-cutting rules — apply to every research item
- [ ] Research never replaces PlanModel as canonical source of truth.
- [ ] External schemas/tools are adapters or evidence sources, not hidden core dependencies.
- [ ] Evidence lineage remains explicit: source -> evidence -> interpretation -> proposed edit -> authorization -> result.
- [ ] Unknown/unsupported/uncertain information stays UNKNOWN/NEEDS_REVIEW/BLOCKED; never silently becomes PASS.
- [ ] Research-derived implementation follows: Implement -> REAL CI -> Verify -> Regression -> Persist -> Continue.
- [ ] No regulatory/legal compliance claim without authoritative, versioned evidence.

---

# 1. Autodesk OAS — PRIORITY: HIGH

Source: Autodesk Platform Services, Open Architecture Standards for 2D Floor Plans.

## Findings to preserve
- [ ] OAS is a lightweight architectural-layout JSON schema, not an industry standard.
- [ ] PlanModel remains our canonical internal model.
- [ ] OAS must be an optional interoperability/schema adapter.
- [ ] Keep file-format adapters outside the deterministic architecture core.
- [ ] Carry explicit units and coordinate-system metadata.
- [ ] Represent rooms/spaces, walls, openings and furniture as explicit semantic entities when evidence supports them.
- [ ] Preserve program constraints and adjacency information where available.
- [ ] Distinguish resolved layout from design intent.
- [ ] Keep render/image representation separate from semantic architectural data.
- [ ] Make target/region references inspectable before execution.
- [ ] Use deterministic, loss-aware OAS -> PlanModel conversion.
- [ ] Never silently discard unsupported OAS fields; preserve as extensions or mark UNKNOWN.
- [ ] Validate units, coordinate system, geometry, topology and element identity during conversion.
- [ ] Use Golden DWGs as regression evidence.
- [ ] Keep future IFC/OpenBIM adapters behind the same interoperability boundary.
- [ ] Keep IDS information validation separate from geometry/topology validation.

## Stage mapping
### H77 Change Proposal
- [ ] Geometry-bearing proposals carry units/coordinate metadata.
- [ ] Proposal targets/regions are inspectable.
- [ ] Semantic target types align with PlanModel, not image-only coordinates.
### H78 Conflict Detection
- [ ] Detect unit/coordinate mismatches as conflicts.
- [ ] Detect conflicts with protected semantic elements.
### H79 ApprovedChangePlan
- [ ] Approved plan records explicit targets/regions and coordinate context.
- [ ] Approval boundary remains deterministic and separate from execution.
### H80 Controlled Editing Contract
- [ ] Editing contract consumes reviewable semantic targets, not raw pixels alone.
### H81 DWG Controlled Editing Runtime
- [ ] Add OAS adapter only if it improves interoperability.
- [ ] Perform deterministic loss-aware mapping.
- [ ] Preserve unsupported fields/UNKNOWN.
- [ ] Validate units/coordinates/geometry/topology/identity.
### H82 Post-Edit Diff
- [ ] Compare semantic and geometric changes, not only pixels.
- [ ] Compare protected-element invariants.
### H83 Post-Edit Validation
- [ ] Revalidate coordinate system, topology, identity and protected constraints.
### H84 Golden DWG End-to-End
- [ ] Run against bagheri7.dwg.
- [ ] Run against afifiiiii.end.edit3.dwg.
- [ ] Record evidence and deterministic diffs.
### Future IFC/OpenBIM
- [ ] IFC remains an adapter.
- [ ] IDS remains information validation, separate from geometry validation.

---

# 2. SALI-FP — Evidence-gated parsing
- [ ] Preserve source evidence separately from derived geometry.
- [ ] Preserve semantic interpretation separately from edit authorization.
- [ ] Require traceable evidence before a visual/CAD observation becomes an editable architectural fact.
- [ ] Use evidence-gated revision concepts in post-edit validation.
Target stages: H77-H83, H85-H86.

# 3. PolarSym — Geometry-aware CAD constraints
- [ ] Preserve orientation where evidenced.
- [ ] Preserve distance constraints where evidenced.
- [ ] Preserve alignment constraints where evidenced.
- [ ] Preserve symmetry only when evidenced.
- [ ] Treat topology/connectivity as explicit validation inputs.
- [ ] Feed geometric invariants into ConstraintMap / ImpactAnalysis / PostEditDiff.
Target stages: H73, H78, H81-H85.

# 4. RePlan — Plan-then-execute
- [ ] Keep explicit plan before execution.
- [ ] Keep reviewable regions/targets.
- [ ] ApprovedChangePlan remains the execution authorization boundary.
- [ ] Never let a model/editor mutate source directly.
Target stages: H77-H81.

# 5. PhysEdit — Physical consistency
- [ ] Treat physical/structural invariants as post-edit validation requirements where applicable.
- [ ] Separate visual plausibility from architectural validity.
Target stages: H80-H86.

# 6. buildingSMART IDS / IFC
- [ ] Keep IFC outside the canonical core via an adapter.
- [ ] Use IDS for machine-interpretable information requirements when IFC becomes active.
- [ ] Keep IDS information validation separate from geometry validation.
- [ ] Preserve schema/version/provenance for IFC/IDS adapters.
- [ ] Use deterministic validation and model-vs-model diff where applicable.
Target stages: future IFC/OpenBIM track; architecture prepared during H81-H90.

# 7. IfcOpenShell
- [ ] Evaluate as an open-source IFC parsing/geometry/validation adapter when IFC work begins.
- [ ] Reuse ifctester/IDS/BCF capabilities only behind explicit adapter boundaries.
- [ ] Validate units, identity, topology and schema/version on import/export.
Target: future IFC/OpenBIM track.

# 8. AFPlan
- [ ] Keep raster/image floor-plan evidence path distinct from vector/CAD evidence.
- [ ] Use as research inspiration, not canonical architecture logic.
- [ ] Preserve evidence provenance if any compatible detector is adopted.
Target: H81-H86 / detector research.

# 9. dwg-bim_AI
- [ ] Keep DWG/vector interpretation distinct from raster interpretation.
- [ ] Evaluate useful segmentation/vectorization ideas without coupling them to the core.
- [ ] Preserve DWG/IFC conversion as explicit adapters.
Target: H81-H84 / future IFC.

# 10. MeshForge and related conversion research
- [ ] Treat DWG/DXF -> segmentation -> 3D as research inspiration only.
- [ ] Do not let 3D conversion replace semantic PlanModel.
- [ ] Preserve source geometry and provenance through conversion if adopted.
Target: post-MVP / 3D track.

# 11. Research governance
- [ ] Every new external research search gets a durable entry here or in the dated research update.
- [ ] Every finding receives an explicit H-stage mapping.
- [ ] Every implemented finding gets CI evidence before being marked implemented/verified.
- [ ] Research files remain versioned in Git.
- [ ] Before starting a mapped H stage, inspect this checklist and apply only relevant items.
- [ ] After each mapped stage, update the corresponding checkboxes and PROJECT_STATE/MASTER_HANDOFF.
- [ ] Never rely on chat memory alone for research requirements.

## Primary research record
- `docs/research/2026-10-02-architecture-ai-research-update.md`
- `docs/research/RESEARCH_INTEGRATION_ROADMAP.md`

## Golden regression artifacts
- `test-assets/golden-projects/bagheri7.dwg`
- `test-assets/golden-projects/afifiiiii.end.edit3.dwg`
