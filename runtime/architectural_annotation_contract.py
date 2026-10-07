"""Evidence-backed architectural drawing annotations (H100).

Annotations are first-class drawing semantics but never override PlanModel
geometry or constraints. Missing/contradictory evidence remains unresolved.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AnnotationType = Literal[
    "DIMENSION", "LEVEL", "ELEVATION", "SECTION_MARKER", "GRID",
    "ROOM_LABEL", "NORTH_ARROW", "SCALE", "TITLE_BLOCK", "DETAIL_MARKER",
]
AnnotationStatus = Literal["SUPPORTED", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"]

_ALLOWED_TYPES = {
    "DIMENSION", "LEVEL", "ELEVATION", "SECTION_MARKER", "GRID",
    "ROOM_LABEL", "NORTH_ARROW", "SCALE", "TITLE_BLOCK", "DETAIL_MARKER",
}


@dataclass(frozen=True)
class ArchitecturalAnnotation:
    annotation_id: str
    annotation_type: AnnotationType
    source_sha256: str
    evidence_ids: tuple[str, ...]
    geometry: dict
    text: str | None = None
    status: AnnotationStatus = "UNKNOWN"

    def validate(self) -> None:
        if not self.annotation_id or not self.source_sha256:
            raise ValueError("ANNOTATION_ID_OR_SOURCE_INVALID")
        if len(self.source_sha256) != 64:
            raise ValueError("ANNOTATION_SOURCE_INVALID")
        if self.annotation_type not in _ALLOWED_TYPES:
            raise ValueError("ANNOTATION_TYPE_INVALID")
        if not self.evidence_ids:
            raise ValueError("ANNOTATION_EVIDENCE_MISSING")
        if not isinstance(self.geometry, dict):
            raise ValueError("ANNOTATION_GEOMETRY_INVALID")
        if self.status not in {"SUPPORTED", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"}:
            raise ValueError("ANNOTATION_STATUS_INVALID")
        if self.status == "SUPPORTED" and not self.text and self.annotation_type in {
            "DIMENSION", "LEVEL", "ELEVATION", "ROOM_LABEL", "GRID", "SECTION_MARKER",
            "DETAIL_MARKER",
        }:
            raise ValueError("ANNOTATION_SUPPORTED_TEXT_MISSING")


def validate_annotation_set(source_sha256: str, annotations: tuple[ArchitecturalAnnotation, ...]) -> None:
    if len(source_sha256) != 64:
        raise ValueError("ANNOTATION_SET_SOURCE_INVALID")
    ids = [item.annotation_id for item in annotations]
    if len(ids) != len(set(ids)):
        raise ValueError("ANNOTATION_ID_DUPLICATE")
    for item in annotations:
        item.validate()
        if item.source_sha256 != source_sha256:
            raise ValueError("ANNOTATION_SOURCE_MISMATCH")
