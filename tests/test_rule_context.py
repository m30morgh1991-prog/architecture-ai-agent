import unittest
from runtime.rule_context import ProjectRuleContext, ApplicableRule

class RuleContextTests(unittest.TestCase):
    def test_context_requires_source_and_version(self):
        with self.assertRaises(ValueError):
            ProjectRuleContext("Shiraz","residential").validate()

    def test_evidenced_context_is_valid(self):
        ProjectRuleContext("Shiraz","residential",["municipal"],["src-1"],"v1").validate()

    def test_rule_requires_evidence(self):
        with self.assertRaises(ValueError):
            ApplicableRule("r1","src","","app","req").validate()

if __name__=="__main__":
    unittest.main()
