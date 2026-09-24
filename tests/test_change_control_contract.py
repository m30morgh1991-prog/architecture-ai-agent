import unittest

from runtime.change_control_contract import ChangeProposal, approve_proposal


class ChangeControlContractTests(unittest.TestCase):
    def test_draft_is_not_executable(self):
        p = ChangeProposal("p1", "e1", ["move F01"])
        self.assertFalse(p.executable)

    def test_blocked_proposal_cannot_be_approved(self):
        p = ChangeProposal("p2", "e1", ["move F01"], blocking_reasons=["UNKNOWN"])
        with self.assertRaises(ValueError):
            approve_proposal(p)

    def test_approval_is_explicit_and_traceable(self):
        p = ChangeProposal("p3", "e1", ["move F01"], impacted_elements=["F01"])
        approved = approve_proposal(p)
        self.assertTrue(approved.executable)
        self.assertEqual(approved.trace(), {"proposal_id": "p3", "execution_id": "e1"})

    def test_approved_with_blocker_is_invalid(self):
        p = ChangeProposal("p4", "e1", ["move F01"], blocking_reasons=["LOCKED"], state="APPROVED")
        with self.assertRaises(ValueError):
            p.validate()


if __name__ == "__main__":
    unittest.main()
