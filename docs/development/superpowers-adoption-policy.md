# Superpowers Adoption Policy

## Status

Adopt selected Superpowers engineering practices as a **development-workflow aid** for Architecture AI Agent. This policy does not add Superpowers as a runtime dependency, change the product architecture, or authorize any security or release gate to be bypassed.

Superpowers is a coding-agent workflow/methodology, not a security scanner, SAST engine, dependency auditor, or proof of correctness. Its outputs are proposals and work products that remain subject to the repository's normal verification and review requirements.

## Practices to use

| Practice | When to use | Required evidence / boundary |
|---|---|---|
| Brainstorming | Only when requirements, trade-offs, or a new design are genuinely unresolved | Preserve established architecture decisions; do not reopen settled PlanModel, ConstraintMap, BIM, or MVP scope without an explicit reason and review |
| Writing Plans | Multi-step features, refactors, security fixes, or changes spanning multiple contracts | Plan must name scope, files/contracts, dependencies, risks, tests, and completion criteria before implementation |
| Test-Driven Development | Bug fixes and behavior changes where a regression can be expressed | Add a focused failing regression test first, demonstrate the pre-fix failure when feasible, implement the smallest fix, then rerun focused and required broader tests |
| Systematic Debugging | CI failures, runtime defects, regressions, and unexpected behavior | Establish reproduction and root cause before changing code; do not mask, weaken, skip, or relabel failing gates |
| Code Review | Every material change; mandatory before merging security-sensitive or architectural changes | Review diff against requirements, threat boundaries, tests, and unintended scope; author self-approval is not a substitute for independent review where required |
| Verification Before Completion | Every implementation, fix, and PR readiness/completion claim | Report exact commit/head and real command/CI evidence; distinguish PASS, FAIL, BLOCKED, NOT_RUN, and NEEDS_REVIEW |
| Git Worktrees / isolated branches | Independent parallel work when supported by the available environment | Keep work isolated; verify base/head and dependencies; never create conflicting concurrent edits to the same files |
| Parallel-agent delegation | Only when actual independent subagent execution is available | Assign bounded non-overlapping tasks; integrate only after reviewing each result and running common verification |

## Mandatory project guardrails

1. **GitHub + real CI remain the technical source of truth.** A local result, agent statement, tool-generated summary, or Superpowers checklist cannot replace a completed successful required GitHub Actions run on the exact PR head.
2. **Green Gate remains unchanged.** Queued, in-progress, missing, stale, cancelled, or inconclusive checks are not green. Required gates must complete successfully on the exact head SHA.
3. **Fail-closed remains mandatory.** UNKNOWN, SOURCE_REQUIRED, NEEDS_REVIEW, ABSTAIN, and BLOCKED must never be promoted to PASS without the defined evidence. No heuristic or AI confidence may override this rule.
4. **No bypass of approvals or branch protections.** Do not self-approve, dismiss required reviews, weaken rules, force-push around protections, merge, or enable auto-merge as a shortcut. Follow the repository's independent-review and approval requirements.
5. **Architecture contracts remain authoritative.** PlanModel, ConstraintMap, ApprovedChangePlan, BIM understanding, locked-element rules, and the established pipeline are not modified merely to accommodate a workflow tool.
6. **Golden regression assets are immutable.** Do not edit, regenerate, replace, or normalize the Golden DWG inputs as part of Superpowers adoption. Preserve their provenance and hashes.
7. **No scope expansion by default.** Do not add a runtime dependency, hosted service, external AI provider, telemetry, secrets, permissions, or workflow integration just to use Superpowers.
8. **Security tools remain separate.** Use dedicated SAST, dependency, secret, container, and dynamic security tools for their respective evidence. Superpowers may help organize and reason about those reviews but cannot certify security.
9. **No fabricated capabilities.** If the environment does not expose real subagents, worktrees, or a Superpowers runtime/skill, do not claim those capabilities were executed or installed.
10. **No code display in routine chat updates.** Report concise outcomes, changed paths, commit/PR links, and evidence; keep implementation details in repository artifacts unless the user asks for code.

## Standard operating sequence

1. Read current repository state: default branch/head, active PRs and dependencies, required checks, and current state/handoff documents.
2. Classify the task: requirements/design uncertainty, implementation, debugging, review, or verification.
3. For multi-step work, write a bounded plan. For bug fixes, write the regression test first where feasible.
4. Implement on an isolated branch with minimal scope; do not mix unrelated fixes.
5. Run focused tests and relevant static checks. Preserve negative tests and fail-closed behavior.
6. Open/update the PR with scope, test-first evidence, risk boundaries, and any dependency/stacking notes.
7. Complete the mandatory Bug Hunt evidence for that PR.
8. Review the complete diff and exact-head results. Wait for every required real CI gate to finish successfully.
9. Update durable project state/handoff documents when the change affects project status or decisions.
10. Merge only when all repository protections, independent review, and explicit project merge conditions are satisfied.

## Adoption evaluation

This is a documentation-only process adoption. It does not claim that the Superpowers package/plugin has been installed or executed inside GitHub Actions. Evaluate its value through subsequent work by tracking:
- regression tests added before fixes and demonstrated pre-fix failures;
- root-cause explanations for CI/runtime failures;
- reduced rework and smaller, reviewable PRs;
- complete exact-head verification evidence;
- no increase in bypasses, false PASS results, or changes outside approved scope.

If the practices add overhead without measurable quality or safety benefit, revise or remove the relevant practice through a reviewed PR. Do not weaken the mandatory project guardrails.
