"""Post-edit diff integration for fail-closed before/after verification.

The diff is derived from the before/after detector result, not from image output.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .before_after_detection import BeforeAfterDetection


@dataclass(frozen=True)
class PostEditDiff:
    changed_ids: tuple[str, ...]
    locked_changes: tuple[str, ...]
    unauthorized_changes: tuple[str, ...]
    added_ids: tuple[str, ...]
    removed_ids: tuple[str, ...]
    source_sha256: str
    model_id: str
    valid: bool
    status: str
    reason: str

    def validate(self) -> None:
        if not self.source_sha256 or not self.model_id:
            raise ValueError("POST_EDIT_IDENTITY_MISSING")
        if self.status not in {"PASS", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"}:
            raise ValueError("POST_EDIT_STATUS_INVALID")
        if self.valid and self.status != "PASS":
            raise ValueError("POST_EDIT_PASS_STATUS_MISMATCH")
        if self.status == "PASS" and (
            self.locked_changes or self.unauthorized_changes or self.added_ids or self.removed_ids
        ):
            raise ValueError("POST_EDIT_PASS_HAS_UNAUTHORIZED_DELTA")


def build_post_edit_diff(*, before_after: BeforeAfterDetection | None) -> PostEditDiff:
    if before_after is None:
        return PostEditDiff((), (), (), (), (), "", "", False, "UNKNOWN", "BEFORE_AFTER_DETECTION_MISSING")

    status = before_after.status
    valid = bool(
        before_after.valid
        and not before_after.locked_changed_ids
        and not before_after.unauthorized_changed_ids
        and not before_after.added_ids
        and not before_after.removed_ids
    )
    if valid:
        status = "PASS"
        reason = "Post-edit diff matches approved before/after scope."
    elif before_after.status == "BLOCKED":
        status = "BLOCKED"
        reason = before_after.reason
    elif before_after.status == "UNKNOWN":
        status = "UNKNOWN"
        reason = before_after.reason
    else:
        status = "NEEDS_REVIEW"
        reason = before_after.reason

    result = PostEditDiff(
        changed_ids=tuple(before_after.changed_ids),
        locked_changes=tuple(before_after.locked_changed_ids),
        unauthorized_changes=tuple(before_after.unauthorized_changed_ids),
        added_ids=tuple(before_after.added_ids),
        removed_ids=tuple(before_after.removed_ids),
        source_sha256=before_after.source_sha256,
        model_id=before_after.model_id,
        valid=valid,
        status=status,
        reason=reason,
    )
    result.validate()
    return result


def build_post_edit_diff_from_runtime(
    *,
    before_detection: dict[str, Any] | None,
    after_detection: dict[str, Any] | None,
    source_sha256: str,
    model_id: str,
    before_status: str | None,
    after_status: str | None,
    approved_target_ids=(),
) -> PostEditDiff:
    from .runtime_before_after import compare_runtime_detections

    comparison = compare_runtime_detections(
        before_detection=before_detection,
        after_detection=after_detection,
        source_sha256=source_sha256,
        model_id=model_id,
        before_status=before_status,
        after_status=after_status,
        approved_target_ids=approved_target_ids,
    )
    return build_post_edit_diff(before_after=comparison)
