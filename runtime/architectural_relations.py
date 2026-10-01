"""H72 evidence-backed architectural relations contract.

Relations connect reconstructed architectural elements and spaces without
promoting uncertain topology into architectural truth. Every relation is
source-bound, evidence-backed, and fail-closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from runtime.plan_model_contract import PlanModel

RelationKind = Literal[
    "ELEMENT_ADJACENCY",
    "ELEMENT_CONTAINS",
    "ELEMENT_INTERSECTS",
    "SPACE_BOUNDARY_ELEMENT",
    "SPACE_OPENING_ELEMENT",
    "SPACE_ADJACENCY",
]
RelationStatus = Literal["SUPPORTED", "UNCERTAIN", "CONTRADICTED", "UNKNOWN"]

ALLOWED_RELATION_KINDS = frozenset({
    "ELEMENT_ADJACENCY",
    "ELEMENT_CONTAINS",
    "ELEMENT_INTERSECTS",
    "SPACE_BOUNDARY_ELEMENT",
    "SPACE_OPENING_ELEMENT",
    "SPACE_ADJACENCY",
})
ALLOWED_RELATION_STATUSES = frozenset({
    "SUPPORTED", "UNCERTAIN", "CONTRADICTED", "UNKNOWN",
})


@dataclass(frozen=True)
class ArchitecturalRelation:
    relation_id: str
    source_sha256: str
    relation_kind: RelationKind
    from_id: str
    to_id: str
    evidence_ids: tuple[str, ...]
    status: RelationStatus = "UNKNOWN"
    confidence: float = 0.0

    def validate(self) -> None:
        if not self.relation_id or not self.source_sha256:
            raise ValueError("ARCH_RELATION_ID_OR_SOURCE_MISSING")
        if len(self.source_sha256) != 64:
            raise ValueError("ARCH_RELATION_SOURCE_INVALID")
        if self.relation_kind not in ALLOWED_RELATION_KINDS:
            raise ValueError("ARCH_RELATION_KIND_INVALID")
        if not self.from_id or not self.to_id or self.from_id == self.to_id:
            raise ValueError("ARCH_RELATION_ENDPOINT_INVALID")
        if not self.evidence_ids:
            raise ValueError("ARCH_RELATION_EVIDENCE_MISSING")
        if self.status not in ALLOWED_RELATION_STATUSES:
            raise ValueError("ARCH_RELATION_STATUS_INVALID")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("ARCH_RELATION_CONFIDENCE_INVALID")
        if self.status in {"UNKNOWN", "CONTRADICTED"} and self.confidence > 0.95:
            raise ValueError("UNCERTAIN_RELATION_CANNOT_HAVE_HIGH_CONFIDENCE")


@dataclass(frozen=True)
class ArchitecturalRelationSet:
    set_id: str
    source_sha256: str
    relations: tuple[ArchitecturalRelation, ...]
    unresolved: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.set_id or not self.source_sha256:
            raise ValueError("ARCH_RELATION_SET_ID_OR_SOURCE_MISSING")
        if len(self.source_sha256) != 64:
            raise ValueError("ARCH_RELATION_SET_SOURCE_INVALID")
        ids = {relation.relation_id for relation in self.relations}
        if len(ids) != len(self.relations):
            raise ValueError("ARCH_RELATION_ID_DUPLICATE")
        for relation in self.relations:
            relation.validate()
            if relation.source_sha256 != self.source_sha256:
                raise ValueError("ARCH_RELATION_SOURCE_MISMATCH")
        if not set(self.unresolved).issubset(ids):
            raise ValueError("ARCH_RELATION_UNRESOLVED_UNKNOWN")


def build_architectural_relation_set(
    *,
    set_id: str,
    plan_model: PlanModel,
    relations: list[dict],
) -> ArchitecturalRelationSet:
    plan_model.validate()
    source_sha256 = plan_model.source_sha256
    known_ids = {element.element_id for element in plan_model.elements}
    if plan_model.space_model is not None:
        known_ids.update(space.space_id for space in plan_model.space_model.spaces)

    records = tuple(
        ArchitecturalRelation(
            relation_id=str(item["relation_id"]),
            source_sha256=str(item.get("source_sha256", source_sha256)),
            relation_kind=str(item["relation_kind"]),
            from_id=str(item["from_id"]),
            to_id=str(item["to_id"]),
            evidence_ids=tuple(str(x) for x in item.get("evidence_ids", ())),
            status=str(item.get("status", "UNKNOWN")),
            confidence=float(item.get("confidence", 0.0)),
        )
        for item in relations
    )
    for relation in records:
        if relation.from_id not in known_ids or relation.to_id not in known_ids:
            raise ValueError("ARCH_RELATION_ENDPOINT_UNKNOWN")
        relation.validate()

        if plan_model.element_evidence is not None:
            available = {
                evidence.evidence_id
                for evidence in plan_model.element_evidence.evidences
            }
            if not set(relation.evidence_ids).issubset(available):
                raise ValueError("ARCH_RELATION_EVIDENCE_REFERENCE_MISSING")

    result = ArchitecturalRelationSet(
        set_id=set_id,
        source_sha256=source_sha256,
        relations=records,
        unresolved=tuple(
            relation.relation_id
            for relation in records
            if relation.status != "SUPPORTED"
        ),
    )
    result.validate()
    return result
