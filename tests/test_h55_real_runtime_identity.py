import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

from runtime.real_visual_runtime import RealVisualRuntime


class _FakeAdapter:
    def ingest(self, source_path):
        from runtime.real_visual_runtime import VisualArtifact
        return VisualArtifact(
            source_path=source_path,
            input_type="PNG",
            sha256="a" * 64,
            width=100,
            height=100,
            page_count=1,
            image=np.zeros((100, 100, 3), dtype=np.uint8),
        )

    def detect(self, artifact):
        return {
            "artifact_sha256": artifact.sha256,
            "input_type": artifact.input_type,
            "dimensions": [artifact.width, artifact.height],
            "page_count": 1,
            "visual_line_count": 1,
            "major_regions": [],
            "recognized_space_labels": [],
            "fixed_element_identification": {"status": "ACCESSIBLE"},
        }


class _FakeLockedDetector:
    def detect(self, source_path, artifact_sha256):
        return {
            "status": "ACCESSIBLE",
            "plan_panels": [{"id": "panel-1"}],
            "candidates": [
                {
                    "candidate_id": "C01",
                    "element_type": "COLUMN",
                    "status": "LOCKED",
                    "bbox": [10, 10, 10, 10],
                    "confidence": 0.99,
                    "evidence_ids": ("ev-fixed-1",),
                }
            ],
            "unresolved_fixed_element_types": [],
        }


class _FakeMarkerDetector:
    def detect(self, source_path, artifact_sha256):
        return {"markers": []}


class _FakeCorroboration:
    def evaluate(self, **kwargs):
        class Result:
            status = "ACCESSIBLE"
            semantics = {}
            supporting_evidence = ("wall-1",)
            contradictions = ()
            reason = "synthetic test evidence"
        return Result()


class H55RealRuntimeIdentityTests(unittest.TestCase):
    def test_runtime_exposes_constraint_map_identity_bound_to_contracts(self):
        runtime = RealVisualRuntime(
            adapter=_FakeAdapter(),
            locked_detector=_FakeLockedDetector(),
            marker_detector=_FakeMarkerDetector(),
            corroboration_gate=_FakeCorroboration(),
        )
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "plan.png"
            cv2.imwrite(str(source), np.zeros((100, 100, 3), dtype=np.uint8))
            result = runtime.run("exec-h55", str(source), {"change_type": "FURNITURE_ONLY"})

        self.assertEqual(result["status"], "READY_FOR_APPROVAL")
        self.assertEqual(result["contracts"]["status"], "VALID")
        self.assertEqual(result["constraint_map"]["map_id"], "constraints-" + "a" * 16)
        self.assertEqual(
            result["constraint_map"]["map_id"],
            result["contracts"]["constraint_map_id"],
        )
        self.assertEqual(
            result["constraint_map"]["model_id"],
            result["contracts"]["plan_model_id"],
        )


if __name__ == "__main__":
    unittest.main()
