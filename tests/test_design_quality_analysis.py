import unittest

from runtime.space_model_contract import SpaceModel, SpaceRecord, SpaceRelation
from runtime.design_quality_analysis import (
    SpaceProgramRequirement,
    analyze_space_program_fit,
)


SOURCE = "a" * 64


def _space_model(relations=()):
    spaces = (
        SpaceRecord("LIVING", "h1", (0, 0, 10, 10), (5, 5), 100, "Living",
                    ("ev-living",), status="ACCESSIBLE", identity_status="EXPLICIT"),
        SpaceRecord("KITCHEN", "h2", (10, 0, 16, 10), (13, 5), 60, "Kitchen",
                    ("ev-kitchen",), status="ACCESSIBLE", identity_status="EXPLICIT"),
        SpaceRecord("BEDROOM", "h3", (16, 0, 24, 10), (20, 5), 80, "Bedroom",
                    ("ev-bedroom",), status="ACCESSIBLE", identity_status="EXPLICIT"),
    )
    model = SpaceModel("pm-design-01", SOURCE, spaces, tuple(relations))
    model.validate()
    return model


class DesignQualityAnalysisTests(unittest.TestCase):
    def test_area_deviation_is_advisory_not_blocking(self):
        result = analyze_space_program_fit(
            _space_model(),
            [SpaceProgramRequirement("KITCHEN", min_area=70, target_area=75)],
        )
        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertEqual(
            {item.code for item in result.findings},
            {"SPACE_AREA_BELOW_PROGRAM_MINIMUM", "SPACE_AREA_DIFFERS_FROM_TARGET"},
        )
        self.assertTrue(all(item.severity in {"INFO", "WARNING", "REVIEW"} for item in result.findings))

    def test_explicit_opening_path_is_recognized(self):
        relations = (
            SpaceRelation("r1", "CONNECTED_BY_OPENING", "LIVING", "KITCHEN",
                          ("ev-door-1",), "ACCESSIBLE"),
            SpaceRelation("r2", "CONNECTED_BY_OPENING", "KITCHEN", "BEDROOM",
                          ("ev-door-2",), "ACCESSIBLE"),
        )
        result = analyze_space_program_fit(
            _space_model(relations),
            [SpaceProgramRequirement("LIVING", require_accessible_path_to=("BEDROOM",))],
        )
        self.assertEqual(result.status, "ANALYSIS_COMPLETE")
        self.assertEqual(result.findings, ())

    def test_missing_connectivity_evidence_is_review_not_false_failure(self):
        result = analyze_space_program_fit(
            _space_model(),
            [SpaceProgramRequirement("LIVING", require_accessible_path_to=("BEDROOM",))],
        )
        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertEqual(result.findings[0].code, "ACCESSIBLE_PATH_NOT_ESTABLISHED")
        self.assertIn("not proof", result.findings[0].suggestion)

    def test_required_adjacency_uses_explicit_topology(self):
        relation = SpaceRelation("r1", "DISCONNECTED", "LIVING", "KITCHEN",
                                 ("ev-living", "ev-kitchen"), "UNKNOWN")
        result = analyze_space_program_fit(
            _space_model((relation,)),
            [SpaceProgramRequirement("LIVING", required_adjacent_to=("KITCHEN",))],
        )
        self.assertEqual(result.findings[0].code, "REQUIRED_ADJACENCY_NOT_MET")

    def test_bbox_proximity_alone_does_not_prove_required_adjacency(self):
        result = analyze_space_program_fit(
            _space_model(),
            [SpaceProgramRequirement("LIVING", required_adjacent_to=("KITCHEN",))],
        )
        self.assertEqual(result.findings[0].code, "REQUIRED_ADJACENCY_UNRESOLVED")
        self.assertEqual(result.findings[0].severity, "REVIEW")

    def test_unwanted_adjacency_is_a_design_warning(self):
        relation = SpaceRelation("r1", "SHARED_BOUNDARY", "LIVING", "BEDROOM",
                                 ("ev-living", "ev-bedroom"), "UNKNOWN")
        result = analyze_space_program_fit(
            _space_model((relation,)),
            [SpaceProgramRequirement("LIVING", avoid_adjacent_to=("BEDROOM",))],
        )
        self.assertEqual(result.findings[0].code, "UNWANTED_ADJACENCY_PRESENT")

    def test_invalid_area_range_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "PROGRAM_AREA_RANGE_INVALID"):
            SpaceProgramRequirement("LIVING", min_area=80, max_area=60).validate()

    def test_bool_area_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "PROGRAM_MIN_AREA_INVALID"):
            SpaceProgramRequirement("LIVING", min_area=True).validate()


if __name__ == "__main__":
    unittest.main()
