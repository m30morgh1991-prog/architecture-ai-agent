"""Provider-neutral CAD adapter contract.

AutoCAD-MCP is one possible implementation of this boundary. The Architecture
Core owns semantics, approval, and validation; adapters only inspect or execute
typed, already-approved operations.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Protocol

AdapterStatus = Literal["READY", "UNAVAILABLE", "BLOCKED", "NEEDS_REVIEW"]
ExecutionStatus = Literal["APPLIED", "BLOCKED", "FAILED", "NEEDS_REVIEW"]

@dataclass(frozen=True)
class CADCapability:
    capability_id: str
    read_only: bool
    supports_headless: bool

@dataclass(frozen=True)
class CADInspectionEvidence:
    adapter_id: str
    source_sha256: str
    payload: dict[str, Any]
    status: AdapterStatus

    def validate(self, expected_source_sha256: str) -> None:
        if not self.adapter_id:
            raise ValueError("CAD_ADAPTER_ID_MISSING")
        if len(self.source_sha256) != 64:
            raise ValueError("CAD_SOURCE_SHA_INVALID")
        if self.source_sha256 != expected_source_sha256:
            raise ValueError("CAD_SOURCE_SHA_MISMATCH")
        if self.status not in {"READY", "UNAVAILABLE", "BLOCKED", "NEEDS_REVIEW"}:
            raise ValueError("CAD_ADAPTER_STATUS_INVALID")

@dataclass(frozen=True)
class CADExecutionRequest:
    source_sha256: str
    document_id: str
    expected_revision: str
    idempotency_key: str
    approved_change_plan_id: str
    operations: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    def validate(self) -> None:
        if len(self.source_sha256) != 64:
            raise ValueError("CAD_SOURCE_SHA_INVALID")
        if not self.document_id or not self.expected_revision:
            raise ValueError("CAD_DOCUMENT_FENCE_MISSING")
        if not self.idempotency_key:
            raise ValueError("CAD_IDEMPOTENCY_KEY_MISSING")
        if not self.approved_change_plan_id:
            raise ValueError("APPROVED_CHANGE_PLAN_REQUIRED")
        if not self.operations:
            raise ValueError("CAD_OPERATIONS_EMPTY")

@dataclass(frozen=True)
class CADExecutionResult:
    adapter_id: str
    status: ExecutionStatus
    source_sha256: str
    document_id: str
    before_revision: str
    after_revision: str | None
    requested_operations: tuple[dict[str, Any], ...]
    actual_operations: tuple[dict[str, Any], ...]
    failure_codes: tuple[str, ...] = ()

    def validate(self, request: CADExecutionRequest) -> None:
        if self.source_sha256 != request.source_sha256:
            raise ValueError("CAD_RESULT_SOURCE_MISMATCH")
        if self.document_id != request.document_id:
            raise ValueError("CAD_RESULT_DOCUMENT_MISMATCH")
        if self.status == "APPLIED":
            if not self.after_revision:
                raise ValueError("CAD_POSTCONDITION_REVISION_MISSING")
            if self.requested_operations != self.actual_operations:
                raise ValueError("CAD_REQUEST_ACTUAL_DIFF")

class CADAdapter(Protocol):
    adapter_id: str
    def capabilities(self) -> tuple[CADCapability, ...]: ...
    def inspect(self, source: Any, source_sha256: str) -> CADInspectionEvidence: ...
    def execute(self, request: CADExecutionRequest) -> CADExecutionResult: ...
