import unittest

from runtime.contracts import ChangeRequest, Element, PlanModel
from runtime.real_visual_controlled_bridge import execute_real_visual_approved_change


class H48EndToEndApprovalBridgeTests(unittest.TestCase):
    def _ready(self):
        return {
            "status": "READY_FOR_APPROVAL",
            "contracts": {"status": "VALID"},
            "semantic_corroboration": {"status": "ACCESSIBLE"},
            "constraint_map": {
                "protected_element_ids": ("C01",),
                "editable_element_ids": ("F01",),
                "conditional_element_ids": (),
                "unknown_element_ids": (),
            },
        }

    def _plan(self):
        return PlanModel("P-H48", [
            Element("C01", "COLUMN", "LOCKED", {"x": 10, "y": 10}),
            Element("F01", "FURNITURE", "EDITABLE", {"x": 20, "y": 20}),
        ])

    def test_ready_visual_evidence_reaches_controlled_execution(self):
        request = ChangeRequest("FURNITURE", ["F01"], "Move sofa")
        result = execute_real_visual_approved_change(
            self._ready(), request, self._plan(), {"F01": {"x": 30, "y": 20}}
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["stage"], "EXECUTION")
        self.assertEqual(result["approval"]["approved_target_ids"], ["F01"])
        self.assertEqual(result["execution"]["post_edit_diff"]["locked_delta_ids"], [])
        self.assertEqual(result["execution"]["post_edit_diff"]["unauthorized_delta_ids"], [])

    def test_blocked_visual_evidence_never_reaches_execution(self):
        request = ChangeRequest("FURNITURE", ["F01"], "Move sofa")
        result = execute_real_visual_approved_change(
            {"status": "BLOCKED", "blockers": ["LOCKED_ELEMENT_UNCERTAIN"]},
            request, self._plan(), {"F01": {"x": 30, "y": 20}}
        )
        self.assertEqual(result["status"], "REJECT")
        self.assertEqual(result["stage"], "APPROVAL")
        self.assertIn("LOCKED_ELEMENT_UNCERTAIN", result["failure_codes"])
        self.assertNotIn("execution", result)

    def test_approved_visual_target_cannot_bypass_plan_permission(self):
        request = ChangeRequest("FURNITURE", ["F01"], "Move sofa")
        plan = PlanModel("P-H48-LOCK", [
            Element("C01", "COLUMN", "LOCKED", {"x": 10, "y": 10}),
            Element("F01", "FURNITURE", "LOCKED", {"x": 20, "y": 20}),
        ])
        result = execute_real_visual_approved_change(
            self._ready(), request, plan, {"F01": {"x": 30, "y": 20}}
        )
        self.assertEqual(result["status"], "REJECT")
        self.assertEqual(result["stage"], "EXECUTION_AUTHORIZATION")
        self.assertIn("EDIT_PERMISSION_REQUIRED:F01", result["failure_codes"])


if __name__ == "__main__":
    unittest.main()
