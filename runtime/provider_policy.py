"""Deterministic provider selection policy for the AI Router.

Selection uses declared capability, health, cost class and explicit priority.
No provider-specific business logic is placed in the Architecture Core.
"""
from dataclasses import dataclass
from typing import FrozenSet


@dataclass(frozen=True)
class ProviderCapability:
    provider_id: str
    capabilities: FrozenSet[str]
    healthy: bool = True
    cost_class: str = "standard"
    priority: int = 100


class ProviderSelectionPolicy:
    def select(self, providers: list[ProviderCapability], required: set[str]) -> ProviderCapability:
        eligible = [
            p for p in providers
            if p.healthy and required.issubset(p.capabilities)
        ]
        if not eligible:
            raise RuntimeError("NO_CAPABLE_PROVIDER")
        return sorted(eligible, key=lambda p: (p.priority, p.cost_class, p.provider_id))[0]
