"""H101 geometry reference contract.

Keeps model units, sheet scale, coordinate frame, raster calibration and
dimension reconciliation as separate source-bound evidence domains. This
contract records evidence; it does not infer or normalize geometry.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal

LinearUnit = Literal["MM", "CM", "M", "IN", "FT", "UNKNOWN"]
CoordinateFrame = Literal[
    "WCS", "OCS", "PDF_PAGE", "IMAGE_PIXELS", "IFC_LOCAL", "UNKNOWN"
]
EvidenceStatus = Literal["SUPPORTED", "UNCERTAIN", "CONTRADICTED", "UNKNOWN"]
ScaleBasis = Literal["MODEL_SPACE", "PAPER_SPACE", "RASTER_CALIBRATION", "UNKNOWN"]

_ALLOWED_UNITS = {"MM", "CM", "M", "IN", "FT", "UNKNOWN"}
_ALLOWED_FRAMES = {"WCS", "OCS", "PDF_PAGE", "IMAGE_PIXELS", "IFC_LOCAL", "UNKNOWN"}
_ALLOWED_STATUSES = {"SUPPORTED", "UNCERTAIN", "CONTRADICTED", "UNKNOWN"}
_ALLOWED_SCALE_BASES = {"MODEL_SPACE", "PAPER_SPACE", "RASTER_CALIBRATION", "UNKNOWN"}

_AREA_TO_M2 = {
    "MM": 1e-6,
    "CM": 1e-4,
    "M": 1.0,
    "IN": 0.00064516,
    "FT": 0.09290304,
}


def _finite_tuple(values: tuple[float, ...] | None, expected: int, code: str):
    if values is None:
        return None
    if len(values) != expected:
        raise ValueError(code)
    result = []
    for value in values:
        if isinstance(value, bool):
            raise ValueError(code)
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError):
            raise ValueError(code) from None
        if not isfinite(number):
            raise ValueError(code)
        result.append(number)
    return tuple(result)


def _ids(values: tuple[str, ...], code: str) -> None:
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise ValueError(code)
    if len(values) != len(set(values)):
        raise ValueError(code)


@dataclass(frozen=True)
class GeometryReferenceEvidence:
    evidence_id: str
    source_sha256: str
    domain: str
    status: EvidenceStatus
    source_ref: str
    value: str

    def validate(self, expected_source_sha256: str) -> None:
        if not self.evidence_id or not self.source_ref or not self.value:
            raise ValueError("GEOMETRY_REFERENCE_EVIDENCE_INCOMPLETE")
        if self.source_sha256 != expected_source_sha256:
            raise ValueError("GEOMETRY_REFERENCE_EVIDENCE_SOURCE_MISMATCH")
        if self.domain not in {"COORDINATE_FRAME", "UNIT", "SCALE", "TRANSFORM", "DIMENSION"}:
            raise ValueError("GEOMETRY_REFERENCE_EVIDENCE_DOMAIN_INVALID")
        if self.status not in _ALLOWED_STATUSES:
            raise ValueError("GEOMETRY_REFERENCE_EVIDENCE_STATUS_INVALID")


@dataclass(frozen=True)
class GeometryReference:
    """Verified provenance for interpreting geometry coordinates and areas.

    paper_scale_ratio=(1, 100) describes sheet representation only; it never
    changes model-space coordinates. Raster calibration is represented
    separately by a 3x3 pixel-to-world affine transform.
    """

    reference_id: str
    source_sha256: str
    coordinate_frame: CoordinateFrame = "UNKNOWN"
    coordinate_frame_status: EvidenceStatus = "UNKNOWN"
    linear_unit: LinearUnit = "UNKNOWN"
    unit_status: EvidenceStatus = "UNKNOWN"
    scale_basis: ScaleBasis = "UNKNOWN"
    scale_status: EvidenceStatus = "UNKNOWN"
    paper_scale_ratio: tuple[int, int] | None = None
    pixel_to_world_transform: tuple[float, ...] | None = None
    coordinate_transform_4x4: tuple[float, ...] | None = None
    coordinate_evidence_ids: tuple[str, ...] = ()
    unit_evidence_ids: tuple[str, ...] = ()
    scale_evidence_ids: tuple[str, ...] = ()
    transform_evidence_ids: tuple[str, ...] = ()
    dimension_evidence_ids: tuple[str, ...] = ()
    dimension_reconciliation_status: EvidenceStatus = "UNKNOWN"
    evidence_records: tuple[GeometryReferenceEvidence, ...] = ()

    def validate(self) -> None:
        if not self.reference_id:
            raise ValueError("GEOMETRY_REFERENCE_ID_MISSING")
        if (
            len(self.source_sha256) != 64
            or any(ch not in "0123456789abcdef" for ch in self.source_sha256.lower())
        ):
            raise ValueError("GEOMETRY_REFERENCE_SOURCE_HASH_INVALID")
        if self.coordinate_frame not in _ALLOWED_FRAMES:
            raise ValueError("GEOMETRY_REFERENCE_FRAME_INVALID")
        if self.linear_unit not in _ALLOWED_UNITS:
            raise ValueError("GEOMETRY_REFERENCE_UNIT_INVALID")
        if self.scale_basis not in _ALLOWED_SCALE_BASES:
            raise ValueError("GEOMETRY_REFERENCE_SCALE_BASIS_INVALID")
        for status in (
            self.coordinate_frame_status, self.unit_status, self.scale_status,
            self.dimension_reconciliation_status,
        ):
            if status not in _ALLOWED_STATUSES:
                raise ValueError("GEOMETRY_REFERENCE_STATUS_INVALID")

        for values, code in (
            (self.coordinate_evidence_ids, "GEOMETRY_REFERENCE_COORDINATE_EVIDENCE_INVALID"),
            (self.unit_evidence_ids, "GEOMETRY_REFERENCE_UNIT_EVIDENCE_INVALID"),
            (self.scale_evidence_ids, "GEOMETRY_REFERENCE_SCALE_EVIDENCE_INVALID"),
            (self.transform_evidence_ids, "GEOMETRY_REFERENCE_TRANSFORM_EVIDENCE_INVALID"),
            (self.dimension_evidence_ids, "GEOMETRY_REFERENCE_DIMENSION_EVIDENCE_INVALID"),
        ):
            _ids(values, code)

        evidence_by_id = {}
        for record in self.evidence_records:
            record.validate(self.source_sha256)
            if record.evidence_id in evidence_by_id:
                raise ValueError("GEOMETRY_REFERENCE_EVIDENCE_ID_DUPLICATE")
            evidence_by_id[record.evidence_id] = record
        for ids, domain in (
            (self.coordinate_evidence_ids, "COORDINATE_FRAME"),
            (self.unit_evidence_ids, "UNIT"),
            (self.scale_evidence_ids, "SCALE"),
            (self.transform_evidence_ids, "TRANSFORM"),
            (self.dimension_evidence_ids, "DIMENSION"),
        ):
            for evidence_id in ids:
                record = evidence_by_id.get(evidence_id)
                if record is None or record.domain != domain:
                    raise ValueError("GEOMETRY_REFERENCE_EVIDENCE_REFERENCE_INVALID")

        if self.coordinate_frame_status == "SUPPORTED":
            if self.coordinate_frame == "UNKNOWN" or not self.coordinate_evidence_ids:
                raise ValueError("GEOMETRY_REFERENCE_FRAME_SUPPORT_UNPROVEN")
            if any(evidence_by_id[x].status != "SUPPORTED" for x in self.coordinate_evidence_ids):
                raise ValueError("GEOMETRY_REFERENCE_FRAME_EVIDENCE_NOT_SUPPORTED")
        if self.unit_status == "SUPPORTED":
            if self.linear_unit == "UNKNOWN" or not self.unit_evidence_ids:
                raise ValueError("GEOMETRY_REFERENCE_UNIT_SUPPORT_UNPROVEN")
            if any(evidence_by_id[x].status != "SUPPORTED" for x in self.unit_evidence_ids):
                raise ValueError("GEOMETRY_REFERENCE_UNIT_EVIDENCE_NOT_SUPPORTED")
        if self.scale_status == "SUPPORTED":
            if self.scale_basis == "UNKNOWN" or not self.scale_evidence_ids:
                raise ValueError("GEOMETRY_REFERENCE_SCALE_SUPPORT_UNPROVEN")
            if any(evidence_by_id[x].status != "SUPPORTED" for x in self.scale_evidence_ids):
                raise ValueError("GEOMETRY_REFERENCE_SCALE_EVIDENCE_NOT_SUPPORTED")
        if self.dimension_reconciliation_status == "SUPPORTED":
            if not self.dimension_evidence_ids:
                raise ValueError("GEOMETRY_REFERENCE_DIMENSION_SUPPORT_UNPROVEN")
            if any(evidence_by_id[x].status != "SUPPORTED" for x in self.dimension_evidence_ids):
                raise ValueError("GEOMETRY_REFERENCE_DIMENSION_EVIDENCE_NOT_SUPPORTED")

        if self.paper_scale_ratio is not None:
            if len(self.paper_scale_ratio) != 2:
                raise ValueError("GEOMETRY_REFERENCE_PAPER_SCALE_INVALID")
            numerator, denominator = self.paper_scale_ratio
            if (
                isinstance(numerator, bool) or isinstance(denominator, bool)
                or not isinstance(numerator, int) or not isinstance(denominator, int)
                or numerator <= 0 or denominator <= 0
            ):
                raise ValueError("GEOMETRY_REFERENCE_PAPER_SCALE_INVALID")
        if self.scale_basis == "PAPER_SPACE" and self.scale_status == "SUPPORTED":
            if self.paper_scale_ratio is None:
                raise ValueError("GEOMETRY_REFERENCE_PAPER_SCALE_MISSING")

        pixel_transform = _finite_tuple(
            self.pixel_to_world_transform, 9, "GEOMETRY_REFERENCE_PIXEL_TRANSFORM_INVALID"
        )
        if pixel_transform is not None:
            if not self.transform_evidence_ids or any(
                evidence_by_id[x].status != "SUPPORTED" for x in self.transform_evidence_ids
            ):
                raise ValueError("GEOMETRY_REFERENCE_TRANSFORM_EVIDENCE_UNPROVEN")
            # A 3x3 affine transform uses homogeneous coordinates [0, 0, 1]
            # in its final row. A projective matrix must not be accepted here.
            if (
                abs(pixel_transform[6]) > 1e-12
                or abs(pixel_transform[7]) > 1e-12
                or abs(pixel_transform[8] - 1.0) > 1e-12
            ):
                raise ValueError("GEOMETRY_REFERENCE_PIXEL_TRANSFORM_NOT_AFFINE")
            a, b, _, c, d, _, _, _, _ = pixel_transform
            if abs(a * d - b * c) <= 1e-12:
                raise ValueError("GEOMETRY_REFERENCE_PIXEL_TRANSFORM_SINGULAR")
            if not self.transform_evidence_ids:
                raise ValueError("GEOMETRY_REFERENCE_TRANSFORM_EVIDENCE_MISSING")
        _finite_tuple(
            self.coordinate_transform_4x4, 16,
            "GEOMETRY_REFERENCE_COORDINATE_TRANSFORM_INVALID",
        )
        if self.coordinate_transform_4x4 is not None:
            if not self.transform_evidence_ids:
                raise ValueError("GEOMETRY_REFERENCE_TRANSFORM_EVIDENCE_MISSING")
            if any(evidence_by_id[x].status != "SUPPORTED" for x in self.transform_evidence_ids):
                raise ValueError("GEOMETRY_REFERENCE_TRANSFORM_EVIDENCE_UNPROVEN")
        if (
            self.scale_basis == "RASTER_CALIBRATION"
            and self.scale_status == "SUPPORTED"
            and pixel_transform is None
        ):
            raise ValueError("GEOMETRY_REFERENCE_RASTER_CALIBRATION_MISSING")

    @property
    def area_unit(self) -> str:
        return "UNKNOWN" if self.unit_status != "SUPPORTED" else f"{self.linear_unit}^2"

    @property
    def square_metre_factor(self) -> float | None:
        if self.unit_status != "SUPPORTED":
            return None
        return _AREA_TO_M2.get(self.linear_unit)

    @property
    def can_report_area_m2(self) -> bool:
        return self.square_metre_factor is not None


def build_geometry_reference(**data) -> GeometryReference:
    """Build and validate a GeometryReference from a JSON-like mapping."""
    for key in (
        "paper_scale_ratio", "pixel_to_world_transform", "coordinate_transform_4x4",
        "coordinate_evidence_ids", "unit_evidence_ids", "scale_evidence_ids",
        "transform_evidence_ids", "dimension_evidence_ids", "evidence_records",
    ):
        if data.get(key) is not None:
            data[key] = tuple(data[key])
    if data.get("evidence_records") is not None:
        data["evidence_records"] = tuple(
            item if isinstance(item, GeometryReferenceEvidence)
            else GeometryReferenceEvidence(**item)
            for item in data["evidence_records"]
        )
    reference = GeometryReference(**data)
    reference.validate()
    return reference
