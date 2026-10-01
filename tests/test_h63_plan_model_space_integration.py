"""H63 tests for PlanModel ↔ SpaceModel integration."""
import unittest

from runtime.plan_model_contract import PlanModel, PlanElement
from runtime.space_model_contract import SpaceModel, SpaceRecord, SpaceRelation


SHA = "a" * 64


def make_space_model(source_sha=SHA):
    space = SpaceRecord(
        space_id="S01",
        boundary_handle="B01",
        bbox=(0.0, 0.0, 10.0, 10.0),
        centroid=(5.0, 5.0),
        area=100.0,
        label="Living",
        evidence_ids=("dwg-space-B01",),
        status="UNKNOWN",
    )
    relation = SpaceRelation(
        relation_id="R01",
        relation_type="OPENING_CONNECTIVITY_UNKNOWN",
        from_space_id=None,
        to_space_id=None,
        evidence_ids=("dwg-opening-O01",),
        status="UNKNOWN",
    )
    return SpaceModel(
        model_id="SM01",
        source_sha256=source_sha,
        spaces=(space,),
        relations=(relation,),
        unresolved=("R01",),
    )


def make_plan(space_model=None, source_sha=SHA):
    element = PlanElement(
        element_id="W01",
        element_type="WALL",
        state="UNKNOWN",
        geometry={"bbox": [0, 0, 10, 10]},
        evidence_ids=("dwg-wall-01",),
        confidence=0.70,
    )
    return PlanModel(
        model_id="PM01",
        source_sha256=source_sha,
        drawing_count=1,
        elements=(element,),
        space_model=space_model,
    )


class H63PlanModelSpaceIntegrationTests(unittest.TestCase):
    def test_plan_model_preserves_validated_space_model(self):
        space_model = make_space_model()
        plan = make_plan(space_model)
        plan.validate()
        self.assertIs(plan.space_model, space_model)
        self.assertEqual(plan.spaces[0].space_id, "S01")
        self.assertEqual(plan.space_relations[0].relation_type, "OPENING_CONNECTIVITY_UNKNOWN")

    def test_plan_model_without_space_model_remains_backward_compatible(self):
        plan = make_plan()
        plan.validate()
        self.assertEqual(plan.spaces, ())
        self.assertEqual(plan.space_relations, ())

    def test_space_source_mismatch_blocks_integration(self):
        plan = make_plan(make_space_model("b" * 64))
        with self.assertRaisesRegex(ValueError, "SPACE_MODEL_SOURCE_MISMATCH"):
            plan.validate()

    def test_space_uncertainty_is_not_promoted_by_plan_integration(self):
        space_model = make_space_model()
        plan = make_plan(space_model)
        plan.validate()
        self.assertEqual(plan.space_model.spaces[0].status, "UNKNOWN")
        self.assertEqual(plan.space_model.relations[0].status, "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
