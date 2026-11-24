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


## 2026-11-24 regulatory watch — reference only / no rule activation

- The first-stage Shiraz master-plan framework was reported as approved at the 16th Supreme Council meeting (1405/08/26), with high-rise development directed to a defined area away from historic/degraded fabric, protection of Qasr-e Dasht gardens, transit-oriented development, and preparation of a detailed plan. The signed resolution and spatial maps have not been retrieved; this is not parcel-level zoning.
- The reported 350 cm residential floor-height amendment remains ANNOUNCED / PRESS_LEAD until the Article 5 resolution, measurement definition, applicability map and notification date are obtained.
- The reproduced Topic 24 first-edition 1404 PDF reports letter 140461/100/2 dated 1404/07/27 and six-month delayed effect; 1405/01/27 is a calendar calculation only. Official Ministry-hosted binary and SHA-256 remain pending.
- Judgment 1405/05/06 annulled letter 134252/420 that attempted to impose a new duty on supervisors to compare approved drawings against National Building Regulations. It does not waive the National Building Regulations or remove the supervisor's execution-stage duty to monitor conformity with the permit, approved drawings and technical calculations.
- Shiraz judgments 1405/02/08, 1405/03/05 and 1405/04/09 affect only the exact municipal clauses/resolution described in the source register. Do not generalize them to all fees or all permit procedures.
- All entries above are research references only. No new executable rule was added; uncertain applicability remains SOURCE_REQUIRED / NEEDS_REVIEW / UNKNOWN.
