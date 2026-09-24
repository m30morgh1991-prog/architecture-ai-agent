import unittest

from runtime.ai_router import AIRouter
from runtime.visual_adapter import VisualAdapterBoundary


class FakeProvider:
    def __init__(self, provider_id, available, payload):
        self.provider_id = provider_id
        self._available = available
        self.payload = payload

    def available(self):
        return self._available

    def interpret(self, request):
        return self.payload


class FakeVisual:
    adapter_id = "fake-visual"

    def detect(self, document):
        return {"type": "evidence", "elements": ["C01"]}

    def render_candidate(self, approved_change_plan, document):
        return {"candidate": True}


class AIRouterTests(unittest.TestCase):
    def test_routes_to_first_available_provider(self):
        router = AIRouter([
            FakeProvider("p1", False, {}),
            FakeProvider("p2", True, {"intent": "furniture"}),
        ])
        result = router.route({"prompt": "move sofa"})
        self.assertEqual(result.provider_id, "p2")
        self.assertEqual(result.evidence["intent"], "furniture")

    def test_no_provider_is_explicit_failure(self):
        router = AIRouter([FakeProvider("p1", False, {})])
        with self.assertRaisesRegex(RuntimeError, "AI_PROVIDER_UNAVAILABLE"):
            router.route({})


class VisualAdapterTests(unittest.TestCase):
    def test_detection_returns_evidence(self):
        boundary = VisualAdapterBoundary(FakeVisual())
        result = boundary.detect("plan")
        self.assertEqual(result.adapter_id, "fake-visual")
        self.assertEqual(result.payload["elements"], ["C01"])

    def test_render_requires_approved_change_plan(self):
        boundary = VisualAdapterBoundary(FakeVisual())
        with self.assertRaisesRegex(ValueError, "APPROVED_CHANGE_PLAN_REQUIRED"):
            boundary.render_candidate({"status": "PROPOSED"}, "plan")

    def test_render_accepts_approved_change_plan(self):
        boundary = VisualAdapterBoundary(FakeVisual())
        result = boundary.render_candidate({"status": "APPROVED"}, "plan")
        self.assertTrue(result["candidate"])


if __name__ == "__main__":
    unittest.main()
