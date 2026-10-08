"""Fail-closed reconciliation of multi-source drawing evidence.

Reconciliation produces a decision about a candidate fact; it does not mutate
PlanModel directly. Contradictions and missing evidence stay unresolved.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Literal

Decision = Literal["SUPPORTED","CONTRADICTED","NEEDS_REVIEW","UNKNOWN"]

@dataclass(frozen=True)
class CandidateFact:
    fact_id: str
    subject_id: str
    predicate: str
    value: str
    evidence_ids: tuple[str,...]

    def validate(self):
        if not self.fact_id or not self.subject_id or not self.predicate or not self.value:
            raise ValueError("CANDIDATE_FACT_INVALID")
        if not self.evidence_ids:
            raise ValueError("CANDIDATE_FACT_EVIDENCE_MISSING")

@dataclass(frozen=True)
class ReconciliationResult:
    fact_id: str
    decision: Decision
    supporting_evidence_ids: tuple[str,...]
    contradicting_evidence_ids: tuple[str,...]
    missing_requirements: tuple[str,...]

    def validate(self):
        if self.decision not in {"SUPPORTED","CONTRADICTED","NEEDS_REVIEW","UNKNOWN"}:
            raise ValueError("RECONCILIATION_DECISION_INVALID")
        if self.decision=="SUPPORTED" and self.contradicting_evidence_ids:
            raise ValueError("SUPPORTED_FACT_HAS_CONTRADICTION")
        if self.decision=="CONTRADICTED" and not self.contradicting_evidence_ids:
            raise ValueError("CONTRADICTED_FACT_MISSING_EVIDENCE")
        if self.decision=="NEEDS_REVIEW" and not (self.contradicting_evidence_ids or self.missing_requirements):
            raise ValueError("NEEDS_REVIEW_REASON_MISSING")

def reconcile_fact(
    fact: CandidateFact,
    *,
    supporting: Iterable[str]=(),
    contradicting: Iterable[str]=(),
    required_evidence: Iterable[str]=(),
) -> ReconciliationResult:
    fact.validate()
    support=tuple(dict.fromkeys(str(x) for x in supporting))
    conflict=tuple(dict.fromkeys(str(x) for x in contradicting))
    missing=tuple(dict.fromkeys(str(x) for x in required_evidence if x not in support))
    if conflict:
        decision="CONTRADICTED"
    elif missing:
        decision="NEEDS_REVIEW"
    elif support:
        decision="SUPPORTED"
    else:
        decision="UNKNOWN"
    result=ReconciliationResult(fact.fact_id,decision,support,conflict,missing)
    result.validate()
    return result
