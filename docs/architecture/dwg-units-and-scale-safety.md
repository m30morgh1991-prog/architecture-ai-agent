# DWG Units, Geometry Scale, and Plot Scale Safety

## Purpose
Prevent a drawing's unit metadata, displayed dimensions, geometry coordinates, and plot scale from being treated as interchangeable evidence.

## Core distinction
- **Coordinate magnitude**: raw model-space geometry values returned by the parser.
- **Declared drawing units**: DWG header / INSUNITS metadata, when available.
- **Dimension annotation**: displayed dimension text and actual measurement, if the parser exposes them.
- **Plot configuration**: paper-space viewport and print scale settings, when available.
These are separate evidence sources. A declared unit does not prove that the geometry was authored in that unit, and changing print settings alone does not prove that model-space geometry was converted.

## Fail-closed rules
1. Preserve raw coordinates and raw header unit metadata exactly as evidence.
2. Report the unit metadata source and raw code when available; map known INSUNITS values only as a descriptive interpretation.
3. If unit metadata is absent, unspecified, contradictory, or inconsistent with known dimension evidence, mark effective units UNKNOWN / NEEDS_REVIEW.
4. Never infer inches, centimetres, millimetres, or metres from coordinate magnitude alone.
5. Never silently scale geometry or convert the immutable Golden DWG files during evidence extraction.
6. Do not compare geometry to parking regulations until units and measurement interpretation have been independently reconciled.
7. Distinguish geometry-unit confidence from paper-space / plot-scale confidence. If plotting data is unavailable, plot scale is UNKNOWN; do not infer it from printed-looking dimensions.
8. Dimension text is not authoritative by itself. Prefer parser-exposed actual measurement and defining points, retain raw annotation text, and mark association/interpretation NEEDS_REVIEW.
9. If a plausible reference length is available, use it only as a review cross-check and require human confirmation before assigning effective units or changing any drawing.
10. Preserve provenance, source SHA-256, and coordinate status for every evidence row.

## Known INSUNITS descriptions
- 0: Unitless / unspecified
- 1: Inches
- 2: Feet
- 4: Millimetres
- 5: Centimetres
- 6: Metres

These codes describe AutoCAD insertion scaling metadata; they are not proof of how a user authored geometry or configured plotting.

## First Golden DWG artifact review — 2026-10-11
Read-only evidence was exported successfully from both immutable Golden DWGs. The artifact reports the parser's `doc.units` value as `inches` for both plans, but the current extractor does not establish that this value came directly from the raw DWG `$INSUNITS` header variable. Treat it as **parser-reported units, provenance unverified**, not as confirmed declared drawing units.

- `bagheri7.dwg`: 13,205 model-space entities, 9,737 direct geometry rows, 60 dimension entities. The parser reports bounds approximately X=69.94..1974.14, Y=-314.66..363.33, Z=-10.8..1500.872. Dimension actual measurements range approximately 0.305..38.96 coordinate units.
- `afifiiiii.end.edit3.dwg`: 72,922 model-space entities, 72,520 direct geometry rows, 8 dimension entities. The parser reports bounds approximately X=37.76..126.86, Y=5.86..51.95, Z=0. Dimension actual measurements include 21.14, 3.18, 1.2, and 0.8 coordinate units; text evidence includes `CM` labels and `EXPANSION JOINT=8`.

### Review finding
The unit label cannot safely be used as the conversion factor for either drawing. In particular, treating the second plan's 21.14 dimension as inches would yield a very different physical interpretation than treating it as metres; the extracted evidence alone does not establish which interpretation is correct. This is a **unit-provenance / geometry-scale review flag**, not proof that the drawing is wrong or compliant.

### Engineering follow-up completed
The extractor now exposes the raw `$INSUNITS` code and metadata source when available, keeps `parser_reported_units` separate, and reports plot scale as UNKNOWN unless actual plot/layout configuration is extracted. It does not scale, convert, save, or edit either Golden DWG. A human-confirmed reference dimension and its association to a specific plan element are still required before selecting effective units.

## Suggested evidence fields
- raw_insunits_code
- declared_units
- units_metadata_source
- parser_reported_units
- effective_units_status: SUPPORTED / UNKNOWN / NEEDS_REVIEW
- raw_geometry_coordinates
- raw_dimension_text
- actual_measurement_status
- plot_scale_status: SUPPORTED / UNKNOWN / NEEDS_REVIEW
- cross_check_findings
- human_review_required
- source_sha256

## Golden DWG policy
The following files are immutable regression inputs and must not be resaved, converted, or scaled by this workflow:
- test-assets/golden-projects/bagheri7.dwg
- test-assets/golden-projects/afifiiiii.end.edit3.dwg

## Decision boundary
This document defines a conservative evidence policy only. It does not assert that either Golden DWG is inch-based or centimetre-based, and it does not establish parking-rule compliance.


## Raw header extraction review — 2026-10-11
The newer artifact reads raw `$INSUNITS` code **1 (inches)** from both Golden DWGs, and the parser-reported label is also `inches` for both. This confirms the header declaration and parser label agree; it does **not** establish that the coordinate geometry is physically inch-scaled. Therefore:
- `declared_units_metadata_status` may be SUPPORTED when raw metadata is recognized and does not conflict with the parser label.
- `effective_units_status` remains NEEDS_REVIEW whenever a nonzero known raw unit code exists, until an independent reference length and its geometry/dimension association are reviewed.
- If the raw code is absent or unitless, effective units remain UNKNOWN.
- `plot_scale_status` remains UNKNOWN.

This is intentionally conservative. The two drawings have substantially different coordinate extents and dimension patterns; no unit conversion, parking-space classification, or regulatory verdict is authorized by the header code alone.
