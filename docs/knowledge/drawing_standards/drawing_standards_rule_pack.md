# Drawing Standards Rule Pack — D10/D11 + ISO + نشریه 256

## Purpose
Evidence-backed candidate rules for architectural drawing interpretation and validation in Architecture AI Agent. This pack separates educational foundations from normative sources.

## Authority
1. Binding Iranian regulations / project-specific official requirements
2. Official standards and approved technical publications
3. Educational textbooks
4. General reference books

A rule is NORMATIVE only when its source is authoritative and its applicability/version are known. Otherwise it remains CANDIDATE or EDUCATIONAL and must fail closed for compliance claims.

## Source registry
- ISO-128-1:2020 — general principles and fundamental requirements for technical drawings; applicable to construction and architecture, manual and computer-based.
- ISO-128-3:2022 — views, sections and cuts, including architectural/civil applications.
- ISO-129-1:2018 — general principles for presentation of dimensions and associated tolerances.
- ISO-5457 — sizes and layout of drawing sheets.
- ISO-7200 — data fields in title blocks and document headers.
- PUB-256:1381 — استاندارد نقشه‌کشی ساختمانی, issued by دفتر تدوین ضوابط و معیارهای فنی / سازمان مدیریت و برنامه‌ریزی کشور.
- EDU-D10-210626 — Grade 10 educational foundation, Part 3 Chapter 9 — نقشه‌کشی معماری.
- EDU-D11-211208 — Grade 11 Phase 1/2 architecture and construction-detail foundation.

## Rule schema
Each executable rule carries:
- rule_id
- source_id
- source_level: NORMATIVE / EDUCATIONAL / CANDIDATE
- scope
- preconditions
- evidence_required
- check
- pass_condition
- fail_closed_condition
- severity
- version/applicability

## Core rules

### DRAW-REP-001 — Unambiguous technical representation
source: ISO-128-1:2020
level: NORMATIVE
check: representation must have a single unambiguous interpretation within its documented purpose.
evidence: drawing geometry + representation metadata + applicable standard/version.
fail_closed: UNKNOWN when view/type/geometry is ambiguous.

### DRAW-SCALE-001 — Representation proportionality
source: ISO-128-1:2020
level: NORMATIVE
check: represented outlines/details are proportional to the represented object.
evidence: source geometry + declared scale + drawing units.
fail_closed: UNKNOWN when scale or units are unknown.
Guard: dimensions must not be reconstructed merely by measuring pixels or displayed image size.

### DRAW-SHEET-001 — Sheet layout
source: ISO-5457
level: NORMATIVE
check: when sheet-format validation is in scope, verify sheet size/layout metadata against the declared applicable ISO 5457 requirements.
evidence: sheet metadata + declared format/orientation + applicable edition.
fail_closed: UNKNOWN when sheet metadata or edition is unavailable.

### DRAW-TITLE-001 — Title-block data fields
source: ISO-7200
level: NORMATIVE
check: when title-block validation is in scope, verify required/selected data fields against the applicable ISO 7200 profile.
evidence: title-block extraction + project profile + applicable edition.
fail_closed: UNKNOWN when title block cannot be reliably detected.

### DRAW-DIM-001 — Dimension presentation
source: ISO-129-1:2018
level: NORMATIVE
check: dimension presentation follows applicable general principles; dimensions are annotations, not values guessed from rendered scale.
evidence: dimension entities + units + associated geometry + applicable edition.
fail_closed: UNKNOWN for ambiguous association, missing units, or conflicting source geometry.

### DRAW-VIEW-001 — Views, sections and cuts
source: ISO-128-3:2022
level: NORMATIVE
check: view/section/cut representation and references are consistent with applicable projection and section conventions.
evidence: view type + geometry + section/cut markers + projection metadata where applicable.
fail_closed: UNKNOWN when projection/view identity is uncertain.

### DRAW-CROSSVIEW-001 — Cross-view consistency
source: ISO-128-1:2020 + ISO-128-3:2022
level: CANDIDATE until project profile activates it
check: corresponding plan/elevation/section geometry and references do not contradict each other.
evidence: linked view identities + common coordinate/reference system + extracted geometry.
fail_closed: NEEDS_REVIEW on unresolved correspondence or conflicting geometry.
Note: exact architectural acceptance tolerances are not invented here.

### DRAW-EDU-001 — Educational architectural drawing semantics
source: EDU-D10-210626
level: EDUCATIONAL
check: use D10 Chapter 9 concepts for interpretation of plan/elevation/section, symbols, scale, dimensioning and presentation.
never_use_for: independent regulatory compliance approval.

### DRAW-PHASE1-001 — Phase 1 drawing scope
source: EDU-D11-211208 + PUB-256:1381
level: CANDIDATE
check: classify Phase 1 deliverables and expected drawing types only when project profile explicitly declares this phase.
fail_closed: UNKNOWN when project phase is not declared.

### DRAW-PHASE2-001 — Phase 2 execution/detail scope
source: EDU-D11-211208 + PUB-256:1381
level: CANDIDATE
check: distinguish execution plans, sections, elevations and construction details from Phase 1 documentation.
fail_closed: UNKNOWN when phase/profile is missing.

### DRAW-LINE-001 — Line hierarchy
source: ISO-128 series
level: CANDIDATE until exact applicable part/profile is resolved
check: validate line type/weight semantics only against the exact applicable ISO 128 part and construction/architecture profile.
fail_closed: UNKNOWN if the exact line convention/profile is not identified.

## Integration boundary
- Rule Engine consumes these rules only after source/version/applicability resolution.
- Detection uncertainty never becomes compliance PASS.
- Educational rules can support interpretation but cannot override authoritative requirements.
- Project-specific Iranian requirements take precedence when legally/contractually applicable.
- Every PASS must be traceable to rule_id + source_id + evidence IDs.

## Initial executable subset
1. scale/unit consistency guard
2. dimension-geometry association guard
3. view/section identity guard
4. sheet metadata guard
5. title-block extraction/field guard
6. cross-view contradiction detector (no automatic approval)
7. fail-closed evidence gate

## Important limitation
This pack records source-grounded rule intent and integration boundaries and does not reproduce copyrighted standard text. Exact clause-level enforcement requires the applicable licensed/official standard text and project profile.
