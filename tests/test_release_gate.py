import unittest
from runtime.release_gate import evaluate_release


class ReleaseGateTests(unittest.TestCase):
    def complete(self):
        return {
            "contracts": True, "workflow": True, "final_validation": True,
            "regression": True, "semantic_corroboration": True,
            "audit": True, "idempotency": True, "runtime": True,
        }

    def test_complete_evidence_passes(self):
        result = evaluate_release(self.complete())
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failure_codes, [])

    def test_missing_evidence_blocks(self):
        checks = self.complete()
        del checks["audit"]
        result = evaluate_release(checks)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_AUDIT_FAILED", result.failure_codes)

    def test_truthy_non_boolean_does_not_pass(self):
        checks = self.complete()
        checks["runtime"] = "PASS"
        result = evaluate_release(checks)
        self.assertEqual(result.status, "BLOCKED")

    def test_fail_closed_states_do_not_pass(self):
        checks = self.complete()
        checks["audit"] = "UNKNOWN"
        checks["idempotency"] = "NEEDS_REVIEW"
        result = evaluate_release(checks)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("RELEASE_AUDIT_FAILED", result.failure_codes)
        self.assertIn("RELEASE_IDEMPOTENCY_FAILED", result.failure_codes)


if __name__ == "__main__":
    unittest.main()
