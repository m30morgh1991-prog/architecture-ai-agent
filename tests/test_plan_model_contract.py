import unittest

from runtime.plan_model_contract import ConstraintMap, PlanElement, PlanModel


class PlanModelContractTests(unittest.TestCase):
    def test_locked_element_requires_strong_evidence(self):
        with self.assertRaisesRegex(ValueError, "LOCKED_ELEMENT_CONFIDENCE_TOO_LOW"):
            PlanElement(
                "W01","WALL","LOCKED",{"bbox":[1,2,3,4]},("ev-1",),0.80
            ).validate()

    def test_real_source_model_can_remain_unresolved_without_false_pass(self):
        element=PlanElement(
            "PANEL-A1","PLAN_PANEL","CONDITIONAL",
            {"bbox":[0,0,100,200]},("real-f5748f3f",),0.96
        )
        model=PlanModel(
            "pm-real-01",
            "f5748f3f19f34b1503497616e82db15f985ec4bc5b202cca3cd6f3a05d2399d7",
            4,(element,),("columns","structural-fixed-elements")
        )
        model.validate()
        cmap=ConstraintMap(
            "cm-real-01","pm-real-01",(),("PANEL-A1",),(),("C01-C12",),
            ("real-f5748f3f",)
        )
        cmap.validate()
        self.assertIn("C01-C12", cmap.unknown_element_ids)

    def test_constraint_states_must_not_overlap(self):
        with self.assertRaisesRegex(ValueError, "CONSTRAINT_STATE_OVERLAP"):
            ConstraintMap(
                "cm","pm",("E1",),("E1",),(),(),("ev",)
            ).validate()


if __name__ == "__main__":
    unittest.main()
