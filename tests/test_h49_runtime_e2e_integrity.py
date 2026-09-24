import unittest

from runtime.contracts import ChangeRequest, Element, PlanModel
from runtime.real_visual_controlled_bridge import execute_real_visual_approved_change


class H49RuntimeE2EIntegrityTests(unittest.TestCase):
    def _ready(self):
        return {
            "status": "READY_FOR_APPROVAL",
            "contracts": {"status": "VALID"},
            "semantic_corroboration": {"status": "ACCESSIBLE"},
            "constraint_map": {
                "protected_element_ids": ["C01"],
                "editable_element_ids": ["F01"],
                "conditional_element_ids": [],
                "unknown_element_ids": [],
            },
        }

    def _plan(self):
        return PlanModel("P-H49", [
            Element("C01", "COLUMN", "LOCKED", {"x": 10, "y": 10}),
            Element("F01", "FURNITURE", "EDITABLE", {"x": 20, "y": 20}),
        ])

    def test_runtime_constraint_map_contract_reaches_approval(self):
        request = ChangeRequest("FURNITURE", ["F01"], "Move sofa")
        result = execute_real_visual_approved_change(
            self._ready(), request, self._plan(), {"F01": {"x": 30, "y": 20}}
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["approval"]["approved_target_ids"], ["F01"])

    def test_missing_constraint_map_fails_closed(self):
        visual = self._ready()
        visual.pop("constraint_map")
        result = execute_real_visual_approved_change(
            visual, ChangeRequest("FURNITURE", ["F01"], "Move sofa"),
            self._plan(), {"F01": {"x": 30, "y": 20}}
        )
        self.assertEqual(result["status"], "REJECT")
        self.assertEqual(result["stage"], "APPROVAL")

    def test_unknown_constraint_element_blocks_approval(self):
        visual = self._ready()
        visual["constraint_map"]["unknown_element_ids"] = ["U01"]
        result = execute_real_visual_approved_change(
            visual, ChangeRequest("FURNITURE", ["F01"], "Move sofa"),
            self._plan(), {"F01": {"x": 30, "y": 20}}
        )
        self.assertEqual(result["status"], "REJECT")
        self.assertEqual(result["stage"], "APPROVAL")

    def test_locked_delta_remains_rejected_after_bridge(self):
        result = execute_real_visual_approved_change(
            self._ready(), ChangeRequest("FURNITURE", ["F01"], "Move sofa"),
            self._plan(), {"F01": {"x": 30, "y": 20}, "C01": {"x": 99, "y": 99}}
        )
        self.assertEqual(result["status"], "REJECT")
        self.assertEqual(
            result["execution"]["post_edit_diff"]["locked_delta_ids"], ["C01"]
        )


if __name__ == "__main__":
    unittest.main()
