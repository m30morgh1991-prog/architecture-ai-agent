import unittest

from runtime.opening_connectivity import classify_opening_connectivity


class OpeningConnectivityTests(unittest.TestCase):
    def setUp(self):
        self.spaces = [
            {"space_id": "A", "boundary_handle": "A", "evidence_ids": ["ea"]},
            {"space_id": "B", "boundary_handle": "B", "evidence_ids": ["eb"]},
        ]
        self.boundaries = {
            "A": [(0, 0), (10, 0), (10, 10), (0, 10)],
            "B": [(10, 0), (20, 0), (20, 10), (10, 10)],
        }
        self.opening = {
            "opening_id": "D2",
            "point": [10, 5],
            "span": [[10, 4], [10, 6]],
            "evidence_id": "ed2",
            "span_evidence_id": "span-d2",
            "host_wall_id": "W1",
            "host_wall_evidence_id": "wall-d2",
        }

    def test_insertion_point_alone_never_approves_connection(self):
        opening = {"opening_id": "D1", "point": [10, 5], "evidence_id": "ed1"}
        result = classify_opening_connectivity(
            [opening], self.spaces, self.boundaries, tolerance=0.01
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")
        self.assertEqual(result[0]["status"], "UNKNOWN")

    def test_verified_span_and_host_wall_remain_review_only(self):
        result = classify_opening_connectivity(
            [self.opening], self.spaces, self.boundaries,
            tolerance=0.01, host_wall_ids={"W1"},
        )
        self.assertEqual(result[0]["type"], "CONNECTED_BY_OPENING")
        self.assertEqual(result[0]["status"], "UNKNOWN")
        self.assertIn("span-d2", result[0]["evidence_ids"])
        self.assertIn("wall-d2", result[0]["evidence_ids"])

    def test_missing_host_wall_inventory_never_verifies_host(self):
        result = classify_opening_connectivity(
            [self.opening], self.spaces, self.boundaries, tolerance=0.01
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")
        self.assertFalse(result[0]["host_wall_evidenced"])

    def test_empty_host_wall_inventory_never_verifies_host(self):
        result = classify_opening_connectivity(
            [self.opening], self.spaces, self.boundaries,
            tolerance=0.01, host_wall_ids=set(),
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")
        self.assertFalse(result[0]["host_wall_evidenced"])

    def test_unmatched_host_wall_id_stays_unknown(self):
        result = classify_opening_connectivity(
            [self.opening], self.spaces, self.boundaries,
            tolerance=0.01, host_wall_ids={"W-OTHER"},
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")
        self.assertFalse(result[0]["host_wall_evidenced"])

    def test_missing_host_wall_evidence_id_stays_unknown_without_crashing(self):
        opening = {**self.opening}
        opening.pop("host_wall_evidence_id")
        result = classify_opening_connectivity(
            [opening], self.spaces, self.boundaries,
            tolerance=0.01, host_wall_ids={"W1"},
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")

    def test_missing_span_evidence_id_stays_unknown_without_crashing(self):
        opening = {**self.opening}
        opening.pop("span_evidence_id")
        result = classify_opening_connectivity(
            [opening], self.spaces, self.boundaries,
            tolerance=0.01, host_wall_ids={"W1"},
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")

    def test_missing_space_evidence_never_yields_connected_relation(self):
        spaces = [{**self.spaces[0], "evidence_ids": []}, self.spaces[1]]
        result = classify_opening_connectivity(
            [self.opening], spaces, self.boundaries,
            tolerance=0.01, host_wall_ids={"W1"},
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")
        self.assertFalse(result[0]["space_evidence_complete"])

    def test_connected_relation_requires_two_distinct_space_ids(self):
        spaces = [self.spaces[0], {**self.spaces[1], "space_id": "A"}]
        result = classify_opening_connectivity(
            [self.opening], spaces, self.boundaries,
            tolerance=0.01, host_wall_ids={"W1"},
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")

    def test_degenerate_boundaries_remain_unresolved_without_crashing(self):
        boundaries = {"A": [(0, 0), (10, 0)], "B": [(10, 0), (20, 0)]}
        result = classify_opening_connectivity(
            [self.opening], self.spaces, boundaries,
            tolerance=0.01, host_wall_ids={"W1"},
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")
        self.assertEqual(result[0]["touched_space_count"], 0)

    def test_invalid_tolerance_is_rejected(self):
        for tolerance in (float("nan"), float("inf"), -0.1, True, "bad"):
            with self.subTest(tolerance=tolerance):
                with self.assertRaisesRegex(
                    ValueError, "OPENING_CONNECTIVITY_TOLERANCE_INVALID"
                ):
                    classify_opening_connectivity(
                        [self.opening], self.spaces, self.boundaries,
                        tolerance=tolerance, host_wall_ids={"W1"},
                    )


    def test_boolean_boundary_coordinates_cannot_create_connection(self):
        boundaries = {
            "A": [(0, 0), (True, 0), (True, 10), (0, 10)],
            "B": [(True, 0), (20, 0), (20, 10), (True, 10)],
        }
        opening = {**self.opening, "span": [[1, 4], [1, 6]]}
        result = classify_opening_connectivity(
            [opening], self.spaces, boundaries,
            tolerance=0.01, host_wall_ids={"W1"},
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")
        self.assertEqual(result[0]["touched_space_count"], 0)

    def test_boolean_span_coordinates_cannot_create_connection(self):
        boundaries = {
            "A": [(0, 0), (1, 0), (1, 10), (0, 10)],
            "B": [(1, 0), (20, 0), (20, 10), (1, 10)],
        }
        opening = {**self.opening, "span": [[True, 4], [True, 6]]}
        result = classify_opening_connectivity(
            [opening], self.spaces, boundaries,
            tolerance=0.01, host_wall_ids={"W1"},
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")
        self.assertEqual(result[0]["touched_space_count"], 0)

    def test_non_finite_or_malformed_boundaries_remain_unresolved(self):
        invalid_boundaries = [
            {"A": [(0, 0), (10, 0), (float("nan"), 10), (0, 10)],
             "B": [(10, 0), (20, 0), (20, 10), (10, 10)]},
            {"A": [(0, 0), (10,), (10, 10), (0, 10)],
             "B": [(10, 0), (20, 0), (20, 10), (10, 10)]},
        ]
        for boundaries in invalid_boundaries:
            with self.subTest(boundaries=boundaries):
                result = classify_opening_connectivity(
                    [self.opening], self.spaces, boundaries,
                    tolerance=0.01, host_wall_ids={"W1"},
                )
                self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")

    def test_string_host_wall_inventory_cannot_verify_wall(self):
        opening = {**self.opening, "host_wall_id": "W"}
        result = classify_opening_connectivity(
            [opening], self.spaces, self.boundaries,
            tolerance=0.01, host_wall_ids="W",
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")
        self.assertFalse(result[0]["host_wall_evidenced"])

    def test_invalid_host_wall_inventory_type_fails_closed(self):
        result = classify_opening_connectivity(
            [self.opening], self.spaces, self.boundaries,
            tolerance=0.01, host_wall_ids=42,
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")
        self.assertFalse(result[0]["host_wall_evidenced"])

    def test_missing_opening_id_is_handled_as_unresolved(self):
        opening = {**self.opening}
        opening.pop("opening_id")
        result = classify_opening_connectivity(
            [opening], self.spaces, self.boundaries,
            tolerance=0.01, host_wall_ids={"W1"},
        )
        self.assertEqual(result[0]["type"], "OPENING_CONNECTIVITY_UNKNOWN")
        self.assertEqual(result[0]["opening_id"], "UNKNOWN-0")


if __name__ == "__main__":
    unittest.main()
