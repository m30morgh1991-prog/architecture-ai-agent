"""Reconcile source-bound DWG evidence into canonical CandidateFacts.

This is a normalization/reconciliation layer only. It never mutates PlanModel
and never treats a CAD candidate as authoritative without source-bound evidence.
"""
from __future__ import annotations

import hashlib
from typing import Any

from runtime.evidence_reconciliation import CandidateFact, ReconciliationResult, reconcile_fact
from runtime.drawing_semantic_evidence import DrawingEvidenceSet


def _fact_id(source_sha256: str, predicate: str, subject_id: str, value: str) -> str:
    raw = f"{source_sha256}:{predicate}:{subject_id}:{value}".encode("utf-8")
    return "fact:" + hashlib.sha256(raw).hexdigest()[:24]


def reconcile_dwg_candidates(
    evidence_set: DrawingEvidenceSet,
    *,
    contradictions: dict[str, tuple[str, ...]] | None = None,
    required_evidence: dict[str, tuple[str, ...]] | None = None,
) -> tuple[tuple[CandidateFact, ...], tuple[ReconciliationResult, ...]]:
    """Create provenance-bound facts and fail-closed reconciliation results.

    Only SUPPORTED DrawingEvidence may support a fact. CONTRADICTED evidence is
    never silently discarded; it is passed to the canonical contradiction path.
    Contradiction and required-evidence references must belong to the same
    source-bound DrawingEvidenceSet; cross-source or missing references fail
    closed instead of influencing the result.
    UNKNOWN/UNCERTAIN evidence yields UNKNOWN unless required evidence is
    missing, in which case NEEDS_REVIEW is returned.
    """
    evidence_set.validate()
    contradictions = contradictions or {}
    required_evidence = required_evidence or {}

    evidence_by_id = {item.evidence_id: item for item in evidence_set.evidences}

    def validate_refs(refs: tuple[str, ...], error_code: str) -> None:
        for evidence_id in refs:
            evidence = evidence_by_id.get(evidence_id)
            if evidence is None:
                raise ValueError(error_code)
            if evidence.source_sha256 != evidence_set.source_sha256:
                raise ValueError("CANDIDATE_FACT_SOURCE_MISMATCH")

    facts: list[CandidateFact] = []
    results: list[ReconciliationResult] = []

    for evidence in evidence_set.evidences:
        fact = CandidateFact(
            fact_id=_fact_id(evidence_set.source_sha256, evidence.predicate, evidence.subject_id, evidence.value),
            subject_id=evidence.subject_id,
            predicate=evidence.predicate,
            value=evidence.value,
            evidence_ids=(evidence.evidence_id,),
        )
        fact.validate()

        supporting = (evidence.evidence_id,) if evidence.status == "SUPPORTED" else ()
        contradicting = tuple(dict.fromkeys(contradictions.get(fact.fact_id, ())))
        required = tuple(dict.fromkeys(required_evidence.get(fact.fact_id, ())))

        validate_refs(contradicting, "CANDIDATE_FACT_CONTRADICTION_REFERENCE_MISSING")
        validate_refs(required, "CANDIDATE_FACT_REQUIRED_EVIDENCE_REFERENCE_MISSING")

        if evidence.evidence_id in contradicting:
            raise ValueError("CANDIDATE_FACT_SUPPORT_CONTRADICTION_OVERLAP")

        result = reconcile_fact(
            fact,
            supporting=supporting,
            contradicting=contradicting,
            required_evidence=required,
        )
        facts.append(fact)
        results.append(result)

    return tuple(facts), tuple(results)


def validate_dwg_fact_provenance(
    evidence_set: DrawingEvidenceSet,
    facts: tuple[CandidateFact, ...],
) -> None:
    """Reject facts that reference evidence from another source or missing IDs."""
    evidence_set.validate()
    evidence_by_id = {item.evidence_id: item for item in evidence_set.evidences}
    for fact in facts:
        fact.validate()
        for evidence_id in fact.evidence_ids:
            evidence = evidence_by_id.get(evidence_id)
            if evidence is None:
                raise ValueError("CANDIDATE_FACT_EVIDENCE_REFERENCE_MISSING")
            if evidence.source_sha256 != evidence_set.source_sha256:
                raise ValueError("CANDIDATE_FACT_SOURCE_MISMATCH")
