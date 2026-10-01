import hashlib
import unittest
from pathlib import Path

from runtime.locked_element_detection import ConservativeLockedElementDetector


ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "test-assets" / "golden-projects"
ASSETS = (
    GOLDEN / "bagheri7.dwg",
    GOLDEN / "afifiiiii.end.edit3.dwg",
)
ALLOWED_TYPES = {
    "COLUMNS",
    "OUTER_BOUNDARY",
    "WALLS",
    "DOORS",
    "WINDOWS",
    "OVERALL_PLAN_FORM",
}


class H68ArchitecturalElementDetectionTests(unittest.TestCase):
    @staticmethod
    def sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def test_golden_dwgs_produce_evidence_backed_element_candidates(self):
        detector = ConservativeLockedElementDetector()

        for path in ASSETS:
            with self.subTest(asset=path.name):
                self.assertTrue(path.is_file(), f"missing golden asset: {path}")
                source_sha256 = self.sha256(path)
                result = detector.detect(str(path), source_sha256)

                self.assertEqual(
                    result["detector_id"],
                    "conservative-vector-fixed-v0.2-dwg",
                )
                self.assertEqual(result["source_sha256"], source_sha256)
                self.assertIn(result["status"], {"UNKNOWN", "ACCESSIBLE"})

                candidates = result["candidates"]
                self.assertIsInstance(candidates, list)
                self.assertGreater(
                    len(candidates),
                    0,
                    f"no architectural element candidates: {path.name}",
                )

                candidate_ids = [candidate["candidate_id"] for candidate in candidates]
                self.assertEqual(len(candidate_ids), len(set(candidate_ids)))

                for candidate in candidates:
                    self.assertIn(candidate["element_type"], ALLOWED_TYPES)
                    self.assertTrue(candidate["evidence_ids"])
                    self.assertGreaterEqual(candidate["confidence"], 0.0)
                    self.assertLessEqual(candidate["confidence"], 1.0)
                    self.assertIn(
                        candidate["status"],
                        {"LOCKED", "EDITABLE", "CONDITIONAL", "UNKNOWN"},
                    )

                    # Detection evidence alone must not silently promote a
                    # candidate to an approval-grade LOCKED state.
                    if candidate["status"] == "LOCKED":
                        self.assertGreaterEqual(candidate["confidence"], 0.95)

                self.assertEqual(result["locked_element_types"], [])

    def test_detection_is_deterministic_for_same_golden_dwg(self):
        detector = ConservativeLockedElementDetector()

        for path in ASSETS:
            with self.subTest(asset=path.name):
                source_sha256 = self.sha256(path)
                first = detector.detect(str(path), source_sha256)
                second = detector.detect(str(path), source_sha256)

                self.assertEqual(first["detector_id"], second["detector_id"])
                self.assertEqual(first["source_sha256"], second["source_sha256"])
                self.assertEqual(first["candidates"], second["candidates"])
                self.assertEqual(first["unresolved_fixed_element_types"],
                                 second["unresolved_fixed_element_types"])

    def test_uncertainty_remains_fail_closed(self):
        detector = ConservativeLockedElementDetector()

        source_sha256 = "0" * 64
        result = detector._dwg_unknown(source_sha256, "TEST_UNKNOWN")

        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(result["source_sha256"], source_sha256)
        self.assertEqual(result["locked_element_types"], [])
        self.assertEqual(
            set(result["unresolved_fixed_element_types"]),
            ALLOWED_TYPES,
        )


if __name__ == "__main__":
    unittest.main()
