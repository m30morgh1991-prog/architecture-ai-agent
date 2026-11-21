# HTTPS Transport Security Contract — v2 (HTTPS-only)

## Mandatory policy
HTTPS is mandatory for every operational client-to-service connection, including loopback/local runtime clients. Plaintext HTTP is prohibited: no HTTP listener, redirect, fallback, development exception, or dormant HTTP execution handler. HTTP requests must be rejected at the transport boundary and must never carry credentials, request bodies, or mutations.

## Runtime boundary
- The current runtime is HTTPS-only, bound to `127.0.0.1:8443`.
- Startup requires explicit TLS certificate/private-key paths and a high-entropy bearer token (minimum 32 UTF-8 bytes); startup fails closed if missing or invalid.
- TLS 1.2 minimum; clients must validate certificate chains and host/IP SAN. Certificate verification must never be disabled.
- Remote/LAN access is disabled. A future remote deployment requires a separate threat-model/security review, explicit authorization, trusted TLS termination and protected edge-to-runtime channel, host/origin policy, authentication and authorization, CSRF controls appropriate to auth, rate limiting, request bounds/timeouts, safe secret handling/rotation, and independent verification.
- Authenticated execution-record GET is read-only. `POST /v1/execute` remains BLOCKED before body consumption until server-owned canonical evidence and the approval/impact pipeline are implemented and validated.

## Canonical authority
Transport authentication does not authorize architectural changes. Mutations must be based on source-bound server-owned PlanModel and ConstraintMap, impact/conflict analysis, explicit approval, controlled editing, post-edit diff, final validation, and audit. Client-supplied geometry, state labels (including EDITABLE), approval, or snapshots must not grant authority. UNKNOWN, SOURCE_REQUIRED, NEEDS_REVIEW, ABSTAIN, and BLOCKED are never PASS.

## TLS evidence boundary
CI's ephemeral certificate integration demonstrates the TLS code path, trusted test-chain/IP-SAN verification, rejection of an untrusted certificate, and authentication behavior. It does not verify the operational certificate, deployment hostname/chain, renewal/rotation, or production secret-management. Those remain NOT_RUN until real evidence is collected.

## Development and deployment
There is no plaintext development exception. Use a trusted local certificate or test-only TLS identity and HTTPS. Keep certificate/private key outside version control. Never place secrets in URLs or logs. No CORS origin is implicitly trusted. Do not trust forwarded headers unless a proxy is explicitly configured and strips client-supplied values. Remote access must not be enabled by a config switch alone.

## Required checks before remote access or execution
1. Operational certificate-chain and hostname validation from a real client; test expiry, mismatch, untrusted certificate, and rotation.
2. Verify private-key permissions, secret redaction, token rotation/lifecycle.
3. Implement and test scoped authorization, Origin/CORS allowlist and CSRF protection where applicable.
4. Implement rate limiting, request/read timeouts, size limits, and bounded concurrency.
5. Implement canonical source-bound PlanModel/ConstraintMap and the complete approval/impact/final-validation/audit chain.
6. Independently review all negative cases and preserve fail-closed behavior.
7. Windows/AutoCAD host and visual runtime tests remain NOT_RUN until actually performed.

## Governance
This contract is a security requirement, not runtime evidence. It cannot be marked accepted based on documentation or CI alone. Any proposed exception must be reviewed and explicitly authorized; no HTTP exception is permitted under the current decision.
