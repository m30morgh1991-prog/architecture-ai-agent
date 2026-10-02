"""H79 evidence-backed BIM binding into ConstraintMap."""
from __future__ import annotations
from dataclasses import dataclass
from runtime.bim_constraint_contract import BIMConstraintBinding, evaluate_bim_constraint_binding
from runtime.plan_model_contract import ConstraintMap, PlanElement

@dataclass(frozen=True)
class ConstraintMapBuildResult:
    status: str
    constraint_map: ConstraintMap | None
    reasons: tuple[str, ...] = ()

def build_constraint_map_from_bim(model_id: str, elements: tuple[PlanElement, ...], bindings: tuple[BIMConstraintBinding, ...]) -> ConstraintMapBuildResult:
    if not model_id:
        return ConstraintMapBuildResult("BLOCKED", None, ("MODEL_ID_MISSING",))
    by_id = {b.element_id: b for b in bindings}
    if len(by_id) != len(bindings):
        return ConstraintMapBuildResult("BLOCKED", None, ("BIM_BINDING_DUPLICATE",))
    protected, editable, conditional, unknown = [], [], [], []
    evidence: set[str] = set()
    reasons: list[str] = []
    for element in elements:
        evidence.update(element.evidence_ids)
        binding = by_id.get(element.element_id)
        if binding is None:
            unknown.append(element.element_id)
            reasons.append(f"BIM_BINDING_MISSING:{element.element_id}")
            continue
        evidence.update(binding.evidence_ids)
        evaluation = evaluate_bim_constraint_binding(element, binding)
        if evaluation.status != "PASS":
            reasons.extend(evaluation.reasons)
            if evaluation.status in {"BLOCKED", "UNKNOWN"}:
                unknown.append(element.element_id)
                continue
        if element.state == "LOCKED":
            protected.append(element.element_id)
        elif element.state == "EDITABLE":
            editable.append(element.element_id)
        elif element.state == "CONDITIONAL":
            conditional.append(element.element_id)
        else:
            unknown.append(element.element_id)
    blocked = any(reason.startswith(("BIM_CONSTRAINT_", "PLANMODEL_BIM_", "BIM_BINDING_EXPECTATION")) for reason in reasons)
    status = "BLOCKED" if blocked else ("NEEDS_REVIEW" if reasons else "PASS")
    if not evidence:
        return ConstraintMapBuildResult("UNKNOWN", None, ("BIM_BINDING_EVIDENCE_MISSING",))
    constraint_map = ConstraintMap(
        map_id=f"{model_id}:constraints", model_id=model_id,
        protected_element_ids=tuple(protected), editable_element_ids=tuple(editable),
        conditional_element_ids=tuple(conditional), unknown_element_ids=tuple(unknown),
        evidence_ids=tuple(sorted(evidence)),
    )
    constraint_map.validate()
    return ConstraintMapBuildResult(status, constraint_map, tuple(reasons))
