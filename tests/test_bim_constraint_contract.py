import unittest

from runtime.bim_ready_contract import BIMElementIdentity
from runtime.bim_constraint_contract import (
    BIMConstraintBinding,
    build_bim_constraint_binding,
    evaluate_bim_constraint_binding,
)
from runtime.plan_model_contract import PlanElement


def element(category, state):
    return PlanElement(
        element_id="E01",
        element_type=category,
        state=state,
        geometry={"kind": "point"},
        evidence_ids=("ev1",),
        confidence=0.99,
        bim_identity=BIMElementIdentity(
            category=category,
            ifc_class="IfcBuildingElement",
            name="E01",
            level_id="L01",
        ),
    )


class BIMConstraintContractTests(unittest.TestCase):
    def test_structural_category_binds_locked(self):
        e = element("Column", "LOCKED")
        b = build_bim_constraint_binding(e, ("ev1",))
        self.assertEqual(b.expected_state, "LOCKED")
        self.assertEqual(evaluate_bim_constraint_binding(e, b).status, "PASS")

    def test_furniture_category_binds_editable(self):
        e = element("Furniture", "EDITABLE")
        b = build_bim_constraint_binding(e, ("ev1",))
        self.assertEqual(evaluate_bim_constraint_binding(e, b).status, "PASS")

    def test_unmapped_category_fails_closed(self):
        e = element("CustomUnknown", "EDITABLE")
        b = BIMConstraintBinding("E01", "CustomUnknown", "EDITABLE", ("ev1",))
        self.assertEqual(evaluate_bim_constraint_binding(e, b).status, "UNKNOWN")

    def test_planmodel_state_conflict_is_blocked(self):
        e = element("Wall", "EDITABLE")
        b = BIMConstraintBinding("E01", "Wall", "LOCKED", ("ev1",))
        result = evaluate_bim_constraint_binding(e, b)
        self.assertEqual(result.status, "BLOCKED")

    def test_missing_bim_identity_is_unknown(self):
        e = PlanElement(
            element_id="E01",
            element_type="Furniture",
            state="EDITABLE",
            geometry={"kind": "point"},
            evidence_ids=("ev1",),
            confidence=0.99,
        )
        b = BIMConstraintBinding("E01", "Furniture", "EDITABLE", ("ev1",))
        self.assertEqual(evaluate_bim_constraint_binding(e, b).status, "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
