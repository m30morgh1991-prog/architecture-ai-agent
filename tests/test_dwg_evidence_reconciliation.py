import unittest

from runtime.dwg_evidence_reconciliation import (
    reconcile_dwg_candidates,
    validate_dwg_fact_provenance,
)
from runtime.drawing_semantic_evidence import build_drawing_evidence_set


SHA = "a" * 64


class DWGEvidenceReconciliationTests(unittest.TestCase):
    def make_set(self, status="SUPPORTED"):
        return build_drawing_evidence_set(
            set_id=f"dwg:{SHA}",
            source_sha256=SHA,
            records=[{
                "evidence_id": "dwg:e1",
                "source_sha256": SHA,
                "domain": "SYMBOL",
                "subject_id": "WALLS:H1",
                "predicate": "architectural_element_candidate",
                "value": "WALLS",
                "status": status,
                "confidence": 1.0 if status == "SUPPORTED" else 0.5,
                "source_ref": f"dwg:{SHA}:entity:H1",
            }],
        )

    def test_supported_evidence_becomes_supported_fact(self):
        evidence = self.make_set()
        facts, results = reconcile_dwg_candidates(evidence)
        self.assertEqual(len(facts), 1)
        self.assertEqual(results[0].decision, "SUPPORTED")
        validate_dwg_fact_provenance(evidence, facts)

    def test_unknown_evidence_does_not_become_pass(self):
        evidence = self.make_set("UNKNOWN")
        _, results = reconcile_dwg_candidates(evidence)
        self.assertEqual(results[0].decision, "UNKNOWN")

    def test_uncertain_evidence_does_not_become_pass(self):
        evidence = self.make_set("UNCERTAIN")
        _, results = reconcile_dwg_candidates(evidence)
        self.assertEqual(results[0].decision, "UNKNOWN")

    def test_contradiction_is_preserved(self):
        evidence = self.make_set()
        facts, _ = reconcile_dwg_candidates(evidence)
        _, results = reconcile_dwg_candidates(
            evidence,
            contradictions={facts[0].fact_id: ("dwg:e1",)},
        )
        self.assertEqual(results[0].decision, "CONTRADICTED")


    def test_missing_contradiction_reference_fails_closed(self):
        evidence = self.make_set()
        facts, _ = reconcile_dwg_candidates(evidence)
        with self.assertRaisesRegex(ValueError, "CANDIDATE_FACT_CONTRADICTION_REFERENCE_MISSING"):
            reconcile_dwg_candidates(
                evidence,
                contradictions={facts[0].fact_id: ("foreign:evidence",)},
            )

    def test_missing_required_evidence_reference_fails_closed(self):
        evidence = self.make_set()
        facts, _ = reconcile_dwg_candidates(evidence)
        with self.assertRaisesRegex(ValueError, "CANDIDATE_FACT_REQUIRED_EVIDENCE_REFERENCE_MISSING"):
            reconcile_dwg_candidates(
                evidence,
                required_evidence={facts[0].fact_id: ("missing:required",)},
            )

    def test_support_and_contradiction_overlap_fails_closed(self):
        evidence = self.make_set()
        facts, _ = reconcile_dwg_candidates(evidence)
        with self.assertRaisesRegex(ValueError, "CANDIDATE_FACT_SUPPORT_CONTRADICTION_OVERLAP"):
            reconcile_dwg_candidates(
                evidence,
                contradictions={facts[0].fact_id: ("dwg:e1",)},
            )

    def test_missing_evidence_reference_blocks_provenance(self):
        evidence = self.make_set()
        facts, _ = reconcile_dwg_candidates(evidence)
        bad = type(facts[0])(
            fact_id=facts[0].fact_id,
            subject_id=facts[0].subject_id,
            predicate=facts[0].predicate,
            value=facts[0].value,
            evidence_ids=("missing",),
        )
        with self.assertRaisesRegex(ValueError, "CANDIDATE_FACT_EVIDENCE_REFERENCE_MISSING"):
            validate_dwg_fact_provenance(evidence, (bad,))


if __name__ == "__main__":
    unittest.main()
