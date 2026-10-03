"""Fail-closed final validation contract for controlled architectural edits.

This contract is intentionally independent of any specific AI/provider. It consumes
validated post-edit evidence and requires source/model identity, audit completeness,
and an explicit approved scope before returning PASS.
"""
from dataclasses import dataclass
from typing import Any

_ALLOWED = {"PASS", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"}

@dataclass(frozen=True)
class FinalValidationContract:
    status: str
    failure_codes: tuple[str, ...]
    source_sha256: str
    model_id: str
    checks: dict[str, Any]
    def validate(self) -> None:
        if self.status not in _ALLOWED: raise ValueError("FINAL_VALIDATION_STATUS_INVALID")
        if not self.source_sha256 or len(self.source_sha256) != 64: raise ValueError("FINAL_VALIDATION_IDENTITY_INVALID")
        if not self.model_id: raise ValueError("FINAL_VALIDATION_MODEL_ID_MISSING")
        if self.status == "PASS" and self.failure_codes: raise ValueError("FINAL_VALIDATION_PASS_HAS_FAILURE_CODES")

def evaluate_final_validation(*, source_sha256: str, model_id: str, approved: bool,
    post_edit_status: str, post_edit_valid: bool, before_after_status: str,
    before_after_valid: bool, audit_complete: bool, approved_target_ids=(), changed_ids=()):
    checks={"identity":bool(source_sha256 and len(source_sha256)==64 and model_id),
            "approved":bool(approved),"post_edit_pass":post_edit_status=="PASS" and bool(post_edit_valid),
            "before_after_pass":before_after_status=="PASS" and bool(before_after_valid),
            "audit_complete":bool(audit_complete)}
    if not checks["identity"]: status,code="BLOCKED","FINAL_VALIDATION_IDENTITY_INVALID"
    elif post_edit_status in {"UNKNOWN","NEEDS_REVIEW"} or before_after_status in {"UNKNOWN","NEEDS_REVIEW"}: status,code="NEEDS_REVIEW","FINAL_VALIDATION_EVIDENCE_UNCERTAIN"
    elif post_edit_status=="BLOCKED" or before_after_status=="BLOCKED": status,code="BLOCKED","FINAL_VALIDATION_EVIDENCE_BLOCKED"
    elif not approved: status,code="BLOCKED","FINAL_VALIDATION_NOT_APPROVED"
    elif not checks["post_edit_pass"]: status,code="BLOCKED","FINAL_VALIDATION_POST_EDIT_NOT_PASS"
    elif not checks["before_after_pass"]: status,code="BLOCKED","FINAL_VALIDATION_BEFORE_AFTER_NOT_PASS"
    elif not audit_complete: status,code="BLOCKED","FINAL_VALIDATION_AUDIT_INCOMPLETE"
    elif set(changed_ids)-set(approved_target_ids): status,code="BLOCKED","FINAL_VALIDATION_SCOPE_MISMATCH"
    else: status,code="PASS",""
    result=FinalValidationContract(status,(code,) if code else (),source_sha256,model_id,checks); result.validate(); return result
