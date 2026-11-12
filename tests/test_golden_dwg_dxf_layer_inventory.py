from __future__ import annotations

import unittest

from runtime.convert_golden_dwg_to_dxf import resolve_source_layer_names


class TestGoldenDwgDxfLayerInventory(unittest.TestCase):
    def test_resolves_modelspace_layer_handles_to_names(self):
        names, unresolved = resolve_source_layer_names(
            {10, 11, 12},
            [
                (10, 7, None, 100),
                (11, 2, None, 200),
                (12, 7, None, 100),
            ],
            [(100, "WALLS"), (200, "DOORS")],
        )
        self.assertEqual(names, ["DOORS", "WALLS"])
        self.assertEqual(unresolved, [])

    def test_reports_missing_entity_layer_mapping_without_defaulting_to_zero(self):
        names, unresolved = resolve_source_layer_names(
            {10, 11},
            [(10, 7, None, 100)],
            [(100, "WALLS")],
        )
        self.assertEqual(names, ["WALLS"])
        self.assertEqual(unresolved, [11])

    def test_reports_unknown_layer_handle(self):
        names, unresolved = resolve_source_layer_names(
            {10},
            [(10, 7, None, 999)],
            [(100, "WALLS")],
        )
        self.assertEqual(names, [])
        self.assertEqual(unresolved, [10])


if __name__ == "__main__":
    unittest.main()
