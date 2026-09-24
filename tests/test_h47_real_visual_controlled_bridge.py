import unittest

from runtime.contracts import ChangeRequest
from runtime.real_visual_controlled_bridge import evaluate_real_visual_change


class H47RealVisualControlledBridgeTests(unittest.TestCase):
    def _ready(self, editable=(), unknown=()):
        return {
            "status": "READY_FOR_APPROVAL",
            "contracts": {"status": "VALID"},
            "semantic_corroboration": {"status": "ACCESSIBLE"},
            "constraint_map": {
                "protected_element_ids": ("C01",),
                "editable_element_ids": tuple(editable),
                "conditional_element_ids": (),
                "unknown_element_ids": tuple(unknown),
            },
        }

    def test_real_runtime_blocked_cannot_reach_approval(self):
        result = evaluate_real_visual_change(
            {
                "status": "BLOCKED",
                "blockers": ["LOCKED_ELEMENT_UNCERTAIN"],
            },
            ChangeRequest("FURNITURE", ["F01"], "Move furniture"),
        )
        self.assertEqual(result["status"], "REJECT")
        self.assertIn("LOCKED_ELEMENT_UNCERTAIN", result["failure_codes"])

    def test_missing_editable_target_is_rejected_fail_closed(self):
        result = evaluate_real_visual_change(
            self._ready(),
            ChangeRequest("FURNITURE", ["F01"], "Move furniture"),
        )
        self.assertEqual(result["status"], "REJECT")
        self.assertEqual(result["failure_codes"], ["LOCKED_ELEMENT_CONFLICT:F01"])

    def test_unresolved_elements_block_even_with_semantic_access(self):
        result = evaluate_real_visual_change(
            self._ready(unknown=("U01",)),
            ChangeRequest("FURNITURE", ["F01"], "Move furniture"),
        )
        self.assertEqual(result["status"], "REJECT")
        self.assertIn("UNCERTAINTY_BLOCKING:BLOCKED", result["failure_codes"])

    def test_explicit_editable_target_can_be_approved(self):
        result = evaluate_real_visual_change(
            self._ready(editable=("F01",)),
            ChangeRequest("FURNITURE", ["F01"], "Move furniture"),
        )
        self.assertEqual(result["status"], "APPROVED")
        self.assertEqual(result["approved_target_ids"], ["F01"])


if __name__ == "__main__":
    unittest.main()
