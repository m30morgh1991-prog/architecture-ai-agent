"""Evidence-backed corroboration contract for fixed architectural elements.

Native geometry alone never promotes an element to LOCKED. Approval-grade
semantics require independent evidence sources and fail closed on conflict.
"""
from dataclasses import dataclass

_FIXED = {"COLUMNS", "WALLS", "DOORS", "WINDOWS", "OUTER_BOUNDARY", "OVERALL_PLAN_FORM"}


@dataclass(frozen=True)
class FixedElementCorroboration:
    element_id: str
    element_type: str
    status: str
    confidence: float
    evidence_ids: tuple[str, ...]
    reason: str

    def validate(self):
        if not self.element_id or self.element_type not in _FIXED:
            raise ValueError("FIXED_ELEMENT_IDENTITY_INVALID")
        if self.status not in {"LOCKED", "UNKNOWN", "BLOCKED", "NEEDS_REVIEW"}:
            raise ValueError("FIXED_ELEMENT_STATUS_INVALID")
        if not 0 <= self.confidence <= 1:
            raise ValueError("FIXED_ELEMENT_CONFIDENCE_INVALID")
        if not self.evidence_ids:
            raise ValueError("FIXED_ELEMENT_EVIDENCE_MISSING")
        if not self.reason.strip():
            raise ValueError("FIXED_ELEMENT_REASON_MISSING")
        if self.status == "LOCKED" and self.confidence < 0.95:
            raise ValueError("FIXED_ELEMENT_LOCK_CONFIDENCE_LOW")


def corroborate_fixed_element(
    *,
    element_id: str,
    element_type: str,
    geometry_evidence: bool,
    semantic_evidence: bool,
    source_metadata_evidence: bool,
    topology_evidence: bool,
    contradiction: bool = False,
    evidence_ids: tuple[str, ...] = (),
) -> FixedElementCorroboration:
    """Require independent corroboration before structural locking.

    For protected structural classes (columns/walls/doors/windows), at least
    two independent evidence families are required, including either semantic,
    metadata, or topology evidence. Contradictions always block.
    """
    sources = sum(bool(x) for x in (
        geometry_evidence, semantic_evidence,
        source_metadata_evidence, topology_evidence,
    ))
    if contradiction:
        result = FixedElementCorroboration(
            element_id, element_type, "BLOCKED", 0.0, evidence_ids,
            "Contradictory evidence prevents approval-grade fixed-element semantics.",
        )
    elif sources >= 2 and geometry_evidence and (
        semantic_evidence or source_metadata_evidence or topology_evidence
    ):
        confidence = 0.95 if sources >= 3 else 0.90
        status = "LOCKED" if confidence >= 0.95 else "NEEDS_REVIEW"
        result = FixedElementCorroboration(
            element_id, element_type, status, confidence, evidence_ids,
            "Independent geometry plus semantic/metadata/topology evidence corroborate the element.",
        )
    else:
        result = FixedElementCorroboration(
            element_id, element_type, "UNKNOWN", 0.0, evidence_ids,
            "Insufficient independent evidence for approval-grade fixed-element locking.",
        )
    result.validate()
    return result
