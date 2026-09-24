import unittest

from runtime.real_visual_runtime import RealVisualArtifactAdapter, RealVisualRuntime, VisualArtifact


class FakeAdapter(RealVisualArtifactAdapter):
    def ingest(self, source_path):
        return VisualArtifact(
            source_path=source_path,
            input_type="PNG",
            sha256="a" * 64,
            width=1000,
            height=800,
            page_count=1,
            image=None,
        )

    def detect(self, artifact):
        return {
            "artifact_sha256": artifact.sha256,
            "input_type": artifact.input_type,
            "dimensions": [artifact.width, artifact.height],
            "page_count": artifact.page_count,
            "visual_line_count": 12,
            "major_regions": [],
            "recognized_space_labels": [],
            "fixed_element_identification": {
                "status": "UNKNOWN",
                "reason": "test fixture is intentionally conservative",
            },
        }


class FakeLockedDetector:
    def detect(self, source_path, source_sha256):
        return {
            "status": "UNKNOWN",
            "source_sha256": source_sha256,
            "plan_panels": [],
            "candidates": [
                {
                    "candidate_id": "C01",
                    "element_type": "COLUMNS",
                    "bbox": [10, 20, 20, 30],
                    "confidence": 0.62,
                    "evidence_ids": ["ev-column-1"],
                    "status": "UNKNOWN",
                }
            ],
            "locked_element_types": [],
            "unresolved_fixed_element_types": [
                "COLUMNS", "OUTER_BOUNDARY", "WALLS", "DOORS", "WINDOWS",
                "OVERALL_PLAN_FORM",
            ],
        }


class FakeMarkerDetector:
    def detect(self, source_path, source_sha256):
        return {"markers": [], "marker_count": 0}


class FakeCorroboration:
    def evaluate(self, **kwargs):
        class Result:
            status = "UNKNOWN"
            semantics = "UNKNOWN"
            supporting_evidence = ()
            contradictions = ()
            reason = "test"
        return Result()


class H39RuntimeIntegrationTests(unittest.TestCase):
    def test_contracts_are_materialized_and_validated(self):
        runtime = RealVisualRuntime()
        artifact = VisualArtifact("x.png", "PNG", "b" * 64, 1000, 800, 1, None)
        model, constraints = runtime._build_contracts(
            artifact=artifact,
            locked_elements={
                "candidates": [{
                    "candidate_id": "C01",
                    "element_type": "COLUMNS",
                    "bbox": [1, 2, 10, 10],
                    "confidence": 0.62,
                    "evidence_ids": ["ev-1"],
                    "status": "UNKNOWN",
                }],
                "unresolved_fixed_element_types": ["WALLS"],
            },
            evidence_id="real-h39",
        )
        self.assertEqual(model.source_sha256, artifact.sha256)
        self.assertEqual(model.elements[0].state, "UNKNOWN")
        self.assertEqual(constraints.unknown_element_ids, ("C01",))
        self.assertEqual(constraints.model_id, model.model_id)

    def test_real_runtime_keeps_fail_closed_status_after_contract_wiring(self):
        runtime = RealVisualRuntime(
            adapter=FakeAdapter(),
            locked_detector=FakeLockedDetector(),
            marker_detector=FakeMarkerDetector(),
            corroboration_gate=FakeCorroboration(),
        )
        result = runtime.run("h39-1", "fixture.png", {"change_type": "FURNITURE"})
        self.assertEqual(result["contracts"]["status"], "VALID")
        self.assertEqual(result["contracts"]["element_count"], 1)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["blockers"], ["LOCKED_ELEMENT_UNCERTAIN"])
        self.assertEqual(result["next_stage"], None)


if __name__ == "__main__":
    unittest.main()
