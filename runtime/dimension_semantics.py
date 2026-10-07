"""Deterministic dimension semantics for architectural plans (H100).

This layer separates detected dimension evidence from geometric truth. A
dimension becomes approval-grade only when its text, unit/scale, referenced
geometry, and source evidence are all explicit and consistent.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

DimensionStatus = Literal["SUPPORTED", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"]


@dataclass(frozen=True)
class DimensionReference:
    element_ids: tuple[str, ...]
    geometry_roles: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.element_ids:
            raise ValueError("DIMENSION_REFERENCES_MISSING")
        if any(not item for item in self.element_ids):
            raise ValueError("DIMENSION_REFERENCE_ID_INVALID")
        if len(self.geometry_roles) not in {0, len(self.element_ids)}:
            raise ValueError("DIMENSION_GEOMETRY_ROLE_COUNT_MISMATCH")


@dataclass(frozen=True)
class DimensionSemantic:
    dimension_id: str
    source_sha256: str
    evidence_ids: tuple[str, ...]
    value: float | None
    unit: str
    status: DimensionStatus
    reference: DimensionReference | None
    annotation_id: str | None = None
    tolerance: float | None = None

    def validate(self) -> None:
        if not self.dimension_id or len(self.source_sha256) != 64:
            raise ValueError("DIMENSION_ID_OR_SOURCE_INVALID")
        if not self.evidence_ids:
            raise ValueError("DIMENSION_EVIDENCE_MISSING")
        if self.unit not in {"MM", "CM", "M", "IN", "FT", "UNKNOWN"}:
            raise ValueError("DIMENSION_UNIT_INVALID")
        if self.status not in {"SUPPORTED", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"}:
            raise ValueError("DIMENSION_STATUS_INVALID")
        if self.value is not None and self.value <= 0:
            raise ValueError("DIMENSION_VALUE_INVALID")
        if self.tolerance is not None and self.tolerance < 0:
            raise ValueError("DIMENSION_TOLERANCE_INVALID")
        if self.reference is not None:
            self.reference.validate()
        if self.status == "SUPPORTED":
            if self.value is None or self.unit == "UNKNOWN" or self.reference is None:
                raise ValueError("DIMENSION_PASS_REQUIRES_VALUE_UNIT_REFERENCE")


def build_dimension_semantic(
    *,
    dimension_id: str,
    source_sha256: str,
    evidence_ids: tuple[str, ...],
    value: float | None,
    unit: str,
    reference_element_ids: tuple[str, ...] = (),
    geometry_roles: tuple[str, ...] = (),
    status: DimensionStatus = "UNKNOWN",
    annotation_id: str | None = None,
    tolerance: float | None = None,
) -> DimensionSemantic:
    reference = (
        DimensionReference(reference_element_ids, geometry_roles)
        if reference_element_ids else None
    )
    result = DimensionSemantic(
        dimension_id=dimension_id,
        source_sha256=source_sha256,
        evidence_ids=evidence_ids,
        value=value,
        unit=unit,
        status=status,
        reference=reference,
        annotation_id=annotation_id,
        tolerance=tolerance,
    )
    result.validate()
    return result


def resolve_dimension_status(
    *,
    value: float | None,
    unit: str,
    reference_element_ids: tuple[str, ...],
    evidence_ids: tuple[str, ...],
    source_sha256: str,
    explicit_geometry_association: bool,
) -> DimensionStatus:
    """Resolve only from explicit evidence; never infer a reference."""
    if not evidence_ids:
        return "BLOCKED"
    if value is None or unit == "UNKNOWN":
        return "UNKNOWN"
    if not reference_element_ids:
        return "UNKNOWN"
    if not explicit_geometry_association:
        return "NEEDS_REVIEW"
    return "SUPPORTED"
