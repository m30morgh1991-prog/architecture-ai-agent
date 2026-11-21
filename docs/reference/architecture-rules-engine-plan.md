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


## Source/version gate updates — 2026-11-21



## National regulation and judicial updates — 2026-11-21 (reference only)
- Topic 24 first edition 1404: reproduced ministerial letter No. 140461/100/2 dated 1404/07/27 states effectiveness six months later. Calculated date 1405/01/27; a secondary summary says Ordibehesht 1405, so exact date is unresolved. Keep official-host verification pending.
- Topic 24 tall-building definition in reproduced text: 47 m or more, OR 8+ floors including ground, OR highest usable floor >44 m above average ground. Older 27/23 m figures are not supported by this reproduced first-edition text and must be flagged as conflicting/possibly different criterion, not attributed to M24. No executable compliance check from this source.
- Topic 24 density increase for 8+ floors is described as requiring high-rise zone/axis context, not isolated building. The reproduced text states 24% land coverage for high-rise buildings; applicability must be checked against official detailed plan and primary source.
- Topic 19 fifth edition 1404: initial mandatory date reported as 1404/10/19. Subsequent IRCEO announcement permits parallel application of fourth (1399) and fifth (1404) editions from 1404/10/20 through 1405/12/29. One-day start discrepancy and minister-letter metadata are SOURCE_REQUIRED. Preserve selected edition and source evidence per project; do not force v5-only checks during the reported transition.
- Topic 12 fifth edition (Safety, occupational health and environment during construction) was announced with minister letter dated 1403/09/12 and effective from that date according to IRCEO; full PDF/letter is SOURCE_REQUIRED before clause-level implementation.
- General Board judgment 1405313900001131406 (1405/05/06) annulled letter 134252/420 (1404/08/11) issued by the National Building Regulations office, concerning supervisor instruction to compare approved drawings with National Regulations and report discrepancies. This is a narrow annulment of that letter, not of the regulations or design/execution duties. Full reproduced text has a wording tension; official judgment copy required.
- The source-only additions must not generate PASS, FAIL, legal authorization, permit prediction, or automated enforcement.

**Source provenance correction:** the full M24 text/thresholds were read from the ATNasr-hosted PDF. The letter number/date were found in a search-indexed QSCE PDF result, but its exact direct URL could not be verified. Do not imply that the ATNasr PDF itself contains the ministerial letter. Official-host PDF and hash remain pending.