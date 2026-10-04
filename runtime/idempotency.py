"""Execution-scoped idempotency guard for deterministic recovery.

A completed execution is replayed from its stored result instead of being
executed a second time. In-flight/unknown keys remain fail-closed.
"""
from __future__ import annotations

from typing import Any


class IdempotencyGuard:
    def __init__(self):
        self._completed: dict[str, Any] = {}

    def check(self, key: str):
        return self._completed.get(key)

    def store(self, key: str, result):
        if key in self._completed:
            return self._completed[key]
        self._completed[key] = result
        return result

    def has_completed(self, key: str) -> bool:
        return key in self._completed

    def clear(self, key: str) -> None:
        self._completed.pop(key, None)
