import unittest
from pathlib import Path


class DrawingStandardsRulePackTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(__file__).resolve().parents[1] / "docs" / "knowledge" / "drawing_standards" / "drawing_standards_rule_pack.md"
        self.text = self.path.read_text(encoding="utf-8")

    def test_required_authoritative_sources_are_registered(self):
        for source_id in (
            "ISO-128-1:2020",
            "ISO-128-3:2022",
            "ISO-129-1:2018",
            "ISO-5457",
            "ISO-7200",
            "PUB-256:1381",
        ):
            self.assertIn(source_id, self.text)

    def test_rules_have_fail_closed_boundaries(self):
        for rule_id in (
            "DRAW-REP-001",
            "DRAW-SCALE-001",
            "DRAW-SHEET-001",
            "DRAW-TITLE-001",
            "DRAW-DIM-001",
            "DRAW-VIEW-001",
            "DRAW-CROSSVIEW-001",
            "DRAW-EDU-001",
            "DRAW-PHASE1-001",
            "DRAW-PHASE2-001",
            "DRAW-LINE-001",
        ):
            self.assertIn(rule_id, self.text)
        self.assertIn("fail_closed", self.text)

    def test_educational_sources_cannot_be_used_as_regulatory_approval(self):
        marker = "never_use_for: independent regulatory compliance approval."
        self.assertIn(marker, self.text)

    def test_initial_executable_subset_preserves_traceability_boundary(self):
        self.assertIn("Every PASS must be traceable to rule_id + source_id + evidence IDs.", self.text)
        self.assertIn("Detection uncertainty never becomes compliance PASS.", self.text)


if __name__ == "__main__":
    unittest.main()
