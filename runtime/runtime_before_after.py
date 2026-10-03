"""Runtime adapter for turning real detector output into before/after snapshots.

This keeps the before/after contract independent from any editing provider.
No snapshot is promoted to PASS unless the caller supplies an approval-grade
detection status.
"""
from __future__ import annotations
from typing import Any
from .before_after_detection import DetectionSnapshot, BeforeAfterDetection, compare_before_after

def snapshot_from_detection(*, source_sha256: str, model_id: str, detection: dict[str, Any], status: str) -> DetectionSnapshot:
    candidates = detection.get("native_dwg_candidates", ())
    elements = []
    for candidate in candidates:
        raw_state = str(candidate.get("status", "UNKNOWN"))
        state = raw_state if raw_state in {"LOCKED", "EDITABLE", "CONDITIONAL", "UNKNOWN"} else "UNKNOWN"
        elements.append({"element_id": str(candidate.get("candidate_id", "")), "element_type": str(candidate.get("element_type", "")), "state": state, "geometry": candidate.get("geometry"), "evidence_ids": tuple(candidate.get("evidence_ids", ()))})
    snapshot = DetectionSnapshot(source_sha256=source_sha256, model_id=model_id, elements=tuple(elements), status=status)
    snapshot.validate()
    return snapshot

def compare_runtime_detections(*, before_detection: dict[str, Any] | None, after_detection: dict[str, Any] | None, source_sha256: str, model_id: str, before_status: str | None, after_status: str | None, approved_target_ids=()) -> BeforeAfterDetection:
    if before_detection is None or after_detection is None or before_status is None or after_status is None:
        return compare_before_after(before=None, after=None, approved_target_ids=approved_target_ids)
    before = snapshot_from_detection(source_sha256=source_sha256, model_id=model_id, detection=before_detection, status=before_status)
    after = snapshot_from_detection(source_sha256=source_sha256, model_id=model_id, detection=after_detection, status=after_status)
    return compare_before_after(before=before, after=after, approved_target_ids=approved_target_ids)
