import unittest

from runtime.contracts import ChangeRequest
from runtime.approved_change_plan_contract import build_approved_change_plan
from runtime.controlled_editing_contract import build_controlled_editing_decision, EditPermission
from runtime.controlled_editing_runtime import build_runtime_controlled_decision
from runtime.plan_model_contract import ConstraintMap


class H40H41RuntimeContractTests(unittest.TestCase):
    def test_approved_change_plan_requires_editable_targets(self):
        request = ChangeRequest("FURNITURE", ["F01"], "Move sofa")
        result = build_approved_change_plan(
            change_request=request,
            available_element_ids=["C01", "F01"],
            editable_element_ids=["F01"],
        )
        self.assertEqual(result.status, "APPROVED")
        self.assertEqual(result.approved_target_ids, ("F01",))

    def test_approved_change_plan_rejects_locked_target(self):
        request = ChangeRequest("FURNITURE", ["C01"], "Move column")
        result = build_approved_change_plan(
            change_request=request,
            available_element_ids=["C01", "F01"],
            editable_element_ids=["F01"],
        )
        self.assertEqual(result.status, "REJECT")
        self.assertEqual(result.reason, "EDIT_PERMISSION_REQUIRED")

    def test_controlled_decision_blocks_locked_target(self):
        cmap = ConstraintMap(
            "cm1", "pm1", ("C01",), ("F01",), (), (), ("ev1",)
        )
        decision = build_runtime_controlled_decision(cmap, ["C01"])
        self.assertFalse(decision.executable)
        self.assertIn("LOCKED_ELEMENT_CONFLICT:C01", decision.blocking_reasons())

    def test_controlled_decision_allows_editable_target(self):
        cmap = ConstraintMap(
            "cm1", "pm1", ("C01",), ("F01",), (), (), ("ev1",)
        )
        decision = build_runtime_controlled_decision(cmap, ["F01"])
        self.assertTrue(decision.executable)
        self.assertEqual(decision.blocking_reasons(), [])

    def test_controlled_decision_blocks_unresolved_constraint_map(self):
        cmap = ConstraintMap(
            "cm1", "pm1", (), ("F01",), (), ("X01",), ("ev1",)
        )
        decision = build_runtime_controlled_decision(cmap, ["F01"])
        self.assertFalse(decision.executable)
        self.assertIn("UNCERTAINTY_BLOCKING:UNKNOWN", decision.blocking_reasons())


if __name__ == "__main__":
    unittest.main()
