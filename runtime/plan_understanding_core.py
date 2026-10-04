"""Evidence-backed Plan Understanding Core (H98).

Composes the existing detector and PlanModel reconstruction into one
provider-neutral understanding boundary. It does not guess missing semantics:
UNKNOWN/NEEDS_REVIEW/BLOCKED remain unresolved and therefore cannot become PASS.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.locked_element_detection import ConservativeLockedElementDetector
from runtime.plan_model_contract import ConstraintMap, PlanModel
from runtime.plan_model_reconstruction import build_plan_model_from_detection


@dataclass(frozen=True)
class PlanUnderstandingResult:
    """Single structured understanding snapshot for downstream stages."""

    detection: dict[str, Any]
    plan_model: PlanModel
    constraint_map: ConstraintMap
    status: str

    def validate(self) -> None:
        self.plan_model.validate()
        self.constraint_map.validate()
        if self.status not in {"PASS", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"}:
            raise ValueError("PLAN_UNDERSTANDING_STATUS_INVALID")


class PlanUnderstandingCore:
    """Compose source detection -> PlanModel -> ConstraintMap deterministically."""

    core_id = "plan-understanding-core-v0.1"

    def __init__(self, detector: ConservativeLockedElementDetector | None = None):
        self.detector = detector or ConservativeLockedElementDetector()

    def understand(
        self,
        *,
        source_path: str,
        source_sha256: str,
        model_id: str,
        drawing_count: int = 1,
        space_model=None,
    ) -> PlanUnderstandingResult:
        detection = self.detector.detect(source_path, source_sha256)

        reconstruction = build_plan_model_from_detection(
            model_id=model_id,
            source_sha256=source_sha256,
            detection_result=detection,
            drawing_count=drawing_count,
            space_model=space_model,
        )
        plan_model = reconstruction.plan_model

        protected = tuple(
            element.element_id for element in plan_model.elements
            if element.state == "LOCKED"
        )
        editable = tuple(
            element.element_id for element in plan_model.elements
            if element.state == "EDITABLE"
        )
        conditional = tuple(
            element.element_id for element in plan_model.elements
            if element.state == "CONDITIONAL"
        )
        unknown = tuple(
            element.element_id for element in plan_model.elements
            if element.state == "UNKNOWN"
        )

        # Preserve missing fixed architectural types as explicit UNKNOWN
        # constraints. A type-level UNKNOWN is safer than silently omitting it.
        unknown_types = tuple(
            str(item) for item in detection.get("unresolved_fixed_element_types", ())
        )
        unknown = tuple(dict.fromkeys((*unknown, *unknown_types)))

        evidence_ids = tuple(
            evidence.evidence_id
            for evidence in (plan_model.element_evidence.evidences
                             if plan_model.element_evidence is not None else ())
        )
        if not evidence_ids:
            evidence_ids = tuple(
                str(item.get("evidence_id"))
                for item in detection.get("candidates", ())
                for _ in [0]
                if item.get("evidence_id") or item.get("evidence_ids")
            )
            # Candidate payloads normally expose evidence_ids; flatten them.
            flattened = []
            for item in detection.get("candidates", ()):
                flattened.extend(str(x) for x in item.get("evidence_ids", ()))
            evidence_ids = tuple(dict.fromkeys(flattened))

        constraint_map = ConstraintMap(
            map_id=f"{model_id}:constraints",
            model_id=model_id,
            protected_element_ids=protected,
            editable_element_ids=editable,
            conditional_element_ids=conditional,
            unknown_element_ids=unknown,
            evidence_ids=evidence_ids,
        )

        # Any unresolved evidence, missing fixed type, or non-LOCKED fixed
        # candidate keeps the core fail-closed.
        has_unresolved = bool(
            plan_model.unresolved
            or detection.get("unresolved_fixed_element_types")
            or detection.get("status") != "ACCESSIBLE"
            or unknown
        )
        status = "UNKNOWN" if has_unresolved else "PASS"

        result = PlanUnderstandingResult(
            detection=detection,
            plan_model=plan_model,
            constraint_map=constraint_map,
            status=status,
        )
        result.validate()
        return result
