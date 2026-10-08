import unittest

from runtime.drawing_semantic_evidence import (
    DimensionEvidence, DrawingEvidenceSet, LevelEvidence, ViewMarkerEvidence,
    build_drawing_evidence_set,
)
from runtime.evidence_reconciliation import CandidateFact, reconcile_fact

SOURCE="a"*64

class H100SemanticEvidenceTests(unittest.TestCase):
    def test_evidence_requires_provenance_and_source_binding(self):
        result=build_drawing_evidence_set(
            set_id="S1", source_sha256=SOURCE,
            records=[{"evidence_id":"E1","domain":"TEXT","subject_id":"room-1",
                      "predicate":"label","value":"خواب","status":"SUPPORTED",
                      "confidence":0.99,"source_ref":"page=1:bbox=10,10,40,40"}])
        self.assertEqual(result.evidences[0].source_sha256,SOURCE)

    def test_contradiction_cannot_pass(self):
        fact=CandidateFact("F1","room-1","type","BEDROOM",("E1","E2"))
        result=reconcile_fact(fact,supporting=("E1",),contradicting=("E2",))
        self.assertEqual(result.decision,"CONTRADICTED")

    def test_missing_required_evidence_is_review(self):
        fact=CandidateFact("F2","stair-1","count","17",("E1",))
        result=reconcile_fact(fact,supporting=("E1",),required_evidence=("E1","E2"))
        self.assertEqual(result.decision,"NEEDS_REVIEW")

    def test_no_evidence_remains_unknown(self):
        fact=CandidateFact("F3","wall-1","material","brick",("E1",))
        result=reconcile_fact(fact)
        self.assertEqual(result.decision,"UNKNOWN")

    def test_supported_section_requires_direction_and_cut_plane(self):
        with self.assertRaisesRegex(ValueError,"SECTION_MARKER_SEMANTICS_INCOMPLETE"):
            ViewMarkerEvidence("M1","E1","SECTION",None,None,"SEC-A",("wall-1",),"SUPPORTED").validate()

    def test_dimension_requires_geometry_links(self):
        with self.assertRaisesRegex(ValueError,"DIMENSION_GEOMETRY_REFERENCE_MISSING"):
            DimensionEvidence("D1","E1",(),("ext-1",),100,"CM","SUPPORTED").validate()

    def test_level_requires_explicit_elevation(self):
        with self.assertRaisesRegex(ValueError,"LEVEL_ELEVATION_UNKNOWN"):
            LevelEvidence("L1","E1","+3.20",None,"M","F2","SUPPORTED").validate()

    def test_evidence_set_rejects_duplicate_ids(self):
        with self.assertRaisesRegex(ValueError,"DRAWING_EVIDENCE_ID_DUPLICATE"):
            build_drawing_evidence_set(
                set_id="S2",source_sha256=SOURCE,
                records=[
                    {"evidence_id":"E1","domain":"TEXT","subject_id":"x","predicate":"label","value":"A","source_ref":"p1"},
                    {"evidence_id":"E1","domain":"TEXT","subject_id":"x","predicate":"label","value":"B","source_ref":"p1"},
                ])
