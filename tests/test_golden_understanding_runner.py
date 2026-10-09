import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from runtime.golden_understanding_runner import (
    run_golden_case,
    run_manifest_to_report,
    sha256_file,
)
from runtime.golden_understanding_regression import GoldenCase


class GoldenUnderstandingRunnerTests(unittest.TestCase):
    def test_sha256_is_stable(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sample.dwg"
            source.write_bytes(b"golden-source")
            self.assertEqual(sha256_file(source), hashlib.sha256(b"golden-source").hexdigest())

    def test_runner_emits_machine_checkable_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "sample.dwg"
            source.write_bytes(b"not-a-real-dwg")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({
                "schema": "golden-understanding-v1",
                "version": "2026-10-08",
                "truth_policy": "DIRECT_AND_VALIDATED_DERIVED_ONLY",
                "cases": [{
                    "case_id": "CASE-RUNNER",
                    "source_path": str(source),
                    "source_sha256": digest,
                    "expected_elements": [],
                    "expected_domains": [
                        "source_profile", "elements", "geometry", "topology",
                        "relations", "drawing_evidence", "scale_unit", "provenance",
                        "fail_closed_decision"
                    ],
                    "expected_status": "UNKNOWN",
                    "expected_domain_status": {d: "UNKNOWN" for d in [
                        "source_profile", "elements", "geometry", "topology", "relations", "drawing_evidence", "scale_unit", "provenance", "fail_closed_decision"
                    ]}
                }]
            }), encoding="utf-8")
            report = run_manifest_to_report(manifest)
            case = report["cases"][0]
            self.assertEqual(report["schema"], "golden-understanding-report-v1")
            self.assertTrue(case["source_exists"])
            self.assertEqual(len(case["source_sha256"]), 64)
            self.assertEqual(case["observed"]["source_profile"]["sha256"], case["source_sha256"])
            self.assertEqual(case["observed"]["source_profile"]["source_class"], "ENGINEERING_VECTOR")
            self.assertEqual(case["observed"]["source_profile"]["input_mode"], "ENGINEERING_PLAN")
            self.assertEqual(case["observed"]["scale_unit"], "UNKNOWN")
            self.assertIn(case["decision"], {"UNKNOWN", "NEEDS_REVIEW", "BLOCKED"})


    def test_standalone_cli_emits_machine_checkable_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "sample.dwg"
            source.write_bytes(b"cli-golden-source")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            manifest = root / "manifest.json"
            output = root / "report.json"
            manifest.write_text(json.dumps({
                "schema": "golden-understanding-v1",
                "version": "2026-10-08",
                "truth_policy": "DIRECT_AND_VALIDATED_DERIVED_ONLY",
                "cases": [{
                    "case_id": "CASE-CLI",
                    "source_path": str(source),
                    "source_sha256": digest,
                    "expected_elements": [],
                    "expected_domains": ["source_profile", "elements", "scale_unit", "fail_closed_decision"],
                    "expected_status": "UNKNOWN",
                    "expected_domain_status": {"source_profile": "UNKNOWN", "elements": "UNKNOWN", "scale_unit": "UNKNOWN", "fail_closed_decision": "UNKNOWN"},
                    "expected_domain_status": {"source_profile": "UNKNOWN", "elements": "UNKNOWN", "fail_closed_decision": "UNKNOWN"}
                }]
            }), encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "runtime.golden_understanding_runner",
                    "--manifest",
                    str(manifest),
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0)
            self.assertTrue(output.is_file())
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["schema"], "golden-understanding-report-v1")
            self.assertEqual(report["summary"]["case_count"], 1)
            self.assertIn(report["cases"][0]["decision"], {"UNKNOWN", "NEEDS_REVIEW", "BLOCKED"})

    def test_understanding_exception_becomes_blocked_report(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sample.dwg"
            source.write_bytes(b"source")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            case = GoldenCase(
                case_id="CASE-EXCEPTION",
                source_path=str(source),
                source_sha256=digest,
                expected_elements=(),
                expected_domains=("source_profile", "elements", "scale_unit", "fail_closed_decision"),
                expected_status="UNKNOWN",
                expected_domain_status={"source_profile": "UNKNOWN", "elements": "UNKNOWN", "scale_unit": "UNKNOWN", "fail_closed_decision": "UNKNOWN"},
            )

            class _FailingCore:
                def understand(self, **_kwargs):
                    raise ValueError("MISSING_CONSTRAINT_EVIDENCE")

            report = run_golden_case(case, core=_FailingCore())
            self.assertTrue(report["source_exists"])
            self.assertEqual(report["observed"]["fail_closed_decision"], "BLOCKED")
            self.assertEqual(report["decision"], "NEEDS_REVIEW")
            self.assertIn("UNDERSTANDING_EXECUTION_BLOCKED", report["failures"])


if __name__ == "__main__":
    unittest.main()
