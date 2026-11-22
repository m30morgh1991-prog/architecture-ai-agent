# Security Review Tooling (Pilot)

This folder contains offline, read-only security-review utilities for project-specific fail-closed invariants.

## Invariant linter

Run from the repository root:

```bash
python3 security_review/invariant_lint.py --repo . --json security_review/lint-results.json
```

It uses only Python's standard library. Exit code 1 means heuristic findings were found; exit code 2 means an internal error. Results are triage signals (`NEEDS_REVIEW`), not proof of vulnerabilities. A clean run is not a security pass.

Optional baseline:
- `--write-baseline PATH` writes a list of current finding keys.
- `--baseline PATH` suppresses matching keys and reports only new findings.

**Do not create or accept a baseline without reviewing each finding.** A baseline can hide unresolved risks. The linter is not yet wired into CI; workflow integration requires separate review, tests, baseline review, and verified pinned action SHAs.

The Stage-2 reproducer from the supplied package is not included yet because it depends on a helper module (`repro_findings.py`) absent from the package. It must be made self-contained and reconciled with current main before being added.

The supplied security-gates workflow and Dependabot files remain proposals and are intentionally not activated: they contain placeholders and unverified configuration.
