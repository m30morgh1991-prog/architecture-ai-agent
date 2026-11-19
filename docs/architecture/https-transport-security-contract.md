# HTTPS Transport Security Contract — v1

## Status

Decision baseline for the Architecture AI Agent runtime and future Web App/PWA deployment. This document defines the required transport-security direction; it does not claim that HTTPS, authentication, or remote deployment is already implemented.

## Normative decisions

1. **HTTPS is mandatory for every non-loopback client-to-service connection in an operational deployment.** Browser/PWA traffic to the public application/API must use HTTPS with a valid, trusted certificate.
2. **Plain HTTP is not an operational transport.** Do not expose an HTTP execution endpoint on a public or LAN interface. An HTTP request may only be redirected to HTTPS at the edge when doing so cannot leak credentials or request bodies; otherwise reject it. Never accept credentials or execute mutations over plaintext HTTP.
3. **Local development remains loopback-only by default.** A local development server may bind to 127.0.0.1 and use HTTP only for local testing without real credentials, real user data, remote exposure, or production use. This exception does not authorize a LAN bind.
4. **TLS termination belongs at an explicit, configurable edge boundary** (for example, a reverse proxy or application server with TLS). The runtime behind that boundary must remain private and must not be directly exposed. The selected deployment must document which component terminates TLS and how the edge-to-runtime hop is protected.
5. **Do not trust forwarded headers by default.** The runtime may consume forwarded scheme/client-address headers only from explicitly configured trusted proxies. Strip or overwrite client-supplied forwarding headers at the trusted edge.
6. **Authentication and authorization are separate mandatory controls.** HTTPS does not authenticate a user or authorize an operation. Remote API access remains disabled until identity, session/token lifecycle, authorization, CSRF/origin controls appropriate to the auth mechanism, and audit behavior are implemented and reviewed.
7. **No secrets in URLs or logs.** Credentials must not be placed in query strings. Authorization headers, cookies, session tokens, private keys, and sensitive request bodies must be redacted from logs and error reports.
8. **TLS baseline:** support TLS 1.2 or newer, prefer TLS 1.3 where available, reject obsolete SSL/TLS protocols, validate certificate chains and hostnames, and provide an operational certificate renewal/expiry process. No self-signed or invalid certificate bypass in production.
9. **Browser policy:** use a strict origin allowlist for CORS where cross-origin access is needed. If cookie-based authentication is used, add CSRF protection and secure cookie attributes (Secure, HttpOnly, and an appropriate SameSite policy). Apply HSTS only to HTTPS hostnames after deployment is confirmed; do not blindly enable preload or includeSubDomains.
10. **Abuse and resource controls:** retain request-size and schema validation; add explicit request/read timeouts, rate limits, bounded concurrency, and safe error responses before enabling remote access.
11. **Performance is measured, not assumed.** HTTPS is a security requirement, not a claim of higher raw throughput. HTTP/2 or HTTP/3 may be enabled when supported by the deployment edge and validated with representative latency/throughput tests. Do not weaken TLS or validation to chase performance.
12. **Provider and hosting neutrality:** the contract must work with self-hosted/on-premises and cloud deployments. No mandatory CDN, cloud vendor, certificate vendor, reverse-proxy product, or AI provider is introduced.

## Canonical execution boundary

Transport security does not grant edit authority. Every mutating request must still pass through the server-owned canonical execution path:

source identity → PlanModel → ConstraintMap → impact/conflict analysis → explicit approval → controlled editing → post-edit diff → final validation → audit

Client-supplied geometry, element states, EDITABLE, approvals, or detached model snapshots must never grant authority. Missing or inconsistent canonical evidence remains UNKNOWN, SOURCE_REQUIRED, NEEDS_REVIEW, ABSTAIN, or BLOCKED; it must never become PASS.

Until the server-owned canonical snapshot registry and complete approval/impact chain are implemented and tested, the legacy execution route must remain fail-closed. HTTPS must not be used as a reason to reopen it.

## Deployment profiles

### Local development
- Bind to loopback only (127.0.0.1).
- No LAN/public bind by default.
- No production credentials or real user data over local plaintext HTTP.
- Remote access is not enabled by a configuration toggle alone; it requires the reviewed operational profile.

### Operational Web App/PWA
- Browser and API endpoints use HTTPS with valid certificates.
- Public edge terminates TLS and enforces host/origin policy.
- Runtime is private and reachable only through the configured trusted edge or protected internal channel.
- Authentication, authorization, CSRF/origin policy, rate limiting, bounded request handling, audit, and canonical execution gates are all enabled before remote mutation routes are opened.
- Certificate issuance, renewal, expiry alerting, and rotation are documented and tested.

### Internal service-to-service
- Use HTTPS/TLS when crossing a host, network, or trust boundary.
- A same-host private Unix socket or loopback channel may be used when justified and access-controlled; this is not a public API and must not bypass authentication/authorization or canonical execution.
- Use mutual TLS when service identity across a network boundary requires it; do not add mTLS complexity to a same-process/local socket without a threat-model reason.

## Required acceptance tests before remote access

- Plain HTTP cannot submit credentials or execute mutations; edge redirects or rejects safely.
- HTTPS rejects invalid, expired, hostname-mismatched, and untrusted certificates.
- TLS protocol floor and cipher policy match the deployment baseline.
- Runtime is not reachable directly from an untrusted interface when TLS terminates at an edge.
- Spoofed forwarding headers from untrusted clients cannot alter scheme, client identity, or authorization decisions.
- Unauthenticated and unauthorized requests are rejected before any execution record, approval, mutation, or PASS audit state is created.
- Cookie-based sessions have CSRF protection and secure cookie attributes; token-based sessions do not leak credentials in URLs or logs.
- CORS allows only explicitly configured origins and methods.
- Oversized, malformed, slow, repeated, and concurrent requests are bounded and fail safely.
- No client-supplied EDITABLE, geometry, approval, or snapshot can bypass canonical authority.
- All negative cases preserve fail-closed states and leave no false PASS or partial mutation.
- Certificate renewal/rotation is tested without disabling certificate validation.
- HTTP/2/HTTP/3 performance is benchmarked separately from correctness and security tests.

## Relationship to current runtime PRs

- PR #171 is interim P0 containment: the legacy execute route is intentionally 503 / BLOCKED until canonical authority exists. Keep this behavior.
- PRs #150 → #151 → #152 → #154 form a dependent runtime-hardening stack. Their request validation, audit, idempotency, serialization, and loopback changes must be integrated without reintroducing an open execution route.
- PR #154 explicitly leaves remote access disabled until authentication and TLS are designed and reviewed. This contract supplies the design baseline only; it does not itself enable remote access.
- The HTTPS contract must be implemented as a separate, reviewed deployment/transport change after the runtime stack is reconciled with PR #171.

## Out of scope

- Enabling remote execution now.
- Selecting a specific hosting provider, reverse proxy, certificate authority, identity provider, or AI provider.
- Claiming HTTPS increases application throughput by itself.
- Enabling CAD writes or changing PlanModel/ConstraintMap/BIM semantics.
- Treating TLS as a replacement for authorization, canonical evidence, approval, validation, or audit.

## Verification and governance

This document is a design contract. It has no runtime effect until implemented. Before operational deployment, add implementation-specific tests and exact-head CI evidence. Any deviation must be explicit, threat-modelled, reviewed, and documented; insecure fallback is not permitted.
