"""Compatibility adapter for the hardened H91 final-validation contract.

The legacy dictionary API remains available, but it is fail-closed: it cannot return
PASS unless all H91 evidence fields are present and validated. It never grants edit
authority.
"""
from dataclasses import dataclass
from typing import Any

from .final_validation_contract import evaluate_final_validation


@dataclass(frozen=True)
class FinalValidationResult:
    status: str
    failure_codes: list[str]
    checks: dict[str, Any]


_REQUIRED = (
    "source_sha256",
    "model_id",
    "approved",
    "post_edit_status",
    "post_edit_valid",
    "before_after_status",
    "before_after_valid",
    "audit_complete",
)


def validate_post_edit(post_edit_diff: dict[str, Any]) -> FinalValidationResult:
    """Validate through the H91 contract; missing evidence is never a PASS."""
    missing = [key for key in _REQUIRED if key not in post_edit_diff]
    if missing:
        return FinalValidationResult(
            "UNKNOWN",
            ["FINAL_VALIDATION_EVIDENCE_MISSING"],
            {"missing_required_evidence": tuple(missing)},
        )

    try:
        result = evaluate_final_validation(
            source_sha256=post_edit_diff["source_sha256"],
            model_id=post_edit_diff["model_id"],
            approved=post_edit_diff["approved"],
            post_edit_status=post_edit_diff["post_edit_status"],
            post_edit_valid=post_edit_diff["post_edit_valid"],
            before_after_status=post_edit_diff["before_after_status"],
            before_after_valid=post_edit_diff["before_after_valid"],
            audit_complete=post_edit_diff["audit_complete"],
            approved_target_ids=tuple(post_edit_diff.get("approved_target_ids", ())),
            changed_ids=tuple(post_edit_diff.get("changed_ids", ())),
        )
    except (TypeError, ValueError) as exc:
        return FinalValidationResult(
            "BLOCKED",
            ["FINAL_VALIDATION_INPUT_INVALID"],
            {"error": str(exc)},
        )

    return FinalValidationResult(
        result.status,
        list(result.failure_codes),
        dict(result.checks),
    )
