"""Evidence-backed PlanModel and ConstraintMap contracts.

H63 adds the validated SpaceModel as a first-class structural component of
PlanModel. H70 binds the source-bound H69 ElementEvidenceBundle so a
reconstructed PlanModel remains traceable to its evidence and fail-closed.
H77 adds optional BIM-ready semantic identity and relationship graph support.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from runtime.bim_ready_contract import BIMElementIdentity, BIMElementRelation, validate_bim_graph
from runtime.element_evidence_contract import ElementEvidenceBundle
from runtime.space_model_contract import SpaceModel

ConstraintState = Literal["LOCKED", "EDITABLE", "CONDITIONAL", "UNKNOWN"]


@dataclass(frozen=True)
class PlanElement:
    element_id: str
    element_type: str
    state: ConstraintState
    geometry: dict[str, Any]
    evidence_ids: tuple[str, ...]
    confidence: float
    bim_identity: BIMElementIdentity | None = None

    def validate(self) -> None:
        if not self.element_id or not self.element_type:
            raise ValueError("INVALID_PLAN_ELEMENT")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("INVALID_CONFIDENCE")
        if not self.evidence_ids:
            raise ValueError("MISSING_ELEMENT_EVIDENCE")
        if self.state == "LOCKED" and self.confidence < 0.95:
            raise ValueError("LOCKED_ELEMENT_CONFIDENCE_TOO_LOW")
        if self.state == "EDITABLE" and self.confidence < 0.90:
            raise ValueError("EDITABLE_ELEMENT_CONFIDENCE_TOO_LOW")
        if self.bim_identity is not None:
            self.bim_identity.validate()


@dataclass(frozen=True)
class PlanModel:
    model_id: str
    source_sha256: str
    drawing_count: int
    elements: tuple[PlanElement, ...]
    unresolved: tuple[str, ...] = ()
    space_model: SpaceModel | None = None
    element_evidence: ElementEvidenceBundle | None = None
    bim_relations: tuple[BIMElementRelation, ...] = ()

    def validate(self) -> None:
        if not self.model_id or not self.source_sha256:
            raise ValueError("INVALID_PLAN_MODEL")
        if len(self.source_sha256) != 64:
            raise ValueError("INVALID_PLAN_MODEL_SOURCE")
        if self.drawing_count < 1:
            raise ValueError("INVALID_DRAWING_COUNT")

        element_ids = [element.element_id for element in self.elements]
        if len(element_ids) != len(set(element_ids)):
            raise ValueError("PLAN_ELEMENT_ID_DUPLICATE")

        for element in self.elements:
            element.validate()

        validate_bim_graph(set(element_ids), self.bim_relations)

        if self.element_evidence is not None:
            self.element_evidence.validate()
            if self.element_evidence.source_sha256 != self.source_sha256:
                raise ValueError("ELEMENT_EVIDENCE_SOURCE_MISMATCH")
            evidence_ids = {item.evidence_id for item in self.element_evidence.evidences}
            for element in self.elements:
                if not set(element.evidence_ids).issubset(evidence_ids):
                    raise ValueError("PLAN_ELEMENT_EVIDENCE_REFERENCE_MISSING")

        if self.space_model is not None:
            self.space_model.validate()
            if self.space_model.source_sha256 != self.source_sha256:
                raise ValueError("SPACE_MODEL_SOURCE_MISMATCH")

    @property
    def spaces(self):
        if self.space_model is None:
            return ()
        return self.space_model.spaces

    @property
    def space_relations(self):
        if self.space_model is None:
            return ()
        return self.space_model.relations


@dataclass(frozen=True)
class ConstraintMap:
    map_id: str
    model_id: str
    protected_element_ids: tuple[str, ...]
    editable_element_ids: tuple[str, ...]
    conditional_element_ids: tuple[str, ...]
    unknown_element_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]

    def validate(self) -> None:
        if not self.map_id or not self.model_id:
            raise ValueError("INVALID_CONSTRAINT_MAP")
        if not self.evidence_ids:
            raise ValueError("MISSING_CONSTRAINT_EVIDENCE")
        buckets = [
            set(self.protected_element_ids),
            set(self.editable_element_ids),
            set(self.conditional_element_ids),
            set(self.unknown_element_ids),
        ]
        for i in range(len(buckets)):
            for j in range(i + 1, len(buckets)):
                if buckets[i] & buckets[j]:
                    raise ValueError("CONSTRAINT_STATE_OVERLAP")
