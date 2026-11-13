# Open-source AEC / CAD agent landscape review — 2026-11-13

## Purpose and decision

Review open-source projects that may improve Architecture AI Agent after the Autodesk Project Intelligence announcement. This is a research and integration-planning record only. It does not authorize importing code, adding dependencies, changing the canonical model, enabling CAD write access, or advancing an H-stage.

**Decision:** reuse narrow, replaceable capabilities behind existing provider-neutral boundaries. Do not adopt a third-party project as the project brain or as a second semantic source of truth.

The non-negotiable architecture remains:

`Source Evidence → Element Identity → Geometry → Topology → Spatial Relation → Architectural Semantics → BIM Semantics → Rule Context`

Canonical truth remains `PlanModel + ConstraintMap + ApprovedChangePlan`. All uncertain or unsupported claims remain `UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW / ABSTAIN / BLOCKED`.

## Shortlist

| Project | What it provides | License / deployment notes | Fit and decision |
|---|---|---|---|
| [U-C4N/Autocad-MCP](https://github.com/U-C4N/Autocad-MCP) | MCP server for reading, inspecting and editing CAD drawings; live AutoCAD through Windows COM and headless DXF through ezdxf; operation history, checkpoints, dry-run and QA coverage are described in its v1.8 README | Repository LICENSE is MIT. Live COM requires Windows and an installed AutoCAD. Headless DWG opening depends on external conversion tooling; README documents capability refusals when unavailable. README reports a large test suite, but those are upstream claims and not our compatibility evidence. | **P1 adapter pilot candidate**, not a core dependency. First test read-only calls and tool-surface quality on disposable DXF. Do not enable write operations or rely on it for AutoCAD 2020 until independently tested on that exact host. Do not import the whole server. |
| [IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell) / [Bonsai](https://bonsaibim.org/) | IFC parsing, geometry, Python/C++ APIs, IFC conversion, model queries, diffs, clash tools, IDS auditing, and a Blender-based IFC authoring/viewing application | The ecosystem contains distinct packages and licenses (including LGPL and GPL components); inspect the exact package and distribution obligations before bundling. Bonsai is GPL-licensed. It is a substantial optional BIM toolchain, not a lightweight MVP dependency. | **P1 provider-neutral BIM adapter candidate.** Use IFC as an interchange/evidence adapter after PlanModel semantics are stable. Pilot read-only IFC inspection, IDS checks, and model diff in an isolated optional environment. No IFC output is proof of correct plan understanding. |
| [bbl-dres/plan-extract](https://github.com/bbl-dres/plan-extract) | Research pipeline for extracting rooms, attributes, walls, openings, stairs and area data from heterogeneous floor plans; documents CV, graph-based reconstruction, datasets and limitations | Repository code LICENSE is MIT. README labels the project research/demo, not production. Its app uses PyMuPDF (AGPL-3.0); third-party datasets/models have their own terms and some are non-commercial. | **P1 research/evaluation reference**, not a production dependency. Study graph pipeline, evidence and evaluation methodology. Reproduce only with clean-room fixtures or separately licensed data. Avoid its demo app dependency stack. |
| [Jane-o-O-o-O/Agent-CAD](https://github.com/Jane-o-O-o-O/Agent-CAD) | AI CAD workbench, typed CAD IR, revisions, geometry checks, editable DXF/SVG and parametric 3D workflows | MIT. README describes a strict default worker requiring Linux Landlock ABI >= 3 and libseccomp; it does not claim native Windows strict-worker support. It is mainly mechanical/parametric CAD, not architectural plan understanding. | **P2 design-pattern reference only.** Study immutable revisions, typed IR and measured validation. Do not adopt its 3D/mechanical stack for our 2D architecture MVP. |
| [mlightcad/awesome-cad-agent](https://github.com/mlightcad/awesome-cad-agent) | Curated directory of CAD MCP servers, agents, skills and benchmarks | It is an index, not a CAD engine. Each listed project has separate license, maturity and dependency status. | **Research discovery index only.** Use to discover candidates, then verify each upstream repository directly. |

## What is genuinely reusable

### 1. CAD execution adapter patterns

AutoCAD-MCP is the closest practical analogue to an Autodesk-style tool connector. Its most useful patterns for us are:
- typed tool contracts and capability discovery;
- explicit separation of live AutoCAD COM from headless DXF processing;
- read-only inspection separated from mutation;
- dry-run / expected-count guards before bulk changes;
- transaction or checkpoint history and explicit rollback semantics;
- QA coverage that says what was checked and what was not checked;
- bounded tool exposure rather than advertising every tool to the model.

**Integration boundary:** keep the existing provider-neutral AutoCAD-MCP adapter and capability registry. Evaluate upstream MCP tools as an optional external adapter or reference. Do not route LLM-authored raw AutoLISP or arbitrary CAD commands directly to AutoCAD. All writes must remain downstream of `ApprovedChangePlan`, with a disposable drawing, snapshot binding, post-edit diff, and final validation.

### 2. BIM and rule checking

IfcOpenShell provides a mature technical foundation for IFC parsing and geometry; IfcTester/IDS can support machine-readable information-delivery checks. These capabilities can help inspect or validate BIM exchange artifacts.

**Integration boundary:** PlanModel remains canonical. IFC entities and properties are evidence/representations mapped into existing BIM-ready contracts. IFC schema validity, IDS conformance, geometric validity, and architectural/regulatory correctness must be reported as separate outcomes.

### 3. Plan-understanding research

plan-extract is useful because it treats plan extraction as a staged pipeline and documents the difficult areas: vector/raster input, room/wall/opening/stair extraction, graph reconstruction, data provenance, evaluation, and dataset restrictions.

**Integration boundary:** extend existing DrawingEvidence → CandidateFact → PlanModel and topology contracts. Do not introduce another canonical graph. Evaluate walls, rooms, openings and stairs separately, and include topology validity, uncertainty, and human correction cost rather than one aggregate score.

### 4. Revision and verification discipline

Agent-CAD demonstrates useful ideas around typed intermediate representations, immutable revisions, reproducible artifacts and measured geometry checks. Those ideas align with our existing ApprovedChangePlan / PostEditDiff / Audit direction, but its mechanical CAD scope and Linux-specific strict worker make it unsuitable as an MVP runtime dependency.

## Recommended work plan

1. **Now — repository governance:** finish the active geometry PR sequence (#135–#138) and keep the current H-stage gate intact. Do not mix this research into their implementation branches.
2. **Read-only CAD adapter pilot:** on a disposable DXF only, inventory upstream AutoCAD-MCP tools and test a minimal allowlisted subset: drawing info, entity listing, layer listing, dimensions/text inspection, screenshot/export, and structured critique. Record OS, AutoCAD version, DXF version, exact upstream commit, input hash, output hash, and every unsupported capability. No Golden DWG writes.
3. **BIM adapter spike:** in a separate optional environment, read a small synthetic IFC fixture using IfcOpenShell; report schema, entity counts, spatial hierarchy, units, placements, and IDS validation separately. Do not add it to mandatory runtime dependencies yet.
4. **Plan-extraction benchmark review:** extract evaluation categories and build our own small synthetic/adversarial fixtures. No third-party training dataset is imported until artifact-level rights and commercial-use terms are approved.
5. **Decision gate:** adopt only if the pilot demonstrates measurable value, license compatibility, reproducibility, offline/local operation, acceptable resource cost, and no weakening of fail-closed semantics.

## Explicit non-adoption list

- No wholesale AutoCAD-MCP server import or immediate write access.
- No adoption of QCAD-MCP as a core engine because the reviewed workflow depends on QCAD Pro for some conversion/automation functions.
- No use of non-commercial datasets (including AEC benchmark or FloorPlanCAD-derived material) in commercial training or product distribution without separate permission.
- No use of Agent-CAD as an architectural plan interpreter or as a reason to add 3D modeling to the MVP.
- No change to PlanModel, ConstraintMap, ApprovedChangePlan, Golden fixtures, or H100/H101 gates from this research alone.

## Sources reviewed

- AutoCAD MCP Pro README and repository LICENSE: https://github.com/U-C4N/Autocad-MCP
- IfcOpenShell README and ecosystem/package license table: https://github.com/IfcOpenShell/IfcOpenShell
- IfcOpenShell documentation: https://docs.ifcopenshell.org/introduction
- Floor Plan Extraction README and LICENSE: https://github.com/bbl-dres/plan-extract
- Floor Plan Extraction open-solutions review: https://github.com/bbl-dres/plan-extract/blob/main/docs/solutions-open.md
- Agent-CAD README and LICENSE: https://github.com/Jane-o-O-o-O/Agent-CAD
- Awesome CAD Agent index: https://github.com/mlightcad/awesome-cad-agent

## Evidence limits

This is source/README/license-surface research, not a runtime integration test. Upstream feature counts, test counts, performance claims, and compatibility claims have not been reproduced by this repository. License notes are preliminary engineering triage, not legal advice. No external code or dataset has been copied and no runtime dependency has been added.

## Upstream CI and maintenance audit — 2026-11-13

### U-C4N/Autocad-MCP snapshot

- Exact upstream main commit reviewed: `6f6a538255ca9f885232e845ac32f10b4433fe3e`.
- Repository metadata declares MIT; pyproject declares Python >=3.11 and direct dependencies FastMCP 3.x, ezdxf 1.x and Pydantic 2.x. COM is an optional Windows extra; headless DXF is the default alternative.
- Locked CI from 2026-11-06 passed on Linux (Python 3.11/3.12) and Windows (Python 3.11), along with lint/package checks.
- Scheduled floating-dependency CI from 2026-11-09 failed on both Python 3.11 and 3.12: 7,261 passed, 319 skipped, 1 xfailed, 2 failed in each lane.
- Failures: benchmark report pinned expectation mismatch (ezdxf 1.4.5 expected vs 1.4.4 resolved) and nested `pytest.approx` usage in entity property tests.

**Decision update:** retain AutoCAD-MCP as a promising adapter candidate, but downgrade from "pilot-ready without caveat" to **conditional pilot candidate**. Pin upstream commit and all dependencies; do not copy its floating dependency ranges into our core. Our own disposable-DXF compatibility tests are mandatory before adoption. A red floating-dependency lane is a maintenance risk and must remain visible in future reviews.

This audit only observes upstream CI evidence; it does not mean we ran the upstream suite or server ourselves.
