import unittest

from runtime.production_readiness_gate import evaluate_production_readiness


class H60ProductionReadinessGateTests(unittest.TestCase):
    def green(self, **overrides):
        checks = {
            "runtime_release_ok": True,
            "real_runtime_e2e_ok": True,
            "fixed_element_detection_ok": True,
            "complete_visual_evidence_ok": True,
        }
        checks.update(overrides)
        return evaluate_production_readiness(**checks)

    def test_all_required_checks_pass(self):
        result = self.green()
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failure_codes, [])

    def test_real_runtime_release_is_required(self):
        result = self.green(runtime_release_ok=False)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("PRODUCTION_RUNTIME_RELEASE_FAILED", result.failure_codes)

    def test_real_runtime_e2e_is_required(self):
        result = self.green(real_runtime_e2e_ok=False)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("PRODUCTION_REAL_RUNTIME_E2E_FAILED", result.failure_codes)

    def test_fixed_element_detection_is_required(self):
        result = self.green(fixed_element_detection_ok=False)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("PRODUCTION_FIXED_ELEMENT_DETECTION_FAILED", result.failure_codes)

    def test_complete_visual_evidence_is_required(self):
        result = self.green(complete_visual_evidence_ok=False)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("PRODUCTION_COMPLETE_VISUAL_EVIDENCE_FAILED", result.failure_codes)

    def test_no_extra_flag_can_bypass_required_checks(self):
        result = evaluate_production_readiness(
            runtime_release_ok=False,
            real_runtime_e2e_ok=True,
            fixed_element_detection_ok=True,
            complete_visual_evidence_ok=True,
        )
        self.assertEqual(result.status, "BLOCKED")

if __name__ == "__main__":
    unittest.main()
