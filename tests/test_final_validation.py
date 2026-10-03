import unittest

from runtime.final_validation import validate_post_edit


GOOD = {
    "source_sha256": "a" * 64,
    "model_id": "model-01",
    "approved": True,
    "post_edit_status": "PASS",
    "post_edit_valid": True,
    "before_after_status": "PASS",
    "before_after_valid": True,
    "audit_complete": True,
    "approved_target_ids": ("F01",),
    "changed_ids": ("F01",),
}


class FinalValidationTests(unittest.TestCase):
    def test_clean_evidence_passes_through_h91_contract(self):
        result = validate_post_edit(GOOD)
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failure_codes, [])

    def test_legacy_minimal_input_never_passes(self):
        result = validate_post_edit(
            {"locked_delta_ids": [], "unauthorized_delta_ids": []}
        )
        self.assertNotEqual(result.status, "PASS")
        self.assertEqual(result.status, "UNKNOWN")
        self.assertIn("FINAL_VALIDATION_EVIDENCE_MISSING", result.failure_codes)

    def test_locked_delta_requires_complete_evidence_then_blocks(self):
        result = validate_post_edit(
            {**GOOD, "post_edit_status": "BLOCKED", "post_edit_valid": False,
             "locked_delta_ids": ("C01",)}
        )
        self.assertEqual(result.status, "BLOCKED")

    def test_unauthorized_delta_requires_complete_evidence_then_blocks(self):
        result = validate_post_edit(
            {**GOOD, "post_edit_status": "BLOCKED", "post_edit_valid": False,
             "unauthorized_delta_ids": ("W01",)}
        )
        self.assertEqual(result.status, "BLOCKED")

    def test_missing_model_id_never_passes(self):
        result = validate_post_edit({**GOOD, "model_id": ""})
        self.assertEqual(result.status, "BLOCKED")

    def test_unknown_before_after_never_passes(self):
        result = validate_post_edit(
            {**GOOD, "before_after_status": "UNKNOWN", "before_after_valid": False}
        )
        self.assertEqual(result.status, "NEEDS_REVIEW")


if __name__ == "__main__":
    unittest.main()
