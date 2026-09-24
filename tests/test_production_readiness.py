import unittest
from runtime.production_readiness import ProductionReadiness

class ProductionReadinessTests(unittest.TestCase):
    def test_missing_real_visual_check_blocks_readiness(self):
        r=ProductionReadiness(["contracts","regression","real_visual"],["contracts","regression"],["REAL_VISUAL_RUNTIME_UNVERIFIED"])
        self.assertFalse(r.ready)

    def test_all_checks_without_blockers_are_ready(self):
        r=ProductionReadiness(["contracts","regression"],["contracts","regression"])
        self.assertTrue(r.ready)

    def test_undeclared_pass_is_rejected(self):
        with self.assertRaises(ValueError):
            ProductionReadiness(["contracts"],["contracts","extra"]).validate()

if __name__=="__main__":
    unittest.main()
