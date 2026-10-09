# Architectural Book Review — Evidence Map

**Status:** Initial content review. This is not a claim that every page and drawing has been fully audited.
**Purpose:** Extract traceable, testable architectural-plan knowledge for Architecture AI Agent. The PDFs remain reference sources; they do not become executable rules automatically.

## Review principles
- Preserve the original PDFs in the user's Library. This document records findings, not replacement copies.
- Attach source title, edition/year when known, PDF page and printed page when available to every extracted rule.
- Separate drafting conventions from binding/current requirements. Older books help decode drawing language; legal/regulatory claims must be verified against current official sources.
- Uncertain symbols, dimensions, levels, stair direction/count, section markers and geometry must not become authoritative PlanModel data without adequate evidence.
- Keep the canonical chain: source evidence → semantic candidate → PlanModel → ConstraintMap → Impact/Rules → validated proposal. Do not create a second semantic graph.
- This research document alone changes no runtime behavior or acceptance gate.

## Sources reviewed

### 1. مبانی نقشه‌کشی معماری — پایه دهم، نسخه ۱۴۰۵–۱۴۰۶ (Rasanika)
**Status:** Previously reviewed at a high level; selected topics identified, not a full page-by-page audit.
Useful topics: line types (including thick/dashed lines and axes), walls, floor plans, elevations and sections, roof slope arrows/percentages, drainage, elevation levels, grid/axis interpretation and relationships between roof plan and section.
**Mapping:** Iranian Drawing Language / Semantic & Drawing Evidence; roof/level/section evidence; drafting-symbol recognition tests.
**Caution:** Each item needs a source-backed candidate and test; examples are not automatically universal.

### 2. اصول نقشه‌کشی و نقشه‌خوانی ساختمان ۱ (سازه و معماری) — نوید سلیمانی‌پور، ۱۳۹۶
**Length:** 48 PDF pages. The file identifies itself as volume 1, “سازه و معماری,” and includes construction details and photographs.
**Status:** Initial text/index review, not a complete visual audit.
Contents identified: plan definitions and types, scale and drawing-sheet conventions; common building symbols; walls/columns, doors, windows, closets, level differences, ducts and north arrow; space labels and plan titles; internal/external dimensioning; sections, section lines, hatching and section scales; stair terminology and geometry (risers, treads, run, slope, path line, headroom, landing, railing and labels); structural details including concrete/steel topics and foundation/rebar plan examples.
**Mapping:** Drawing-symbol ontology; dimension/scale evidence; section-marker-to-view relations; stair/landing/level interpretation; architectural/structural drawing consistency.
**Limit:** A 2017 reference is useful for drawing vocabulary and recurring conventions, not proof of current code. This file is volume 1; a separate volume 2 for building services is mentioned but is not included here.

### 3. آموزش فاز ۲ در معماری — هنرستان معمار گلد
**Length:** 18 PDF pages.
**Status:** Initial chapter-level review.
The file identifies itself as chapter 12, “ترسیم پلان.” Objectives include explaining the building plan, recognizing symbols, dimensioning a plan and drawing a one-storey plan. It distinguishes preliminary designs, execution drawings and services drawings; covers plans/section planes, vertical sections, elevations and details; and notes that each non-identical floor generally needs its own plan.
**Mapping:** Plan/section/elevation/detail view types; floor identity and typical-floor reuse only when evidence supports equivalence; dimensioning and symbol fixtures; drawing-set completeness.
**Limit:** Short extract, not a complete book.

### 4. روش تهیه نقشه فاز ۲ معماری — فایل با نام «معمار گلد»
**Length:** 31 PDF pages.
**Status:** Initial index/snippet review; further visual/content verification needed.
The extracted content describes an execution-drawing checklist: floor plans with axes, dimensions, levels, room uses/areas and service-equipment locations; coordination with structural and MEP drawings; stairs, doors/windows and roof information; site plan, roof plan with slopes/drainage coordination, longitudinal/transverse sections, elevations and execution details. Further topics include wall sections, stair details, kitchen/sanitary layouts, door/window schedules, expansion joints, retaining walls/ramps, finish/material schedules and other construction details. Coordination notes mention view labels, axes, levels, door/window types and consistency with site/municipal information.
**Mapping:** Phase-2 drawing-set manifest; plan↔section↔elevation↔roof↔detail↔schedule relations; architecture/structure/MEP coordination warnings; evidence checks for axes, dimensions, levels, slopes and door/window types.
**Limit:** Treat items as candidates. Verify numerical thresholds and regulatory claims against current authoritative sources.

### 5. faz2-www.archline.ir_.pdf
**Length:** 31 PDF pages.
**Status:** Initial text/index review.
Extracted topics include floor-finish/build-up alternatives, roof build-ups, façade finish cases and technical-detail categories. The text structure strongly overlaps with source 4, but exact duplicate identity has not been proven.
**Mapping:** Same phase-2 completeness and cross-view coordination lane as source 4.
**Next verification:** Compare title/credits, page images and content fingerprints before merging the records as duplicates. Preserve both separately until then.

### 6. طراحی معماری — پایه یازدهم/دوازدهم کاردانش, code 311122
**Length:** 232 PDF pages. Bibliographic metadata identifies Parastoo Aryan-Nejad and the official vocational textbook publication office.
**Status:** Initial bibliographic and table-of-contents review.
Contents include design process/programming; functional zones in a dwelling; human scale, spatial dimensions/proportions; spatial relationships, movement and circulation; house volume/elevation, roofline and external influences; site/context analysis, climate, topography/slope, access, soil and natural/man-made site features; residential design-related requirements for façade, open/semi-open spaces, parking, services, stairs, doors/windows, internal dimensions and daylight; residential lighting; office and commercial design.
**Mapping:** Spatial relation/circulation semantics for PlanModel; room adjacency/accessibility candidates; site/context constraints; traceable rule-layer candidates for light, stairs, doors/windows and space dimensions.
**Limit:** Primarily a design-planning reference, not a phase-2 drafting standard. Regulatory content is historical until checked against current official requirements.

## Cross-source implementation candidates
1. **Drawing vocabulary:** candidate classes for wall, column, door, window, closet, duct, north arrow, level difference, stairs, section/elevation markers, axes and dimensions.
2. **View relations:** explicit links among floor plans, sections, elevations, roof/site plans, details and schedules. Missing a view is not proof that the underlying element is absent.
3. **Phase-2 completeness:** expected fields per drawing type, including view title, floor identity, scale when available, axes, dimensions, levels, room labels, door/window types, slopes, material notes and detail references.
4. **Cross-view consistency:** compare features across plan/section/elevation/roof/detail; contradictions become NEEDS_REVIEW, not automatic correction.
5. **Stairs and levels:** infer count/direction/landing/level changes only from sufficient, consistent evidence; otherwise retain UNKNOWN or SOURCE_REQUIRED.
6. **ConstraintMap:** candidate geometry/dimensions never unlock protected columns, outer boundary, walls, doors, windows or overall plan form. Existing lock policy remains authoritative.
7. **Traceability:** each candidate should record source_id, title/edition, PDF page, printed page if available, excerpt/figure, confidence, drawing type, rule-vs-convention classification and validation status.
8. **Tests:** only add fixtures grounded in legible source examples. Include positive, ambiguous, missing-view, contradictory-view and wrong-scale/unit cases. No PASS on absent evidence.

## Source-to-project matrix

| Knowledge area | Best source(s) | Target project area | Validation direction |
|---|---|---|---|
| Symbols, dimensions, scale | Principles of drawing/reading; grade-10 drafting | Semantic/Drawing Evidence | Labeled symbol/dimension fixtures |
| Sections, hatching, view direction | Principles; phase-2 lesson | View relations / evidence provenance | Section marker ↔ section-view tests |
| Stair geometry and vertical circulation | Principles; phase-2 references | PlanModel / relations / levels | Ambiguous stair/level tests; fail closed |
| Phase-2 set completeness | Phase-2 method; Archline file | Drawing-set manifest / validation | Missing view/schedule tests |
| Roof slopes, levels, drainage | Grade-10 book; phase-2 method | Roof/level semantics | Arrow, slope, elevation and cross-view tests |
| Room function, adjacency, circulation | Design Architecture textbook | Spatial relation model | Adjacency/accessibility candidate tests |
| Site slope, context, climate | Design Architecture textbook | Site/context input layer | Keep distinct from plan-only evidence |
| Regulations | Design Architecture and phase-2 references | Traceable Rule layer | Re-verify against current official sources |

## Initial feature-to-file-to-test map

This map ties research candidates to existing repository anchors on the main snapshot used by this research branch. It is a routing map, not a claim that every feature is complete or fully validated.

| Candidate feature | Existing canonical file(s) | Existing test anchor(s) | Current limitation / safe interpretation |
|---|---|---|---|
| Drawing symbols, text, dimensions, levels, section/elevation markers and hatch | runtime/drawing_semantic_evidence.py | tests/test_h100_semantic_evidence.py | Candidate evidence only; preserve source binding and UNKNOWN/NEEDS_REVIEW where corroboration is missing |
| DWG-native semantic evidence | runtime/dwg_semantic_evidence.py, runtime/dwg_evidence_bridge.py | tests/test_dwg_semantic_evidence.py, tests/test_dwg_evidence_bridge.py | Native CAD cues do not by themselves prove architectural meaning |
| Scale and units | runtime/scale_unit_evidence.py | tests/test_scale_unit_evidence.py | PASS requires a verified unit and adequate evidence; do not infer a ratio from scale labels alone |
| Geometry and space topology | runtime/geometry_topology_validation.py, runtime/spatial_topology.py | tests/test_spatial_topology.py | Bounding-box overlap alone is not adjacency or a valid room boundary |
| Architectural relations / opening connectivity | runtime/architectural_relations.py, runtime/opening_connectivity.py | Existing relation and opening-connectivity tests | Relation claims must stay evidence-linked; incomplete links remain unresolved |
| Canonical PlanModel and BIM-to-ConstraintMap boundary | runtime/plan_model_contract.py, runtime/bim_constraintmap_contract.py | tests/test_bim_constraintmap_contract.py | Do not create a second PlanModel or unlock protected elements from book examples |
| Drawing-standard/rule interpretation | runtime/drawing_standards_validation.py, runtime/rule_context.py, runtime/rule_engine.py | tests/test_drawing_standards_validation.py, tests/test_drawing_standards_rule_pack.py | Historical educational statements are not current regulatory authority |
| Golden understanding / regression | runtime/golden_understanding_runner.py, runtime/golden_dwg_regression.py | tests/test_golden_understanding_runner.py, tests/test_golden_dwg_regression.py | Golden source assets are preserved; any new fixture must have source provenance and a reproducible expected decision |

## Next work
1. Review remaining pages/figures in phase-2 sources and compare the two 31-page files for duplication.
2. Inspect page images where OCR is unreliable, especially symbols, line conventions and details.
3. Verify each matrix row against the current main branch before creating runtime fixtures; some test anchors are broader suites rather than one feature-specific test.
4. Implement only the smallest evidence-backed fixtures on an isolated branch; run exact-head real CI, Runtime and Bug Hunt.
5. Update PROJECT_STATE.md only with verified repository/test facts. H100 remains active; this research does not unlock H101.
