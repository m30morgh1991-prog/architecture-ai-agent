"""H47 bridge: real visual evidence into controlled approval.

Fail-closed adapter between the real visual runtime and the frozen
controlled-editing / approved-change-plan contracts. It deliberately does not
invent editable elements when the visual runtime has not established them.
"""

from __future__ import annotations

from typing import Any

from .approved_change_plan_contract import build_approved_change_plan
from .controlled_editing_runtime import build_runtime_controlled_decision


def evaluate_real_visual_change(
    visual_result: dict[str, Any],
    change_request: Any,
) -> dict[str, Any]:
    """Evaluate a real-visual change request without executing geometry.

    Approval is possible only when the visual runtime is ready, contracts are
    valid, semantic corroboration is accessible, and requested targets are
    explicitly editable. Missing data is treated as blocked.
    """
    if not isinstance(visual_result, dict):
        return {
            "status": "REJECT",
            "failure_codes": ["VISUAL_RESULT_INVALID"],
        }

    if visual_result.get("status") != "READY_FOR_APPROVAL":
        return {
            "status": "REJECT",
            "failure_codes": list(visual_result.get("blockers") or [
                "VISUAL_RUNTIME_NOT_READY"
            ]),
        }

    contracts = visual_result.get("contracts") or {}
    if contracts.get("status") != "VALID":
        return {
            "status": "REJECT",
            "failure_codes": ["VISUAL_CONTRACTS_INVALID"],
        }

    semantics = visual_result.get("semantic_corroboration") or {}
    if semantics.get("status") != "ACCESSIBLE":
        return {
            "status": "REJECT",
            "failure_codes": ["SEMANTIC_CORROBORATION_REQUIRED"],
        }

    constraint = visual_result.get("constraint_map") or {}
    protected = tuple(constraint.get("protected_element_ids") or ())
    editable = tuple(constraint.get("editable_element_ids") or ())
    conditional = tuple(constraint.get("conditional_element_ids") or ())
    unknown = tuple(constraint.get("unknown_element_ids") or ())

    class ConstraintMapView:
        protected_element_ids = protected
        editable_element_ids = editable
        conditional_element_ids = conditional
        unknown_element_ids = unknown

    targets = tuple(getattr(change_request, "target_ids", ()) or ())
    controlled = build_runtime_controlled_decision(
        ConstraintMapView(),
        targets,
        uncertainty_state="BLOCKED" if unknown else "UNKNOWN",
        uncertainty_reason="Real visual runtime contains unresolved elements.",
    )
    if not controlled.executable:
        return {
            "status": "REJECT",
            "failure_codes": controlled.blocking_reasons(),
        }

    approval = build_approved_change_plan(
        change_request=change_request,
        available_element_ids=protected + editable + conditional + unknown,
        editable_element_ids=editable,
    )
    if approval.status != "APPROVED":
        return {
            "status": "REJECT",
            "failure_codes": [approval.reason],
        }

    return {
        "status": "APPROVED",
        "approved_target_ids": list(approval.approved_target_ids),
        "change_type": approval.change_type,
    }



def execute_real_visual_approved_change(
    visual_result: dict[str, Any],
    change_request: Any,
    plan: Any,
    simulated_geometry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """H48 E2E bridge: visual evidence -> approval -> controlled execution.

    The visual bridge is authoritative for whether the request may enter the
    execution path. Execution is delegated to the frozen runtime executor;
    blocked or rejected visual evidence never reaches it.
    """
    decision = evaluate_real_visual_change(visual_result, change_request)
    if decision.get("status") != "APPROVED":
        return {
            "status": "REJECT",
            "stage": "APPROVAL",
            "failure_codes": list(decision.get("failure_codes", [])),
        }

    # Defensive consistency check: the executable plan must expose exactly the
    # approved targets as editable. This prevents approval metadata from being
    # used to bypass the runtime's own authorization contract.
    by_id = {element.element_id: element for element in plan.elements}
    for element_id in decision["approved_target_ids"]:
        element = by_id.get(element_id)
        if element is None or element.state != "EDITABLE":
            return {
                "status": "REJECT",
                "stage": "EXECUTION_AUTHORIZATION",
                "failure_codes": [f"EDIT_PERMISSION_REQUIRED:{element_id}"],
            }

    from .app import execute

    execution = execute(plan, change_request, simulated_geometry)
    return {
        "status": execution.get("status", "REJECT"),
        "stage": "EXECUTION",
        "approval": decision,
        "execution": execution,
    }
