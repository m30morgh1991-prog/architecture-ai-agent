"""H101 GeometryReference attachment to canonical PlanModel and SpaceModel."""
import unittest

from runtime.geometry_reference_contract import build_geometry_reference
from runtime.plan_model_contract import PlanModel
from runtime.plan_model_reconstruction import build_plan_model_from_detection
from runtime.space_model_contract import build_space_model

SHA = "a" * 64
OTHER_SHA = "b" * 64


def geometry(source=SHA):
    return build_geometry_reference(reference_id="GR-01", source_sha256=source)


def spaces(source=SHA, ref=None):
    return build_space_model(
        model_id="SM-01",
        source_sha256=source,
        spaces=[{
            "space_id": "S01", "boundary_handle": "B01",
            "bbox": [0, 0, 10, 10], "centroid": [5, 5],
            "area": 100, "label": "Living", "evidence_ids": ["E-S01"],
        }],
        relations=[],
        geometry_reference=ref,
    )


class H101GeometryModelIntegrationTests(unittest.TestCase):
    def test_geometry_reference_attaches_to_space_model_and_plan_model(self):
        ref = geometry()
        space_model = spaces(SHA, ref)
        plan = PlanModel(
            model_id="PM-01", source_sha256=SHA, drawing_count=1,
            elements=(), space_model=space_model, geometry_reference=ref,
        )
        plan.validate()
        self.assertIs(plan.geometry_reference, ref)
        self.assertIs(plan.space_model.geometry_reference, ref)
        self.assertEqual(plan.geometry_reference.source_sha256, SHA)

    def test_space_model_rejects_geometry_reference_source_mismatch(self):
        model = spaces(SHA, geometry(OTHER_SHA))
        with self.assertRaisesRegex(ValueError, "SPACE_GEOMETRY_REFERENCE_SOURCE_MISMATCH"):
            model.validate()

    def test_plan_model_rejects_geometry_reference_source_mismatch(self):
        plan = PlanModel(
            model_id="PM-01", source_sha256=SHA, drawing_count=1,
            elements=(), geometry_reference=geometry(OTHER_SHA),
        )
        with self.assertRaisesRegex(ValueError, "GEOMETRY_REFERENCE_SOURCE_MISMATCH"):
            plan.validate()

    def test_reconstruction_accepts_geometry_reference_and_preserves_binding(self):
        result = build_plan_model_from_detection(
            model_id="PM-RECON", source_sha256=SHA,
            detection_result={"source_sha256": SHA, "candidates": [],
                             "unresolved_fixed_element_types": []},
            geometry_reference=geometry(),
        )
        self.assertEqual(result.plan_model.geometry_reference.source_sha256, SHA)
        result.validate()

    def test_reconstruction_rejects_geometry_reference_source_mismatch(self):
        with self.assertRaisesRegex(
            ValueError, "PLAN_RECONSTRUCTION_GEOMETRY_REFERENCE_SOURCE_MISMATCH"
        ):
            build_plan_model_from_detection(
                model_id="PM-RECON", source_sha256=SHA,
                detection_result={"source_sha256": SHA, "candidates": [],
                                 "unresolved_fixed_element_types": []},
                geometry_reference=geometry(OTHER_SHA),
            )

    def test_existing_models_remain_backward_compatible_without_reference(self):
        space_model = spaces(SHA, None)
        plan = PlanModel(
            model_id="PM-OLD", source_sha256=SHA, drawing_count=1,
            elements=(), space_model=space_model,
        )
        plan.validate()
        self.assertIsNone(plan.geometry_reference)
        self.assertIsNone(plan.space_model.geometry_reference)


if __name__ == "__main__":
    unittest.main()
