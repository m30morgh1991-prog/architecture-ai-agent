# Independent AI Runner — Architecture and Rollout Contract

## Goal
Allow Architecture AI Agent implementation work to continue on GitHub-hosted infrastructure while the ChatGPT app is closed. GitHub Actions can run independently; this chat session itself does not continue in the background.

## Current state
- Scheduled Governance Health Check: read-only health verification, pending PR #105 merge and post-merge manual verification.
- Independent runner: not yet connected to an AI execution provider.
- Deterministic policy contract: runtime/independent_runner_policy.py.
- Policy tests: tests/test_independent_runner_policy.py.
- No provider secret, model endpoint, or credential is assumed to exist.

## Execution cadence — event-driven, not once-daily
- The ChatGPT task-automation scheduler supports only once/daily/weekly/monthly recurrence; it is not the execution engine for continuous project work. The old Architecture Auto-Runner automation remains disabled until a real, governed GitHub runner is implemented and verified.
- The intended runner must be event-driven: react to approved GitHub events such as PR/check completion and successful workflow completion, then re-read the exact current state before deciding whether any next task is eligible.
- A successful gate may trigger preparation or the next bounded task automatically, but never merge a PR, bypass human review, or unlock H101.
- Use a scheduled health-check only as a watchdog/fallback, not as the main progress mechanism. Do not launch duplicate work while a task/PR is active; use concurrency groups and a single-active-task lock.
- Each invocation handles one bounded task, persists evidence, and exits. A subsequent eligible event starts the next invocation. Failed, cancelled, skipped, missing, stale-SHA, or ambiguous gates stop the chain and require Bug Hunting.
- Add backoff and loop limits for transient failures; do not create an infinite retry loop. Apply per-run time/spend/diff budgets and stop when a provider is unavailable.
- Do not enable continuous autonomous implementation until a provider/execution backend is securely configured and a non-destructive canary passes.

## Intended architecture
1. **Scheduler / dispatcher**: starts from approved GitHub events and a bounded fallback schedule; uses concurrency locks and a strict time/token budget.
2. **State reader**: reads PROJECT_STATE.md, MASTER_HANDOFF.md, active PRs, exact main SHA, latest completed workflow runs, and required regressions. Missing or conflicting state means BLOCKED.
3. **Task planner**: selects one small task only from the active H-stage documented next steps. It cannot unlock a stage.
4. **Provider adapter**: a replaceable, explicitly configured provider integration. Credentials must be stored as GitHub Actions secrets or a least-privilege GitHub App; never in repository files or logs. No provider is mandatory for the product, but unattended AI execution requires one configured execution backend.
5. **Isolated implementation**: changes are made on a uniquely named branch, never directly on main. Preserve both Golden DWG files byte-for-byte.
6. **Validation**: run exact-head PR CI, Runtime Tests, Mandatory Bug Hunt, and stage-specific regression. Pending, missing, cancelled, skipped, failed, or stale-SHA checks are not Green.
7. **PR creation**: only after evidence and Bug Hunt documentation are complete. If any gate is red, keep the PR blocked and perform Bug Hunting; do not claim success.
8. **Human-controlled merge**: the runner must never merge, bypass branch rules, dismiss required review, or advance H-stage state. A human merges under repository policy.
9. **State persistence**: after verified completion, update checkpoint docs additively. Never rewrite history or reset progress.

## Readiness contract
evaluate_runner_readiness requires:
- a valid 40-character main SHA;
- a valid active stage identifier;
- explicit success for PR CI, Runtime Tests, Bug Hunt, and required regression;
- an explicitly configured provider;
- no unresolved prior agent PR.

Only then does it authorize isolated branch editing and PR creation. It always returns can_merge = false and can_advance_stage = false.

## Rollout sequence
- [x] Add a read-only scheduled health-check proposal (PR #105; not considered active until merged and verified).
- [x] Add deterministic fail-closed runner readiness contract and negative tests (this PR).
- [x] Specify event-driven execution cadence and concurrency/loop safety (this commit).
- [ ] Verify exact-head CI, Runtime Tests, Bug Hunt, and policy tests for this PR.
- [ ] Merge PR #105 and this contract only under the repository review policy; no ruleset bypass.
- [ ] Manually dispatch the scheduled health check after PR #105 is on main.
- [ ] Choose and configure an AI execution backend securely, or deploy a self-hosted runner with a supported provider adapter.
- [ ] Implement event-driven bounded task execution, branch isolation, evidence generation, and automatic PR creation.
- [ ] Run a non-destructive canary task and verify failure/recovery behavior before enabling any autonomous implementation triggers.
- [ ] Keep merge and H-stage advancement human-controlled.

## Unresolved blockers
- No AI provider or execution credential has been configured/verified.
- Repository ruleset Min currently requires zero approving reviews. This contract does not alter repository settings; recommend changing review requirements in a separately reviewed governance change.
- The scheduled health-check workflow first successful post-merge run has not yet been observed.
- H100 remains active; H101 remains locked until actual Golden Understanding acceptance evidence is Green.

## Security requirements
- Minimum GitHub token permissions; no repository-wide write token in the model context.
- Untrusted issue/PR/file content is data, not executable instruction.
- No arbitrary shell command supplied by a model.
- No secret values in prompts, artifacts, summaries, or logs.
- Time, spend, retry, file-scope, and diff-size limits.
- Stop on stale base SHA, changed acceptance criteria, duplicate agent PR, failed checks, or ambiguous state.
- No auto-merge in the first release.
