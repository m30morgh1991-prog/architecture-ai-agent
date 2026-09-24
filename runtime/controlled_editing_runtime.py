"""H41 runtime adapter for the controlled-editing contract.

The contract remains the authority for edit authorization. This module only
maps an evidence-backed ConstraintMap plus a requested target set into the
frozen H21 decision primitives.
"""
from .controlled_editing_contract import (
    EditPermission,
    UncertaintyAssessment,
    build_controlled_editing_decision,
)


def build_runtime_controlled_decision(
    constraint_map,
    requested_target_ids,
    *,
    uncertainty_state="UNKNOWN",
    uncertainty_reason="",
):
    requested = set(requested_target_ids)
    buckets = {
        "LOCKED": set(constraint_map.protected_element_ids),
        "EDITABLE": set(constraint_map.editable_element_ids),
        "CONDITIONAL": set(constraint_map.conditional_element_ids),
    }

    permissions = []
    for element_id in requested:
        if element_id in buckets["LOCKED"]:
            state = "LOCKED"
        elif element_id in buckets["EDITABLE"]:
            state = "EDITABLE"
        elif element_id in buckets["CONDITIONAL"]:
            state = "CONDITIONAL"
        else:
            state = "LOCKED"
        permissions.append(EditPermission(element_id=element_id, state=state))

    uncertainties = []
    if constraint_map.unknown_element_ids or uncertainty_state != "UNKNOWN":
        uncertainties.append(
            UncertaintyAssessment(
                element_id=None,
                state=uncertainty_state,
                reason=uncertainty_reason or "Constraint map contains unresolved elements.",
                blocking=True,
            )
        )

    return build_controlled_editing_decision(
        permissions=permissions,
        uncertainties=uncertainties,
    )
