import unittest
from runtime.app import execute
from runtime.contracts import Element, PlanModel, ChangeRequest

class RuntimeSliceTests(unittest.TestCase):
    def setUp(self):
        self.plan = PlanModel("P-001", [
            Element("C01", "COLUMN", "LOCKED", {"x": 10, "y": 10}),
            Element("F01", "FURNITURE", "EDITABLE", {"x": 20, "y": 20}),
        ])

    def test_furniture_move_passes_and_column_stays_locked(self):
        result = execute(self.plan, ChangeRequest("FURNITURE", ["F01"], "Move sofa"), {"F01": {"x": 30, "y": 20}})
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["post_edit_diff"]["locked_delta_ids"], [])

    def test_column_move_is_rejected(self):
        result = execute(self.plan, ChangeRequest("FURNITURE", ["C01"], "Move column"), {"C01": {"x": 99, "y": 99}})
        self.assertEqual(result["status"], "REJECT")
        self.assertIn("LOCKED_ELEMENT_CONFLICT", result["validation"]["failure_codes"])

if __name__ == "__main__":
    unittest.main()
