import json
import hashlib
import hmac
import os
import ssl
from dataclasses import asdict, is_dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import BoundedSemaphore
from copy import deepcopy
from .contracts import Element, PlanModel, ChangeRequest, ApprovedChangePlan, ValidationResult, PostEditDiff
from .execution_record import ExecutionRecordStore
from .final_validation import validate_post_edit
from .controlled_editing_contract import EDIT_PERMISSION_STATES, EditPermission, build_controlled_editing_decision
from .approved_change_plan_contract import build_approved_change_plan
from .audit import AuditTrail
from .idempotency import IdempotencyConflictError, IdempotencyGuard


MAX_REQUEST_BODY_BYTES = 16 * 1024 * 1024
MAX_CONCURRENT_REQUESTS = 8
REQUEST_TIMEOUT_SECONDS = 5
REQUEST_QUEUE_SIZE = 16


def _reject_duplicate_json_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("JSON_DUPLICATE_KEY")
        result[key] = value
    return result


def _reject_non_finite_json(value):
    raise ValueError("JSON_NON_FINITE_NUMBER")


def validate_execution_payload(body):
    if not isinstance(body, dict):
        return "REQUEST_SCHEMA_INVALID"

    required = {
        "execution_id", "project_id", "input_version_id",
        "plan_id", "elements", "request",
    }
    allowed = required | {"simulated_geometry"}
    if not required.issubset(body) or not set(body).issubset(allowed):
        return "REQUEST_SCHEMA_INVALID"

    for field in ("execution_id", "project_id", "input_version_id", "plan_id"):
        value = body.get(field)
        if not isinstance(value, str) or not value.strip():
            return "REQUEST_SCHEMA_INVALID"
        if len(value) > 256:
            return "REQUEST_SCHEMA_INVALID"

    elements = body.get("elements")
    if not isinstance(elements, list):
        return "REQUEST_SCHEMA_INVALID"

    seen_ids = set()
    allowed_element_fields = {"element_id", "element_type", "state", "geometry"}
    for element in elements:
        if not isinstance(element, dict):
            return "REQUEST_SCHEMA_INVALID"
        if not {"element_id", "element_type", "state"}.issubset(element):
            return "REQUEST_SCHEMA_INVALID"
        if not set(element).issubset(allowed_element_fields):
            return "REQUEST_SCHEMA_INVALID"
        element_id = element.get("element_id")
        element_type = element.get("element_type")
        state = element.get("state")
        if not isinstance(element_id, str) or not element_id.strip() or len(element_id) > 256:
            return "REQUEST_SCHEMA_INVALID"
        if element_id in seen_ids:
            return "REQUEST_SCHEMA_INVALID"
        seen_ids.add(element_id)
        if not isinstance(element_type, str) or not element_type.strip():
            return "REQUEST_SCHEMA_INVALID"
        if not isinstance(state, str) or state not in EDIT_PERMISSION_STATES:
            return "REQUEST_SCHEMA_INVALID"
        if "geometry" in element and not isinstance(element["geometry"], dict):
            return "REQUEST_SCHEMA_INVALID"

    request = body.get("request")
    if not isinstance(request, dict):
        return "REQUEST_SCHEMA_INVALID"
    if set(request) != {"change_type", "target_ids", "instruction"}:
        return "REQUEST_SCHEMA_INVALID"
    if not isinstance(request.get("change_type"), str) or not request["change_type"].strip():
        return "REQUEST_SCHEMA_INVALID"
    target_ids = request.get("target_ids")
    if (
        not isinstance(target_ids, list)
        or not target_ids
        or not all(isinstance(value, str) and value.strip() for value in target_ids)
        or len(set(target_ids)) != len(target_ids)
    ):
        return "REQUEST_SCHEMA_INVALID"
    if not isinstance(request.get("instruction"), str) or not request["instruction"].strip():
        return "REQUEST_SCHEMA_INVALID"

    simulated_geometry = body.get("simulated_geometry")
    if simulated_geometry is not None:
        if not isinstance(simulated_geometry, dict):
            return "REQUEST_SCHEMA_INVALID"
        if not all(
            isinstance(key, str) and key.strip() and isinstance(value, dict)
            for key, value in simulated_geometry.items()
        ):
            return "REQUEST_SCHEMA_INVALID"

    return None


execution_records = ExecutionRecordStore()
audit_trail = AuditTrail()
idempotency_guard = IdempotencyGuard()


def _json_default(value):
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    raise TypeError(
        f"Object of type {type(value).__name__} is not JSON serializable"
    )


def fingerprint_request_payload(payload) -> str:
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


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


def execute(plan: PlanModel, request: ChangeRequest, simulated_geometry=None, execution_id=None):
    audit_id = execution_id or f"local:{plan.plan_id}"
    audit_trail.record(audit_id, "EXECUTE", "STARTED")
    validation = validate_request(plan, request)
    if validation.status != "PASS":
        audit_trail.record(
            audit_id, "EXECUTE", "BLOCKED",
            {"failure_codes": list(validation.failure_codes)},
        )
        return {
            "status": validation.status,
            "validation": validation.__dict__,
            "audit_complete": False,
            "audit_ok": False,
            "runtime_ok": False,
        }

    permissions = [
        EditPermission(element_id=e.element_id, state=e.state)
        for e in plan.elements if e.element_id in request.target_ids
    ]
    controlled = build_controlled_editing_decision(permissions=permissions)
    if not controlled.executable:
        reasons = controlled.blocking_reasons()
        audit_trail.record(
            audit_id, "EXECUTE", "BLOCKED",
            {"failure_codes": reasons},
        )
        return {
            "status": "REJECT",
            "validation": {
                "status": "REJECT",
                "failure_codes": reasons,
                "messages": ["Controlled editing gate blocked execution"],
            },
            "audit_complete": False,
            "audit_ok": False,
            "runtime_ok": False,
        }

    approval = build_approved_change_plan(
        change_request=request,
        available_element_ids=[e.element_id for e in plan.elements],
        editable_element_ids=[e.element_id for e in plan.elements if e.state == "EDITABLE"],
    )
    if approval.status != "APPROVED":
        audit_trail.record(
            audit_id, "EXECUTE", "BLOCKED",
            {"failure_codes": [approval.reason]},
        )
        return {
            "status": "REJECT",
            "validation": {
                "status": "REJECT",
                "failure_codes": [approval.reason],
                "messages": ["Approved change plan rejected"],
            },
            "audit_complete": False,
            "audit_ok": False,
            "runtime_ok": False,
        }

    approved = ApprovedChangePlan(request, list(approval.approved_target_ids), approval.status)
    audit_trail.record(audit_id, "EXECUTE", "PASS")
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

    source_payload = json.dumps(
        [(e.element_id, e.element_type, e.state, e.geometry) for e in plan.elements],
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode()
    audit_trail.record(audit_id, "POST_EDIT_DIFF", "PASS" if not diff.locked_delta_ids and not diff.unauthorized_delta_ids else "BLOCKED")
    audit_complete = audit_trail.is_complete(audit_id, ("EXECUTE", "POST_EDIT_DIFF"))
    final_validation = validate_post_edit({
        **diff.__dict__,
        "source_sha256": hashlib.sha256(source_payload).hexdigest(),
        "model_id": plan.plan_id,
        "approved": approved.status == "APPROVED",
        "post_edit_status": "PASS" if not diff.locked_delta_ids and not diff.unauthorized_delta_ids else "BLOCKED",
        "post_edit_valid": not diff.locked_delta_ids and not diff.unauthorized_delta_ids,
        "before_after_status": "PASS",
        "before_after_valid": True,
        "audit_complete": audit_complete,
        "approved_target_ids": tuple(approved.approved_target_ids),
        "changed_ids": tuple(diff.changed_ids),
    })
    final = final_validation.status
    code = final_validation.failure_codes[0] if final_validation.failure_codes else None

    return {
        "status": final,
        "approved_change_plan": approved.__dict__,
        "post_edit_diff": diff.__dict__,
        "failure_code": code,
        "audit_complete": audit_complete,
        "audit_ok": audit_complete is True and final == "PASS",
        "runtime_ok": final == "PASS",
    }


def load_runtime_security_config(environ=None):
    """Require TLS material and a minimum-length bearer token before startup.

    Token entropy is an operator provisioning responsibility; this function
    enforces length only and does not claim to measure randomness.
    """
    env = os.environ if environ is None else environ
    cert_file = env.get("ARCH_AGENT_TLS_CERT_FILE")
    key_file = env.get("ARCH_AGENT_TLS_KEY_FILE")
    api_token = env.get("ARCH_AGENT_API_TOKEN")

    if not cert_file or not key_file:
        raise RuntimeError("TLS_CONFIGURATION_REQUIRED")
    if not api_token or len(api_token.encode("utf-8")) < 32:
        raise RuntimeError("AUTHENTICATION_CONFIGURATION_INVALID")
    return cert_file, key_file, api_token


def _has_valid_bearer_token(headers, expected_token):
    if not expected_token:
        return False
    values = headers.get_all("Authorization", [])
    if len(values) != 1:
        return False
    scheme, separator, supplied = values[0].partition(" ")
    return (
        scheme.lower() == "bearer"
        and bool(separator)
        and bool(supplied)
        and hmac.compare_digest(
            supplied.encode("utf-8"), expected_token.encode("utf-8")
        )
    )


class Handler(BaseHTTPRequestHandler):
    api_token = None

    def _json(self, status, body):
        payload = json.dumps(body, default=_json_default).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Strict-Transport-Security", "max-age=31536000")
        if status == 401:
            self.send_header("WWW-Authenticate", "Bearer")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        prefix = "/v1/executions/"
        if not self.path.startswith(prefix):
            return self.send_error(404)
        if not _has_valid_bearer_token(self.headers, self.api_token):
            return self._json(401, {"error": "AUTHENTICATION_REQUIRED"})
        execution_id = self.path[len(prefix):]
        try:
            return self._json(200, execution_records.public(execution_id))
        except KeyError:
            return self._json(404, {"error": "EXECUTION_RECORD_NOT_FOUND"})

    def do_POST(self):
        if self.path != "/v1/execute":
            return self.send_error(404)

        # No HTTP execution adapter exists. The server-owned canonical
        # PlanModel/ConstraintMap and approval pipeline are not wired yet.
        # Reject before reading any request bytes; there is no dormant handler.
        return self._json(503, {
            "error": "CANONICAL_EXECUTION_NOT_CONFIGURED",
            "status": "BLOCKED",
            "message": "Execution is unavailable until canonical server-owned evidence and approval are implemented.",
        })


class BoundedThreadingHTTPServer(ThreadingHTTPServer):
    """HTTPS request server with bounded workers and per-connection timeouts."""

    daemon_threads = True
    request_queue_size = REQUEST_QUEUE_SIZE

    def __init__(self, server_address, RequestHandlerClass):
        self._request_slots = BoundedSemaphore(MAX_CONCURRENT_REQUESTS)
        super().__init__(server_address, RequestHandlerClass)

    def get_request(self):
        request, client_address = super().get_request()
        request.settimeout(REQUEST_TIMEOUT_SECONDS)
        return request, client_address

    def process_request(self, request, client_address):
        if not self._request_slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except BaseException:
            self._request_slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._request_slots.release()


def build_tls_context(cert_file, key_file):
    """Create a server TLS context and load the explicitly configured identity."""
    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    tls_context.minimum_version = ssl.TLSVersion.TLSv1_2
    tls_context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    return tls_context


def main():
    cert_file, key_file, api_token = load_runtime_security_config()
    tls_context = build_tls_context(cert_file, key_file)

    # The listener is HTTPS-only and loopback-only. There is no plaintext
    # listener, redirect, or HTTP fallback.
    Handler.api_token = api_token
    server = BoundedThreadingHTTPServer(("127.0.0.1", 8443), Handler)
    try:
        server.socket = tls_context.wrap_socket(server.socket, server_side=True)
        print("Architecture AI Agent HTTPS runtime listening on 127.0.0.1:8443")
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
