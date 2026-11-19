import unittest

from runtime.final_validation_contract import (
    FinalValidationContract,
    evaluate_final_validation,
)

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
        self.assertEqual(evaluate_final_validation(**GOOD).status, "PASS")

    def test_missing_audit_blocks(self):
        self.assertEqual(evaluate_final_validation(**{**GOOD, "audit_complete": False}).status, "BLOCKED")

    def test_missing_evidence_never_passes(self):
        self.assertEqual(evaluate_final_validation(**{
            **GOOD, "before_after_status": "UNKNOWN", "before_after_valid": False
        }).status, "NEEDS_REVIEW")

    def test_blocked_evidence_blocks(self):
        self.assertEqual(evaluate_final_validation(**{
            **GOOD, "post_edit_status": "BLOCKED", "post_edit_valid": False
        }).status, "BLOCKED")

    def test_unapproved_scope_blocks(self):
        self.assertEqual(evaluate_final_validation(**{
            **GOOD, "changed_ids": ("F01", "W01")
        }).status, "BLOCKED")

    def test_bad_identity_blocks(self):
        self.assertEqual(evaluate_final_validation(**{**GOOD, "source_sha256": "bad"}).status, "BLOCKED")

    def test_needs_review_post_edit_never_passes(self):
        self.assertEqual(evaluate_final_validation(**{
            **GOOD, "post_edit_status": "NEEDS_REVIEW", "post_edit_valid": False
        }).status, "NEEDS_REVIEW")

    def test_missing_model_id_blocks(self):
        self.assertEqual(evaluate_final_validation(**{**GOOD, "model_id": ""}).status, "BLOCKED")

    def test_fail_closed_statuses_are_explicit(self):
        for status in ("UNKNOWN", "NEEDS_REVIEW", "BLOCKED"):
            self.assertNotEqual(
                evaluate_final_validation(**{
                    **GOOD, "before_after_status": status, "before_after_valid": False
                }).status,
                "PASS",
            )

    def test_truthy_strings_cannot_replace_boolean_evidence(self):
        for field in ("approved", "post_edit_valid", "before_after_valid", "audit_complete"):
            with self.subTest(field=field):
                result = evaluate_final_validation(**{**GOOD, field: "false"})
                self.assertEqual(result.status, "BLOCKED")
                self.assertIn("FINAL_VALIDATION_BOOLEAN_EVIDENCE_INVALID", result.failure_codes)

    def test_non_hex_64_character_source_hash_blocks(self):
        self.assertEqual(
            evaluate_final_validation(**{**GOOD, "source_sha256": "g" * 64}).status,
            "BLOCKED",
        )

    def test_scope_string_is_rejected(self):
        result = evaluate_final_validation(**{**GOOD, "approved_target_ids": "F01"})
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("FINAL_VALIDATION_SCOPE_INVALID", result.failure_codes)

    def test_direct_pass_with_failed_check_is_rejected(self):
        result = FinalValidationContract(
            status="PASS",
            failure_codes=(),
            source_sha256="a" * 64,
            model_id="model-01",
            checks={
                "identity": True,
                "approved": True,
                "post_edit_pass": False,
                "before_after_pass": True,
                "audit_complete": True,
            },
        )
        with self.assertRaisesRegex(ValueError, "FINAL_VALIDATION_PASS_HAS_FAILED_CHECKS"):
            result.validate()
