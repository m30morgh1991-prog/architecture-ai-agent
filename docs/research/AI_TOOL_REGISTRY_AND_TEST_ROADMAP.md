# AI Tool Registry and Stage-Gated Evaluation Plan

**Status:** Consolidated research inventory and future test plan; not an implementation decision.  
**Consolidated:** 2026-11-21

## 1. Product goals and active scope

The active priority is accurate 2D architectural-plan understanding, generation, editing, alternatives, and professional presentation. The user explicitly deprioritized 3D modeling, rendering, and maquette/model-making.

Eight active capability groups:
1. Plan understanding and geometry extraction.
2. Plan generation from scratch.
3. Existing-plan editing and redesign.
4. Alternatives and optimization.
5. Architectural plan presentation and sheet production.
6. 2D plan graphics and illustration.
7. Agents and automation.
8. CAD, BIM, and engineering.

Core rules:
- PlanModel + ConstraintMap + ApprovedChangePlan remain the source of truth; never a generated image.
- Presentation/beautification must preserve approved geometry, dimensions, walls, columns, openings, and plan form.
- Fail closed: UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW / ABSTAIN / BLOCKED never become PASS without evidence.
- Distinguish documentation review, installation, functional test, repeatable acceptance, and production readiness.
- External tools are candidates, not authorities for Iranian regulations or substitutes for custom architectural understanding.
- Check licenses, dataset terms, offline feasibility, hardware, API dependency, privacy, editability, and exports before adoption.
- Prefer low-cost/open-source, provider-neutral, tablet-friendly, low-hardware and degraded-internet-compatible options.

## 2. Candidate registry

Status key: **Research noted** = prior documentation/repository review, not a current hands-on test; **Test candidate** = shortlist when its stage arrives; **Reference** = dataset/method, not a ready product; **Early/uncertain** = maturity/license/access requires recheck.

### 2.1 Plan understanding and geometry extraction

| Candidate | Known role | Status / caution |
|---|---|---|
| [FloorPlanNet](https://github.com/thatguywhodoestecheverysatnight/FloorPlanNet) | Segmentation/vectorization; SVG, DXF, GeoJSON | Test candidate; synthetic-domain claims do not prove real-plan accuracy; inspect maturity/license |
| [Raster-to-Graph](https://github.com/SizheHu/Raster-to-Graph) | Junction and wall-segment detection; graph reconstruction | Test candidate; research code, older dependencies/CUDA and dataset access |
| RedrawAI | Raster/PDF segmentation, wall reconstruction, doors/windows, DXF | Research noted; geometry fidelity/manual correction and license need testing |
| [Neural Floorplan](https://github.com/daegeun-kim/neural_floorplan) | SegFormer + Raster-to-Graph | Research noted; reported results modest; verify before relying |
| [FloorplanTransformation](https://github.com/art-programmer/FloorplanTransformation) | Junction heatmaps + integer-programming vectorization | Algorithmic reference; legacy dependencies |
| [AI Floor Plan to CAD File Generator](https://github.com/spanwair/AI-floor-plan-to-CAD-file-generator) | Raster-to-DXF using detection, morphology, OCR and geometry libraries | Early/uncertain; orthogonal limitations, external API, license unclear |
| JMU Architectural Design Assistant | Plan → scene graph → GNN/LLM → validation → SVG/DXF | Research prototype |
| [FloorPlanCAD](https://floorplancad.github.io/) | Real CAD-plan dataset and object annotations | Dataset reference; non-commercial terms/source rights |
| [CubiCasa5K](https://github.com/CubiCasa/CubiCasa5k) | Annotated floor-plan dataset with SVG labels | Dataset reference; verify data terms |
| [CAGE](https://arxiv.org/abs/2509.15459) | Point-cloud density maps to vector floorplans | Paper candidate; public code/input fit not confirmed |
| dwg-bim_AI | DWG/BIM AI exploration | Early/low priority; previous review shallow |

### 2.2 Plan generation from scratch

| Candidate | Known role | Status / caution |
|---|---|---|
| [Graph2Plan](https://github.com/HanHan55/Graph2plan) | Room-graph and boundary-conditioned generation | Test candidate; older research code |
| [GSDiff](https://github.com/SizheHu/GSDiff) | Vector generation via geometry-enhanced structural-graph diffusion | High-priority research; check weights/data terms and GPU needs |
| [DiffPlanner](https://github.com/shidong-wang/DiffPlanner) | Vector generation with node, adjacency, partitioning diffusion | High-priority research; dependencies/reproducibility |
| [House-GAN++](https://github.com/ennauata/houseganpp) | Relational room-layout generation/refinement | Layout reference; not complete wall/opening engineering |
| DiscreteDiffFloorPlans | Graph diffusion for constrained alternatives | Early/uncertain; GPU and license |
| HypergraphFormer | Access-graph to BSP/hypergraph layouts | Research only; substantial hardware/software likely |
| [Maket AI](https://www.maket.ai/) | Residential plan generation from requirements and options | Commercial test candidate; check current free/paid limits and export rights |

### 2.3 Existing-plan editing and redesign

| Candidate | Known role | Status / caution |
|---|---|---|
| Maket AI | Upload/revise plans; room, wall, door, window edits; DXF/PDF may be paid | Priority practical test; verify actual geometry preservation, not image-like redraw |
| [ChatHouseDiffusion](https://github.com/ChatHouseDiffusion/chathousediffusion) | Text-guided plan generation/editing, UI and pretrained model | Research noted; external LLM API and Windows/Python setup may limit offline use |
| Graph2Plan / JMU assistant | Graph-driven regeneration/editing | Research references; test edit locality |
| Rayon | Design/editing workflow | Product review noted; verify 2D control and export |
| Planner 5D | Plan/design application | Capability investigation started; no completed practical-test claim |
| [Synaps](https://synaps.app) | Editable architectural drawings and plan workflow | Early research; focus only on 2D plan editing/export |

### 2.4 Alternatives and optimization

Candidates: GSDiff, DiffPlanner, Graph2Plan, HypergraphFormer, House-GAN++, DiscreteDiffFloorPlans, Maket AI, ChatHouseDiffusion. Visually different images are not necessarily valid alternatives. Validate dimensions, area, adjacency, circulation, topology, boundary fit, locked constraints, and regulations. Measure diversity separately from validity.

### 2.5 Architectural plan presentation and sheet production — high priority

Test graphic hierarchy, text/dimension/symbol legibility, scale/geometric fidelity, furniture and space differentiation, color/hatching/2D floor finishes, sheet composition/title blocks/legends/schedules, print-ready PDF and high-resolution image export, post-generation editability, and preservation of approved geometry.

Candidates:
- Maket AI — inspect actual plan presentation and editability.
- Adobe Photoshop / Adobe Firefly — 2D graphic refinement; never geometry-authoritative.
- LookX AI / PromeAI — architectural image/plan visualization; strict geometry-preservation test.
- CAD/layout tools — dimensionally accurate annotation, sheets and print output.

### 2.6 2D plan graphics and illustration

Candidates: Stable Diffusion + ControlNet, LookX AI, PromeAI, Adobe Firefly, Leonardo AI, Midjourney, Vizcom. Evaluate local-vs-cloud runtime, hardware, API availability, image-to-image control, legibility, and geometry preservation. These are visual assistants, not geometry sources of truth. RoomGPT, Interior AI, ReimagineHome are lower priority unless a clear 2D plan use case is demonstrated.

### 2.7 Agents and automation

| Candidate | Known role | Status / caution |
|---|---|---|
| Langflow | Visual agent/flow experimentation, API composability | Candidate agent lab; no end-to-end architecture test yet |
| Dify | Agent/workflow orchestration | Compare candidate |
| Teamily | Multi-agent flows, APIs/MCP/REST, files/images, memory | Candidate only; no architectural expertise or constraint authority |
| Make | External workflow automation | Research noted; avoid unnecessary hosted dependencies |
| MCP | Tool/service integration protocol | Integration approach, not an architecture agent itself |
| [Claude Skill repository](https://github.com/Motionsites-AI/claude-skill) | Reusable skill patterns for future web-app/agent work | Preserve for Web App stage; inspect license and adapt selectively |
| Browser Agent | Browser automation/fallback | Reference only; explicit permissions and audit trail required |

### 2.8 CAD, BIM, and engineering

Candidates/references: Autodesk Product Help and AutoCAD-MCP; ArchLang; CAD_IFC_agent; OpenBIM-FloorPlan-AI; YQArch; IFC and DXF. BIM semantics belong in the project's core plan-understanding model; external BIM tools do not replace it. Engineering checks include inch/cm unit mistakes, plotting scale, coordinate frames, layers, blocks/inserts, wall/opening relationships, levels, stairs, sections, and local drafting conventions.

## 3. Shared practical test protocol

Fixed inputs:
1. Hand sketch.
2. Clean/simple plan.
3. Complex plan.
4. Angled/non-orthogonal walls.
5. Furniture-rich plan.
6. Plan with columns/structural elements.
7. Doors/windows and dimensions.
8. Localized request to modify one room.
9. Request for three alternatives.
10. Known units/scale metadata, including inch/cm conversion cases.

Metrics:
- Wall/column/opening precision and recall.
- Room count, room area, topology and opening-to-host-wall relation.
- Geometric deviation, scale and dimension fidelity.
- Edit locality and locked-element preservation.
- Alternative diversity and constraint validity.
- Runtime, peak RAM/VRAM, CPU suitability and setup complexity.
- Offline/degraded-internet behavior and external API dependency.
- Export validity, editability, reproducibility, license and dataset permissions.

Presentation acceptance: improve visual clarity while preserving source geometry, dimensions, scale, and approved annotations. Inspect on-screen output and exported PDF/image at intended print resolution. Attractive but distorted plans fail.

## 4. Stage gates

- Do not install/integrate all candidates now; this registry is preparation only.
- At the matching project milestone, check only material changes (version, license, availability, API, hardware), select a small shortlist, and run identical controlled tests.
- Validate test inputs and ground truth before scoring tools.
- Record documentation review, installation, functional test, and repeatable acceptance separately.
- No candidate becomes a runtime dependency until license, security, offline/hardware feasibility, and regression impact are approved.
- No candidate output overrides PlanModel, ConstraintMap, approved constraints, engineering sources, or human review.
- Preserve failed tests and reasons to prevent unnecessary rediscovery.

## 5. Explicit exclusions

3D modeling, rendering, maquette/model-making, and 3D visualization are not active research categories. Do not test tools whose primary value is 3D output or heavy GPU rendering. **Maquete AI is excluded. Do not confuse Maquete with Maket AI**: Maket remains a 2D plan-generation/editing candidate. Revisit 3D only if the user explicitly changes priorities or a specific 2D presentation capability is independently demonstrated.

## 6. Evidence limitations

This document consolidates prior research notes and user-approved priorities; it is not a fresh verification of every external repository/product on this date. Previous ratings/estimates are not benchmark results and are intentionally omitted. Recheck links, releases, licenses, pricing, dataset access and claims selectively at the actual test stage.

## 7. Related records

- `docs/research/ARCHITECTURE_AGENT_FEATURE_FILE_MATRIX.md`
- `docs/research/INTEGRATED_RESEARCH_CHECKPOINT_2026-10-08.md`
- `docs/research/plan-understanding-research-and-revit-ai-review-2026-10-10.md`
- `docs/research/controlled-architectural-editing-evidence.md`
