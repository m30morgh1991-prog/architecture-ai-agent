import unittest

from runtime.production_readiness_gate import (
    ProductionReadinessResult,
    evaluate_production_readiness,
)


class ProductionReadinessGateTests(unittest.TestCase):
    def test_all_exact_true_checks_allow_production_readiness(self):
        result = evaluate_production_readiness(
            runtime_release_ok=True,
            real_runtime_e2e_ok=True,
            fixed_element_detection_ok=True,
            complete_visual_evidence_ok=True,
        )
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failure_codes, [])

    def test_truthy_string_false_never_passes(self):
        result = evaluate_production_readiness(
            runtime_release_ok="false",
            real_runtime_e2e_ok=True,
            fixed_element_detection_ok=True,
            complete_visual_evidence_ok=True,
        )
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("PRODUCTION_RUNTIME_RELEASE_FAILED", result.failure_codes)

    def test_direct_pass_with_failed_check_is_rejected(self):
        result = ProductionReadinessResult(
            status="PASS",
            checks={
                "runtime_release": True,
                "real_runtime_e2e": True,
                "fixed_element_detection": False,
                "complete_visual_evidence": True,
            },
            failure_codes=[],
        )
        with self.assertRaisesRegex(ValueError, "PRODUCTION_READINESS_FALSE_PASS"):
            result.validate()


if __name__ == "__main__":
    unittest.main()
