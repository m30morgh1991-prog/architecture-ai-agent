import unittest

from runtime.space_model_contract import SpaceModel, SpaceRecord, SpaceRelation


class H67SpaceTopologyNormalizationTests(unittest.TestCase):
    def _spaces(self):
        return (
            SpaceRecord(
                space_id="S01", boundary_handle="B01",
                bbox=(0.0, 0.0, 10.0, 10.0), centroid=(5.0, 5.0),
                area=100.0, label="Room A", evidence_ids=("E01",),
            ),
            SpaceRecord(
                space_id="S02", boundary_handle="B02",
                bbox=(10.0, 0.0, 20.0, 10.0), centroid=(15.0, 5.0),
                area=100.0, label="Room B", evidence_ids=("E02",),
            ),
        )

    def test_relation_normalization_is_deterministic(self):
        relations = (
            SpaceRelation(
                relation_id="R01", relation_type="SHARED_BOUNDARY",
                from_space_id="S02", to_space_id="S01", evidence_ids=("E02",),
            ),
            SpaceRelation(
                relation_id="R02", relation_type="CONNECTED_BY_OPENING",
                from_space_id="S01", to_space_id="S02", evidence_ids=("E03",),
            ),
        )
        model = SpaceModel(
            model_id="M67-01", source_sha256="a" * 64,
            spaces=self._spaces(), relations=relations,
        )
        model.validate()
        self.assertEqual(len(model.relations), 2)
        self.assertEqual(
            {r.relation_type for r in model.relations},
            {"SHARED_BOUNDARY", "CONNECTED_BY_OPENING"},
        )

    def test_unknown_opening_relation_remains_unresolved(self):
        relation = SpaceRelation(
            relation_id="R99", relation_type="OPENING_CONNECTIVITY_UNKNOWN",
            from_space_id=None, to_space_id=None, evidence_ids=("E99",),
        )
        model = SpaceModel(
            model_id="M67-02", source_sha256="b" * 64,
            spaces=self._spaces(), relations=(relation,),
        )
        model.validate()
        self.assertIsNone(model.relations[0].from_space_id)
        self.assertIsNone(model.relations[0].to_space_id)


if __name__ == "__main__":
    unittest.main()
