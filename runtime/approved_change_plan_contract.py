"""H40 explicit ChangeRequest -> ApprovedChangePlan contract boundary.

This adapter preserves the frozen legacy wire contract while making approval
an explicit, validated step before execution.
"""
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class ApprovedChangePlanDecision:
    status: str
    approved_target_ids: tuple[str, ...]
    change_type: str
    reason: str = ""

    def validate(self) -> None:
        if self.status not in {"APPROVED", "REJECT"}:
            raise ValueError("APPROVAL_STATUS_INVALID")
        if self.status == "APPROVED" and not self.approved_target_ids:
            raise ValueError("APPROVED_TARGETS_MISSING")


def build_approved_change_plan(
    *,
    change_request: Any,
    available_element_ids: Iterable[str],
    editable_element_ids: Iterable[str],
    uncertainty_blocked: bool = False,
) -> ApprovedChangePlanDecision:
    targets = tuple(change_request.target_ids)
    available = set(available_element_ids)
    editable = set(editable_element_ids)

    missing = [x for x in targets if x not in available]
    if missing:
        decision = ApprovedChangePlanDecision(
            "REJECT", (), change_request.change_type,
            f"TARGET_NOT_FOUND:{','.join(missing)}",
        )
    elif uncertainty_blocked:
        decision = ApprovedChangePlanDecision(
            "REJECT", (), change_request.change_type,
            "UNCERTAINTY_BLOCKING",
        )
    elif not targets or not all(x in editable for x in targets):
        decision = ApprovedChangePlanDecision(
            "REJECT", (), change_request.change_type,
            "EDIT_PERMISSION_REQUIRED",
        )
    else:
        decision = ApprovedChangePlanDecision(
            "APPROVED", targets, change_request.change_type,
        )

    decision.validate()
    return decision
