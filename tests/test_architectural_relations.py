import unittest

from runtime.architectural_relations import (
    ArchitecturalRelation,
    ArchitecturalRelationSet,
    build_architectural_relation_set,
)
from runtime.element_evidence_contract import build_element_evidence_bundle
from runtime.plan_model_contract import PlanElement, PlanModel


SOURCE = "a" * 64


def model_with_evidence():
    evidence = build_element_evidence_bundle(
        bundle_id="m:evidence",
        source_sha256=SOURCE,
        evidences=[
            {
                "evidence_id": "e1",
                "element_type": "WALLS",
                "status": "SUPPORTED",
                "description": "Native wall geometry",
                "confidence": 0.99,
            },
            {
                "evidence_id": "e2",
                "element_type": "DOORS",
                "status": "SUPPORTED",
                "description": "Native door geometry",
                "confidence": 0.99,
            },
        ],
    )
    return PlanModel(
        model_id="m",
        source_sha256=SOURCE,
        drawing_count=1,
        elements=(
            PlanElement("W1", "WALLS", "LOCKED", {}, ("e1",), 0.99),
            PlanElement("D1", "DOORS", "LOCKED", {}, ("e2",), 0.99),
        ),
        element_evidence=evidence,
    )


class ArchitecturalRelationsTests(unittest.TestCase):
    def test_supported_relation_is_source_bound(self):
        result = build_architectural_relation_set(
            set_id="m:relations",
            plan_model=model_with_evidence(),
            relations=[{
                "relation_id": "r1",
                "relation_kind": "ELEMENT_ADJACENCY",
                "from_id": "W1",
                "to_id": "D1",
                "evidence_ids": ["e1", "e2"],
                "status": "SUPPORTED",
                "confidence": 0.99,
            }],
        )
        self.assertEqual(result.relations[0].source_sha256, SOURCE)
        self.assertEqual(result.unresolved, ())

    def test_unknown_relation_is_fail_closed(self):
        result = build_architectural_relation_set(
            set_id="m:relations",
            plan_model=model_with_evidence(),
            relations=[{
                "relation_id": "r1",
                "relation_kind": "ELEMENT_ADJACENCY",
                "from_id": "W1",
                "to_id": "D1",
                "evidence_ids": ["e1"],
                "status": "UNKNOWN",
            }],
        )
        self.assertEqual(result.unresolved, ("r1",))

    def test_unknown_endpoint_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "ARCH_RELATION_ENDPOINT_UNKNOWN"):
            build_architectural_relation_set(
                set_id="m:relations",
                plan_model=model_with_evidence(),
                relations=[{
                    "relation_id": "r1",
                    "relation_kind": "ELEMENT_ADJACENCY",
                    "from_id": "W1",
                    "to_id": "NOPE",
                    "evidence_ids": ["e1"],
                }],
            )

    def test_missing_evidence_reference_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "ARCH_RELATION_EVIDENCE_REFERENCE_MISSING"):
            build_architectural_relation_set(
                set_id="m:relations",
                plan_model=model_with_evidence(),
                relations=[{
                    "relation_id": "r1",
                    "relation_kind": "ELEMENT_ADJACENCY",
                    "from_id": "W1",
                    "to_id": "D1",
                    "evidence_ids": ["missing"],
                }],
            )

    def test_duplicate_relation_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "ARCH_RELATION_ID_DUPLICATE"):
            ArchitecturalRelationSet(
                "s", SOURCE,
                (
                    ArchitecturalRelation("r1", SOURCE, "ELEMENT_ADJACENCY", "W1", "D1", ("e1",)),
                    ArchitecturalRelation("r1", SOURCE, "ELEMENT_ADJACENCY", "W1", "D1", ("e1",)),
                ),
            ).validate()


if __name__ == "__main__":
    unittest.main()
