import unittest

from runtime.architectural_annotation_contract import (
    ArchitecturalAnnotation,
    validate_annotation_set,
)
from runtime.dimension_semantics import (
    build_dimension_semantic,
    resolve_dimension_status,
)


SOURCE = "a" * 64


class ArchitecturalAnnotationContractTests(unittest.TestCase):
    def test_supported_dimension_annotation_requires_text_and_evidence(self):
        annotation = ArchitecturalAnnotation(
            annotation_id="dim-1",
            annotation_type="DIMENSION",
            source_sha256=SOURCE,
            evidence_ids=("e1",),
            geometry={"kind": "line", "points": [[0, 0], [100, 0]]},
            text="1000",
            status="SUPPORTED",
        )
        validate_annotation_set(SOURCE, (annotation,))

    def test_source_mismatch_is_rejected(self):
        annotation = ArchitecturalAnnotation(
            annotation_id="dim-1",
            annotation_type="DIMENSION",
            source_sha256="b" * 64,
            evidence_ids=("e1",),
            geometry={"kind": "line", "points": [[0, 0], [100, 0]]},
            text="1000",
        )
        with self.assertRaises(ValueError):
            validate_annotation_set(SOURCE, (annotation,))


class DimensionSemanticsTests(unittest.TestCase):
    def test_missing_reference_never_becomes_supported(self):
        status = resolve_dimension_status(
            value=3000,
            unit="MM",
            reference_element_ids=(),
            evidence_ids=("e1",),
            source_sha256=SOURCE,
            explicit_geometry_association=True,
        )
        self.assertEqual(status, "UNKNOWN")

    def test_reference_without_explicit_association_requires_review(self):
        status = resolve_dimension_status(
            value=3000,
            unit="MM",
            reference_element_ids=("W1", "W2"),
            evidence_ids=("e1",),
            source_sha256=SOURCE,
            explicit_geometry_association=False,
        )
        self.assertEqual(status, "NEEDS_REVIEW")

    def test_supported_dimension_requires_value_unit_and_reference(self):
        result = build_dimension_semantic(
            dimension_id="d1",
            source_sha256=SOURCE,
            evidence_ids=("e1",),
            value=3000,
            unit="MM",
            reference_element_ids=("W1", "W2"),
            geometry_roles=("start", "end"),
            status="SUPPORTED",
        )
        self.assertEqual(result.reference.element_ids, ("W1", "W2"))


if __name__ == "__main__":
    unittest.main()
