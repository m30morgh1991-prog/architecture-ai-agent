"""H21 controlled-editing contract primitives.

Additive to the frozen H15-H20 runtime contracts. No visual editor is invoked here.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


EDIT_PERMISSION_STATES: Set[str] = {"LOCKED", "EDITABLE", "CONDITIONAL"}
UNCERTAINTY_STATES: Set[str] = {
    "UNKNOWN", "SOURCE_REQUIRED", "NEEDS_REVIEW", "ABSTAIN", "BLOCKED"
}


@dataclass(frozen=True)
class EditPermission:
    element_id: str
    state: str
    authorized: bool = False
    conditions: List[str] = field(default_factory=list)

    def validate(self) -> None:
        if not self.element_id:
            raise ValueError("EDIT_PERMISSION_ELEMENT_ID_MISSING")
        if self.state not in EDIT_PERMISSION_STATES:
            raise ValueError("EDIT_PERMISSION_STATE_INVALID")
        if self.state == "LOCKED" and self.authorized:
            # Authorization is explicit metadata; LOCKED remains a guard state.
            return
        if self.state == "EDITABLE" and self.conditions:
            raise ValueError("EDIT_PERMISSION_EDITABLE_HAS_CONDITIONS")


@dataclass(frozen=True)
class UncertaintyAssessment:
    element_id: Optional[str]
    state: str
    reason: str = ""
    blocking: bool = True

    def validate(self) -> None:
        if self.state not in UNCERTAINTY_STATES:
            raise ValueError("UNCERTAINTY_STATE_INVALID")
        if self.blocking and self.state in UNCERTAINTY_STATES:
            return


@dataclass(frozen=True)
class ImpactDependency:
    source_id: str
    affected_ids: List[str]
    dependency_types: List[str] = field(default_factory=list)

    def validate(self) -> None:
        if not self.source_id:
            raise ValueError("IMPACT_SOURCE_ID_MISSING")
        if not all(isinstance(value, str) and value for value in self.affected_ids):
            raise ValueError("IMPACT_AFFECTED_ID_INVALID")


@dataclass(frozen=True)
class ControlledEditingDecision:
    permissions: List[EditPermission]
    uncertainties: List[UncertaintyAssessment] = field(default_factory=list)
    impacts: List[ImpactDependency] = field(default_factory=list)

    def validate(self) -> None:
        for permission in self.permissions:
            permission.validate()
        for uncertainty in self.uncertainties:
            uncertainty.validate()
        for impact in self.impacts:
            impact.validate()

    def blocking_reasons(self) -> List[str]:
        reasons: List[str] = []
        for permission in self.permissions:
            if permission.state == "LOCKED" and not permission.authorized:
                reasons.append(f"LOCKED_ELEMENT_CONFLICT:{permission.element_id}")
            if permission.state == "CONDITIONAL" and not permission.conditions:
                reasons.append(f"CONDITIONAL_STATE_UNRESOLVED:{permission.element_id}")
        for uncertainty in self.uncertainties:
            if uncertainty.blocking:
                reasons.append(f"UNCERTAINTY_BLOCKING:{uncertainty.state}")
        return reasons

    @property
    def executable(self) -> bool:
        return not self.blocking_reasons()


def build_controlled_editing_decision(
    permissions: List[EditPermission],
    uncertainties: Optional[List[UncertaintyAssessment]] = None,
    impacts: Optional[List[ImpactDependency]] = None,
) -> ControlledEditingDecision:
    decision = ControlledEditingDecision(
        permissions=permissions,
        uncertainties=uncertainties or [],
        impacts=impacts or [],
    )
    decision.validate()
    return decision
