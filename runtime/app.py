import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from copy import deepcopy
from .contracts import Element, PlanModel, ChangeRequest, ApprovedChangePlan, ValidationResult, PostEditDiff
from .execution_record import ExecutionRecordStore
from .final_validation import validate_post_edit
from .controlled_editing_contract import EditPermission, build_controlled_editing_decision
from .approved_change_plan_contract import build_approved_change_plan


execution_records = ExecutionRecordStore()


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

    permissions = [
        EditPermission(element_id=e.element_id, state=e.state)
        for e in plan.elements if e.element_id in request.target_ids
    ]
    controlled = build_controlled_editing_decision(permissions=permissions)
    if not controlled.executable:
        return {
            "status": "REJECT",
            "validation": {
                "status": "REJECT",
                "failure_codes": controlled.blocking_reasons(),
                "messages": ["Controlled editing gate blocked execution"],
            },
        }

    approval = build_approved_change_plan(
        change_request=request,
        available_element_ids=[e.element_id for e in plan.elements],
        editable_element_ids=[e.element_id for e in plan.elements if e.state == "EDITABLE"],
    )
    if approval.status != "APPROVED":
        return {
            "status": "REJECT",
            "validation": {
                "status": "REJECT",
                "failure_codes": [approval.reason],
                "messages": ["Approved change plan rejected"],
            },
        }

    approved = ApprovedChangePlan(request, list(approval.approved_target_ids), approval.status)
    before = {e.element_id: deepcopy(e.geometry) for e in plan.elements}
    after = deepcopy(before)

    if simulated_geometry:
        for element_id, geometry in simulated_geometry.items():
            if element_id in after:
                after[element_id] = deepcopy(geometry)

    changed = [i for i in before if before[i] != after[i]]
    locked_delta = [
        e.element_id for e in plan.elements
        if e.state == "LOCKED" and before[e.element_id] != after[e.element_id]
    ]
    unauthorized = [i for i in changed if i not in approved.approved_target_ids]
    diff = PostEditDiff(changed, unauthorized, locked_delta)

    final_validation = validate_post_edit(diff.__dict__)
    final = final_validation.status
    code = final_validation.failure_codes[0] if final_validation.failure_codes else None

    return {
        "status": final,
        "approved_change_plan": approved.__dict__,
        "post_edit_diff": diff.__dict__,
        "failure_code": code,
    }


class Handler(BaseHTTPRequestHandler):
    def _json(self, status, body):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        prefix = "/v1/executions/"
        if self.path.startswith(prefix):
            execution_id = self.path[len(prefix):]
            try:
                return self._json(200, execution_records.public(execution_id))
            except KeyError:
                return self._json(404, {"error": "EXECUTION_RECORD_NOT_FOUND"})
        self.send_error(404)

    def do_POST(self):
        if self.path != "/v1/execute":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length) or b"{}")

        execution_id = body["execution_id"]
        project_id = body["project_id"]
        input_version_id = body["input_version_id"]
        try:
            execution_records.create(execution_id, project_id, input_version_id)
        except ValueError:
            return self._json(409, {"error": "DUPLICATE_EXECUTION_ID"})

        execution_records.update(execution_id, "RUNNING")
        plan = PlanModel(body["plan_id"], [Element(**e) for e in body["elements"]])
        request = ChangeRequest(**body["request"])
        result = execute(plan, request, body.get("simulated_geometry"))

        if result["status"] == "PASS":
            execution_records.update(
                execution_id, "SUCCEEDED", f"result://{execution_id}"
            )
        else:
            execution_records.update(
                execution_id, "FAILED",
                error={"failure_code": result.get("failure_code"),
                       "validation": result.get("validation")}
            )

        return self._json(200, {
            "execution_id": execution_id,
            "job": execution_records.public(execution_id),
            "result": result,
        })


def main():
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("Architecture AI Agent runtime listening on :8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
