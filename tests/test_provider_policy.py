import unittest
from runtime.provider_policy import ProviderCapability, ProviderSelectionPolicy


class ProviderSelectionPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = ProviderSelectionPolicy()

    def test_selects_healthy_capable_provider_by_priority(self):
        providers = [
            ProviderCapability("expensive", frozenset({"vision"}), True, "premium", 20),
            ProviderCapability("cheap", frozenset({"vision"}), True, "low", 10),
        ]
        self.assertEqual(self.policy.select(providers, {"vision"}).provider_id, "cheap")

    def test_unhealthy_provider_is_excluded(self):
        providers = [
            ProviderCapability("bad", frozenset({"vision"}), False, "low", 1),
            ProviderCapability("good", frozenset({"vision"}), True, "standard", 10),
        ]
        self.assertEqual(self.policy.select(providers, {"vision"}).provider_id, "good")

    def test_missing_capability_is_explicit_failure(self):
        providers = [ProviderCapability("text", frozenset({"text"}))]
        with self.assertRaisesRegex(RuntimeError, "NO_CAPABLE_PROVIDER"):
            self.policy.select(providers, {"vision"})


if __name__ == "__main__":
    unittest.main()
