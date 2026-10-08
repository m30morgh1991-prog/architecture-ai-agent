import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class MainlineH100CheckpointTests(unittest.TestCase):
    def test_golden_manifest_is_source_bound(self):
        manifest = json.loads((ROOT / "test-assets/golden-understanding/golden_manifest.json").read_text())
        for case in manifest["cases"]:
            self.assertRegex(case["source_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(len(case["expected_elements"]), 4)
            self.assertEqual(case["expected_status"], "UNKNOWN")

    def test_state_does_not_claim_post_merge_green(self):
        state = (ROOT / "PROJECT_STATE.md").read_text()
        self.assertIn("post-merge Green is not claimed", state)
        self.assertIn("H100 — Golden Understanding Gate", state)

    def test_live_cad_write_is_not_enabled(self):
        adapter_doc = (ROOT / "docs/integrations/AUTOCAD_MCP_ADAPTER.md").read_text()
        self.assertIn("read-only", adapter_doc.lower())
        self.assertIn("ApprovedChangePlan", adapter_doc)
        self.assertIn("fail-closed", adapter_doc.lower())

if __name__ == "__main__":
    unittest.main()
