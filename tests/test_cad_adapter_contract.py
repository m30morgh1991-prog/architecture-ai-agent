import unittest

from runtime.cad_adapter_contract import CADExecutionRequest, CADExecutionResult, CADInspectionEvidence

class CADAdapterContractTests(unittest.TestCase):
    SHA = "a" * 64

    def test_inspection_must_bind_to_source(self):
        evidence = CADInspectionEvidence("autocad-mcp", self.SHA, {}, "READY")
        evidence.validate(self.SHA)
        with self.assertRaisesRegex(ValueError, "CAD_SOURCE_SHA_MISMATCH"):
            evidence.validate("b" * 64)

    def test_execution_requires_approved_plan_and_fence(self):
        with self.assertRaisesRegex(ValueError, "APPROVED_CHANGE_PLAN_REQUIRED"):
            CADExecutionRequest(
                self.SHA, "doc-1", "7", "idem-1", "", ({"op": "move", "id": "wall-1"},)
            ).validate()

    def test_applied_execution_requires_postcondition_and_exact_readback(self):
        request = CADExecutionRequest(
            self.SHA, "doc-1", "7", "idem-1", "plan-1",
            ({"op": "move", "id": "wall-1"},)
        )
        request.validate()
        result = CADExecutionResult(
            "autocad-mcp", "APPLIED", self.SHA, "doc-1", "7", None,
            request.operations, request.operations
        )
        with self.assertRaisesRegex(ValueError, "CAD_POSTCONDITION_REVISION_MISSING"):
            result.validate(request)

    def test_actual_diff_cannot_be_hidden(self):
        request = CADExecutionRequest(
            self.SHA, "doc-1", "7", "idem-1", "plan-1",
            ({"op": "move", "id": "wall-1"},)
        )
        result = CADExecutionResult(
            "autocad-mcp", "APPLIED", self.SHA, "doc-1", "7", "8",
            request.operations, ()
        )
        with self.assertRaisesRegex(ValueError, "CAD_REQUEST_ACTUAL_DIFF"):
            result.validate(request)

if __name__ == "__main__":
    unittest.main()
