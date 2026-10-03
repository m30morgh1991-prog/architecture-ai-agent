import unittest

from runtime.final_validation_contract import evaluate_final_validation


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


class FinalValidationContractTests(unittest.TestCase):
    def test_clean_approved_change_passes(self):
        result = evaluate_final_validation(**GOOD)
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failure_codes, ())

    def test_missing_audit_blocks(self):
        result = evaluate_final_validation(**{**GOOD, "audit_complete": False})
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("FINAL_VALIDATION_AUDIT_INCOMPLETE", result.failure_codes)

    def test_missing_evidence_never_passes(self):
        result = evaluate_final_validation(**{**GOOD, "before_after_status": "UNKNOWN", "before_after_valid": False})
        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertNotEqual(result.status, "PASS")

    def test_blocked_evidence_blocks(self):
        result = evaluate_final_validation(**{**GOOD, "post_edit_status": "BLOCKED", "post_edit_valid": False})
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("FINAL_VALIDATION_EVIDENCE_BLOCKED", result.failure_codes)

    def test_unapproved_scope_blocks(self):
        result = evaluate_final_validation(**{**GOOD, "approved_target_ids": ("F01",), "changed_ids": ("F01", "W01")})
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("FINAL_VALIDATION_SCOPE_MISMATCH", result.failure_codes)

    def test_bad_identity_blocks(self):
        result = evaluate_final_validation(**{**GOOD, "source_sha256": "bad"})
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("FINAL_VALIDATION_IDENTITY_INVALID", result.failure_codes)

    def test_needs_review_post_edit_never_passes(self):
        result = evaluate_final_validation(**{**GOOD, "post_edit_status": "NEEDS_REVIEW", "post_edit_valid": False})
        self.assertEqual(result.status, "NEEDS_REVIEW")

    def test_fail_closed_statuses_are_explicit(self):
        for status in ("UNKNOWN", "NEEDS_REVIEW", "BLOCKED"):
            result = evaluate_final_validation(**{**GOOD, "before_after_status": status, "before_after_valid": False})
            self.assertNotEqual(result.status, "PASS")


if __name__ == "__main__":
    unittest.main()
