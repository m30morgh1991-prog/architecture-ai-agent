"""H75 deterministic impact analysis contract.

Impact analysis identifies which plan elements are directly or indirectly affected
by a ChangeRequest and whether the requested change can safely proceed to the
proposal stage. It never grants approval or execution authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from runtime.change_request_contract import ChangeRequest
from runtime.plan_model_contract import ConstraintMap, PlanModel

ImpactStatus = Literal["PASS", "NEEDS_REVIEW", "BLOCKED", "UNKNOWN"]
ImpactScope = Literal["DIRECT", "INDIRECT", "PROTECTED", "UNKNOWN"]

_EDITABLE_TYPES = {"FURNITURE", "FURNITURE_LAYOUT_CHANGE"}
_OVERALL = "OVERALL_ARCHITECTURAL_LAYOUT_CHANGE"


@dataclass(frozen=True)
class ImpactItem:
    element_id: str
    scope: ImpactScope
    reason: str

    def validate(self) -> None:
        if not self.element_id:
            raise ValueError("IMPACT_ELEMENT_ID_MISSING")
        if self.scope not in {"DIRECT", "INDIRECT", "PROTECTED", "UNKNOWN"}:
            raise ValueError("IMPACT_SCOPE_INVALID")
        if not self.reason.strip():
            raise ValueError("IMPACT_REASON_MISSING")


@dataclass(frozen=True)
class ImpactAnalysis:
    source_sha256: str
    model_id: str
    request_id: str
    status: ImpactStatus
    impacted_element_ids: tuple[str, ...] = ()
    items: tuple[ImpactItem, ...] = ()
    blockers: tuple[str, ...] = ()

    def validate(self) -> None:
        if len(self.source_sha256) != 64:
            raise ValueError("IMPACT_SOURCE_INVALID")
        if not self.model_id or not self.request_id:
            raise ValueError("IMPACT_TRACE_INVALID")
        if self.status not in {"PASS", "NEEDS_REVIEW", "BLOCKED", "UNKNOWN"}:
            raise ValueError("IMPACT_STATUS_INVALID")
        if len(set(self.impacted_element_ids)) != len(self.impacted_element_ids):
            raise ValueError("IMPACT_ELEMENT_ID_DUPLICATE")
        for item in self.items:
            item.validate()
        if self.status == "PASS" and self.blockers:
            raise ValueError("PASS_CANNOT_HAVE_IMPACT_BLOCKERS")


def analyze_impact(
    plan_model: PlanModel,
    constraint_map: ConstraintMap,
    request: ChangeRequest,
) -> ImpactAnalysis:
    plan_model.validate()
    constraint_map.validate()
    request.validate()

    if request.source_sha256 != plan_model.source_sha256:
        return ImpactAnalysis(
            plan_model.source_sha256, plan_model.model_id, request.request_id,
            "BLOCKED", blockers=("CHANGE_REQUEST_SOURCE_MISMATCH",)
        )
    if request.model_id != plan_model.model_id or constraint_map.model_id != plan_model.model_id:
        return ImpactAnalysis(
            plan_model.source_sha256, plan_model.model_id, request.request_id,
            "BLOCKED", blockers=("MODEL_ID_MISMATCH",)
        )

    element_ids = {element.element_id for element in plan_model.elements}
    protected = set(constraint_map.protected_element_ids)
    editable = set(constraint_map.editable_element_ids)
    conditional = set(constraint_map.conditional_element_ids)
    unknown = set(constraint_map.unknown_element_ids)

    if not request.target_ids:
        return ImpactAnalysis(
            plan_model.source_sha256, plan_model.model_id, request.request_id,
            "NEEDS_REVIEW", blockers=("TARGETS_REQUIRED_FOR_DETERMINISTIC_IMPACT",)
        )

    missing = sorted(set(request.target_ids) - element_ids)
    if missing:
        return ImpactAnalysis(
            plan_model.source_sha256, plan_model.model_id, request.request_id,
            "UNKNOWN", blockers=("TARGET_ELEMENT_MISSING",)
        )

    items = []
    blockers = []

    # BIM relations expand impact symmetrically but never grant edit authority.
    direct_targets = set(request.target_ids)
    indirect_ids = set()
    for relation in tuple(getattr(plan_model, "bim_relations", ()) or ()):
        if relation.source_id in direct_targets:
            indirect_ids.add(relation.target_id)
        if relation.target_id in direct_targets:
            indirect_ids.add(relation.source_id)
    indirect_ids -= direct_targets
    for element_id in request.target_ids:
        if element_id in protected:
            items.append(ImpactItem(element_id, "PROTECTED", "Target is protected by ConstraintMap."))
            blockers.append("PROTECTED_TARGET")
        elif element_id in unknown:
            items.append(ImpactItem(element_id, "UNKNOWN", "Target constraint state is unknown."))
            blockers.append("UNKNOWN_TARGET_STATE")
        elif element_id in conditional:
            items.append(ImpactItem(element_id, "DIRECT", "Target is conditional and requires rule review."))
            blockers.append("CONDITIONAL_TARGET")
        elif element_id in editable:
            items.append(ImpactItem(element_id, "DIRECT", "Target is explicitly editable."))
        else:
            items.append(ImpactItem(element_id, "UNKNOWN", "Target is not classified by ConstraintMap."))
            blockers.append("UNCLASSIFIED_TARGET")

    for element_id in sorted(indirect_ids):
        if element_id not in element_ids:
            items.append(ImpactItem(element_id, "UNKNOWN", "BIM relation references an element absent from PlanModel."))
            blockers.append("UNKNOWN_INDIRECT_IMPACT")
        elif element_id in protected:
            items.append(ImpactItem(element_id, "PROTECTED", "BIM relation makes a protected neighbor indirectly impacted."))
            blockers.append("PROTECTED_INDIRECT_IMPACT")
        elif element_id in unknown:
            items.append(ImpactItem(element_id, "UNKNOWN", "BIM relation makes an unknown neighbor indirectly impacted."))
            blockers.append("UNKNOWN_INDIRECT_IMPACT")
        elif element_id in conditional:
            items.append(ImpactItem(element_id, "INDIRECT", "BIM relation makes a conditional neighbor indirectly impacted."))
            blockers.append("CONDITIONAL_INDIRECT_IMPACT")
        elif element_id in editable:
            items.append(ImpactItem(element_id, "INDIRECT", "BIM relation makes an editable neighbor indirectly impacted."))
        else:
            items.append(ImpactItem(element_id, "UNKNOWN", "BIM relation neighbor is unclassified."))
            blockers.append("UNCLASSIFIED_INDIRECT_IMPACT")

    if request.change_type == _OVERALL:
        if protected:
            blockers.append("OVERALL_LAYOUT_REQUIRES_PROTECTED_IMPACT_REVIEW")
        # Overall architectural edits are conservatively treated as broad impact.
        for element_id in sorted(protected):
            if element_id not in request.target_ids:
                items.append(ImpactItem(
                    element_id, "PROTECTED",
                    "Overall architectural layout may affect protected structure."
                ))
        status = "BLOCKED" if blockers else "NEEDS_REVIEW"
        if not blockers:
            blockers.append("OVERALL_LAYOUT_REQUIRES_RULE_REVIEW")
            status = "NEEDS_REVIEW"
    else:
        status = "BLOCKED" if blockers else "PASS"

    impacted = tuple(dict.fromkeys(item.element_id for item in items))
    return ImpactAnalysis(
        plan_model.source_sha256,
        plan_model.model_id,
        request.request_id,
        status,
        impacted,
        tuple(items),
        tuple(dict.fromkeys(blockers)),
    )
