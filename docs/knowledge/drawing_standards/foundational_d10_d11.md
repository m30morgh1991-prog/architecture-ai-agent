# Foundational Architectural Drawing Knowledge — D10/D11

## Purpose
Foundational educational knowledge for the Architecture AI Agent. This is a knowledge/reference layer, not a substitute for binding regulations, official standards, or project-specific authority.

## Source hierarchy
1. Binding regulations / official requirements
2. Official standards and approved technical publications
3. This educational foundation
4. General reference books

Rules derived here must retain source_id and source_level=EDUCATIONAL and must not be promoted to normative compliance without an authoritative source.

## D10 — ترسیم فنی و نقشه‌کشی
Code: 210626
Relevant section: Part 3 — نقشه‌کشی; Chapter 9 — نقشه‌کشی معماری.

### Chapter 9 knowledge map
- purpose and role of architectural drawings
- architectural drawing language, symbols and conventions
- plan, elevation, section, perspective
- Phase 1 architectural drawing
- scale as a function of drawing purpose and required information
- geometric consistency between related views
- plan representation and architectural elements
- furniture plan versus dimensioned plan
- dimensioning principles
- elevation representation and relation to plan
- section representation and vertical dimensions
- presentation and readability
- introduction to more detailed / Phase 2 drawings

### High-value principles
- A drawing communicates design information to builders; accuracy and completeness are core quality requirements.
- Scale determines how much information can be communicated, not just a numeric reduction.
- Smaller scales require less graphical detail; larger scales permit more detail.
- Related views must remain geometrically consistent.
- Furniture shown in a furniture plan is representational but should remain dimensionally plausible.
- Dimensioned plans should prioritize construction-relevant dimensions and avoid unnecessary clutter.
- Dimension chains should be consistent and readable; repeated/conflicting dimensions should be detectable.
- Sections primarily communicate vertical information; plan dimensions and section elevations have different roles.
- Elevations should be derived consistently from plan geometry and vertical information rather than guessed independently.
- Line-weight/detail hierarchy should communicate cut versus visible elements.

### Scale as educational reference
Chapter 9 discusses common architectural examples such as 1:50, 1:100 and 1:200; site/location drawings may use smaller scales, while details may use larger scales such as 1:20, 1:10 and 1:5. These are educational examples, not universal regulatory requirements.

## D11 — نقشه‌کشی ساختمان
Code: 211208
Structure:
- Module 1: Architectural drafting — Phase 1
- Module 2: Architectural drafting — Phase 2
- Module 3: Construction details and materials
- Module 4: Structural drafting — Phase 1
- Module 5: Structural drafting — Phase 2

### Module 1 — Phase 1 architecture
- plans, elevations, sections
- site/location plan
- architectural representation for two-storey-and-higher buildings
- AutoCAD drafting principles
- textbook references نشریه 256 and ISO standards
- communication of placement, spatial relationships, architectural characteristics and elevations
- common educational examples include 1:50 and 1:100

### Module 2 — Phase 2 architecture
- executive/working architectural drawings
- roof slope plan and material information
- execution plans for floors
- execution sections
- execution elevations
- interior elevations
- increased information/detail compared with Phase 1

### Module 3 — construction details and materials
- floor build-ups and details
- wall construction and details
- skirting/base details
- parapet/roof-edge details
- suspended ceilings
- material identification
- construction details as Phase 2 documentation
- detailing connected to execution and energy-related requirements

## Architecture AI Agent mapping

### Knowledge-only
- drawing purpose
- drawing-type semantics
- conventional architectural symbols
- view relationships
- presentation hierarchy
- educational scale examples
- furniture representation conventions

### Candidate deterministic validation rules
These require an evidence-backed rule contract before activation:
- plan/elevation/section identity and cross-view consistency
- dimension-chain consistency
- dimensioned-plan readability
- scale metadata consistency
- drawing-type required elements
- view projection consistency
- furniture scale plausibility
- line hierarchy / cut-vs-visible distinction

### Fail-closed
- uncertain scale
- uncertain view type
- uncertain element identity
- missing source geometry
- conflicting dimensions
- inferred standards without authoritative evidence

## Contract boundary
Educational knowledge may guide interpretation and candidate validation, but cannot independently declare regulatory compliance. Any normative rule must cite its authoritative source and version.

## Suggested future Rule Pack IDs
- EDU-D10-DRAW-001
- EDU-D10-DRAW-002
- EDU-D10-SCALE-001
- EDU-D10-DIM-001
- EDU-D10-VIEW-001
- EDU-D11-P1-001
- EDU-D11-P2-001
- EDU-D11-DETAIL-001

## Source notes
D10: Ministry of Education textbook, code 210626; retrieved copy identifies Chapter 9 as نقشه‌کشی معماری in Part 3.
D11: Ministry of Education textbook, code 211208; retrieved PDF states that its content continues the Grade 10 foundation and covers Phase 1/2 architectural drafting and construction details.
