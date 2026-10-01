"""H69 evidence contract for architectural element candidates.

Evidence is traceable, typed, source-bound, and fail-closed. This contract
does not promote candidates to architectural truth or LOCKED state.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

EvidenceKind = Literal[
    "DWG_ENTITY",
    "DWG_LAYER",
    "DWG_GEOMETRY",
    "DWG_TEXT",
    "PDF_VECTOR",
    "PDF_TEXT",
    "DERIVED_GEOMETRY",
    "UNKNOWN",
]

ElementEvidenceStatus = Literal["SUPPORTED", "UNCERTAIN", "CONTRADICTED", "UNKNOWN"]

ALLOWED_ELEMENT_TYPES = frozenset({
    "COLUMNS",
    "OUTER_BOUNDARY",
    "WALLS",
    "DOORS",
    "WINDOWS",
    "OVERALL_PLAN_FORM",
})


@dataclass(frozen=True)
class ElementEvidence:
    evidence_id: str
    source_sha256: str
    kind: EvidenceKind
    element_type: str
    status: ElementEvidenceStatus
    description: str
    native_id: str | None = None
    confidence: float = 0.0

    def validate(self) -> None:
        if not self.evidence_id or not self.source_sha256:
            raise ValueError("ELEMENT_EVIDENCE_ID_OR_SOURCE_MISSING")
        if len(self.source_sha256) != 64:
            raise ValueError("ELEMENT_EVIDENCE_SOURCE_INVALID")
        if self.element_type not in ALLOWED_ELEMENT_TYPES:
            raise ValueError("ELEMENT_EVIDENCE_ELEMENT_TYPE_INVALID")
        if self.kind not in {
            "DWG_ENTITY", "DWG_LAYER", "DWG_GEOMETRY", "DWG_TEXT",
            "PDF_VECTOR", "PDF_TEXT", "DERIVED_GEOMETRY", "UNKNOWN",
        }:
            raise ValueError("ELEMENT_EVIDENCE_KIND_INVALID")
        if self.status not in {"SUPPORTED", "UNCERTAIN", "CONTRADICTED", "UNKNOWN"}:
            raise ValueError("ELEMENT_EVIDENCE_STATUS_INVALID")
        if not self.description:
            raise ValueError("ELEMENT_EVIDENCE_DESCRIPTION_MISSING")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("ELEMENT_EVIDENCE_CONFIDENCE_INVALID")
        if self.status in {"UNKNOWN", "CONTRADICTED"} and self.confidence > 0.95:
            raise ValueError("UNCERTAIN_EVIDENCE_CANNOT_HAVE_HIGH_CONFIDENCE")


@dataclass(frozen=True)
class ElementEvidenceBundle:
    bundle_id: str
    source_sha256: str
    evidences: tuple[ElementEvidence, ...]
    unresolved_element_types: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.bundle_id or not self.source_sha256:
            raise ValueError("ELEMENT_EVIDENCE_BUNDLE_ID_OR_SOURCE_MISSING")
        if len(self.source_sha256) != 64:
            raise ValueError("ELEMENT_EVIDENCE_BUNDLE_SOURCE_INVALID")

        ids = {item.evidence_id for item in self.evidences}
        if len(ids) != len(self.evidences):
            raise ValueError("ELEMENT_EVIDENCE_ID_DUPLICATE")

        for item in self.evidences:
            item.validate()
            if item.source_sha256 != self.source_sha256:
                raise ValueError("ELEMENT_EVIDENCE_SOURCE_MISMATCH")

        unknown = set(self.unresolved_element_types)
        if not unknown.issubset(ALLOWED_ELEMENT_TYPES):
            raise ValueError("ELEMENT_EVIDENCE_UNRESOLVED_TYPE_INVALID")

    def evidence_for(self, element_type: str) -> tuple[ElementEvidence, ...]:
        if element_type not in ALLOWED_ELEMENT_TYPES:
            raise ValueError("ELEMENT_EVIDENCE_ELEMENT_TYPE_INVALID")
        return tuple(
            item for item in self.evidences
            if item.element_type == element_type
        )


def build_element_evidence_bundle(
    *,
    bundle_id: str,
    source_sha256: str,
    evidences: list[dict],
    unresolved_element_types: list[str] | tuple[str, ...] = (),
) -> ElementEvidenceBundle:
    bundle = ElementEvidenceBundle(
        bundle_id=bundle_id,
        source_sha256=source_sha256,
        evidences=tuple(
            ElementEvidence(
                evidence_id=str(item["evidence_id"]),
                source_sha256=str(item.get("source_sha256", source_sha256)),
                kind=str(item.get("kind", "UNKNOWN")),
                element_type=str(item["element_type"]),
                status=str(item.get("status", "UNKNOWN")),
                description=str(item["description"]),
                native_id=item.get("native_id"),
                confidence=float(item.get("confidence", 0.0)),
            )
            for item in evidences
        ),
        unresolved_element_types=tuple(str(x) for x in unresolved_element_types),
    )
    bundle.validate()
    return bundle
