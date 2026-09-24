from .app import execute
from .contracts import Element, PlanModel, ChangeRequest

def run():
    plan = PlanModel("P-001", [
        Element("C01", "COLUMN", "LOCKED", {"x": 10, "y": 10}),
        Element("F01", "FURNITURE", "EDITABLE", {"x": 20, "y": 20}),
    ])
    passed = 0
    r1 = execute(plan, ChangeRequest("FURNITURE", ["F01"], "Move sofa"), {"F01": {"x": 30, "y": 20}})
    assert r1["status"] == "PASS"
    assert r1["post_edit_diff"]["locked_delta_ids"] == []
    passed += 1
    r2 = execute(plan, ChangeRequest("FURNITURE", ["C01"], "Move column"), {"C01": {"x": 99, "y": 99}})
    assert r2["status"] == "REJECT"
    assert "LOCKED_ELEMENT_CONFLICT" in r2["validation"]["failure_codes"]
    passed += 1
    print(f"Runtime slice tests: {passed}/2 PASS")

if __name__ == "__main__":
    run()
