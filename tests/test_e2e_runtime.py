import unittest
from runtime.ai_router import AIRouter
from runtime.execution_orchestrator import ExecutionOrchestrator
from runtime.provider_policy import ProviderCapability
from runtime.visual_adapter import VisualAdapterBoundary
from runtime.visual_orchestration import VisualExecutionBoundary
from runtime.e2e_runtime import E2ERuntimeBoundary

class Provider:
    provider_id="p"
    def available(self): return True
    def interpret(self, request): return {"evidence": True}

class Visual:
    adapter_id="v"
    def detect(self, document): return {"elements":["C01"]}
    def render_candidate(self, approved_change_plan, document):
        return {"candidate": True}

class E2ETests(unittest.TestCase):
    def make(self):
        router=AIRouter([Provider()])
        orch=ExecutionOrchestrator(router,[ProviderCapability("p",frozenset({"interpret"}))])
        visual=VisualExecutionBoundary(orch,VisualAdapterBoundary(Visual()))
        def execute(plan,request):
            return {"status":"PASS","plan":plan,"request":request}
        return E2ERuntimeBoundary(visual,execute)
    def test_full_boundary_requires_approval_and_executes(self):
        r=self.make().run("e2e-1",{"change":"move furniture"},"plan.png",
                           {"status":"APPROVED"},{"elements":["C01","F01"]})
        self.assertTrue(r.visual.candidate["candidate"])
        self.assertEqual(r.execution["status"],"PASS")
    def test_unapproved_plan_is_blocked_before_execute(self):
        called=[]
        router=AIRouter([Provider()])
        orch=ExecutionOrchestrator(router,[ProviderCapability("p",frozenset({"interpret"}))])
        visual=VisualExecutionBoundary(orch,VisualAdapterBoundary(Visual()))
        def execute(plan,request):
            called.append(True); return {"status":"PASS"}
        with self.assertRaisesRegex(ValueError,"APPROVED_CHANGE_PLAN_REQUIRED"):
            E2ERuntimeBoundary(visual,execute).run("e2e-2",{}, "plan.png", {"status":"PROPOSED"}, {})
        self.assertEqual(called,[])
if __name__=="__main__": unittest.main()
