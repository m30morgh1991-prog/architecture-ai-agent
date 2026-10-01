import hashlib
import unittest
from pathlib import Path

import ezdwg

from runtime.locked_element_detection import ConservativeLockedElementDetector
from runtime.space_model_contract import build_space_model


ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "test-assets" / "golden-projects"


class H66GoldenDwgSpaceRegressionTests(unittest.TestCase):
    ASSETS = (
        GOLDEN / "bagheri7.dwg",
        GOLDEN / "afifiiiii.end.edit3.dwg",
    )

    def sha256(self, path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def test_golden_dwgs_are_parseable_and_produce_spaces(self):
        detector = ConservativeLockedElementDetector()

        for path in self.ASSETS:
            with self.subTest(asset=path.name):
                self.assertTrue(path.is_file(), f"missing golden asset: {path}")
                doc = ezdwg.read(str(path))
                self.assertTrue(doc.version)
                self.assertIsNotNone(doc.modelspace())

                source_sha256 = self.sha256(path)
                result = detector.detect(str(path), source_sha256)

                self.assertEqual(result["source_sha256"], source_sha256)
                self.assertEqual(result["detector_id"], "conservative-vector-fixed-v0.2-dwg")
                self.assertIsInstance(result["spaces"], list)
                self.assertGreater(
                    len(result["spaces"]),
                    0,
                    f"no spaces extracted from golden DWG: {path.name}",
                )

                model = build_space_model(
                    model_id=f"h66-{path.stem}",
                    source_sha256=source_sha256,
                    spaces=result["spaces"],
                    relations=result["space_relations"],
                )
                model.validate()
                self.assertEqual(len(model.spaces), len(result["spaces"]))
                self.assertEqual(model.source_sha256, source_sha256)

                space_ids = {space.space_id for space in model.spaces}
                for relation in model.relations:
                    if relation.relation_type == "OPENING_CONNECTIVITY_UNKNOWN":
                        self.assertIsNone(relation.from_space_id)
                        self.assertIsNone(relation.to_space_id)
                    else:
                        self.assertIn(relation.from_space_id, space_ids)
                        self.assertIn(relation.to_space_id, space_ids)

                for space in model.spaces:
                    self.assertEqual(space.status, "UNKNOWN")

    def test_golden_dwgs_preserve_evidence_and_no_duplicate_space_ids(self):
        detector = ConservativeLockedElementDetector()

        for path in self.ASSETS:
            with self.subTest(asset=path.name):
                source_sha256 = self.sha256(path)
                result = detector.detect(str(path), source_sha256)
                spaces = result["spaces"]

                ids = [space["space_id"] for space in spaces]
                self.assertEqual(len(ids), len(set(ids)))
                for space in spaces:
                    self.assertTrue(space["boundary_handle"])
                    self.assertTrue(space["evidence_ids"])
                    self.assertGreater(space["area"], 0)
                    self.assertEqual(space["status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
