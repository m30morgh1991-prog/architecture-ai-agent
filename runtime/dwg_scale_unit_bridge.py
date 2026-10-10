"""Conservative bridge from native DWG INSUNITS metadata to scale/unit evidence.

A recognized INSUNITS value proves only a unit declaration, not drawing scale
or dimension-to-geometry correspondence. Therefore metadata alone is
NEEDS_REVIEW, never PASS.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any

from runtime.scale_unit_evidence import evaluate_scale_evidence

# DXF $INSUNITS codes. Unsupported and unitless codes intentionally stay unknown.
_INSUNITS_TO_UNIT = {1: "IN", 2: "FT", 4: "MM", 5: "CM", 6: "M"}


def observe_dwg_scale_unit(detection: dict[str, Any], source_sha256: str) -> dict[str, Any]:
    raw_units = detection.get("dwg_units")
    unit = None
    if isinstance(raw_units, int) and not isinstance(raw_units, bool):
        unit = _INSUNITS_TO_UNIT.get(raw_units)

    known_metadata = unit is not None
    evidence = evaluate_scale_evidence(
        source_id=source_sha256,
        unit=unit or "UNKNOWN",
        explicit_unit=None,
        header_unit=None,
        dimension_evidence=False,
        source_metadata=known_metadata,
        evidence_ids=(f"dwg-insunits:{source_sha256}",),
    )
    return asdict(evidence)
