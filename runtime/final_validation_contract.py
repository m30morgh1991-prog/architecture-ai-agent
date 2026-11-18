"""Fail-closed final validation contract for controlled architectural edits."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_ALLOWED = {"PASS", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"}
_ALLOWED_EVIDENCE_STATES = {"PASS", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"}


def _valid_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and value == value.lower()
        and all(character in "0123456789abcdef" for character in value)
    )


def _valid_ids(value: object) -> bool:
    return (
        isinstance(value, (tuple, list))
        and all(isinstance(item, str) and item.strip() for item in value)
        and len(value) == len(set(value))
    )


@dataclass(frozen=True)
class FinalValidationContract:
    status: str
    failure_codes: tuple[str, ...]
    source_sha256: str
    model_id: str
    checks: dict[str, Any]

    def validate(self) -> None:
        if self.status not in _ALLOWED:
            raise ValueError("FINAL_VALIDATION_STATUS_INVALID")
        if self.status == "PASS":
            if not _valid_sha256(self.source_sha256):
                raise ValueError("FINAL_VALIDATION_IDENTITY_INVALID")
            if not isinstance(self.model_id, str) or not self.model_id.strip():
                raise ValueError("FINAL_VALIDATION_MODEL_ID_MISSING")
            if self.failure_codes:
                raise ValueError("FINAL_VALIDATION_PASS_HAS_FAILURE_CODES")
            required = ("identity", "approved", "post_edit_pass", "before_after_pass", "audit_complete")
            if not isinstance(self.checks, dict) or any(self.checks.get(key) is not True for key in required):
                raise ValueError("FINAL_VALIDATION_PASS_HAS_FAILED_CHECKS")


def evaluate_final_validation(
    *,
    source_sha256: str,
    model_id: str,
    approved: bool,
    post_edit_status: str,
    post_edit_valid: bool,
    before_after_status: str,
    before_after_valid: bool,
    audit_complete: bool,
    approved_target_ids=(),
    changed_ids=(),
):
    boolean_inputs = {
        "approved": approved,
        "post_edit_valid": post_edit_valid,
        "before_after_valid": before_after_valid,
        "audit_complete": audit_complete,
    }
    booleans_valid = all(type(value) is bool for value in boolean_inputs.values())
    ids_valid = _valid_ids(approved_target_ids) and _valid_ids(changed_ids)
    statuses_valid = (
        post_edit_status in _ALLOWED_EVIDENCE_STATES
        and before_after_status in _ALLOWED_EVIDENCE_STATES
    )
    identity_valid = _valid_sha256(source_sha256) and isinstance(model_id, str) and bool(model_id.strip())

    checks = {
        "identity": identity_valid,
        "approved": approved is True,
        "post_edit_pass": post_edit_status == "PASS" and post_edit_valid is True,
        "before_after_pass": before_after_status == "PASS" and before_after_valid is True,
        "audit_complete": audit_complete is True,
    }

    if not booleans_valid:
        status, code = "BLOCKED", "FINAL_VALIDATION_BOOLEAN_EVIDENCE_INVALID"
    elif not ids_valid:
        status, code = "BLOCKED", "FINAL_VALIDATION_SCOPE_INVALID"
    elif not statuses_valid:
        status, code = "BLOCKED", "FINAL_VALIDATION_EVIDENCE_STATUS_INVALID"
    elif not identity_valid:
        status, code = "BLOCKED", "FINAL_VALIDATION_IDENTITY_INVALID"
    elif post_edit_status in {"UNKNOWN", "NEEDS_REVIEW"} or before_after_status in {"UNKNOWN", "NEEDS_REVIEW"}:
        status, code = "NEEDS_REVIEW", "FINAL_VALIDATION_EVIDENCE_UNCERTAIN"
    elif post_edit_status == "BLOCKED" or before_after_status == "BLOCKED":
        status, code = "BLOCKED", "FINAL_VALIDATION_EVIDENCE_BLOCKED"
    elif approved is not True:
        status, code = "BLOCKED", "FINAL_VALIDATION_NOT_APPROVED"
    elif not checks["post_edit_pass"]:
        status, code = "BLOCKED", "FINAL_VALIDATION_POST_EDIT_NOT_PASS"
    elif not checks["before_after_pass"]:
        status, code = "BLOCKED", "FINAL_VALIDATION_BEFORE_AFTER_NOT_PASS"
    elif audit_complete is not True:
        status, code = "BLOCKED", "FINAL_VALIDATION_AUDIT_INCOMPLETE"
    elif set(changed_ids) - set(approved_target_ids):
        status, code = "BLOCKED", "FINAL_VALIDATION_SCOPE_MISMATCH"
    else:
        status, code = "PASS", ""

    result = FinalValidationContract(
        status,
        (code,) if code else (),
        source_sha256,
        model_id,
        checks,
    )
    result.validate()
    return result
