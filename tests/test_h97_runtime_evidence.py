import unittest

from runtime.app import execute
from runtime.contracts import ChangeRequest, Element, PlanModel


class H97RuntimeEvidenceTests(unittest.TestCase):
    def test_success_exposes_audit_and_runtime_evidence(self):
        plan = PlanModel(
            "h97-model",
            [Element("F01", "FURNITURE", "EDITABLE", {"x": 0, "y": 0})],
        )
        request = ChangeRequest("FURNITURE", ["F01"], "move furniture")
        result = execute(
            plan,
            request,
            simulated_geometry={"F01": {"x": 10, "y": 10}},
            execution_id="h97-success",
        )
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["audit_complete"])
        self.assertTrue(result["audit_ok"])
        self.assertTrue(result["runtime_ok"])

    def test_blocked_execution_cannot_claim_runtime_or_audit_pass(self):
        plan = PlanModel(
            "h97-blocked",
            [Element("C01", "COLUMN", "LOCKED", {"x": 0, "y": 0})],
        )
        request = ChangeRequest("FURNITURE", ["C01"], "move furniture")
        result = execute(plan, request, execution_id="h97-blocked")
        self.assertNotEqual(result["status"], "PASS")
        self.assertFalse(result.get("audit_ok", False))
        self.assertFalse(result.get("runtime_ok", False))


if __name__ == "__main__":
    unittest.main()
