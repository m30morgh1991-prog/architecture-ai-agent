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


## Additional DWG engine and browser viewer candidates — 2026-11-15

A second source-checked pass found a more directly relevant native DWG/DXF library and two optional viewer/application candidates. These are research findings only; no dependency, code, drawing, or Golden fixture has been imported.

### 1. hakanaktt/acadrust — strongest new conversion-engine pilot candidate

- Upstream: https://github.com/hakanaktt/acadrust
- Current upstream release observed: v0.6.8; latest repository push observed 2026-11-15.
- License declared by the upstream repository and Cargo.toml: MPL-2.0 (not MIT).
- Pure-Rust library exposing native binary DWG and ASCII/binary DXF read/write APIs without requiring AutoCAD. Upstream documents R12–R2018+ format coverage, 48 top-level entity variants, optional failsafe diagnostics, and configurable Rayon concurrency.
- This is materially more relevant to a headless DWG→DXF backend than an AutoCAD UI/MCP server. A narrow isolated Rust adapter could read with DwgReader and write DXF directly with DxfWriter, avoiding a full intermediate DXF text buffer. This is a hypothesis to test, not a verified performance result.
- Entity/version support is not equivalent to lossless fidelity. The library's own documentation says entity availability varies by version. The MPL-2.0 notice and third-party DWG code provenance must be reviewed before distribution.

**Decision:** promote to P1 for a read-only conversion pilot, not a mandatory dependency. Pin exact crate version and checksum. First test synthetic fixtures, then owner-approved copies of the two Golden DWGs. Record input/output SHA-256, DWG version, entity/property inventories, unsupported and recovered records, units, memory peak, elapsed time, and independent DXF reopen results. Any skipped or recovered record keeps fidelity UNKNOWN / NEEDS_REVIEW.

### 2. CADCraft — useful integration/CLI reference, not a proven fidelity engine

- Upstream: https://github.com/storytold/cadcraft
- Declared license: MIT OR Apache-2.0; README explicitly labels the application early development.
- Provides cross-platform Rust desktop/CLI/MCP workflows and uses acadrust for DWG input/output. Its current bridge converts DWG to an in-memory DXF byte buffer and then parses that DXF into its own document model.
- Its own file-format parity document says the review used no real third-party file and that unsupported objects can be dropped on save. It identifies R13/R14 as untested and R2018+ real-file reads as untested.
- A public performance report for a 47.8 MB DWG measured 16–28 seconds and 4.54 GB maximum resident memory on an Apple M1 Pro; the report attributes much of the overhead to holding a 276 MB intermediate DXF text buffer before parsing. This is evidence about CADCraft's bridge path, not proof that direct acadrust DwgReader→DxfWriter use has the same overhead.

**Decision:** reuse only CLI/MCP capability-discovery and test-harness ideas. Do not adopt the full desktop app or its intermediate-DXF bridge. Our pilot should test direct document-to-writer conversion and explicitly measure peak memory on large files.

### 3. HakanSeven12/OpenCADStudio — technically interesting, license-incompatible by default

- Upstream: https://github.com/HakanSeven12/OpenCADStudio
- Declared license: GPL-3.0. README describes native DWG/DXF read/write (R14–2018), headless conversion, and a JSON/MCP automation endpoint.
- It is a large, active 2D/3D CAD application and uses acadrust as a core engine. Its broader application scope and GPL-3.0 license make it unsuitable as a default embedded dependency for our provider-neutral, commercializable 2D agent.

**Decision:** inspect as an external reference or separately launched optional tool only. Do not copy code or bundle it into the MVP without an explicit license/product decision.

### 4. MLightCAD — promising optional tablet/browser viewer, not our DWG conversion backend

- Upstream: https://github.com/mlightcad/cad-viewer
- Main viewer/data-model packages are MIT-licensed and DXF parsing is built in. DWG loading is opt-in through a separate LibreDWG-based WebAssembly worker package licensed GPL-3.0.
- Upstream documents limitations in the open-source DWG path: incomplete entity coverage, larger bundle, slower startup, high memory use, and possible out-of-memory errors on large drawings. A separate proprietary parser is offered, so it is not part of the free/open-source path.

**Decision:** keep as a P2 candidate for a future read-only browser viewer on Android/tablet, initially with DXF only. Do not add its GPL DWG worker to the product until distribution/licensing and mobile memory tests are resolved. The viewer is not a replacement for our conversion or validation engine.

### 5. dwgdxf WASM wrapper and additional AutoCAD MCP candidate — do not adopt yet

- https://github.com/ducflair/dwgdxf advertises a browser/server DWG→DXF wrapper around acadrust, but the repository metadata reports no asserted license, the README describes acadrust as MIT while the current acadrust project declares MPL-2.0, and the wrapper's latest observed push was 2026-07-02. This license mismatch and maintenance gap block adoption pending clarification.
- https://github.com/thewisekape/autocad-mcp is Apache-2.0 and describes File IPC, COM and ezdxf backends, but its latest observed push was 2026-04-05 and it has a small public footprint. It is not a stronger candidate than the already evaluated U-C4N/Autocad-MCP project.

### Updated implementation sequence

1. Finish the exact-head provenance correction and DXF comparator CI in PR #143.
2. Keep the open geometry/research PRs under review; do not let a CAD-engine pilot modify PlanModel, ConstraintMap, ApprovedChangePlan, BIM semantics, or H101.
3. Create an isolated acadrust pilot harness with a pinned MPL-2.0 dependency and no production routing. Compare direct DwgReader→DxfWriter against the current ODA/LibreDWG routes where legally and technically available.
4. Add resource limits, timeouts, cancellation, temporary-output isolation, atomic output promotion, and post-conversion validation. Never trust exit code alone.
5. Run synthetic tests first. Run Golden DWG tests only read-only and only when the workflow has access to the fixtures. Real AutoCAD/Windows host tests remain NOT_RUN until the user confirms the Windows environment is restored.
6. Adopt only after entity-by-entity coverage, real-file round trips, memory/time limits, license review, and fail-closed reporting pass independently.

No candidate in this section is approved as the production conversion provider. PlanModel remains canonical; converter output remains untrusted evidence until independently validated.


### acadrust upstream CI snapshot — 2026-11-15

The current upstream `hakanaktt/acadrust` main commit observed during this review is `52034a673ff59bf6936ebf01ec794b07a97df246`. All ten reported check-runs on that exact upstream SHA completed successfully: Rust analysis, Python/Actions/C# analysis, Ubuntu tests, Windows tests, macOS tests, FreeBSD aarch64/x86_64 checks, and WebAssembly checks.

This is a positive maintenance signal for a pilot candidate, but it is **upstream CI only**, not our own integration, entity-fidelity, Golden DWG, memory, or conversion-roundtrip evidence. The upstream README also notes that tests requiring drawing files not present in the repository are ignored unless the user supplies those fixtures. Our pilot must therefore use independently controlled synthetic and Golden fixtures and report skipped coverage explicitly.


### Existing Golden fixture baseline: ezdwg conversion is currently rejected — 2026-11-15

The live PR #131 workflow `Golden DWG to DXF Fidelity Test` run #24 (run ID `43270191429`) was inspected on PR head `d4231b5c68be56e737977c1b909fb3a05607ae0d`. It completed/failure for the correct reason: the generated DXF files do not preserve the Golden source entity inventory.

- For `bagheri7.dwg`, the source modelspace contains 8,842 LINE entities, while the `modelspace_only=True` conversion output contained only 2 LINE entities. Other source categories were also lost.
- For `afifiiiii.end.edit3.dwg`, the source includes 72,447 LINE, 8 DIMENSION, 141 HATCH, 151 INSERT, 70 LWPOLYLINE, 14 MTEXT, and 85 TEXT entities; the conversion output contained only two HATCH entities.
- The adapter reported zero skipped entities because it only counted the tiny selected export set; independent source-vs-output counts exposed the much larger mismatch. This is exactly why source-side inventory and independent reopen checks are mandatory.
- The strict native DWG writer probe was BLOCKED on both files because block XDATA, preview, extension-dictionary, and (for Bagheri7) Xref metadata could not be preserved.
- Both original DWG SHA-256 values matched before and after; the source fixtures were not modified.
- Overall report: `NEEDS_REVIEW`; native writer overall status: `BLOCKED`. No lossless-conversion claim is justified.

**Decision update:** retain ezdwg as a read/inspection experiment only; reject its current Golden DWG→DXF and native DWG write paths as production conversion providers. Do not weaken the failed Golden gate to obtain green CI. Use these two immutable fixtures as the baseline for the isolated acadrust pilot in issue #145, and require the same independent entity/property/hash checks.
