"""Execution boundary for visual evidence and approved candidate rendering.

The visual adapter is reached only through the execution orchestration layer.
Detection produces evidence; rendering requires an explicitly approved change
plan and never decides editability or validation.
"""
from dataclasses import dataclass
from typing import Any

from .execution_orchestrator import ExecutionOrchestrator, OrchestrationResult
from .visual_adapter import VisualAdapterBoundary, VisualEvidence


@dataclass(frozen=True)
class VisualExecutionResult:
    orchestration: OrchestrationResult
    evidence: VisualEvidence
    candidate: Any = None


class VisualExecutionBoundary:
    def __init__(
        self,
        orchestrator: ExecutionOrchestrator,
        visual: VisualAdapterBoundary,
    ):
        self.orchestrator = orchestrator
        self.visual = visual

    def detect(
        self,
        execution_id: str,
        request: dict[str, Any],
        document: Any,
        required_capabilities=None,
    ) -> VisualExecutionResult:
        orchestration = self.orchestrator.prepare(
            execution_id, request, required_capabilities
        )
        evidence = self.visual.detect(document)
        return VisualExecutionResult(orchestration, evidence)

    def render(
        self,
        execution_id: str,
        request: dict[str, Any],
        document: Any,
        approved_change_plan: dict[str, Any],
        required_capabilities=None,
    ) -> VisualExecutionResult:
        orchestration = self.orchestrator.prepare(
            execution_id, request, required_capabilities
        )
        candidate = self.visual.render_candidate(approved_change_plan, document)
        evidence = self.visual.detect(document)
        return VisualExecutionResult(orchestration, evidence, candidate)
