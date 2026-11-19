"""Execution-scoped idempotency guard bound to a canonical request fingerprint.

Completed executions may be replayed only for the exact same request payload.
Reusing a key with a different payload is a conflict and remains fail-closed.
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

    def has_completed(self, key: str) -> bool:
        return key in self._completed

    def clear(self, key: str) -> None:
        self._completed.pop(key, None)
