import unittest

from runtime.element_evidence_contract import (
    ElementEvidence,
    ElementEvidenceBundle,
    build_element_evidence_bundle,
)


class H69ElementEvidenceContractTests(unittest.TestCase):
    SHA = "a" * 64

    def test_valid_bundle_is_source_bound_and_queryable(self):
        bundle = build_element_evidence_bundle(
            bundle_id="B01",
            source_sha256=self.SHA,
            evidences=[
                {
                    "evidence_id": "E01",
                    "kind": "DWG_ENTITY",
                    "element_type": "WALLS",
                    "status": "SUPPORTED",
                    "description": "Native line entities support wall candidate geometry.",
                    "native_id": "42",
                    "confidence": 0.82,
                }
            ],
            unresolved_element_types=["DOORS"],
        )
        self.assertEqual(bundle.source_sha256, self.SHA)
        self.assertEqual(len(bundle.evidence_for("WALLS")), 1)
        self.assertEqual(bundle.unresolved_element_types, ("DOORS",))
        bundle.validate()

    def test_source_mismatch_is_rejected(self):
        bundle = ElementEvidenceBundle(
            bundle_id="B01",
            source_sha256=self.SHA,
            evidences=(
                ElementEvidence(
                    evidence_id="E01",
                    source_sha256="b" * 64,
                    kind="DWG_GEOMETRY",
                    element_type="OUTER_BOUNDARY",
                    status="SUPPORTED",
                    description="Geometry evidence.",
                    confidence=0.7,
                ),
            ),
        )
        with self.assertRaisesRegex(ValueError, "ELEMENT_EVIDENCE_SOURCE_MISMATCH"):
            bundle.validate()

    def test_uncertain_evidence_cannot_claim_high_confidence(self):
        evidence = ElementEvidence(
            evidence_id="E01",
            source_sha256=self.SHA,
            kind="UNKNOWN",
            element_type="WINDOWS",
            status="UNKNOWN",
            description="Semantics unresolved.",
            confidence=0.99,
        )
        with self.assertRaisesRegex(ValueError, "UNCERTAIN_EVIDENCE_CANNOT_HAVE_HIGH_CONFIDENCE"):
            evidence.validate()

    def test_duplicate_ids_are_rejected(self):
        item = {
            "evidence_id": "E01",
            "kind": "DWG_TEXT",
            "element_type": "DOORS",
            "status": "UNCERTAIN",
            "description": "Door label evidence.",
            "confidence": 0.5,
        }
        with self.assertRaisesRegex(ValueError, "ELEMENT_EVIDENCE_ID_DUPLICATE"):
            build_element_evidence_bundle(
                bundle_id="B01",
                source_sha256=self.SHA,
                evidences=[item, item],
            )

    def test_unknown_element_type_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "ELEMENT_EVIDENCE_ELEMENT_TYPE_INVALID"):
            build_element_evidence_bundle(
                bundle_id="B01",
                source_sha256=self.SHA,
                evidences=[{
                    "evidence_id": "E01",
                    "kind": "DWG_ENTITY",
                    "element_type": "FURNITURE",
                    "status": "SUPPORTED",
                    "description": "Not an H69 fixed architectural type.",
                    "confidence": 0.5,
                }],
            )


if __name__ == "__main__":
    unittest.main()
