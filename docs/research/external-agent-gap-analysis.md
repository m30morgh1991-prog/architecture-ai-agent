# External Architecture-Agent Gap Analysis

Date: 2026-10-08

## Purpose

Evaluate external open-source projects/agents that can strengthen Architecture AI Agent without replacing its provider-neutral, fail-closed architecture.

Decision rule:
- reuse ideas/contracts/patterns where they improve a concrete gap;
- do not make an external project the Source of Truth;
- do not add a mandatory runtime dependency unless a later stage proves it necessary;
- respect each project's license before copying code, models, datasets, or generated artifacts;
- preserve the architecture: Evidence -> Semantic Candidate -> PlanModel -> ConstraintMap -> ImpactAnalysis -> Rules -> ApprovedChangePlan -> Controlled Editing -> PostEditDiff -> Validation -> Audit.

## Highest-value projects reviewed

### 1. ConstructDrawingAI

Repository: https://github.com/A-SHOJAEI/ConstructDrawingAI

Useful concepts:
- Canonical Intermediate Representation (CIR) shared across ingestion, perception, grounding, engines and agent layers.
- PDF / DWG-DXF / IFC / image ingestion boundary.
- Symbol/component detection plus connectivity graph extraction.
- Grounding detections to IFC / classification concepts.
- Source-linked confidence for extracted values.
- Evaluation on real held-out drawing datasets with explicit metrics.

Architecture relevance:
- Strong reference for strengthening Evidence -> Semantic Candidate.
- Connectivity graph ideas are relevant to PlanModel relations/topology.
- CIR is conceptually similar to a normalized intermediate layer, but our PlanModel remains the project Source of Truth.

Adoption decision:
- ADOPT AS DESIGN REFERENCE, not as a dependency.
- Reuse concepts only after independent contract design and license review.
- Do not copy code/models/datasets into the project under the repository's current noncommercial license.

License note:
- Repository code is PolyForm Noncommercial 1.0.0; commercial use requires a separate license.
- Upstream datasets/models have separate licenses.

### 2. OpenTakeoff

Repository: https://github.com/kentucky-ai/opentakeoff

Useful concepts:
- One engine shared by human and agent workflows.
- 40 MCP tools over the same geometry/measurement core.
- Scale is explicit and acts as a gate.
- Measurement records preserve scale, method, source/agent/human provenance and corrections.
- Raster fallback and vector-aware geometry.
- Sheet graph, continuation-sheet references and citation/provenance.
- Explicit refusal/withheld states instead of inventing geometry.
- Agent verdicts are separated from human approval.

Architecture relevance:
- Very strong reference for H100 dimension evidence.
- Strong candidate pattern for Evidence records, provenance, human review, and measurement verification.
- Useful for future quantity/measurement services without contaminating PlanModel semantics.

Adoption decision:
- ADOPT PATTERNS SELECTIVELY.
- Apache-2.0 makes it a comparatively permissive implementation reference, subject to normal attribution/license compliance.
- Do not import its takeoff domain as core architecture.

### 3. Floor Plan Document Intelligence

Repository: https://github.com/alifarzadjamali/floor-plan-document-intelligence

Useful concepts:
- Reproducible raster floor-plan pipeline.
- Room/wall/door/window segmentation.
- OCR and structured JSON output.
- Conservative spatial links.
- Review-aware output.
- Dataset audit, held-out evaluation, robustness checks and frozen inference evidence.

Architecture relevance:
- Strong reference for Image/PDF -> candidate evidence.
- Useful for separating perception output from semantic truth.
- Review-aware JSON maps naturally to UNKNOWN / NEEDS_REVIEW.

Adoption decision:
- ADOPT AS RESEARCH REFERENCE.
- Code is MIT.
- CubiCasa5K and other data have separate licenses; do not assume dataset rights from repository code license.
- Small/young project; use it for techniques and evaluation discipline rather than as a production dependency.

### 4. HarnessBIM

Repository: https://github.com/ReverseZoom2151/harnessbim

Useful concepts:
- Backend-neutral BIM abstraction.
- Canonical IFC representation.
- Verification-first loop.
- Schema/IDS/clash/structural/MEP/egress/relationship checks.
- Human-in-the-loop gates.
- Checkpointed agent state.
- BCF issue feedback.
- Local/open-weight model path.

Architecture relevance:
- Strong reference for future BIM validation and Rule/Validation orchestration.
- Reinforces the project's existing separation between semantic planning and backend execution.
- Useful pattern for turning validation into an explicit machine-checkable gate.

Adoption decision:
- ADOPT AS ARCHITECTURE REFERENCE.
- Do not introduce its multi-agent generation pipeline into MVP.
- Extract verification/gate concepts when the repository reaches the relevant Rule/Validation stages.

### 5. AutoCAD-MCP

Repository: https://github.com/U-C4N/Autocad-MCP

Useful concepts:
- Typed capability contract over live AutoCAD and headless ezdxf engines.
- Capability discovery rather than exposing a huge tool catalog blindly.
- Drawing preflight -> plan -> critique -> refine -> finalize quality loop.
- Dimension/measurement validation.
- Drawing diff and delivery/reopen-parity concepts.
- Transactions/rollback.
- Explicit capability keys and refusal defaults.
- Token-efficient discovery mode.

Architecture relevance:
- Directly strengthens the previously registered YQArch/AutoCAD Adapter boundary.
- Supports the Architectural Capability Registry concept.
- Drawing quality loop is useful for Controlled Editing -> PostEditDiff -> Final Validation.
- Capability discovery pattern is useful for provider-neutral backends.

Adoption decision:
- ADOPT PATTERNS.
- MIT licensed.
- Do not expose raw backend commands to the model.
- Keep AutoCAD as an adapter, not PlanModel Source of Truth.

### 6. Bonsai MCP

Repository: https://github.com/Show2Instruct/bonsai-mcp

Useful concepts:
- Local MCP bridge to Blender + Bonsai + IfcOpenShell.
- Read-only IFC queries separated from edit tools.
- Spatial structure, quantities, property sets and viewport verification.
- Local-only bridge and structured tool results.

Architecture relevance:
- Future BIM/IFC runtime adapter candidate.
- Useful for Visual Runtime and IFC inspection.
- Strong reminder that arbitrary code execution must stay outside the model-facing safe boundary.

Adoption decision:
- FUTURE ADAPTER CANDIDATE, not MVP dependency.
- MIT licensed.
- Never expose arbitrary Python/Blender execution as an unrestricted model capability.

## Feature-to-file / stage mapping

| External finding | Project capability | Target stage/layer | Adoption |
|---|---|---|---|
| CIR / connectivity graph | normalized evidence + relations | H100/H101 Plan Understanding | Design reference |
| Source-linked confidence | evidence provenance | H100 Evidence | Adopt pattern |
| Explicit scale gate | dimension/measurement evidence | H100 | Adopt |
| Human vs agent provenance | review/audit | H100+ | Adopt |
| Review-aware JSON | fail-closed status propagation | H98/H100 | Adopt |
| Room/wall/door/window perception | candidate detection | Plan Understanding | Research reference |
| IFC grounding | BIM semantic identity | H98/H101+ | Adopt concept |
| Backend-neutral BIM interface | provider neutrality | BIM layer | Adopt concept |
| Verification checker suite | deterministic validation | Rules/Validation | Future |
| BCF issue feedback | structured conflict/result reporting | Conflict/Validation | Future |
| AutoCAD capability registry | controlled backend execution | Controlled Editing | Adopt concept |
| Transaction/rollback | execution safety | Controlled Editing | Future |
| Drawing preflight/critique | post-edit validation | Diff/Validation | Future |
| Sheet graph/cross-sheet citation | drawing-set context | Evidence/Plan Understanding | Future |
| Vertical circulation semantics | stairs/levels/landings | PlanModel | Future |
| Viewport verification | visual runtime evidence | Visual Runtime | Future |

## New explicit gaps confirmed

1. Evidence graph / source linkage
   - We have evidence-backed annotations, but external work suggests a stronger general-purpose graph connecting evidence -> candidate -> semantic entity -> source sheet/region.

2. Measurement provenance
   - H100 has deterministic dimension semantics; next refinement should preserve measurement method, scale/calibration evidence, geometry reference, source region and reviewer/agent provenance.

3. Connectivity/topology contract
   - Relations need to become first-class enough to support wall-hosted doors/windows, room adjacency, openings, circulation and drawing-set references.

4. Capability discovery
   - Controlled Editing needs a backend-neutral capability registry that can answer what an adapter can safely do before dispatch.

5. Runtime transaction and verification
   - Dispatch/completion must remain distinct from verified success; rollback and post-edit parity should become explicit future contracts.

6. Drawing-set graph
   - Continuation sheets, detail markers, section/elevation references, schedules and callouts should eventually form a queryable graph.

7. Verification as an engine
   - Future validation should be machine-checkable and evidence-producing, not just an LLM judgement.

8. Vertical circulation
   - Stair/level evidence should eventually model storey height, riser, tread, flight, landing, direction and required step count, including plan/section evidence.

## Non-adopted / intentionally excluded

- No external project becomes Architecture AI Agent Source of Truth.
- No mandatory ConstructDrawingAI dependency because of its current noncommercial license and different product boundary.
- No arbitrary AutoLISP / arbitrary AutoCAD command exposure.
- No arbitrary Blender/Python execution from the model-facing boundary.
- No automatic conversion of layer names into semantic truth.
- No replacement of PlanModel with an external CIR/IFC schema.
- No full BIM runtime dependency in MVP.
- No immediate multi-agent generation framework before the understanding/validation gates are mature.

## Recommended implementation order

1. Finish and verify H100 gates.
2. Fold the confirmed evidence/provenance gaps into the next repository-derived stage.
3. Strengthen Relations/Topology before expanding generation.
4. Build the Architectural Capability Registry before Controlled Editing.
5. Add deterministic validation and post-edit evidence before increasing execution power.
6. Introduce IFC/BIM runtime adapters only behind the existing provider-neutral boundary.

This document records research/design decisions only. It does not by itself make a stage GREEN.
