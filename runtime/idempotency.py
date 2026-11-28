"""Execution-scoped idempotency state bound to a canonical request fingerprint.

A key can hold an in-progress or terminal result. Replays require the exact same
fingerprint; a different payload remains a conflict. Completion queries must not
treat a RUNNING workflow decision as terminal.
"""
from __future__ import annotations

from typing import Any


class IdempotencyConflictError(ValueError):
    """Raised when an idempotency key is reused for a different request."""


class IdempotencyGuard:
    def __init__(self):
        self._completed: dict[str, tuple[str, Any]] = {}

    def check(self, key: str, request_fingerprint: str):
        entry = self._completed.get(key)
        if entry is None:
            return None

        stored_fingerprint, result = entry
        if stored_fingerprint != request_fingerprint:
            raise IdempotencyConflictError(
                "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST"
            )
        return result

    def store(self, key: str, request_fingerprint: str, result):
        entry = self._completed.get(key)
        if entry is not None:
            stored_fingerprint, stored_result = entry
            if stored_fingerprint != request_fingerprint:
                raise IdempotencyConflictError(
                    "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST"
                )
            return stored_result

        self._completed[key] = (request_fingerprint, result)
        return result

    def replace(self, key: str, request_fingerprint: str, result):
        """Update the result for the same key/fingerprint during a lifecycle."""
        entry = self._completed.get(key)
        if entry is not None and entry[0] != request_fingerprint:
            raise IdempotencyConflictError(
                "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST"
            )
        self._completed[key] = (request_fingerprint, result)
        return result

    def has_completed(self, key: str) -> bool:
        entry = self._completed.get(key)
        if entry is None:
            return False
        result = entry[1]
        state = getattr(result, "state", None)
        if isinstance(result, dict):
            state = result.get("state", state)
        terminal_states = {"SUCCEEDED", "FAILED", "BLOCKED"}
        if state is not None:
            return isinstance(state, str) and state in terminal_states
        status = result.get("status") if isinstance(result, dict) else None
        terminal_statuses = {
            "PASS", "REJECT", "NEEDS_REVISION", "SUCCEEDED", "FAILED", "BLOCKED"
        }
        if status is not None:
            return isinstance(status, str) and status in terminal_statuses
        # Unknown result shapes are not evidence of completion. Fail closed.
        return False

    def clear(self, key: str) -> None:
        self._completed.pop(key, None)
