"""Deterministic validation boundary for the architectural drawing standards Rule Pack.

The validator intentionally distinguishes PASS, UNKNOWN, and BLOCKED. It never
infers missing scale, units, view identity, sheet metadata, or title-block data.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DrawingStandardsValidation:
    status: str
    checks: dict[str, str]
    evidence_ids: tuple[str, ...]
    unresolved: tuple[str, ...]

    def validate(self) -> None:
        if self.status not in {"PASS", "UNKNOWN", "BLOCKED"}:
            raise ValueError("INVALID_DRAWING_STANDARDS_STATUS")
        if not self.evidence_ids:
            raise ValueError("MISSING_DRAWING_STANDARDS_EVIDENCE")


def _check(value: Any) -> str:
    if value is True:
        return "PASS"
    if value is False:
        return "BLOCKED"
    return "UNKNOWN"


def validate_drawing_standards(
    *,
    source_sha256: str,
    evidence_ids: list[str] | tuple[str, ...],
    metadata: dict[str, Any] | None = None,
    detection: dict[str, Any] | None = None,
) -> DrawingStandardsValidation:
    """Validate only evidence explicitly supplied by upstream extraction.

    The first implementation covers the executable Rule Pack subset. Missing
    evidence is UNKNOWN and therefore cannot support approval.
    """
    metadata = metadata or {}
    detection = detection or {}
    evidence = tuple(str(x) for x in evidence_ids if x)
    if not source_sha256 or not evidence:
        raise ValueError("MISSING_DRAWING_STANDARDS_SOURCE_EVIDENCE")

    checks = {
        "DRAW-SCALE-001": _check(metadata.get("scale_units_consistent")),
        "DRAW-DIM-001": _check(metadata.get("dimensions_geometry_associated")),
        "DRAW-VIEW-001": _check(metadata.get("view_section_identity")),
        "DRAW-SHEET-001": _check(metadata.get("sheet_layout_valid")),
        "DRAW-TITLE-001": _check(metadata.get("title_block_fields_valid")),
        "DRAW-CROSSVIEW-001": _check(metadata.get("cross_view_consistent")),
    }

    unresolved = tuple(
        rule_id for rule_id, result in checks.items() if result != "PASS"
    )

    if any(result == "BLOCKED" for result in checks.values()):
        status = "BLOCKED"
    elif unresolved:
        status = "UNKNOWN"
    else:
        status = "PASS"

    return DrawingStandardsValidation(
        status=status,
        checks=checks,
        evidence_ids=evidence,
        unresolved=unresolved,
    )
