import unittest
from runtime.bim_ready_contract import BIMElementIdentity
from runtime.bim_constraint_contract import BIMConstraintBinding
from runtime.bim_constraintmap_contract import build_constraint_map_from_bim
from runtime.plan_model_contract import PlanElement


def el(i, category, state):
    return PlanElement(i, category, state, {"kind": "point"}, ("ev1",), 0.99,
        BIMElementIdentity(category, "IfcBuildingElement", i, "L01"))


class H79Tests(unittest.TestCase):
    def test_builds_evidence_backed_map(self):
        elements=(el("C01","Column","LOCKED"), el("F01","Furniture","EDITABLE"))
        bindings=tuple(BIMConstraintBinding(e.element_id,e.bim_identity.category,e.state,("ev1",)) for e in elements)
        r=build_constraint_map_from_bim("M01",elements,bindings)
        self.assertEqual(r.status,"PASS")
        self.assertEqual(r.constraint_map.protected_element_ids,("C01",))
        self.assertEqual(r.constraint_map.editable_element_ids,("F01",))

    def test_missing_binding_is_review(self):
        r=build_constraint_map_from_bim("M01",(el("C01","Column","LOCKED"),),())
        self.assertEqual(r.status,"NEEDS_REVIEW")
        self.assertIn("C01",r.constraint_map.unknown_element_ids)

    def test_conflict_blocks(self):
        e=el("C01","Column","LOCKED")
        b=BIMConstraintBinding("C01","Column","EDITABLE",("ev1",))
        r=build_constraint_map_from_bim("M01",(e,),(b,))
        self.assertEqual(r.status,"BLOCKED")

    def test_duplicate_binding_blocks(self):
        e=el("F01","Furniture","EDITABLE")
        b=BIMConstraintBinding("F01","Furniture","EDITABLE",("ev1",))
        r=build_constraint_map_from_bim("M01",(e,),(b,b))
        self.assertEqual(r.status,"BLOCKED")


if __name__ == "__main__":
    unittest.main()
