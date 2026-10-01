import unittest

from runtime.space_model_contract import build_space_model


class H62SpaceModelContractTests(unittest.TestCase):
    def base(self):
        spaces = [
            {
                "space_id": "S01",
                "boundary_handle": "wall-face-01",
                "bbox": [0, 0, 10, 10],
                "centroid": [5, 5],
                "area": 100,
                "label": "LIVING",
                "evidence_ids": ["ev-s01"],
                "status": "UNKNOWN",
            },
            {
                "space_id": "S02",
                "boundary_handle": "wall-face-02",
                "bbox": [10, 0, 20, 10],
                "centroid": [15, 5],
                "area": 100,
                "label": "KITCHEN",
                "evidence_ids": ["ev-s02"],
                "status": "UNKNOWN",
            },
        ]
        relations = [
            {
                "relation_id": "S01__S02__SHARED_BOUNDARY",
                "from": "S01",
                "to": "S02",
                "type": "SHARED_BOUNDARY",
                "evidence_ids": ["ev-s01", "ev-s02"],
                "status": "UNKNOWN",
            }
        ]
        return spaces, relations

    def test_valid_space_model_preserves_unknown_status(self):
        spaces, relations = self.base()
        model = build_space_model(
            model_id="space-model-01",
            source_sha256="src-01",
            spaces=spaces,
            relations=relations,
        )
        self.assertEqual(len(model.spaces), 2)
        self.assertEqual(model.spaces[0].label, "LIVING")
        self.assertEqual(model.relations[0].relation_type, "SHARED_BOUNDARY")
        self.assertEqual(model.spaces[0].status, "UNKNOWN")
        self.assertEqual(model.relations[0].status, "UNKNOWN")
        self.assertEqual(model.unresolved, ("S01__S02__SHARED_BOUNDARY",))

    def test_missing_space_evidence_blocks(self):
        spaces, relations = self.base()
        spaces[0]["evidence_ids"] = []
        with self.assertRaisesRegex(ValueError, "SPACE_EVIDENCE_MISSING"):
            build_space_model(
                model_id="space-model-01",
                source_sha256="src-01",
                spaces=spaces,
                relations=relations,
            )

    def test_relation_to_unknown_space_blocks(self):
        spaces, relations = self.base()
        relations[0]["to"] = "S99"
        with self.assertRaisesRegex(ValueError, "SPACE_RELATION_TARGET_UNKNOWN"):
            build_space_model(
                model_id="space-model-01",
                source_sha256="src-01",
                spaces=spaces,
                relations=relations,
            )

    def test_unresolved_opening_relation_has_no_fake_endpoints(self):
        spaces, relations = self.base()
        relations[0] = {
            "relation_id": "OPENING-D01__UNRESOLVED",
            "from": None,
            "to": None,
            "type": "OPENING_CONNECTIVITY_UNKNOWN",
            "evidence_ids": ["ev-door-01"],
            "status": "UNKNOWN",
        }
        model = build_space_model(
            model_id="space-model-01",
            source_sha256="src-01",
            spaces=spaces,
            relations=relations,
        )
        self.assertEqual(model.relations[0].from_space_id, None)
        self.assertEqual(model.relations[0].to_space_id, None)
        self.assertEqual(model.unresolved, ("OPENING-D01__UNRESOLVED",))

    def test_duplicate_space_id_blocks(self):
        spaces, relations = self.base()
        spaces[1]["space_id"] = "S01"
        with self.assertRaisesRegex(ValueError, "SPACE_ID_DUPLICATE"):
            build_space_model(
                model_id="space-model-01",
                source_sha256="src-01",
                spaces=spaces,
                relations=relations,
            )


if __name__ == "__main__":
    unittest.main()
