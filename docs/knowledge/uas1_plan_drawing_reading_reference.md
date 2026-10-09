# Reference: اصول نقشه‌کشی و نقشه‌خوانی ساختمان 1 (سازه و معماری)

**Source type:** Educational/reference book provided by the user
**Author:** نوید سلیمانیپور
**Edition metadata in source:** 1396, جلد اول، سازه و معماری
**ISBN:** 978-600-04-8122-3
**Source file:** `اصول_نقشه_کشی_و_نقشه_خوانی_ساختمان.pdf`
**Status:** STUDIED / KNOWLEDGE INTEGRATION
**Role in Architecture AI Agent:** Educational reference for architectural drawing language, plan/section reading, drafting conventions, stairs/ramps, and structural-drawing interpretation.

## Copyright / repository handling

The supplied PDF explicitly states that copyright belongs to the author and warns against unauthorized electronic copying/distribution. Therefore the public repository must **not** redistribute the full PDF unless the project has explicit permission/licensing to do so.

This repository stores a bibliographic record and derived, project-relevant knowledge only. The original PDF remains the user-provided source material.

## Why this source matters

The source is unusually relevant to the plan-understanding core because it treats the drawing as a technical language and covers both architectural and structural drawing conventions. Its contents include:

- drawing definitions, drawing types, scale and paper/sheet conventions;
- common building-drawing symbols;
- architectural plans and plan symbols;
- walls, columns, doors, windows, cabinets, ducts and level differences;
- north arrow, titles, space identification and plan dimensioning;
- section lines, hatching, section scale and section construction;
- stair terminology, stair counting/calculation and multiple stair configurations;
- parking and ramps, including ramp-length calculation;
- site/location plans and roof/slope plans;
- structural plans, grids/axes, columns, beams and foundations;
- execution sections and construction details.

## Project-learning extraction

### 1. Drawing language must be modeled as evidence

The agent should treat a drawing as a structured language rather than a collection of pixels.

Useful evidence classes include:
- geometric primitives and boundaries;
- conventional symbols;
- dimensions and extension lines;
- labels/codes;
- section markers and directions;
- level/elevation annotations;
- hatches;
- scale/title information;
- repeated drafting conventions.

A symbol or text cue is evidence. It becomes semantic truth only after the existing evidence/constraint rules support it.

### 2. Plan understanding must include drafting conventions

The semantic pipeline should explicitly account for conventional representations of:
- walls and columns;
- doors and swing/opening direction;
- windows and sill/parapet-height notation;
- ducts;
- stairs, landings and stair direction;
- level differences;
- north direction;
- room/space labels;
- internal and external dimensions;
- section-cut lines.

This strengthens the existing Drawing Representation → Architectural Semantics boundary.

### 3. Sections are not independent drawings

A section marker in plan provides directional and positional evidence for a section. The section itself provides vertical evidence about:
- floor-to-floor relationships;
- stair rise/run;
- roof/floor build-up;
- openings;
- vertical clearances;
- structural and architectural components.

The agent should cross-check plan and section evidence instead of interpreting either view in isolation.

### 4. Stairs require a dedicated semantic relation model

The source treats stairs as a system with:
- total vertical rise;
- riser height;
- tread depth;
- number of risers/steps;
- flight/run;
- landing;
- stair direction/path;
- headroom;
- stair opening/void;
- section representation.

For Architecture AI Agent this means stair understanding should connect **level/elevation evidence + geometry + stair symbols + section evidence**.

A stair count must remain UNKNOWN/NEEDS_REVIEW when the required rise/level/run evidence is missing or contradictory.

### 5. Level/elevation codes are high-value evidence

The source demonstrates how level differences and vertical relationships drive stair and ramp interpretation. This supports the project's current research direction that level/elevation codes should be first-class evidence, not just OCR text.

The semantic chain should preserve:

level code → referenced location → vertical relation → affected stair/ramp/space relation

No level code should be promoted to a building-level fact without location and consistency evidence.

### 6. Ramps require geometric + level reasoning

Ramp interpretation should combine:
- start level;
- end level;
- vertical difference;
- slope;
- available horizontal length;
- interior/exterior constraints;
- parking clearance where applicable.

A single slope label is not enough to validate a ramp.

### 7. Structural drawing language is useful even in an architectural-first MVP

The structural chapter provides useful evidence vocabulary for:
- grids/axes;
- column types;
- beam types;
- foundation plans;
- structural stair members;
- reinforcement/detail notation;
- execution sections.

This should improve cross-discipline understanding without making structural engineering calculation part of the MVP.

## Direct implications for current architecture

1. **Drawing Representation Layer:** add/retain explicit evidence types for section markers, level codes, stair symbols, dimension chains, hatch conventions and plan annotation.
2. **Architectural Semantic Layer:** add dedicated semantic candidates for stair flight/landing, level marker, section marker and dimension chain.
3. **Relation Layer:** support relations such as `SECTION_OF`, `LEVEL_AT`, `STAIR_CONNECTS_LEVEL`, `DIMENSION_REFERENCES`, and `MARKER_REFERENCES` where evidence is sufficient.
4. **PlanModel ↔ ConstraintMap:** preserve source evidence for locked structural elements and architectural boundaries; do not infer editability from drafting style alone.
5. **Impact Analysis:** changing a level, stair, opening or wall should trigger dependent-space and section/vertical-relation checks.
6. **Validation:** cross-view contradictions (plan vs section vs level evidence) should produce `BLOCKED` or `NEEDS_REVIEW`, never silent PASS.
7. **Training/evaluation:** use the book's conventional drawing language as an educational reference when constructing semantic candidate tests and regression fixtures.

## Important boundary

This source is an educational/technical reference, not the highest authority for current Iranian regulations. Where it conflicts with current official regulations, standards, approved project documents, or authoritative engineering requirements, those higher-priority sources win.

## Initial knowledge status

- Bibliographic identity: **PASS**
- Relevance to plan understanding: **PASS**
- Architectural drawing-language extraction: **PASS**
- Stair/level/ramp reasoning relevance: **PASS**
- Structural drawing-language relevance: **PASS**
- Current regulatory authority: **NOT_AUTHORITY / SOURCE_REQUIRED**
- Full PDF redistribution in public repository: **BLOCKED without permission**
