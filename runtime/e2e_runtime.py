"""Provider-neutral end-to-end runtime orchestration slice.

This boundary composes execution orchestration, visual detection/rendering and
the existing deterministic execute path without allowing AI output to bypass
approval or post-edit validation.
"""
from dataclasses import dataclass
from typing import Any

from .execution_orchestrator import ExecutionOrchestrator
from .visual_orchestration import VisualExecutionBoundary


@dataclass(frozen=True)
class E2ERuntimeResult:
    visual: Any
    execution: dict[str, Any]


class E2ERuntimeBoundary:
    def __init__(self, visual_boundary: VisualExecutionBoundary, execute_fn):
        self.visual_boundary = visual_boundary
        self.execute_fn = execute_fn

    def run(
        self,
        execution_id: str,
        request: dict[str, Any],
        document: Any,
        approved_change_plan: dict[str, Any],
        plan: dict[str, Any],
    ) -> E2ERuntimeResult:
        visual = self.visual_boundary.render(
            execution_id,
            request,
            document,
            approved_change_plan,
        )
        execution = self.execute_fn(plan, request)
        return E2ERuntimeResult(visual=visual, execution=execution)
