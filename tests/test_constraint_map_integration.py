import unittest

from runtime.element_evidence_contract import build_element_evidence_bundle
from runtime.plan_model_contract import ConstraintMap, PlanElement, PlanModel
from runtime.constraint_map_integration import build_constraint_map_from_plan_model


class H71ConstraintMapIntegrationTests(unittest.TestCase):
    SHA = "a" * 64

    def bundle(self, *, wall_status="SUPPORTED", wall_confidence=0.92):
        return build_element_evidence_bundle(
            bundle_id="PM01:evidence",
            source_sha256=self.SHA,
            evidences=[
                {
                    "evidence_id": "E-WALL",
                    "source_sha256": self.SHA,
                    "kind": "DWG_GEOMETRY",
                    "element_type": "WALLS",
                    "status": wall_status,
                    "description": "Wall evidence.",
                    "confidence": wall_confidence,
                },
                {
                    "evidence_id": "E-COLUMN",
                    "source_sha256": self.SHA,
                    "kind": "DWG_ENTITY",
                    "element_type": "COLUMNS",
                    "status": "SUPPORTED",
                    "description": "Column evidence.",
                    "confidence": 0.97,
                },
            ],
        )

    def test_supported_states_are_integrated_source_bound(self):
        model = PlanModel(
            "PM01", self.SHA, 1,
            (
                PlanElement("C01", "COLUMNS", "LOCKED", {}, ("E-COLUMN",), 0.97),
                PlanElement("W01", "WALLS", "CONDITIONAL", {}, ("E-WALL",), 0.92),
            ),
            element_evidence=self.bundle(),
        )
        cmap = build_constraint_map_from_plan_model(plan_model=model, map_id="CM01")
        self.assertEqual(cmap.source_sha256, self.SHA)
        self.assertEqual(cmap.model_id, "PM01")
        self.assertEqual(cmap.protected_element_ids, ("C01",))
        self.assertEqual(cmap.conditional_element_ids, ("W01",))
        cmap.validate()

    def test_insufficient_evidence_never_becomes_locked(self):
        model = PlanModel(
            "PM01", self.SHA, 1,
            (PlanElement("W01", "WALLS", "LOCKED", {}, ("E-WALL",), 0.99),),
            element_evidence=self.bundle(wall_status="UNKNOWN", wall_confidence=0.50),
        )
        cmap = build_constraint_map_from_plan_model(plan_model=model, map_id="CM01")
        self.assertEqual(cmap.protected_element_ids, ())
        self.assertEqual(cmap.unknown_element_ids, ("W01",))

    def test_missing_evidence_is_rejected_fail_closed(self):
        model = PlanModel(
            "PM01", self.SHA, 1,
            (PlanElement("W01", "WALLS", "UNKNOWN", {}, ("E-MISSING",), 0.10),),
        )
        with self.assertRaisesRegex(ValueError, "CONSTRAINT_MAP_EVIDENCE_REQUIRED"):
            build_constraint_map_from_plan_model(plan_model=model, map_id="CM01")

    def test_constraint_map_source_is_validated(self):
        cmap = ConstraintMap(
            "CM01", "PM01", ("C01",), (), (), (), ("E-COLUMN",), self.SHA
        )
        cmap.validate()
        bad = ConstraintMap(
            "CM02", "PM01", ("C01",), (), (), (), ("E-COLUMN",), "b" * 64
        )
        self.assertNotEqual(cmap.source_sha256, bad.source_sha256)

    def test_constraint_states_do_not_overlap(self):
        with self.assertRaisesRegex(ValueError, "CONSTRAINT_STATE_OVERLAP"):
            ConstraintMap(
                "CM", "PM", ("E1",), ("E1",), (), (), ("EV",), self.SHA
            ).validate()


if __name__ == "__main__":
    unittest.main()
