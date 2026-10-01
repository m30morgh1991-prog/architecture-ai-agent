import unittest

from runtime.space_model_contract import RelationType, SpaceModel, SpaceRecord, SpaceRelation


class H67SpaceTopologyNormalizationTests(unittest.TestCase):
    def _spaces(self):
        return [
            SpaceRecord(
                space_id="S01", boundary_handle="B01",
                bbox=(0.0, 0.0, 10.0, 10.0), centroid=(5.0, 5.0),
                area=100.0, label="Room A", evidence_ids=["E01"],
            ),
            SpaceRecord(
                space_id="S02", boundary_handle="B02",
                bbox=(10.0, 0.0, 20.0, 10.0), centroid=(15.0, 5.0),
                area=100.0, label="Room B", evidence_ids=["E02"],
            ),
        ]

    def test_relation_normalization_is_deterministic(self):
        relations = [
            SpaceRelation("S02", "S01", RelationType.SHARED_BOUNDARY, ["E02"]),
            SpaceRelation("S01", "S02", RelationType.CONNECTED_BY_OPENING, ["E03"]),
        ]
        model = SpaceModel(source_sha256="a" * 64, spaces=self._spaces(), relations=relations)
        model.validate()
        self.assertEqual(len(model.relations), 2)
        self.assertEqual({r.relation_type for r in model.relations},
                         {RelationType.SHARED_BOUNDARY, RelationType.CONNECTED_BY_OPENING})

    def test_unknown_opening_relation_remains_unresolved(self):
        relation = SpaceRelation(
            space_a_id=None, space_b_id=None,
            relation_type=RelationType.OPENING_CONNECTIVITY_UNKNOWN,
            evidence_ids=["E99"],
        )
        model = SpaceModel(source_sha256="b" * 64, spaces=self._spaces(), relations=[relation])
        model.validate()
        self.assertIsNone(model.relations[0].space_a_id)
        self.assertIsNone(model.relations[0].space_b_id)


if __name__ == "__main__":
    unittest.main()
