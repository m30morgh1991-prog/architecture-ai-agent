from __future__ import annotations

import unittest

from runtime.dwg_evidence_bridge import normalize_dwg_evidence


class TestDwgEvidenceBridge(unittest.TestCase):
    def test_source_bound_candidates_become_drawing_evidence(self):
        sha = "a" * 64
        raw = {
            "source_profile": {"sha256": sha},
            "semantic_candidates": {
                "WALLS": {
                    "status": "SUPPORTED",
                    "evidence": [
                        {"kind": "LAYER_NAME", "value": "A-WALL", "handle": 10}
                    ],
                },
                "DOORS": {
                    "status": "UNKNOWN",
                    "evidence": [],
                },
                "COLUMNS": {
                    "status": "SUPPORTED",
                    "evidence": [
                        {"kind": "LAYER_NAME", "value": "A-COLS", "handle": 11}
                    ],
                },
            },
            "text": [{"handle": 12, "text": "پذیرایی"}],
            "dimensions": [{"handle": 13, "actual_measurement": 300.0}],
        }
        result = normalize_dwg_evidence(raw)
        result.validate()
        self.assertEqual(result.source_sha256, sha)
        self.assertEqual(len(result.evidences), 4)
        self.assertTrue(all(item.source_sha256 == sha for item in result.evidences))
        self.assertEqual(
            {item.domain for item in result.evidences},
            {"SYMBOL", "STRUCTURE", "TEXT", "DIMENSION"},
        )
        self.assertEqual(
            [item.value for item in result.evidences if item.domain == "DIMENSION"],
            ["300.0"],
        )

    def test_missing_source_identity_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "DWG_EVIDENCE_SOURCE_SHA_MISSING"):
            normalize_dwg_evidence({"source_profile": {}})

    def test_bridge_does_not_create_geometry_or_planmodel_truth(self):
        sha = "b" * 64
        result = normalize_dwg_evidence({
            "source_profile": {"sha256": sha},
            "semantic_candidates": {
                "WALLS": {
                    "status": "SUPPORTED",
                    "evidence": [{"kind": "LAYER_NAME", "value": "A-WALL", "handle": 1}],
                }
            },
            "geometry": {"LINE": 999},
        })
        self.assertFalse(hasattr(result, "plan_model"))
        self.assertEqual(len(result.evidences), 1)


if __name__ == "__main__":
    unittest.main()
