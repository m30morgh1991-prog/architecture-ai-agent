"""Golden DWG regression invariants.

The regression gate is intentionally independent from the visual editor. It records
source identity and semantic inventory invariants so a parser change cannot silently
change the architectural understanding contract.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class GoldenDWGSnapshot:
    source_sha256: str
    entity_count: int
    candidate_count: int
    candidate_ids: tuple[str, ...]
    plan_model_valid: bool
    evidence_valid: bool
    bim_graph_valid: bool
    fail_closed: bool

    def validate(self) -> None:
        if len(self.source_sha256) != 64:
            raise ValueError("GOLDEN_SOURCE_SHA256_INVALID")
        if self.entity_count < 0 or self.candidate_count < 0:
            raise ValueError("GOLDEN_COUNT_INVALID")
        if self.candidate_count != len(self.candidate_ids):
            raise ValueError("GOLDEN_CANDIDATE_COUNT_MISMATCH")
        if len(set(self.candidate_ids)) != len(self.candidate_ids):
            raise ValueError("GOLDEN_CANDIDATE_ID_DUPLICATE")
        if not all((self.plan_model_valid, self.evidence_valid, self.bim_graph_valid, self.fail_closed)):
            raise ValueError("GOLDEN_INVARIANT_FAILED")

def validate_golden_dwg(
    *, source_sha256, entity_count, candidate_count, plan_model_valid,
    evidence_valid, bim_graph_valid, fail_closed, candidate_ids=()
):
    snapshot = GoldenDWGSnapshot(
        source_sha256=source_sha256,
        entity_count=entity_count,
        candidate_count=candidate_count,
        candidate_ids=tuple(candidate_ids),
        plan_model_valid=plan_model_valid,
        evidence_valid=evidence_valid,
        bim_graph_valid=bim_graph_valid,
        fail_closed=fail_closed,
    )
    snapshot.validate()
    return True
