import hashlib
import tempfile
import unittest
from pathlib import Path

from runtime.cad_readonly_adapter import ReadOnlyCADInspectionAdapter


class ReadOnlyCADInspectionAdapterTests(unittest.TestCase):
    def test_real_golden_dwg_is_source_bound_and_read_only(self):
        root = Path(__file__).resolve().parents[1]
        source = root / "test-assets" / "golden-projects" / "bagheri7.dwg"
        sha = hashlib.sha256(source.read_bytes()).hexdigest()
        evidence = ReadOnlyCADInspectionAdapter().inspect(source, sha)
        self.assertEqual(evidence.status, "READY")
        evidence.validate(sha)
        self.assertTrue(evidence.payload["read_only"])
        self.assertFalse(evidence.payload["semantic_authority"])

    def test_wrong_hash_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "fixture.dwg"
            source.write_bytes(b"cad-fixture")
            evidence = ReadOnlyCADInspectionAdapter().inspect(source, "0" * 64)
            self.assertEqual(evidence.status, "BLOCKED")
            self.assertEqual(evidence.payload["error"], "CAD_SOURCE_SHA_MISMATCH")

    def test_missing_source_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "missing.dwg"
            evidence = ReadOnlyCADInspectionAdapter().inspect(source, "a" * 64)
            self.assertEqual(evidence.status, "BLOCKED")
            self.assertEqual(evidence.payload["error"], "SOURCE_MISSING")


if __name__ == "__main__":
    unittest.main()
