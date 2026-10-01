"""Deterministic PlanModel -> ConstraintMap integration (H71).

The integration is source-bound and fail-closed. It never upgrades an element
state merely because a PlanModel says so: the state must be supported by the
PlanModel's source-bound evidence. Missing, uncertain, contradicted, or unknown
evidence maps to UNKNOWN.
"""
from __future__ import annotations

from runtime.element_evidence_contract import ElementEvidence
from runtime.plan_model_contract import ConstraintMap, PlanModel


def _evidence_supports_constraint(
    evidence: tuple[ElementEvidence, ...],
    element_confidence: float,
    state: str,
) -> bool:
    if not evidence:
        return False
    if any(item.status != "SUPPORTED" for item in evidence):
        return False
    if state == "LOCKED":
        return element_confidence >= 0.95 and all(item.confidence >= 0.95 for item in evidence)
    if state == "EDITABLE":
        return element_confidence >= 0.90
    if state == "CONDITIONAL":
        return True
    return False


def build_constraint_map_from_plan_model(
    *,
    plan_model: PlanModel,
    map_id: str,
) -> ConstraintMap:
    """Build a deterministic, source-bound ConstraintMap from a validated PlanModel."""
    plan_model.validate()
    bundle = plan_model.element_evidence
    if bundle is None:
        raise ValueError("CONSTRAINT_MAP_EVIDENCE_REQUIRED")
    if bundle.source_sha256 != plan_model.source_sha256:
        raise ValueError("CONSTRAINT_MAP_SOURCE_MISMATCH")

    evidence_by_id = {item.evidence_id: item for item in bundle.evidences}
    buckets = {"LOCKED": [], "EDITABLE": [], "CONDITIONAL": [], "UNKNOWN": []}
    used_evidence: set[str] = set()

    for element in plan_model.elements:
        evidence = tuple(
            evidence_by_id[evidence_id]
            for evidence_id in element.evidence_ids
            if evidence_id in evidence_by_id
        )
        used_evidence.update(item.evidence_id for item in evidence)
        effective_state = (
            element.state
            if _evidence_supports_constraint(evidence, element.confidence, element.state)
            else "UNKNOWN"
        )
        buckets[effective_state].append(element.element_id)

    constraint_map = ConstraintMap(
        map_id=map_id,
        model_id=plan_model.model_id,
        protected_element_ids=tuple(buckets["LOCKED"]),
        editable_element_ids=tuple(buckets["EDITABLE"]),
        conditional_element_ids=tuple(buckets["CONDITIONAL"]),
        unknown_element_ids=tuple(buckets["UNKNOWN"]),
        evidence_ids=tuple(sorted(used_evidence)),
        source_sha256=plan_model.source_sha256,
    )
    constraint_map.validate()
    return constraint_map
