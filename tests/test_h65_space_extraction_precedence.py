import unittest

from runtime.space_extraction import merge_space_boundaries


class H65SpaceExtractionPrecedenceTests(unittest.TestCase):
    def test_keeps_line_derived_faces_when_explicit_boundaries_exist(self):
        explicit = [("P01", [(0, 0), (10, 0), (10, 10), (0, 10)])]
        derived = [
            ([(0, 0), (10, 0), (10, 10), (0, 10)], 100.0),
            ([(10, 0), (20, 0), (20, 10), (10, 10)], 100.0),
        ]
        merged = merge_space_boundaries(explicit, derived)
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0][0], "P01")
        self.assertEqual(merged[1][0], "line-face-002")

    def test_does_not_duplicate_identical_explicit_and_derived_boundary(self):
        explicit = [("P01", [(0, 0), (10, 0), (10, 10), (0, 10)])]
        derived = [
            ([(0, 0), (10, 0), (10, 10), (0, 10)], 100.0),
        ]
        merged = merge_space_boundaries(explicit, derived)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0][0], "P01")

    def test_preserves_explicit_boundary_precedence(self):
        explicit = [("P01", [(0, 0), (10, 0), (10, 10), (0, 10)])]
        derived = [
            ([(0, 0), (10, 0), (10, 10), (0, 10)], 100.0),
            ([(20, 0), (20, 10), (30, 10), (30, 0)], 100.0),
        ]
        merged = merge_space_boundaries(explicit, derived)
        self.assertEqual(merged[0][2], "EXPLICIT_CLOSED_BOUNDARY")
        self.assertEqual(merged[1][2], "DERIVED_LINE_FACE")


if __name__ == "__main__":
    unittest.main()
