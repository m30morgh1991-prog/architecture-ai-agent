"""Visual interpretation/editing boundary.

This module defines the seam between visual workers and the deterministic
Architecture Core. A visual worker may produce evidence or a candidate image;
it never decides editability or bypasses validation.
"""
from dataclasses import dataclass
from typing import Any, Protocol


class VisualAdapter(Protocol):
    adapter_id: str

    def detect(self, document: Any) -> dict[str, Any]: ...
    def render_candidate(
        self, approved_change_plan: dict[str, Any], document: Any
    ) -> Any: ...


@dataclass(frozen=True)
class VisualEvidence:
    adapter_id: str
    payload: dict[str, Any]


class VisualAdapterBoundary:
    def __init__(self, adapter: VisualAdapter):
        self.adapter = adapter

    def detect(self, document: Any) -> VisualEvidence:
        return VisualEvidence(
            adapter_id=self.adapter.adapter_id,
            payload=self.adapter.detect(document),
        )

    def render_candidate(
        self, approved_change_plan: dict[str, Any], document: Any
    ) -> Any:
        # Only an ApprovedChangePlan is accepted at this boundary.
        if approved_change_plan.get("status") != "APPROVED":
            raise ValueError("APPROVED_CHANGE_PLAN_REQUIRED")
        return self.adapter.render_candidate(approved_change_plan, document)
