# HTTPS runtime configuration

## Purpose and current boundary

The local runtime now starts only when explicit TLS certificate/key files and a strong API bearer token are configured. It wraps its listening socket with a TLS server context and binds only to `127.0.0.1:8443`. There is no plaintext HTTP listener, redirect, or HTTP fallback.

The legacy `POST /v1/execute` route remains fail-closed and returns `503 / BLOCKED` before reading the request body. This TLS change does not create an execution path, canonical model registry, CAD write capability, or remote-access permission. The authenticated `GET /v1/executions/{id}` route is read-only.

## Required environment

Set these variables in the runtime process environment or a protected secret manager:

- `ARCH_AGENT_TLS_CERT_FILE`: path to the server certificate or full certificate chain.
- `ARCH_AGENT_TLS_KEY_FILE`: path to the matching private key. Keep the key outside the repository and restrict filesystem permissions.
- `ARCH_AGENT_API_TOKEN`: a high-entropy secret of at least 32 UTF-8 bytes. Never commit it, place it in a URL, or log it.

Startup fails closed if either TLS file path is missing, the token is missing/too short, or the certificate/key cannot be loaded. There is no automatic self-signed certificate generation and no fallback to plaintext.

The listener address and port are fixed to loopback and 8443 in this slice. Remote/LAN binding is intentionally unavailable.

## Client requirements

Clients must validate the server certificate chain and hostname/IP SAN using the platform trust store or an explicitly configured trusted CA. Do not disable certificate verification, use insecure TLS modes, or accept hostname mismatches. For a locally issued certificate, install/trust the issuing CA on the client and include the loopback IP or hostname used by the client in the certificate SAN.

Send the bearer token only in the `Authorization: Bearer` header over the verified TLS connection. Do not use cookies or query-string tokens. The runtime rejects missing, duplicate, or invalid Authorization headers for execution-record reads. No CORS policy is enabled; browser cross-origin access is not granted.

## Verification boundary

Automated tests cover required configuration, fail-closed startup, TLS context creation, TLS 1.2 minimum, socket wrapping, loopback-only binding, bearer authentication, duplicate-header rejection, and the blocked execution route.

These tests do not prove a live TLS handshake, client-side certificate-chain/hostname verification, certificate renewal, or production deployment. Those remain `NOT_RUN` until exercised with a trusted certificate and a real client that verifies it. Do not mark operational HTTPS as fully accepted from unit tests alone.

## Next security gates

Before any remote deployment or execution capability is considered:

1. Verify a live TLS handshake from a real client with certificate-chain and hostname validation enabled.
2. Verify certificate rotation/expiry handling and private-key access controls.
3. Complete authorization, origin/CSRF policy where relevant, rate limiting, and operational secret rotation.
4. Implement the server-owned, source-hash-bound canonical PlanModel/ConstraintMap and the full impact/approval/final-validation chain.
5. Keep remote access disabled and execution blocked until the applicable gates are independently reviewed and evidenced.
