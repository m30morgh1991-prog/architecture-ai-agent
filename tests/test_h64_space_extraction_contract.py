import unittest

from runtime.space_extraction_contract import build_space_extraction_result


class H64SpaceExtractionContractTests(unittest.TestCase):
    def spaces(self):
        return [{
            "space_id": "S01",
            "boundary_handle": "B01",
            "bbox": [0, 0, 10, 10],
            "centroid": [5, 5],
            "area": 100,
            "label": None,
            "evidence_ids": ["ev-s01"],
            "status": "UNKNOWN",
        }]

    def test_result_normalizes_to_typed_space_model(self):
        result = build_space_extraction_result(
            detector_id="dwg-space-v1",
            source_sha256="a" * 64,
            spaces=self.spaces(),
            relations=[],
        )
        model = result.to_space_model()
        self.assertEqual(model.spaces[0].space_id, "S01")
        self.assertEqual(model.source_sha256, "a" * 64)

    def test_missing_space_evidence_blocks(self):
        spaces = self.spaces()
        spaces[0]["evidence_ids"] = []
        with self.assertRaisesRegex(ValueError, "SPACE_EXTRACTION_SPACE_EVIDENCE_MISSING"):
            build_space_extraction_result(
                detector_id="dwg-space-v1",
                source_sha256="a" * 64,
                spaces=spaces,
                relations=[],
            )

    def test_unresolved_list_must_match_relation_status(self):
        result = build_space_extraction_result(
            detector_id="dwg-space-v1",
            source_sha256="a" * 64,
            spaces=self.spaces(),
            relations=[{
                "relation_id": "R01",
                "type": "OPENING_CONNECTIVITY_UNKNOWN",
                "from": None,
                "to": None,
                "evidence_ids": ["ev-opening"],
                "status": "UNKNOWN",
            }],
        )
        self.assertEqual(result.unresolved, ("R01",))
        self.assertEqual(result.to_space_model().unresolved, ("R01",))

    def test_unknown_never_becomes_accessible(self):
        result = build_space_extraction_result(
            detector_id="dwg-space-v1",
            source_sha256="a" * 64,
            spaces=self.spaces(),
            relations=[],
        )
        self.assertEqual(result.to_space_model().spaces[0].status, "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
