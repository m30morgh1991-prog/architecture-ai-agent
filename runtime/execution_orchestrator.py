"""Execution orchestration boundary for AI-assisted interpretation.

The orchestrator may call the AI router for interpretation evidence, but the
deterministic execution path remains authoritative for proposal, validation,
editing, and post-edit checks.
"""
from dataclasses import dataclass
from typing import Any

from .ai_router import AIRouter, AIRouteResult
from .provider_policy import ProviderCapability, ProviderSelectionPolicy


@dataclass(frozen=True)
class OrchestrationResult:
    execution_id: str
    ai_route: AIRouteResult
    request: dict[str, Any]


class ExecutionOrchestrator:
    def __init__(
        self,
        router: AIRouter,
        capabilities: list[ProviderCapability],
    ):
        self.router = router
        self.capabilities = list(capabilities)
        self.policy = ProviderSelectionPolicy()

    def prepare(self, execution_id: str, request: dict[str, Any], required_capabilities=None):
        required = frozenset(required_capabilities or {"interpret"})
        selected = self.policy.select(self.capabilities, required)
        if selected.provider_id not in {p.provider_id for p in self.router.providers}:
            raise RuntimeError("PROVIDER_ADAPTER_MISSING")
        route = self.router.route(
            {**request, "provider_id": selected.provider_id}
        )
        return OrchestrationResult(execution_id, route, request)
