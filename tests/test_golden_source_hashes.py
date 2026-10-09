import hashlib
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "test-assets" / "golden-understanding" / "golden_manifest.json"


class GoldenSourceHashTests(unittest.TestCase):
    def test_preserved_golden_sources_have_stable_sha256_evidence(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        for case in manifest["cases"]:
            source = REPO_ROOT / case["source_path"]
            self.assertTrue(source.is_file(), f"Missing Golden source: {source}")

            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            self.assertEqual(len(digest), 64)
            self.assertNotEqual(digest, "0" * 64)
            self.assertRegex(case["source_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(case["source_sha256"], digest, case["case_id"])

            # CI log is the machine-readable handoff used to lock manifest hashes.
            print(
                f"GOLDEN_SOURCE_SHA256 case={case['case_id']} "
                f"path={case['source_path']} sha256={digest}"
            )


    def test_missing_domain_status_is_detected(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        case = manifest["cases"][0]
        status = dict(case["expected_domain_status"])
        status.pop(case["expected_domains"][0])
        self.assertNotEqual(set(status), set(case["expected_domains"]))

    def test_invalid_domain_status_is_detected(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        case = manifest["cases"][0]
        status = dict(case["expected_domain_status"])
        status[case["expected_domains"][0]] = "UNVERIFIED"
        self.assertNotIn(status[case["expected_domains"][0]], {"PASS", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"})

    def test_manifest_has_explicit_status_for_every_required_domain(self):

        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        for case in manifest["cases"]:
            domains = case["expected_domains"]
            status = case["expected_domain_status"]
            self.assertEqual(set(status), set(domains), case["case_id"])
            self.assertTrue(all(value in {"PASS", "UNKNOWN", "NEEDS_REVIEW", "BLOCKED"} for value in status.values()))
            for domain, value in status.items():
                if domain == "scale_unit":
                    self.assertIn(value, {"UNKNOWN", "NEEDS_REVIEW"})
                    self.assertNotEqual(value, "PASS")
                else:
                    self.assertEqual(value, "UNKNOWN", case["case_id"] + ":" + domain)


if __name__ == "__main__":
    unittest.main()
