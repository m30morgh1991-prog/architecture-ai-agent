import unittest

from runtime.ai_router import AIRouter
from runtime.execution_orchestrator import ExecutionOrchestrator
from runtime.provider_policy import ProviderCapability


class Provider:
    def __init__(self, provider_id, available=True):
        self.provider_id = provider_id
        self._available = available

    def available(self):
        return self._available

    def interpret(self, request):
        return {"echo_provider": self.provider_id, "request": request}


class ExecutionOrchestratorTests(unittest.TestCase):
    def test_policy_selected_provider_is_used_by_router(self):
        providers = [Provider("slow"), Provider("preferred")]
        caps = [
            ProviderCapability("slow", frozenset({"interpret"}), priority=20),
            ProviderCapability("preferred", frozenset({"interpret"}), priority=10),
        ]
        result = ExecutionOrchestrator(AIRouter(providers), caps).prepare(
            "exec-1", {"text": "move sofa"}
        )
        self.assertEqual(result.ai_route.provider_id, "preferred")
        self.assertEqual(result.ai_route.evidence["echo_provider"], "preferred")

    def test_missing_adapter_is_blocked(self):
        caps = [ProviderCapability("ghost", frozenset({"interpret"}), priority=1)]
        with self.assertRaisesRegex(RuntimeError, "PROVIDER_ADAPTER_MISSING"):
            ExecutionOrchestrator(AIRouter([Provider("real")]), caps).prepare(
                "exec-2", {"text": "move sofa"}
            )

    def test_required_capability_is_enforced(self):
        caps = [ProviderCapability("p", frozenset({"vision"}), priority=1)]
        with self.assertRaisesRegex(RuntimeError, "NO_CAPABLE_PROVIDER"):
            ExecutionOrchestrator(AIRouter([Provider("p")]), caps).prepare(
                "exec-3", {"text": "move sofa"}, required_capabilities={"interpret"}
            )


if __name__ == "__main__":
    unittest.main()
