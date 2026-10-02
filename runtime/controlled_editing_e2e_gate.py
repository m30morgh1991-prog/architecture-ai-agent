"""End-to-end fail-closed gate for approved architectural edits."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlledEditingE2EGate:
    source_sha256: str
    model_id: str
    target_ids: tuple[str,...]
    impact_status: str
    approval_status: str
    visual_status: str
    executable: bool
    reason: str

    def validate(self):
        if not self.source_sha256 or not self.model_id or not self.target_ids:
            raise ValueError("E2E_CONTEXT_MISSING")
        if self.impact_status not in {"PASS","BLOCKED","UNKNOWN","NEEDS_REVIEW"}:
            raise ValueError("E2E_IMPACT_STATUS_INVALID")
        if self.approval_status not in {"APPROVED","REJECTED","NEEDS_REVIEW"}:
            raise ValueError("E2E_APPROVAL_STATUS_INVALID")
        if self.visual_status not in {"READY_FOR_APPROVAL","BLOCKED","UNKNOWN","NEEDS_REVIEW"}:
            raise ValueError("E2E_VISUAL_STATUS_INVALID")
        if self.executable and not (
            self.impact_status=="PASS"
            and self.approval_status=="APPROVED"
            and self.visual_status=="READY_FOR_APPROVAL"
        ):
            raise ValueError("E2E_EXECUTION_GATE_VIOLATION")

def evaluate_controlled_editing_e2e(*,source_sha256,model_id,target_ids,impact_status,approval_status,visual_status):
    executable=(impact_status=="PASS" and approval_status=="APPROVED" and visual_status=="READY_FOR_APPROVAL")
    reason="All approval gates passed." if executable else "Execution blocked until impact, approval, and visual gates all pass."
    r=ControlledEditingE2EGate(source_sha256,model_id,tuple(target_ids),impact_status,approval_status,visual_status,executable,reason)
    r.validate()
    return r
