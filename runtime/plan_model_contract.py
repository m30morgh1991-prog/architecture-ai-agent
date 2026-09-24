"""Evidence-backed PlanModel and ConstraintMap contracts."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Literal

ConstraintState = Literal["LOCKED","EDITABLE","CONDITIONAL","UNKNOWN"]

@dataclass(frozen=True)
class PlanElement:
    element_id: str
    element_type: str
    state: ConstraintState
    geometry: dict[str, Any]
    evidence_ids: tuple[str, ...]
    confidence: float

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

@dataclass(frozen=True)
class PlanModel:
    model_id: str
    source_sha256: str
    drawing_count: int
    elements: tuple[PlanElement, ...]
    unresolved: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.model_id or not self.source_sha256:
            raise ValueError("INVALID_PLAN_MODEL")
        if self.drawing_count < 1:
            raise ValueError("INVALID_DRAWING_COUNT")
        for element in self.elements:
            element.validate()

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
