# Mandatory Bug Hunting Governance

## Purpose
Bug Hunting is a mandatory engineering gate for every change in Architecture AI Agent. It is a proactive investigation step, not merely a reaction to red CI.

## Required flow
Implement → Bug Hunt → CI → Verify → Regression → Sync Notion → Continue

For a confirmed defect:
Detect → Reproduce → Isolate → Fix → Regression Test → CI → Verify → Continue

## Mandatory rules
1. Hunt proactively before relying on CI.
2. Tests must exercise real behavior and assert meaningful outcomes; green tests must not be accepted as proof when the tested path is disconnected from production behavior.
3. Every confirmed product bug gets a permanent regression test.
4. Use diff debugging to identify the first bad change when a regression is suspected.
5. Golden DWGs `bagheri7.dwg` and `afifiiiii.end.edit3.dwg` are regression anchors when the affected path is DWG/plan related.
6. UNKNOWN, NEEDS_REVIEW, BLOCKED, missing evidence, or unresolved identity must never be promoted to PASS or LOCKED.
7. Check producer → contract → consumer → tests → runtime → audit for contract drift.
8. Exercise integration boundaries and negative/adversarial cases.
9. Flaky tests are not green; they require investigation and root-cause resolution.
10. Distinguish product defects from fixture, test, tooling, dependency, and CI/environment defects.
11. Every CI failure requires investigation; no fake green is permitted.
12. A required gate with missing/unknown evidence means MERGE = NO.

## Bug categories
Logic, Contract, Integration, Regression, Runtime, Data/DWG, BIM Semantic, Fail-Closed, State/Workflow, Identity/Provenance, Scope/Authorization, Validation, Visual/Detection, Dependency/API Compatibility, Test/Fixture, CI/Environment, Flaky/Non-deterministic.

## Severity
- P0: safety/source-of-truth violation — merge prohibited.
- P1: core logic/integration violation — merge prohibited.
- P2: runtime/data defect — merge prohibited until fixed.
- P3: test/tooling defect — must be fixed; no fake green.
- P4: documentation/non-critical issue — may proceed independently but cannot falsify an H/PR green state.

## Required Bug Ledger fields
Bug ID, detected at, H/PR, category, severity, reproduction, root cause, affected components, fix, regression test, CI run, verification, status.

## Merge gate
Bug Hunt → PR CI → Runtime Tests → Regression → Review → Merge → Main CI → Verify

The repository gate implemented by `runtime/bug_hunting_gate.py` requires a PR-specific evidence record under `docs/bug-hunting/PR-<number>.md`. The record must contain the mandatory sections and an explicit regression statement.

## Stop-the-line
P0/P1 and confirmed regressions stop dependent work. Independent lanes may continue when they do not depend on the affected path.

## Final law
No H, PR, merge, or release is valid solely because of local green or a prior green run. Every change passes Bug Hunting before and after CI. Every real failure gets a root cause. Every fixed bug gets a permanent regression test. Fail-closed violations block merge.
