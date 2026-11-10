"""Read-only AIE facade over the repository's canonical plan contracts.

This module deliberately does not create a second PlanModel, infer geometry,
grant edit permissions, or mutate input objects. It validates the existing
PlanModel/ConstraintMap pair and reports inconsistencies and unresolved
evidence using fail-closed statuses.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from runtime.plan_model_contract import ConstraintMap, PlanModel

AIEStatus = Literal["INSPECTED", "NEEDS_REVIEW", "BLOCKED"]
FindingSeverity = Literal["REVIEW", "BLOCKER"]


@dataclass(frozen=True)
class AIEFinding:
    """A deterministic inspection finding; it is not an approval decision."""

    code: str
    severity: FindingSeverity
    message: str
    element_id: str | None = None


@dataclass(frozen=True)
class AIEInspectionResult:
    """Immutable summary of a read-only inspection."""

    status: AIEStatus
    model_id: str | None
    source_sha256: str | None
    element_count: int
    space_count: int
    state_counts: tuple[tuple[str, int], ...]
    findings: tuple[AIEFinding, ...]

    @property
    def is_blocked(self) -> bool:
        return self.status == "BLOCKED"

    @property
    def requires_review(self) -> bool:
        return self.status == "NEEDS_REVIEW"


_STATE_BUCKETS = {
    "LOCKED": "protected_element_ids",
    "EDITABLE": "editable_element_ids",
    "CONDITIONAL": "conditional_element_ids",
    "UNKNOWN": "unknown_element_ids",
}


def _finding(
    code: str,
    severity: FindingSeverity,
    message: str,
    element_id: str | None = None,
) -> AIEFinding:
    return AIEFinding(code, severity, message, element_id)


def inspect_plan(
    model: PlanModel,
    constraint_map: ConstraintMap,
) -> AIEInspectionResult:
    """Inspect canonical contracts without changing either input.

    INSPECTED means the contract pair is internally consistent and contains
    no known unresolved items. NEEDS_REVIEW means the contracts are structurally
    usable but evidence or source facts remain incomplete. BLOCKED means a
    contract, identity, or permission inconsistency prevents safe reliance.
    None of these statuses authorizes plan editing.
    """
    findings: list[AIEFinding] = []

    try:
        model.validate()
    except (AttributeError, TypeError, ValueError) as exc:
        findings.append(
            _finding(
                "PLAN_MODEL_INVALID",
                "BLOCKER",
                f"Canonical PlanModel validation failed: {exc}",
            )
        )

    try:
        constraint_map.validate()
    except (AttributeError, TypeError, ValueError) as exc:
        findings.append(
            _finding(
                "CONSTRAINT_MAP_INVALID",
                "BLOCKER",
                f"Canonical ConstraintMap validation failed: {exc}",
            )
        )

    if findings:
        return _result("BLOCKED", model, (), findings)

    if constraint_map.model_id != model.model_id:
        findings.append(
            _finding(
                "CONSTRAINT_MODEL_ID_MISMATCH",
                "BLOCKER",
                "ConstraintMap does not refer to the inspected PlanModel.",
            )
        )

    model_elements = {element.element_id: element for element in model.elements}
    bucket_members: dict[str, list[str]] = {
        state: list(getattr(constraint_map, field_name))
        for state, field_name in _STATE_BUCKETS.items()
    }

    for state, members in bucket_members.items():
        if len(members) != len(set(members)):
            findings.append(
                _finding(
                    "CONSTRAINT_BUCKET_DUPLICATE_ID",
                    "BLOCKER",
                    f"ConstraintMap {state} bucket contains duplicate IDs.",
                )
            )

    all_bucket_ids = {
        element_id for members in bucket_members.values() for element_id in members
    }
    for element_id in sorted(all_bucket_ids - set(model_elements)):
        findings.append(
            _finding(
                "CONSTRAINT_ELEMENT_NOT_IN_MODEL",
                "BLOCKER",
                "ConstraintMap references an element absent from PlanModel.",
                element_id,
            )
        )

    for element_id, element in model_elements.items():
        expected_bucket = _STATE_BUCKETS.get(element.state)
        actual_buckets = [
            state
            for state, members in bucket_members.items()
            if element_id in members
        ]
        if expected_bucket is None:
            findings.append(
                _finding(
                    "PLAN_ELEMENT_STATE_UNSUPPORTED",
                    "BLOCKER",
                    f"Unsupported PlanElement state: {element.state}.",
                    element_id,
                )
            )
            continue
        if len(actual_buckets) != 1:
            findings.append(
                _finding(
                    "CONSTRAINT_MEMBERSHIP_INCOMPLETE",
                    "BLOCKER",
                    "Every PlanElement must occur in exactly one ConstraintMap bucket.",
                    element_id,
                )
            )
        elif actual_buckets[0] != element.state:
            findings.append(
                _finding(
                    "PLAN_CONSTRAINT_STATE_MISMATCH",
                    "BLOCKER",
                    "PlanElement state and ConstraintMap bucket disagree.",
                    element_id,
                )
            )

        if not element.geometry:
            findings.append(
                _finding(
                    "ELEMENT_GEOMETRY_MISSING",
                    "REVIEW",
                    "Element has no geometry payload; spatial analysis is unavailable.",
                    element_id,
                )
            )
        elif not (
            element.geometry.get("unit") or element.geometry.get("units")
        ) or not element.geometry.get("coordinate_frame"):
            findings.append(
                _finding(
                    "GEOMETRY_REFERENCE_UNVERIFIED",
                    "REVIEW",
                    "Geometry unit and coordinate frame are not both explicit.",
                    element_id,
                )
            )

    if model.element_evidence is None:
        findings.append(
            _finding(
                "ELEMENT_EVIDENCE_BUNDLE_NOT_ATTACHED",
                "REVIEW",
                "Element evidence IDs exist, but no source-bound evidence bundle is attached.",
            )
        )

    # ConstraintMap carries evidence IDs but has no source-bound evidence
    # bundle field of its own. Do not assume those IDs were reconciled merely
    # because PlanModel has an element evidence bundle.
    findings.append(
        _finding(
            "CONSTRAINT_EVIDENCE_NOT_RECONCILED",
            "REVIEW",
            "ConstraintMap evidence IDs are not yet linked to a source-bound constraint evidence contract.",
        )
    )

    if model.unresolved:
        findings.append(
            _finding(
                "PLAN_MODEL_UNRESOLVED_ITEMS",
                "REVIEW",
                f"PlanModel contains {len(model.unresolved)} unresolved item(s).",
            )
        )

    if model.drawing_evidence is not None and model.drawing_evidence.unresolved:
        findings.append(
            _finding(
                "DRAWING_EVIDENCE_UNRESOLVED",
                "REVIEW",
                f"Drawing evidence contains {len(model.drawing_evidence.unresolved)} unresolved item(s).",
            )
        )

    if model.space_model is not None and model.space_model.unresolved:
        findings.append(
            _finding(
                "SPACE_MODEL_UNRESOLVED",
                "REVIEW",
                f"SpaceModel contains {len(model.space_model.unresolved)} unresolved item(s).",
            )
        )

    if findings and any(item.severity == "BLOCKER" for item in findings):
        status: AIEStatus = "BLOCKED"
    elif findings:
        status = "NEEDS_REVIEW"
    else:
        status = "INSPECTED"

    return _result(status, model, tuple(sorted(model_elements)), findings)


def _result(
    status: AIEStatus,
    model: PlanModel,
    element_ids: tuple[str, ...],
    findings: list[AIEFinding] | tuple[AIEFinding, ...],
) -> AIEInspectionResult:
    state_counts = tuple(
        (
            state,
            sum(1 for element in model.elements if element.state == state),
        )
        for state in _STATE_BUCKETS
    )
    return AIEInspectionResult(
        status=status,
        model_id=getattr(model, "model_id", None),
        source_sha256=getattr(model, "source_sha256", None),
        element_count=len(getattr(model, "elements", ())),
        space_count=len(getattr(model, "spaces", ())),
        state_counts=state_counts,
        findings=tuple(findings),
    )
