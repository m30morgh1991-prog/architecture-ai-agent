"""Deterministic reconstruction of an evidence-backed PlanModel (H70).

The reconstruction layer combines H68 architectural candidates, H69
source-bound evidence, and an optional H62/H64 space model. It never upgrades
uncertain detection into approval-grade semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.element_evidence_contract import (
    ALLOWED_ELEMENT_TYPES,
    ElementEvidenceBundle,
    build_element_evidence_bundle,
)
from runtime.plan_model_contract import PlanElement, PlanModel
from runtime.space_model_contract import SpaceModel


@dataclass(frozen=True)
class PlanModelReconstructionResult:
    plan_model: PlanModel
    evidence_bundle: ElementEvidenceBundle

    def validate(self) -> None:
        self.evidence_bundle.validate()
        self.plan_model.validate()
        if self.plan_model.element_evidence is None:
            raise ValueError("PLAN_MODEL_EVIDENCE_BUNDLE_MISSING")
        if self.plan_model.element_evidence.source_sha256 != self.plan_model.source_sha256:
            raise ValueError("PLAN_MODEL_EVIDENCE_SOURCE_MISMATCH")


def _state(candidate: dict[str, Any]) -> str:
    status = str(candidate.get("status", "UNKNOWN"))
    if status == "LOCKED":
        return "LOCKED"
    if status == "EDITABLE":
        return "EDITABLE"
    if status == "CONDITIONAL":
        return "CONDITIONAL"
    return "UNKNOWN"


def _evidence_status(candidate: dict[str, Any]) -> str:
    state = _state(candidate)
    if state in {"LOCKED", "EDITABLE", "CONDITIONAL"}:
        return "SUPPORTED"
    return "UNKNOWN"


def build_plan_model_from_detection(
    *,
    model_id: str,
    source_sha256: str,
    detection_result: dict[str, Any],
    drawing_count: int = 1,
    space_model: SpaceModel | None = None,
) -> PlanModelReconstructionResult:
    if not model_id or len(source_sha256) != 64:
        raise ValueError("PLAN_RECONSTRUCTION_ID_OR_SOURCE_INVALID")
    if drawing_count < 1:
        raise ValueError("PLAN_RECONSTRUCTION_DRAWING_COUNT_INVALID")
    if str(detection_result.get("source_sha256")) != source_sha256:
        raise ValueError("PLAN_RECONSTRUCTION_SOURCE_MISMATCH")

    candidates = tuple(detection_result.get("candidates", ()))
    evidence_items: list[dict[str, Any]] = []
    elements: list[PlanElement] = []
    unresolved_types = set(str(x) for x in detection_result.get(
        "unresolved_fixed_element_types",
        ALLOWED_ELEMENT_TYPES,
    ))

    for candidate in candidates:
        element_type = str(candidate.get("element_type", ""))
        if element_type not in ALLOWED_ELEMENT_TYPES:
            raise ValueError("PLAN_RECONSTRUCTION_ELEMENT_TYPE_INVALID")

        candidate_id = str(candidate.get("candidate_id", ""))
        evidence_ids = tuple(str(x) for x in candidate.get("evidence_ids", ()))
        if not candidate_id or not evidence_ids:
            raise ValueError("PLAN_RECONSTRUCTION_ELEMENT_EVIDENCE_MISSING")

        confidence = float(candidate.get("confidence", 0.0))
        state = _state(candidate)
        evidence_status = _evidence_status(candidate)

        # Candidate evidence IDs are retained verbatim so every PlanElement
        # remains traceable to native/derived source evidence.
        for evidence_id in evidence_ids:
            evidence_items.append({
                "evidence_id": evidence_id,
                "source_sha256": source_sha256,
                "kind": "DWG_GEOMETRY",
                "element_type": element_type,
                "status": evidence_status,
                "description": str(candidate.get("rationale", "Detection evidence.")),
                "native_id": candidate_id,
                "confidence": confidence,
            })

        geometry = {
            "bbox": [float(x) for x in candidate.get("bbox", ())],
            "candidate_id": candidate_id,
        }
        elements.append(PlanElement(
            element_id=candidate_id,
            element_type=element_type,
            state=state,
            geometry=geometry,
            evidence_ids=evidence_ids,
            confidence=confidence,
        ))
        if state != "LOCKED":
            unresolved_types.add(element_type)

    # De-duplicate evidence records deterministically while preserving order.
    unique_evidence: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in evidence_items:
        if item["evidence_id"] in seen:
            continue
        seen.add(item["evidence_id"])
        unique_evidence.append(item)

    # Any fixed type not represented by approval-grade LOCKED evidence remains
    # unresolved. H70 never promotes UNKNOWN merely because a candidate exists.
    locked_types = {e.element_type for e in elements if e.state == "LOCKED"}
    unresolved_types.update(ALLOWED_ELEMENT_TYPES - locked_types)

    bundle = build_element_evidence_bundle(
        bundle_id=f"{model_id}:evidence",
        source_sha256=source_sha256,
        evidences=unique_evidence,
        unresolved_element_types=sorted(unresolved_types),
    )

    model = PlanModel(
        model_id=model_id,
        source_sha256=source_sha256,
        drawing_count=drawing_count,
        elements=tuple(elements),
        unresolved=tuple(sorted(unresolved_types)),
        space_model=space_model,
        element_evidence=bundle,
    )
    result = PlanModelReconstructionResult(
        plan_model=model,
        evidence_bundle=bundle,
    )
    result.validate()
    return result
