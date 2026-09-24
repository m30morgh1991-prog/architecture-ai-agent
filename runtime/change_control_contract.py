"""H22 controlled change proposal contract.

A proposal is evidence-bearing and cannot itself authorize editing.
"""
from dataclasses import dataclass, field
from typing import Dict, List


PROPOSAL_STATES = {"DRAFT", "BLOCKED", "APPROVED", "REJECTED"}


@dataclass(frozen=True)
class ChangeProposal:
    proposal_id: str
    execution_id: str
    requested_changes: List[str]
    impacted_elements: List[str] = field(default_factory=list)
    blocking_reasons: List[str] = field(default_factory=list)
    state: str = "DRAFT"
    evidence: Dict[str, str] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.proposal_id or not self.execution_id:
            raise ValueError("CHANGE_PROPOSAL_TRACEABILITY_MISSING")
        if not self.requested_changes:
            raise ValueError("CHANGE_PROPOSAL_REQUEST_EMPTY")
        if self.state not in PROPOSAL_STATES:
            raise ValueError("CHANGE_PROPOSAL_STATE_INVALID")
        if self.state == "APPROVED" and self.blocking_reasons:
            raise ValueError("CHANGE_PROPOSAL_APPROVED_WITH_BLOCKERS")

    @property
    def executable(self) -> bool:
        return self.state == "APPROVED" and not self.blocking_reasons

    def trace(self) -> Dict[str, str]:
        return {"proposal_id": self.proposal_id, "execution_id": self.execution_id}


def approve_proposal(proposal: ChangeProposal) -> ChangeProposal:
    proposal.validate()
    if proposal.blocking_reasons:
        raise ValueError("CHANGE_PROPOSAL_BLOCKED")
    return ChangeProposal(
        proposal_id=proposal.proposal_id,
        execution_id=proposal.execution_id,
        requested_changes=proposal.requested_changes,
        impacted_elements=proposal.impacted_elements,
        blocking_reasons=[],
        state="APPROVED",
        evidence=proposal.evidence,
    )
