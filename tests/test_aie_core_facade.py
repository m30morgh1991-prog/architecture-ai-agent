import unittest

from runtime.aie.core_facade import inspect_plan
from runtime.plan_model_contract import ConstraintMap, PlanElement, PlanModel


SOURCE_SHA = "a" * 64


def make_model(*, state="EDITABLE", unresolved=(), geometry=None):
    element = PlanElement(
        element_id="W-001",
        element_type="wall",
        state=state,
        geometry=geometry if geometry is not None else {
            "bbox": [0, 0, 100, 200],
            "unit": "mm",
            "coordinate_frame": "local-plan",
        },
        evidence_ids=("EV-001",),
        confidence=0.99,
    )
    return PlanModel(
        model_id="PM-001",
        source_sha256=SOURCE_SHA,
        drawing_count=1,
        elements=(element,),
        unresolved=tuple(unresolved),
    )


def make_constraints(*, state="EDITABLE", model_id="PM-001"):
    buckets = {
        "LOCKED": (),
        "EDITABLE": (),
        "CONDITIONAL": (),
        "UNKNOWN": (),
    }
    bucket_field = {
        "LOCKED": "LOCKED",
        "EDITABLE": "EDITABLE",
        "CONDITIONAL": "CONDITIONAL",
        "UNKNOWN": "UNKNOWN",
    }[state]
    buckets[bucket_field] = ("W-001",)
    return ConstraintMap(
        map_id="CM-001",
        model_id=model_id,
        protected_element_ids=buckets["LOCKED"],
        editable_element_ids=buckets["EDITABLE"],
        conditional_element_ids=buckets["CONDITIONAL"],
        unknown_element_ids=buckets["UNKNOWN"],
        evidence_ids=("EV-CM-001",),
    )


class AIECoreFacadeTests(unittest.TestCase):
    def test_consistent_contracts_are_inspected_but_not_approved_for_editing(self):
        model = make_model()
        constraints = make_constraints()

        result = inspect_plan(model, constraints)

        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertTrue(result.requires_review)
        self.assertFalse(result.is_blocked)
        self.assertEqual(result.element_count, 1)
        self.assertIn(
            "CONSTRAINT_EVIDENCE_NOT_RECONCILED",
            {finding.code for finding in result.findings},
        )
        self.assertIn(
            "ELEMENT_EVIDENCE_BUNDLE_NOT_ATTACHED",
            {finding.code for finding in result.findings},
        )

    def test_plan_and_constraint_states_must_match(self):
        result = inspect_plan(make_model(state="LOCKED"), make_constraints())

        self.assertEqual(result.status, "BLOCKED")
        self.assertIn(
            "PLAN_CONSTRAINT_STATE_MISMATCH",
            {finding.code for finding in result.findings},
        )

    def test_constraint_map_must_reference_same_model(self):
        result = inspect_plan(
            make_model(),
            make_constraints(model_id="PM-OTHER"),
        )

        self.assertEqual(result.status, "BLOCKED")
        self.assertIn(
            "CONSTRAINT_MODEL_ID_MISMATCH",
            {finding.code for finding in result.findings},
        )

    def test_orphan_constraint_ids_block_inspection(self):
        constraints = ConstraintMap(
            map_id="CM-001",
            model_id="PM-001",
            protected_element_ids=(),
            editable_element_ids=("W-001", "GHOST-001"),
            conditional_element_ids=(),
            unknown_element_ids=(),
            evidence_ids=("EV-CM-001",),
        )

        result = inspect_plan(make_model(), constraints)

        self.assertEqual(result.status, "BLOCKED")
        self.assertIn(
            "CONSTRAINT_ELEMENT_NOT_IN_MODEL",
            {finding.code for finding in result.findings},
        )

    def test_unresolved_model_items_require_review(self):
        result = inspect_plan(
            make_model(unresolved=("scale", "column-classification")),
            make_constraints(),
        )

        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertIn(
            "PLAN_MODEL_UNRESOLVED_ITEMS",
            {finding.code for finding in result.findings},
        )

    def test_missing_units_or_coordinate_frame_requires_review(self):
        result = inspect_plan(
            make_model(geometry={"bbox": [0, 0, 100, 200]}),
            make_constraints(),
        )

        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertIn(
            "GEOMETRY_REFERENCE_UNVERIFIED",
            {finding.code for finding in result.findings},
        )


    def test_malformed_model_collections_block_without_result_crash(self):
        malformed_models = (
            PlanModel(
                model_id="PM-001",
                source_sha256=SOURCE_SHA,
                drawing_count=1,
                elements=None,
            ),
            PlanModel(
                model_id="PM-001",
                source_sha256=SOURCE_SHA,
                drawing_count=1,
                elements=(None,),
            ),
        )

        for model in malformed_models:
            with self.subTest(elements=model.elements):
                result = inspect_plan(model, make_constraints())
                self.assertEqual(result.status, "BLOCKED")
                self.assertIn(
                    "PLAN_MODEL_INVALID",
                    {finding.code for finding in result.findings},
                )
                self.assertEqual(result.space_count, 0)

    def test_invalid_model_is_blocked(self):
        model = PlanModel(
            model_id="PM-001",
            source_sha256="not-a-sha",
            drawing_count=1,
            elements=(),
        )

        result = inspect_plan(model, make_constraints())

        self.assertEqual(result.status, "BLOCKED")
        self.assertIn(
            "PLAN_MODEL_INVALID",
            {finding.code for finding in result.findings},
        )


if __name__ == "__main__":
    unittest.main()
