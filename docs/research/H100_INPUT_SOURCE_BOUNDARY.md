# H100 — Input Source Boundary

## Decision

Image inputs remain supported, but they are explicitly separated from engineering-plan inputs.
The system must never treat a raster image as equivalent to CAD/vector geometry.

## Source hierarchy for geometry reconstruction

1. **DWG/DXF — ENGINEERING_VECTOR**
2. **Vector PDF — DOCUMENT_VECTOR**
3. **Raster PDF — DOCUMENT_RASTER**
4. **JPG/PNG/WEBP — IMAGE_RASTER**

This is a geometry-evidence trust ordering, not a guarantee that every source is correct.
All downstream semantic facts remain evidence-backed and fail closed.

## PDF rule

PDF is not classified by extension alone. A PDF exported from AutoCAD is commonly vector and should enter the engineering-plan path after vector evidence is confirmed. A scanned/raster PDF enters the image path.

Therefore:

`PDF + vector evidence → ENGINEERING_PLAN`

`PDF + raster evidence → IMAGE`

`PDF + unknown representation → UNKNOWN / SOURCE_REQUIRED`

The system must not guess PDF representation from filename alone.

## Execution boundary

- Engineering-plan path: DWG/DXF and confirmed vector PDF.
- Image path: JPG/PNG/WEBP and confirmed raster PDF.
- The image path may produce evidence or visual candidates, but it cannot promote uncertain geometry into authoritative PlanModel state.
- PlanModel + ConstraintMap + ApprovedChangePlan remain the Source of Truth.
- Source classification/provenance must travel with execution metadata so later semantic and validation stages know what evidence class produced a fact.

## Implementation

- `runtime/input_source_contract.py` defines source classes, input modes, PDF inspection requirement, and geometry trust rank.
- `runtime/request_contract.py` carries optional `source_profile` metadata through the execution boundary.
- `tests/test_input_source_contract.py` and `tests/test_request_contract.py` cover hierarchy, PDF fail-closed behavior, and request propagation.