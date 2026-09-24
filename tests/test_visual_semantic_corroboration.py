import unittest

from runtime.visual_semantic_corroboration import VisualSemanticCorroborationGate


class VisualSemanticCorroborationTests(unittest.TestCase):
    def test_single_marker_signal_remains_unknown(self):
        result = VisualSemanticCorroborationGate().evaluate(
            marker_evidence=True,
            wall_geometry_evidence=False,
            vector_or_grid_evidence=False,
            structural_geometry_evidence=False,
        )
        self.assertEqual(result.status, "UNKNOWN")
        self.assertEqual(result.semantics, "UNKNOWN")

    def test_two_independent_signals_can_unlock_structural_semantics(self):
        result = VisualSemanticCorroborationGate().evaluate(
            marker_evidence=True,
            wall_geometry_evidence=True,
            vector_or_grid_evidence=False,
            structural_geometry_evidence=True,
        )
        self.assertEqual(result.status, "ACCESSIBLE")
        self.assertEqual(result.semantics, "COLUMNS")
        self.assertEqual(len(result.supporting_evidence), 3)

    def test_contradiction_is_blocking_even_with_support(self):
        result = VisualSemanticCorroborationGate().evaluate(
            marker_evidence=True,
            wall_geometry_evidence=True,
            vector_or_grid_evidence=True,
            structural_geometry_evidence=True,
            contradiction_evidence=True,
        )
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("contradictory_evidence", result.contradictions)

    def test_empty_evidence_is_fail_closed(self):
        result = VisualSemanticCorroborationGate().evaluate(
            marker_evidence=False,
            wall_geometry_evidence=False,
            vector_or_grid_evidence=False,
            structural_geometry_evidence=False,
        )
        self.assertEqual(result.status, "UNKNOWN")
        self.assertEqual(result.semantics, "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
