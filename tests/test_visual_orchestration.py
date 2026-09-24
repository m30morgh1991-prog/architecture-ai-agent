import unittest

from runtime.ai_router import AIRouter
from runtime.execution_orchestrator import ExecutionOrchestrator
from runtime.provider_policy import ProviderCapability
from runtime.visual_adapter import VisualAdapterBoundary
from runtime.visual_orchestration import VisualExecutionBoundary


class FakeProvider:
    provider_id = "visual-provider"

    def available(self):
        return True

    def interpret(self, request):
        return {"kind": "evidence", "request": request}


class FakeVisual:
    adapter_id = "fake-visual"

    def detect(self, document):
        return {"document": document, "elements": ["COL-01", "FUR-01"]}

    def render_candidate(self, approved_change_plan, document):
        return {"edited": True, "plan": approved_change_plan, "document": document}


def make_boundary():
    router = AIRouter([FakeProvider()])
    orchestrator = ExecutionOrchestrator(
        router, [ProviderCapability("visual-provider", frozenset({"interpret", "vision"}))]
    )
    visual = VisualAdapterBoundary(FakeVisual())
    return VisualExecutionBoundary(orchestrator, visual)


class VisualExecutionBoundaryTests(unittest.TestCase):
    def test_detection_flows_through_orchestrator_and_visual_adapter(self):
        boundary = make_boundary()
        result = boundary.detect("ex-12", {"change": "rearrange furniture"}, "plan.png")
        self.assertEqual(result.orchestration.ai_route.provider_id, "visual-provider")
        self.assertEqual(result.evidence.adapter_id, "fake-visual")
        self.assertIn("COL-01", result.evidence.payload["elements"])
        self.assertIsNone(result.candidate)

    def test_render_requires_approved_change_plan(self):
        boundary = make_boundary()
        with self.assertRaisesRegex(ValueError, "APPROVED_CHANGE_PLAN_REQUIRED"):
            boundary.render(
                "ex-13",
                {"change": "rearrange furniture"},
                "plan.png",
                {"status": "PROPOSED"},
            )

    def test_approved_render_is_allowed(self):
        boundary = make_boundary()
        result = boundary.render(
            "ex-14",
            {"change": "rearrange furniture"},
            "plan.png",
            {"status": "APPROVED", "changes": ["FUR-01"]},
        )
        self.assertTrue(result.candidate["edited"])
        self.assertEqual(result.candidate["plan"]["status"], "APPROVED")

    def test_provider_capability_is_enforced_before_visual_work(self):
        boundary = make_boundary()
        with self.assertRaisesRegex(RuntimeError, "NO_CAPABLE_PROVIDER"):
            boundary.detect(
                "ex-15",
                {"change": "rearrange furniture"},
                "plan.png",
                required_capabilities={"interpret", "3d"},
            )


if __name__ == "__main__":
    unittest.main()
