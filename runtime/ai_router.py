"""Provider-neutral AI routing boundary.

The router is intentionally small: providers are adapters, and their output
cannot become an approved edit directly. The deterministic core remains the
authority for constraints, rules, proposals, and validation.
"""
from dataclasses import dataclass
from typing import Any, Protocol


class AIProviderAdapter(Protocol):
    provider_id: str

    def available(self) -> bool: ...
    def interpret(self, request: dict[str, Any]) -> dict[str, Any]: ...


@dataclass(frozen=True)
class AIRouteResult:
    provider_id: str
    evidence: dict[str, Any]


class AIRouter:
    def __init__(self, providers: list[AIProviderAdapter]):
        self.providers = list(providers)

    def route(self, request: dict[str, Any]) -> AIRouteResult:
        for provider in self.providers:
            if provider.available():
                evidence = provider.interpret(request)
                return AIRouteResult(
                    provider_id=provider.provider_id,
                    evidence=evidence,
                )
        raise RuntimeError("AI_PROVIDER_UNAVAILABLE")
