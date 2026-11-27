# Local HTTPS Security Review — Owner-Approved Alternative Evidence Path

## Decision record

- Decision date: 2026-11-28
- Decision owner: repository owner / project owner
- Scope: PR #180 (HTTPS-only local runtime) and its directly dependent PR #188 (bounded local HTTPS request handling).
- Approval: the project owner explicitly approved this limited alternative evidence path in ChatGPT on 2026-11-28.
- Status: authorized for evidence collection and review; not a merge approval and not a claim that security has passed.

## Why this exception exists

An independent human security reviewer is not currently available to the project owner. For this narrowly scoped local-only remediation, the owner accepts a documented alternative review process. This is a governance exception, not an assertion that an AI review is independent or equivalent to an independent human assessment.

## Required alternative evidence path

All of the following are required on the exact final PR head:

1. **Internal adversarial review:** a documented, skeptical review of the complete changed code and relevant call paths, including concrete file/line findings, abuse cases, and disposition. This review must be labelled internal adversarial review; it must never be represented as independent human approval.
2. **Automated security checks:** run applicable independent static/security and dependency checks available to the repository (for example CodeQL, Bandit, Semgrep, dependency vulnerability audit, and OpenSSF Scorecard). Record which tools actually ran, exact versions/results, and any unavailable or inapplicable checks. A tool not configured or not run is NOT_RUN, not PASS.
3. **Exact-head CI:** PR CI Gate, Runtime Tests, and Mandatory Bug Hunt must each complete successfully on the exact final head SHA. Any new commit invalidates prior exact-head evidence.
4. **Operational local-runtime tests:** demonstrate real loopback HTTPS behavior, trusted-certificate success, untrusted/hostname-mismatch rejection, missing/invalid/duplicate token rejection, absence of a plaintext HTTP listener/fallback, and POST /v1/execute blocked before body consumption.
5. **Resource-exhaustion tests for PR #188:** run live slow-client/trickle-client and concurrency-saturation tests against the actual TLS server. Demonstrate that a slow client cannot monopolize the service, the worker cap is enforced, deadlines close stalled connections, and normal authenticated read-only requests remain serviceable. Unit mocks alone do not satisfy this gate.
6. **Evidence and residual-risk record:** record commands, environment, outcomes, exact SHAs, failures, and unresolved risks. Missing evidence remains NOT_RUN or BLOCKED.
7. **Owner acceptance:** after reviewing the evidence and residual risks, the project owner explicitly confirms acceptance for this local-only slice before any merge action is considered.

## Strict scope boundaries

This alternative path applies only to PR #180 and PR #188 for the loopback-only runtime bound to 127.0.0.1:8443.

It does NOT authorize:
- LAN, remote, public, or production exposure;
- binding to 0.0.0.0 or any non-loopback interface;
- plaintext HTTP, HTTP redirect, fallback, or a development exception;
- CAD/DWG writes or execution;
- enabling POST /v1/execute (it remains BLOCKED before body consumption);
- claiming operational certificate lifecycle, production secret management, Windows/AutoCAD host, or visual runtime as verified;
- legal compliance PASS or H-stage advancement;
- waiving review requirements for PR #189, PRs #184–187, or any other change;
- changing branch protection/rulesets, bypassing required checks, or self-approving a PR.

## Merge and future review policy

This decision does not merge either PR. The project owner must separately authorize any merge after all required evidence is complete and the exact-head CI gates are green. The active repository ruleset remains in force.

Any move beyond loopback/local-only scope, any runtime execution capability, or any materially different security boundary requires a fresh threat model and a new review decision. Independent human review should still be sought when practical, especially before remote or production exposure.

## Honest status vocabulary

- INTERNAL_REVIEW_COMPLETE: internal adversarial review finished; not independent approval.
- TOOL_CHECK_COMPLETED: named tool actually ran and its result is recorded.
- LIVE_TEST_PASS: named operational test actually ran and passed.
- NOT_RUN: evidence has not been collected.
- BLOCKED: a required condition failed or remains unresolved.
- OWNER_ACCEPTED: the owner explicitly accepted the documented residual risk for this limited scope only.

No aggregate security PASS may be claimed while a required item is NOT_RUN or BLOCKED.
