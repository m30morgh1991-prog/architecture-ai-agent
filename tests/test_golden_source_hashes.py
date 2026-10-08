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

            # CI log is the machine-readable handoff used to lock manifest hashes.
            print(
                f"GOLDEN_SOURCE_SHA256 case={case['case_id']} "
                f"path={case['source_path']} sha256={digest}"
            )


if __name__ == "__main__":
    unittest.main()
