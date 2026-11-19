# Architecture Rules Engine — Implementation/Test Plan

This registry is the initial normalized reference catalog. It is **not yet executable compliance logic**.

## Required deterministic behavior
- Validate schema/types, finite numeric inputs, non-boolean numeric values, positive areas/dimensions, and known unit conversions.
- Evaluate only when required inputs, room classification, jurisdiction, building type, floor count, and rule applicability are known.
- Return one of: PASS, FAIL, UNKNOWN, NEEDS_REVIEW, BLOCKED.
- Use PASS only when the rule predicate is deterministically evaluated from trusted evidence.
- Never infer room category, dimensions, or applicability from uncertain raster-only detection for final compliance.
- A candidate rule with no official edition/page evidence cannot yield an official compliance PASS; it may yield a provisional geometric check explicitly marked as such.
- Report rule/source IDs, measured values, required values, evidence references, and reason codes.

## Recommended first executable slices
1. Generic typed comparison primitives (min/max/equality, area ratio, conditional threshold) with unit-safe inputs.
2. Stair landing/tread/riser and room minimum-width checks when geometry is trusted.
3. Parking bay dimensions, opening widths, ramp widths and slope; keep parking count requirements review-gated until source conflicts and municipality are resolved.
4. Light-well area/dimension and window-to-window distance, gated by lot area, served room category, floor count <=5, and reliable geometry.
5. Courtyard and balcony projection checks, gated by street width and local applicability.

## Test matrix
- Exact threshold => PASS (provisional reference check only).
- One unit below minimum / above maximum => FAIL.
- Missing required input => UNKNOWN.
- Invalid type, bool, NaN, infinity, negative area, zero dimension => BLOCKED or UNKNOWN with reason.
- Unknown room class, floor count, lot-area band, ramp type, or direction => NEEDS_REVIEW.
- Conflicting source rule => NEEDS_REVIEW with both source IDs retained.
- Units mixed (cm/m) => explicit conversion; never silently compare.
- Uncertain geometry evidence => no compliance PASS.
- Light-well rule at 5 floors may evaluate only if all other context is known; 6+ floors => NEEDS_REVIEW under supplied summary scope.


## Additional current sources — legal and urban-conformity watch (2026-11-19)
- Keep Topic 24 (national urban conformity) as a separate source family from parcel-specific Shiraz detailed-plan rules. It supplies context and criteria; it does not itself grant a parcel permission.
- Record the reported 350-cm Shiraz residential floor-height change only as ANNOUNCED/UNKNOWN until the Article-5 resolution, amended clause, scope/map, notification and effective date are obtained.
- Add the 1404/05/28 General Board judgment 1295686 as a narrow, binding source for change-of-use enforcement: distinguish the construction/area violation from operating-stage change of use; never model a fine as a right to retain unauthorized use.
- Keep Article 100 and Article 99 jurisdiction separate and parcel/date-specific. Article 100 is not a design compliance substitute; Article 99 outside the approved city harem must not automatically inherit Article-100 grounds.
- The two 1405 legal opinions (7/1405/261 and 7/1405/231) are secondary reproductions only; register them as research leads with SOURCE_REQUIRED. Do not generate PASS, legal authorization, or enforcement conclusions from them.


## Article 99 routing safeguards (reference-only)
- Preserve violation date and the historic approved city-limit/harem map separately from the current parcel map.
- Advisory opinion 7/1403/747 states that the boundary status at the date of violation controls Article-99 vs Article-100 routing for the described boundary-entry scenario; do not route using current status alone.
- Judgment 1065343 annulled only clauses 7, 8, 9, 10, and 14 of circular 145016 in its specified respects. Keep clause-level status and scope; do not mark the whole circular or Article 99 invalid.
- These are source-bound legal routing candidates only. No automated jurisdiction PASS or enforcement decision is permitted without official boundary evidence, violation-date evidence, and primary legal source verification.
