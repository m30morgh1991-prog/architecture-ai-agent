"""Provider-neutral adapters for external floor-plan research outputs.

External projects are optional evidence producers. They never own PlanModel,
ConstraintMap, editability, approval, or execution decisions.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .plan_model_contract import PlanElement, PlanModel

_ALLOWED_TYPES = {
    "wall": "WALLS", "walls": "WALLS",
    "door": "DOORS", "doors": "DOORS",
    "window": "WINDOWS", "windows": "WINDOWS",
    "room": "SPACE", "rooms": "SPACE", "space": "SPACE",
    "furniture": "FURNITURE",
    "boundary": "OUTER_BOUNDARY",
}

@dataclass(frozen=True)
class DetectionItem:
    element_id: str
    element_type: str
    geometry: dict[str, Any]
    evidence_ids: tuple[str, ...]
    confidence: float
    state: str = "UNKNOWN"

    def to_plan_element(self) -> PlanElement:
        element = PlanElement(
            element_id=self.element_id,
            element_type=self.element_type,
            state=self.state if self.state in {"LOCKED","EDITABLE","CONDITIONAL","UNKNOWN"} else "UNKNOWN",
            geometry=dict(self.geometry),
            evidence_ids=self.evidence_ids,
            confidence=float(self.confidence),
        )
        element.validate()
        return element

class ExternalDetectionAdapter:
    """Normalize external detector output into our evidence-backed model.

    Accepted input is deliberately generic: a mapping containing elements,
    or an iterable of element mappings. Common floor-plan fields are tolerated.
    Unknown or unsupported types remain UNKNOWN rather than being guessed.
    """

    adapter_id = "external-detection-normalizer-v0.1"

    def normalize_items(self, payload: Any, *, evidence_prefix: str) -> tuple[DetectionItem, ...]:
        raw = payload.get("elements", []) if isinstance(payload, dict) else payload
        if raw is None:
            raw = []
        result: list[DetectionItem] = []
        for index, item in enumerate(raw, 1):
            if not isinstance(item, dict):
                continue
            raw_type = str(item.get("element_type", item.get("type", item.get("class", "")))).strip().lower()
            element_type = _ALLOWED_TYPES.get(raw_type, "UNKNOWN")
            element_id = str(item.get("element_id", item.get("id", f"EXT-{index:04d}")))
            geometry = item.get("geometry") or item.get("bbox") or {}
            if isinstance(geometry, (list, tuple)):
                geometry = {"bbox": list(geometry)}
            elif not isinstance(geometry, dict):
                geometry = {"raw": geometry}
            try:
                confidence = max(0.0, min(1.0, float(item.get("confidence", 0.0))))
            except (TypeError, ValueError):
                confidence = 0.0
            source_evidence = item.get("evidence_ids") or (f"{evidence_prefix}-{index}",)
            if isinstance(source_evidence, str):
                source_evidence = (source_evidence,)
            state = str(item.get("state", "UNKNOWN")).upper()
            if state == "LOCKED" and confidence < 0.95:
                state = "UNKNOWN"
            if state == "EDITABLE" and confidence < 0.90:
                state = "UNKNOWN"
            result.append(DetectionItem(
                element_id=element_id,
                element_type=element_type,
                geometry=geometry,
                evidence_ids=tuple(str(x) for x in source_evidence if x),
                confidence=confidence,
                state=state if state in {"LOCKED","EDITABLE","CONDITIONAL","UNKNOWN"} else "UNKNOWN",
            ))
        return tuple(result)

    def to_plan_model(self, payload: Any, *, model_id: str, source_sha256: str,
                       drawing_count: int, evidence_prefix: str) -> PlanModel:
        items = self.normalize_items(payload, evidence_prefix=evidence_prefix)
        elements = tuple(item.to_plan_element() for item in items)
        unresolved = tuple(sorted({item.element_type for item in items if item.element_type == "UNKNOWN"}))
        model = PlanModel(
            model_id=model_id,
            source_sha256=source_sha256,
            drawing_count=drawing_count,
            elements=elements,
            unresolved=unresolved,
        )
        model.validate()
        return model
