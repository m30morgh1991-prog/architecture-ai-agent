import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.golden_understanding_regression import (
    evaluate_golden_case,
    load_manifest,
    summarize_domain_metrics,
)


class GoldenUnderstandingRegressionTests(unittest.TestCase):
    def _case(self, root: Path):
        manifest = {
            "schema": "golden-understanding-v1",
            "version": "2026-10-08",
            "truth_policy": "DIRECT_AND_VALIDATED_DERIVED_ONLY",
            "cases": [{
                "case_id": "CASE-1",
                "source_path": "test-assets/golden-projects/example.dwg",
                "source_sha256": None,
                "expected_elements": ["WALL", "DOOR"],
                "expected_domains": [
                    "source_profile", "elements", "geometry",
                    "topology", "relations", "drawing_evidence",
                    "provenance", "fail_closed_decision"
                ],
                "expected_status": "UNKNOWN",
                "expected_domain_status": {d: "UNKNOWN" for d in [
                    "source_profile", "elements", "geometry", "topology", "relations", "drawing_evidence", "provenance", "fail_closed_decision"
                ]},
                "adversarial": False,
            }],
        }
        path = root / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return load_manifest(path)[0]

    def test_manifest_schema_and_case_load(self):
        with TemporaryDirectory() as tmp:
            case = self._case(Path(tmp))
            self.assertEqual(case.case_id, "CASE-1")
            self.assertEqual(case.expected_status, "UNKNOWN")

    def test_complete_observation_passes(self):
        with TemporaryDirectory() as tmp:
            case = self._case(Path(tmp))
            observed = {domain: "UNKNOWN" for domain in case.expected_domains}
            observed["elements"] = ["WALL", "DOOR"]
            observed["fail_closed_decision"] = "UNKNOWN"
            report = evaluate_golden_case(case, observed)
            self.assertEqual(report.decision, "PASS")
            self.assertFalse(report.failures)

    def test_empty_domain_requires_review(self):
        with TemporaryDirectory() as tmp:
            case = self._case(Path(tmp))
            observed = {domain: {} for domain in case.expected_domains}
            observed["elements"] = ["WALL", "DOOR"]
            observed["fail_closed_decision"] = "UNKNOWN"
            report = evaluate_golden_case(case, observed)
            self.assertEqual(report.decision, "NEEDS_REVIEW")
            self.assertIn("MISSING_DOMAIN:source_profile", report.failures)

    def test_explicit_unknown_domain_is_covered(self):
        with TemporaryDirectory() as tmp:
            case = self._case(Path(tmp))
            observed = {domain: "UNKNOWN" for domain in case.expected_domains}
            observed["elements"] = ["WALL", "DOOR"]
            observed["fail_closed_decision"] = "UNKNOWN"
            report = evaluate_golden_case(case, observed)
            self.assertEqual(report.decision, "PASS")
            self.assertFalse(report.failures)

    def test_missing_domain_requires_review(self):
        with TemporaryDirectory() as tmp:
            case = self._case(Path(tmp))
            observed = {
                domain: {} for domain in case.expected_domains if domain != "topology"
            }
            observed["elements"] = ["WALL", "DOOR"]
            observed["fail_closed_decision"] = "UNKNOWN"
            report = evaluate_golden_case(case, observed)
            self.assertEqual(report.decision, "NEEDS_REVIEW")
            self.assertIn("MISSING_DOMAIN:topology", report.failures)

    def test_unresolved_evidence_cannot_pass(self):
        with TemporaryDirectory() as tmp:
            case = self._case(Path(tmp))
            observed = {domain: {} for domain in case.expected_domains}
            observed["elements"] = ["WALL", "DOOR"]
            observed["uncertainties"] = ["LOW_RESOLUTION"]
            observed["fail_closed_decision"] = "PASS"
            report = evaluate_golden_case(case, observed)
            self.assertEqual(report.decision, "BLOCKED")
            self.assertTrue(report.unsafe_acceptance)
            self.assertIn("UNSAFE_ACCEPTANCE:UNRESOLVED_TO_PASS", report.failures)

    def test_invalid_expected_status_is_rejected(self):
        with TemporaryDirectory() as tmp:
            payload = {
                "schema": "golden-understanding-v1",
                "cases": [{
                    "case_id": "BAD",
                    "source_path": "x.dwg",
                    "expected_domains": ["elements"],
                    "expected_status": "NOT_A_DECISION",
                }],
            }
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_manifest(path)

    def test_domain_metrics_do_not_promote_unknown_to_understood(self):
        with TemporaryDirectory() as tmp:
            case = self._case(Path(tmp))
            observed = {domain: "UNKNOWN" for domain in case.expected_domains}
            observed["elements"] = ["WALL", "DOOR"]
            observed["fail_closed_decision"] = "UNKNOWN"
            report = evaluate_golden_case(case, observed)
            metrics = summarize_domain_metrics([report])
            self.assertEqual(metrics["geometry"]["covered"], 1)
            self.assertEqual(metrics["geometry"]["unknown"], 1)
            self.assertEqual(metrics["geometry"]["understood"], 0)
            self.assertEqual(metrics["geometry"]["understood_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()
