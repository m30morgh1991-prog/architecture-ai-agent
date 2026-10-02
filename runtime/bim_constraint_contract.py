"""H78 BIM-to-Constraint binding contract.

Binds BIM semantic categories to PlanModel edit constraints without making BIM
a source of truth. Contradictions fail closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from runtime.bim_ready_contract import BIMElementIdentity
from runtime.plan_model_contract import ConstraintState, PlanElement

BindingStatus = Literal["PASS", "NEEDS_REVIEW", "BLOCKED", "UNKNOWN"]

PROTECTED_BIM_CATEGORIES = {
    "Column", "StructuralColumn", "Wall", "CurtainWall",
    "Door", "Window", "Building", "SiteBoundary",
}
EDITABLE_BIM_CATEGORIES = {
    "Furniture", "FurnitureElement", "Casework", "Equipment",
}
CONDITIONAL_BIM_CATEGORIES = {
    "Room", "Space", "Floor", "Ceiling", "Stair", "Railing",
}


@dataclass(frozen=True)
class BIMConstraintBinding:
    element_id: str
    category: str
    expected_state: ConstraintState
    evidence_ids: tuple[str, ...]

    def validate(self) -> None:
        if not self.element_id or not self.category:
            raise ValueError("BIM_CONSTRAINT_BINDING_ID_MISSING")
        if self.expected_state not in {"LOCKED", "EDITABLE", "CONDITIONAL", "UNKNOWN"}:
            raise ValueError("BIM_CONSTRAINT_STATE_INVALID")
        if not self.evidence_ids:
            raise ValueError("BIM_CONSTRAINT_EVIDENCE_MISSING")


@dataclass(frozen=True)
class BIMConstraintEvaluation:
    status: BindingStatus
    reasons: tuple[str, ...] = ()


def expected_constraint_state(identity: BIMElementIdentity) -> ConstraintState:
    identity.validate()
    if identity.category in PROTECTED_BIM_CATEGORIES:
        return "LOCKED"
    if identity.category in EDITABLE_BIM_CATEGORIES:
        return "EDITABLE"
    if identity.category in CONDITIONAL_BIM_CATEGORIES:
        return "CONDITIONAL"
    return "UNKNOWN"


def evaluate_bim_constraint_binding(
    element: PlanElement,
    binding: BIMConstraintBinding,
) -> BIMConstraintEvaluation:
    binding.validate()
    if binding.element_id != element.element_id:
        return BIMConstraintEvaluation(
            "BLOCKED", ("BIM_CONSTRAINT_ELEMENT_ID_MISMATCH",)
        )
    if element.bim_identity is None:
        return BIMConstraintEvaluation("UNKNOWN", ("BIM_IDENTITY_MISSING",))

    derived = expected_constraint_state(element.bim_identity)
    if derived == "UNKNOWN":
        return BIMConstraintEvaluation(
            "UNKNOWN", ("BIM_CATEGORY_UNMAPPED",)
        )
    if binding.expected_state != derived:
        return BIMConstraintEvaluation(
            "BLOCKED", ("BIM_BINDING_EXPECTATION_CONFLICT",)
        )
    if element.state != derived:
        return BIMConstraintEvaluation(
            "BLOCKED", ("PLANMODEL_BIM_STATE_CONFLICT",)
        )
    return BIMConstraintEvaluation("PASS")


def build_bim_constraint_binding(
    element: PlanElement,
    evidence_ids: tuple[str, ...],
) -> BIMConstraintBinding:
    if element.bim_identity is None:
        raise ValueError("BIM_IDENTITY_MISSING")
    state = expected_constraint_state(element.bim_identity)
    binding = BIMConstraintBinding(
        element_id=element.element_id,
        category=element.bim_identity.category,
        expected_state=state,
        evidence_ids=evidence_ids,
    )
    binding.validate()
    return binding
