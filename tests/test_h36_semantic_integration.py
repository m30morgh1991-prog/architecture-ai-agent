import unittest
from runtime.real_visual_runtime import RealVisualRuntime

class H36SemanticIntegrationTests(unittest.TestCase):
    def test_runtime_exposes_corroboration_and_fail_closes(self):
        runtime = RealVisualRuntime()
        result = runtime.run("H36-01", "tests/fixtures/real_test_03_original.pdf", {"type":"FURNITURE_ONLY"})
        self.assertIn("semantic_corroboration", result)
        self.assertIn(result["semantic_corroboration"]["status"], {"UNKNOWN","BLOCKED","ACCESSIBLE"})
        if result["semantic_corroboration"]["status"] != "ACCESSIBLE":
            self.assertEqual(result["status"], "BLOCKED")

if __name__ == "__main__":
    unittest.main()
