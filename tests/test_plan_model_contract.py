import unittest

from runtime.element_evidence_contract import build_element_evidence_bundle
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

    def test_element_evidence_type_must_match_plan_element_type(self):
        source_sha = "a" * 64
        evidence = build_element_evidence_bundle(
            bundle_id="bundle-01",
            source_sha256=source_sha,
            evidences=[{
                "evidence_id": "E-WALL",
                "source_sha256": source_sha,
                "kind": "UNKNOWN",
                "element_type": "WALLS",
                "status": "UNKNOWN",
                "description": "Unresolved wall evidence.",
                "confidence": 0.0,
            }],
        )
        model = PlanModel(
            model_id="PM-01",
            source_sha256=source_sha,
            drawing_count=1,
            elements=(
                PlanElement(
                    "D01", "DOORS", "UNKNOWN", {}, ("E-WALL",), 0.0
                ),
            ),
            element_evidence=evidence,
        )
        with self.assertRaisesRegex(
            ValueError, "PLAN_ELEMENT_EVIDENCE_TYPE_MISMATCH"
        ):
            model.validate()

    def test_plan_element_rejects_boolean_and_non_finite_confidence(self):
        for confidence in (True, float("nan"), float("inf"), "0.99"):
            with self.subTest(confidence=confidence):
                with self.assertRaisesRegex(ValueError, "INVALID_CONFIDENCE"):
                    PlanElement(
                        "W01", "WALLS", "LOCKED", {}, ("ev-1",), confidence
                    ).validate()

    def test_plan_element_rejects_unknown_state(self):
        with self.assertRaisesRegex(ValueError, "INVALID_PLAN_ELEMENT_STATE"):
            PlanElement("W01", "WALLS", "MAYBE", {}, ("ev-1",), 0.99).validate()

    def test_locked_state_requires_supported_source_evidence(self):
        source_sha = "a" * 64
        evidence = build_element_evidence_bundle(
            bundle_id="bundle-unknown", source_sha256=source_sha,
            evidences=[{
                "evidence_id": "E-UNKNOWN", "kind": "UNKNOWN",
                "element_type": "WALLS", "status": "UNKNOWN",
                "description": "Unresolved wall evidence.", "confidence": 0.0,
            }],
        )
        model = PlanModel(
            model_id="PM-UNKNOWN", source_sha256=source_sha, drawing_count=1,
            elements=(PlanElement("W01", "WALLS", "LOCKED", {}, ("E-UNKNOWN",), 0.99),),
            element_evidence=evidence,
        )
        with self.assertRaisesRegex(
            ValueError, "PLAN_ELEMENT_PROMOTION_EVIDENCE_NOT_SUPPORTED"
        ):
            model.validate()

    def test_element_confidence_cannot_exceed_supported_evidence(self):
        source_sha = "b" * 64
        evidence = build_element_evidence_bundle(
            bundle_id="bundle-low", source_sha256=source_sha,
            evidences=[{
                "evidence_id": "E-LOW", "kind": "DWG_GEOMETRY",
                "element_type": "WALLS", "status": "SUPPORTED",
                "description": "Supported but low-confidence geometry.", "confidence": 0.80,
            }],
        )
        model = PlanModel(
            model_id="PM-LOW", source_sha256=source_sha, drawing_count=1,
            elements=(PlanElement("W01", "WALLS", "LOCKED", {}, ("E-LOW",), 0.99),),
            element_evidence=evidence,
        )
        with self.assertRaisesRegex(
            ValueError, "PLAN_ELEMENT_CONFIDENCE_EXCEEDS_EVIDENCE"
        ):
            model.validate()

    def test_constraint_states_must_not_overlap(self):
        with self.assertRaisesRegex(ValueError, "CONSTRAINT_STATE_OVERLAP"):
            ConstraintMap(
                "cm","pm",("E1",),("E1",),(),(),("ev",)
            ).validate()


if __name__ == "__main__":
    unittest.main()
