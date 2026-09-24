import unittest
from runtime.visual_semantic_corroboration import VisualSemanticCorroborationGate

class CorroborationAdversarialTests(unittest.TestCase):
    def setUp(self):
        self.gate=VisualSemanticCorroborationGate()

    def test_marker_plus_vector_without_structural_geometry_is_not_column(self):
        r=self.gate.evaluate(marker_evidence=True,wall_geometry_evidence=False,
            vector_or_grid_evidence=True,structural_geometry_evidence=False)
        self.assertEqual(r.semantics,"STRUCTURAL_FIXED_ELEMENTS")

    def test_marker_plus_structural_geometry_can_identify_columns(self):
        r=self.gate.evaluate(marker_evidence=True,wall_geometry_evidence=False,
            vector_or_grid_evidence=False,structural_geometry_evidence=True)
        self.assertEqual(r.semantics,"COLUMNS")

    def test_non_marker_independent_evidence_is_structural_not_column(self):
        r=self.gate.evaluate(marker_evidence=False,wall_geometry_evidence=True,
            vector_or_grid_evidence=True,structural_geometry_evidence=True)
        self.assertEqual(r.semantics,"STRUCTURAL_FIXED_ELEMENTS")

    def test_contradiction_always_wins(self):
        r=self.gate.evaluate(marker_evidence=True,wall_geometry_evidence=True,
            vector_or_grid_evidence=True,structural_geometry_evidence=True,
            contradiction_evidence=True)
        self.assertEqual(r.status,"BLOCKED")
        self.assertEqual(r.semantics,"UNKNOWN")

if __name__=="__main__":
    unittest.main()
