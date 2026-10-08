"""H100 semantic evidence contracts for architectural drawing language.

This layer does not create a second PlanModel. It normalizes drawing-language
observations (symbols, dimensions, levels, markers, hatch, scale/unit and
metadata) as source-bound evidence that can be reconciled into the canonical
PlanModel/ConstraintMap chain.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

EvidenceStatus = Literal["SUPPORTED","UNCERTAIN","CONTRADICTED","UNKNOWN"]
EvidenceDomain = Literal[
    "SYMBOL","LINEWORK","TEXT","DIMENSION","LEVEL","SECTION_MARKER",
    "ELEVATION_MARKER","HATCH","STRUCTURE","SCALE_UNIT","TITLE_BLOCK","TOPOLOGY"
]

_ALLOWED_STATUSES={"SUPPORTED","UNCERTAIN","CONTRADICTED","UNKNOWN"}
_ALLOWED_DOMAINS={"SYMBOL","LINEWORK","TEXT","DIMENSION","LEVEL","SECTION_MARKER",
                  "ELEVATION_MARKER","HATCH","STRUCTURE","SCALE_UNIT","TITLE_BLOCK","TOPOLOGY"}

@dataclass(frozen=True)
class DrawingEvidence:
    evidence_id: str
    source_sha256: str
    domain: EvidenceDomain
    subject_id: str
    predicate: str
    value: str
    status: EvidenceStatus
    confidence: float
    source_ref: str
    notes: str = ""

    def validate(self) -> None:
        if not self.evidence_id or not self.source_sha256 or len(self.source_sha256) != 64:
            raise ValueError("DRAWING_EVIDENCE_SOURCE_INVALID")
        if self.domain not in _ALLOWED_DOMAINS:
            raise ValueError("DRAWING_EVIDENCE_DOMAIN_INVALID")
        if not self.subject_id or not self.predicate or not self.value:
            raise ValueError("DRAWING_EVIDENCE_CONTENT_MISSING")
        if self.status not in _ALLOWED_STATUSES:
            raise ValueError("DRAWING_EVIDENCE_STATUS_INVALID")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("DRAWING_EVIDENCE_CONFIDENCE_INVALID")
        if not self.source_ref:
            raise ValueError("DRAWING_EVIDENCE_PROVENANCE_MISSING")
        if self.status in {"UNKNOWN","CONTRADICTED"} and self.confidence > 0.95:
            raise ValueError("UNRESOLVED_EVIDENCE_HIGH_CONFIDENCE")

@dataclass(frozen=True)
class DrawingEvidenceSet:
    set_id: str
    source_sha256: str
    evidences: tuple[DrawingEvidence,...]
    unresolved: tuple[str,...]=()

    def validate(self) -> None:
        if not self.set_id or len(self.source_sha256) != 64:
            raise ValueError("DRAWING_EVIDENCE_SET_INVALID")
        ids=[x.evidence_id for x in self.evidences]
        if len(ids)!=len(set(ids)):
            raise ValueError("DRAWING_EVIDENCE_ID_DUPLICATE")
        for item in self.evidences:
            item.validate()
            if item.source_sha256 != self.source_sha256:
                raise ValueError("DRAWING_EVIDENCE_SOURCE_MISMATCH")
        if any(not x for x in self.unresolved):
            raise ValueError("DRAWING_EVIDENCE_UNRESOLVED_INVALID")

    def for_subject(self, subject_id: str) -> tuple[DrawingEvidence,...]:
        return tuple(x for x in self.evidences if x.subject_id == subject_id)

@dataclass(frozen=True)
class DimensionEvidence:
    dimension_id: str
    evidence_id: str
    measured_geometry_ids: tuple[str,...]
    extension_geometry_ids: tuple[str,...]
    value: float | None
    unit: str
    status: EvidenceStatus

    def validate(self) -> None:
        if not self.dimension_id or not self.evidence_id:
            raise ValueError("DIMENSION_ID_MISSING")
        if not self.measured_geometry_ids or not self.extension_geometry_ids:
            raise ValueError("DIMENSION_GEOMETRY_REFERENCE_MISSING")
        if self.value is None or self.value <= 0:
            raise ValueError("DIMENSION_VALUE_UNKNOWN")
        if not self.unit:
            raise ValueError("DIMENSION_UNIT_MISSING")
        if self.status not in _ALLOWED_STATUSES:
            raise ValueError("DIMENSION_STATUS_INVALID")

@dataclass(frozen=True)
class LevelEvidence:
    level_id: str
    evidence_id: str
    label: str
    elevation: float | None
    unit: str
    floor_id: str | None
    status: EvidenceStatus

    def validate(self) -> None:
        if not self.level_id or not self.evidence_id or not self.label:
            raise ValueError("LEVEL_EVIDENCE_ID_MISSING")
        if self.elevation is None:
            raise ValueError("LEVEL_ELEVATION_UNKNOWN")
        if not self.unit:
            raise ValueError("LEVEL_UNIT_MISSING")
        if self.status not in _ALLOWED_STATUSES:
            raise ValueError("LEVEL_STATUS_INVALID")

@dataclass(frozen=True)
class ViewMarkerEvidence:
    marker_id: str
    evidence_id: str
    marker_type: Literal["SECTION","ELEVATION"]
    direction: str | None
    cut_plane: str | None
    target_view_id: str | None
    referenced_element_ids: tuple[str,...]
    status: EvidenceStatus

    def validate(self) -> None:
        if not self.marker_id or not self.evidence_id:
            raise ValueError("VIEW_MARKER_ID_MISSING")
        if self.marker_type not in {"SECTION","ELEVATION"}:
            raise ValueError("VIEW_MARKER_TYPE_INVALID")
        if not self.referenced_element_ids:
            raise ValueError("VIEW_MARKER_REFERENCES_MISSING")
        if self.status not in _ALLOWED_STATUSES:
            raise ValueError("VIEW_MARKER_STATUS_INVALID")
        if self.marker_type=="SECTION" and self.status=="SUPPORTED":
            if not self.direction or not self.cut_plane:
                raise ValueError("SECTION_MARKER_SEMANTICS_INCOMPLETE")

def build_drawing_evidence_set(*, set_id: str, source_sha256: str,
                               records: list[dict]) -> DrawingEvidenceSet:
    result=DrawingEvidenceSet(
        set_id=set_id, source_sha256=source_sha256,
        evidences=tuple(DrawingEvidence(
            evidence_id=str(x["evidence_id"]), source_sha256=str(x.get("source_sha256",source_sha256)),
            domain=str(x["domain"]), subject_id=str(x["subject_id"]),
            predicate=str(x["predicate"]), value=str(x["value"]),
            status=str(x.get("status","UNKNOWN")), confidence=float(x.get("confidence",0.0)),
            source_ref=str(x["source_ref"]), notes=str(x.get("notes","")),
        ) for x in records),
        unresolved=tuple(str(x) for x in (
            record.get("subject_id","") for record in records
            if record.get("status","UNKNOWN") != "SUPPORTED"
        )),
    )
    result.validate()
    return result
