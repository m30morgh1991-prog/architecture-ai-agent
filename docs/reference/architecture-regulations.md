# Architectural Regulations Reference Pack (User-Supplied)

> **Status:** Reference inputs captured; not yet independently verified against current official regulations.
> **Use:** Rule candidates for plan understanding, constraint modeling, and validation. Never treat these values as universally/currently legally binding without checking jurisdiction, edition, and project context.
> **Fail-closed:** Missing context, conflicting rules, or uncertain interpretation => UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW. Do not auto-promote to PASS.

## Source PDFs
- `آموزش ضوابط طراحی معماری.pdf` — 67 pages; topics include definitions, parking/ramp, stair/elevator, daylighting, projections, fire/egress, accessibility, structure/column layout, and spatial standards.
- `ضوابط پارکینگ.pdf` — 27 pages; parking-specific source (uploaded PDF's extracted page count differs from the user's stated count).
- Original PDFs are attached to the ChatGPT conversation. The repository currently stores this text reference, not the original binary PDF files.

## User-provided rule summary — captured without legal verification

### Stair and elevator core
- Stair enclosure inside-to-inside: 240 x 480 cm; avoid stairwell eye/open void (user note: prevent chimney/smoke-stack effect).
- Elevator shaft inside-to-inside: 160 x 200 cm.
- Elevator-front landing/lobby: 150 x 150 cm.
- Up to 4 residential units per floor: one stair/elevator core stated as sufficient; over 4 units: at least two cores stated.
- Stair riser: 17 cm; tread: 30 cm.
- Stair and elevator enclosure walls: 20 cm.
- Note: dimensions and counts are user-supplied rule candidates and require applicability/official-source verification.

### Light wells / patios
- Lot <= 200 m²:
  - Main rooms (bedrooms, hall/living, reception, dining): light-well area >= 6% of lot area; minimum dimension 2 m.
  - Secondary rooms (kitchen, storage): >= 3% of lot area; minimum dimension 2 m.
- Lot > 200 m²:
  - Main rooms: >= 12 m²; minimum dimension 3 m.
  - Secondary rooms: >= 6 m²; minimum dimension 2 m.
- Facing windows across a shared light well:
  - Main-main: >= 6 m.
  - Secondary-secondary: >= 4 m.
  - Main-secondary: >= 4 m.
- These summarized dimensions are stated for ordinary buildings up to five floors.
- When stated conditions are met, light-well/patio area is excluded from gross floor area (as supplied; verify jurisdiction and definitions).

### Parking / vehicle access
- One parking bay minimum opening width: 2.5 m.
- Two adjacent bays: 4.5 m; three adjacent bays: 7 m.
- Parking bay length: 5 m; nominal bay: 2.5 x 5 m.
- Maneuvering radius/length noted: 5 m.
- Parking entrance clear width: 3 m.
- Straight ramp: one-way 3 m; two-way 6 m.
- Curved ramp: one-way 3.65 m; two-way 7 m.
- Ramp slope: 15%.
- Parking requirement notes supplied:
  - A dwelling over 100 m² on first/second floor requires a parking space (wording/context needs verification).
  - Under 150 m²: 1 space; 150–200 m²: 1.5 spaces; over 200 m²: 2 spaces.
  - If unit count is odd, one unit is exempt (user-supplied note; do not apply automatically without confirming rule/context).
- Keep this section distinct from the dedicated parking PDF and local Shiraz parking rules; contradictions must be surfaced, not silently reconciled.

### Heights and clearances
- Residential clear height: source note says maximum 2.9 m, with 3.1 m suggested as a design value.
- Parking clear height: source note says maximum 2.40 m, with 2.8 m suggested as design value (these statements are internally conflicting as written; flag for review).
- Pilotis clear height: maximum 2.40 m.
- Basement clear height: maximum 2.20 m.
- Commercial clear height: maximum 4.50 m.
- Parking entrance clear height: minimum 1.80 m.
- Roof stair-headroom clear height: 2.20 m.
- Basement daylight opening height: maximum 90 cm.
- Elevator pit minimum dimension/height note: 1.60 m (exact interpretation needs verification).

### Room / courtyard / projection dimensions
- Minimum window area: >= 1/5 of room area (as supplied; interpretation and applicability to be verified).
- Continuous courtyard minimum width: 2 m; non-continuous courtyard minimum width: 3 m.
- Balcony/projection into street: 120 cm for street width 12–20 m; 150 cm for street width over 20 m; underside height above street >= 3.50 m (verify local rules).
- Minimum kitchen and bedroom width: 2.50 m.
- Living room minimum width: 3.00 m.
- Landing minimum width: 1.20 m.

## Project integration requirements (design intent)
- Treat this pack as a **reference-rule source**, not a single authoritative code.
- Store rules as structured, traceable candidates with: rule_id, source/document, source page/section when available, jurisdiction, edition/date, building/use context, inputs, threshold/unit, predicate, severity, and verification status.
- Distinguish hard constraints from design recommendations, notes, and locally scoped requirements.
- Rule conflicts (including parking-source vs. summary differences) must produce a conflict record and NEEDS_REVIEW; never silently choose.
- PlanModel / ConstraintMap should be able to represent geometry, room classifications (main/secondary), floor/unit counts, openings/light-well relations, stairs/elevators, parking layout/access/ramp, heights, and evidence.
- Rule checks should be deterministic and unit-aware; no compliance PASS based only on image interpretation or uncertain geometry.
- Preserve original units and convert explicitly. Unknown lot area, floor count, jurisdiction, room category, or source edition should block definitive checks.
- These references do not replace applicable national building regulations, municipal rules, fire/accessibility requirements, or professional review.

## Initial priority for implementation
1. Source traceability and rule registry (no PASS yet).
2. Parse explicit user constraints and attach source IDs.
3. Build deterministic checks for dimensions/area/counts once the geometry and context are reliable.
4. Report conflicts, missing inputs, and uncertainty visibly.
5. Add regression fixtures for each rule; tests must cover boundary values and unknown context.


## National Topic 24 (1404) and Shiraz height lead — 2026-11-19
A reproduced Ministry of Roads and Urban Development first-edition Topic 24 (Urban Building Conformity) contains ministerial notification no. 140461/100/2 dated 1404/07/27 and says it becomes effective six months after notification. As of 1405/08/28, that period has elapsed; exact calendar effective day is still SOURCE_REQUIRED because secondary reposts disagree and the ministry-hosted original was not retrieved. The copy is hosted at a non-ministry domain and no SHA-256 hash was obtained.

Candidate national Topic 24 topics for later, source-bound review:
- Height definition: average sidewalk level to average roof (sloped roof) / highest parapet (flat roof).
- High-rise classification trigger: height >=27 m OR >=8 floors including ground OR highest usable floor >23 m.
- Density/height, placement, massing, adjacency, privacy/overlooking, shadow/daylight, access width, and cityscape context.
- Residential façade lighting prohibition (ground-floor/entrance security lighting is required).
- Visible façade mechanical equipment prohibition except gas-related installations.

A press lead dated 1405/08/17 reports Fars Article-5 approval for residential floor height up to 350 cm in Shiraz. The original resolution, height definition, zones, conditions, notification and effective date were not obtained. Keep it ANNOUNCED/UNKNOWN; do not use it as a legal threshold or infer building-height/floor-count permission.

Source links: Topic 24 PDF copy (https://qsce.ir/uploads/%D9%85%D8%A8%D8%AD%D8%AB%20%D8%A8%DB%8C%D8%B3%D8%AA%20%D9%88%20%DA%86%D9%87%D8%A7%D8%B1%D9%85%20%D9%85%D9%82%D8%B1%D8%B1%D8%A7%D8%AA%20%D9%85%D9%84%DB%8C.pdf); Tasnim height report (https://newsmedia.tasnimnews.ir/fa/news/1405/08/17/3743048/%D9%85%D8%AC%D9%88%D8%B2-%DA%A9%D9%85%DB%8C%D8%B3%DB%8C%D9%88%D9%86-%D9%85%D8%A7%D8%AF%D9%87-5-%D8%A8%D8%B1%D8%A7%DB%8C-%D8%A7%D9%81%D8%B2%D8%A7%DB%8C%D8%B4-%D8%A7%D8%B1%D8%AA%D9%81%D8%A7%D8%B9-%D8%B7%D8%A8%D9%82%D8%A7%D8%AA-%D9%85%D8%B3%DA%A9%D9%88%D9%86%DB%8C-%D8%B4%DB%8C%D8%B1%D8%A7%D8%B2-%D8%AA%D8%A7-3-5-%D9%85%D8%AA%D8%B1).


## Article 99 jurisdiction and enforcement — follow-up 2026-11-19
The current research found two more sources:
- General Board judgment 1403313900001065343 (1403/05/09) annulled clauses 7, 8, 9, 10, and 14 of Ministry circular 145016 (1401/07/19) in the specified respects. This is not a blanket annulment of Article 99 or the entire guideline.
- Advisory opinion 7/1403/747 (1403/10/30) states that jurisdiction for an earlier violation remains with the Article-99 commission if the parcel was outside city harem at the violation date, even if it later enters; a violation after entry falls to Article 100.

Source links: https://amagestate.com/legal/article-99-building-demolition-ruling/ ; https://hoshyarvakil.ir/opinion/7-1403-747/ . Both are reproductions; official primary copies remain pending.
