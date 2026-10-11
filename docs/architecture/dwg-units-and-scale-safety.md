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

## Suggested evidence fields
- raw_insunits_code
- declared_units
- units_metadata_source
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
