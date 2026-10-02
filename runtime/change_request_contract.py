"""H74 evidence-bound ChangeRequest contract.

A ChangeRequest records what the user wants changed. It is not an approval,
proposal, or execution authorization. Validation is deterministic and
fail-closed; approval remains a later pipeline stage.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ChangeType = Literal[
    "FURNITURE",
    "FURNITURE_LAYOUT_CHANGE",
    "OVERALL_ARCHITECTURAL_LAYOUT_CHANGE",
]

ALLOWED_CHANGE_TYPES = {
    "FURNITURE",
    "FURNITURE_LAYOUT_CHANGE",
    "OVERALL_ARCHITECTURAL_LAYOUT_CHANGE",
}


@dataclass(frozen=True)
class ChangeRequest:
    request_id: str
    source_sha256: str
    model_id: str
    change_type: ChangeType
    instruction: str
    target_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.request_id:
            raise ValueError("CHANGE_REQUEST_ID_MISSING")
        if len(self.source_sha256) != 64:
            raise ValueError("CHANGE_REQUEST_SOURCE_INVALID")
        if not self.model_id:
            raise ValueError("CHANGE_REQUEST_MODEL_ID_MISSING")
        if self.change_type not in ALLOWED_CHANGE_TYPES:
            raise ValueError("CHANGE_REQUEST_TYPE_INVALID")
        if not isinstance(self.instruction, str) or not self.instruction.strip():
            raise ValueError("CHANGE_REQUEST_INSTRUCTION_MISSING")
        if len(set(self.target_ids)) != len(self.target_ids):
            raise ValueError("CHANGE_REQUEST_TARGET_DUPLICATE")
        if any(not isinstance(value, str) or not value for value in self.target_ids):
            raise ValueError("CHANGE_REQUEST_TARGET_INVALID")
        if len(set(self.evidence_ids)) != len(self.evidence_ids):
            raise ValueError("CHANGE_REQUEST_EVIDENCE_DUPLICATE")
        if any(not isinstance(value, str) or not value for value in self.evidence_ids):
            raise ValueError("CHANGE_REQUEST_EVIDENCE_INVALID")

    def trace(self) -> dict[str, str]:
        self.validate()
        return {
            "request_id": self.request_id,
            "source_sha256": self.source_sha256,
            "model_id": self.model_id,
        }

    @property
    def is_targeted(self) -> bool:
        return bool(self.target_ids)


def build_change_request(
    *,
    request_id: str,
    source_sha256: str,
    model_id: str,
    change_type: str,
    instruction: str,
    target_ids: tuple[str, ...] = (),
    evidence_ids: tuple[str, ...] = (),
) -> ChangeRequest:
    request = ChangeRequest(
        request_id=request_id,
        source_sha256=source_sha256,
        model_id=model_id,
        change_type=change_type,
        instruction=instruction,
        target_ids=tuple(target_ids),
        evidence_ids=tuple(evidence_ids),
    )
    request.validate()
    return request
