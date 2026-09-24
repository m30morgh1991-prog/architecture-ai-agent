import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from copy import deepcopy
from .contracts import Element, PlanModel, ChangeRequest, ApprovedChangePlan, ValidationResult, PostEditDiff


def validate_request(plan: PlanModel, request: ChangeRequest) -> ValidationResult:
    by_id = {e.element_id: e for e in plan.elements}
    missing = [i for i in request.target_ids if i not in by_id]
    if missing:
        return ValidationResult("REJECT", ["TARGET_NOT_FOUND"], [f"Unknown targets: {missing}"])
    locked = [i for i in request.target_ids if by_id[i].state == "LOCKED"]
    if locked:
        return ValidationResult("REJECT", ["LOCKED_ELEMENT_CONFLICT"], [f"Locked targets: {locked}"])
    if request.change_type != "FURNITURE":
        return ValidationResult("REJECT", ["UNSUPPORTED_CHANGE_TYPE"], ["First runtime slice accepts FURNITURE only"])
    return ValidationResult("PASS")


def execute(plan: PlanModel, request: ChangeRequest, simulated_geometry=None):
    validation = validate_request(plan, request)
    if validation.status != "PASS":
        return {"status": validation.status, "validation": validation.__dict__}
    approved = ApprovedChangePlan(request, list(request.target_ids), "APPROVED")
    before = {e.element_id: deepcopy(e.geometry) for e in plan.elements}
    after = deepcopy(before)
    if simulated_geometry:
        for element_id, geometry in simulated_geometry.items():
            if element_id in approved.approved_target_ids:
                after[element_id] = geometry
    changed = [i for i in before if before[i] != after[i]]
    locked_delta = [e.element_id for e in plan.elements if e.state == "LOCKED" and before[e.element_id] != after[e.element_id]]
    unauthorized = [i for i in changed if i not in approved.approved_target_ids]
    diff = PostEditDiff(changed, unauthorized, locked_delta)
    final = "PASS" if not locked_delta and not unauthorized else "REJECT"
    if locked_delta:
        code = "POST_EDIT_REJECTED"
    elif unauthorized:
        code = "POST_EDIT_UNAUTHORIZED_DELTA"
    else:
        code = None
    return {"status": final, "approved_change_plan": approved.__dict__, "post_edit_diff": diff.__dict__, "failure_code": code}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/v1/execute":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length) or b"{}")
        plan = PlanModel(body["plan_id"], [Element(**e) for e in body["elements"]])
        request = ChangeRequest(**body["request"])
        result = execute(plan, request, body.get("simulated_geometry"))
        payload = json.dumps(result).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main():
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("Architecture AI Agent runtime listening on :8000")
    server.serve_forever()

if __name__ == "__main__":
    main()
