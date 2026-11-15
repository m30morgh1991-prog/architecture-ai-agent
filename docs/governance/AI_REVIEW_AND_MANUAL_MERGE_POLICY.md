# AI Technical Review and Owner-Controlled Merge Policy

**Status:** Adopted by repository owner on 2026-11-15; implementation recorded in this documentation PR.  
**Repository:** `m30morgh1991-prog/architecture-ai-agent`  
**Authority:** The repository owner retains ownership, administrative control, and the final merge decision.

## 1. Decisions

1. ChatGPT is delegated the project's complete **technical review** responsibility for pull requests (PRs): architecture and scope, changed code, tests, security and dependency implications, regression coverage, documentation, and exact-commit CI evidence.
2. ChatGPT is **not** delegated ownership, repository administration, or autonomous merge authority.
3. **Every PR merge requires a separate, explicit authorization from the repository owner.** No standing permission, prior approval, successful CI run, review comment, silence, or passage of time counts as merge authorization.
4. No PR may be merged by ChatGPT before that authorization. Auto-merge must remain disabled.
5. The owner may revoke or change this policy at any time.

## 2. What “complete technical review” means

For each PR, ChatGPT must:

- Fetch the live PR metadata and complete diff; identify the exact head SHA and base SHA.
- Review every changed file, relevant callers/contracts, tests, workflows, and documentation—not just the PR description.
- Check compatibility with the canonical architecture: `PlanModel`, `ConstraintMap`, and `ApprovedChangePlan` remain the source of truth.
- Preserve fail-closed behavior. `UNKNOWN`, `SOURCE_REQUIRED`, `NEEDS_REVIEW`, `ABSTAIN`, and `BLOCKED` must never be promoted to `PASS` without adequate evidence.
- Check security, data integrity, licensing, dependency/provider neutrality, and unintended scope expansion where relevant.
- Verify required CI checks and applicable regression workflows on the **same exact head SHA**. A result from an earlier SHA is stale evidence.
- Check merge conflicts, unresolved review threads, PR dependencies/stacking, and whether the target base is current.
- Record findings with file/line references, severity, evidence, and reproducible tests where possible.
- State limitations honestly. Windows/AutoCAD host testing remains `NOT_RUN` until actually performed on the user's compatible Windows host. No test may be represented as run when it was not.

## 3. GitHub review identity and review labels

The connected GitHub identity is the repository owner's account. GitHub does not allow a PR author to create a valid approval of their own PR.

Therefore:

- ChatGPT must not submit a misleading `APPROVE` review as if it were an independent human approval.
- For a technically acceptable PR, ChatGPT may submit a `COMMENT` review that clearly says **AI technical review: PASS (not a GitHub approval)** and records the reviewed SHA.
- For material defects, ChatGPT may submit `REQUEST_CHANGES` with concrete evidence and remediation.
- A `COMMENT` review is not an approval and must never be described as one.
- A separate human reviewer is not required by this adopted workflow unless the owner later chooses to add one.

## 4. Mandatory owner authorization gate

The review and merge are separate decisions.

After technical review, ChatGPT must stop and send the owner a concise decision report containing:

- PR number and URL;
- exact head SHA and base SHA reviewed;
- changed scope and architectural impact;
- findings and unresolved risks;
- exact-head CI status for every required check;
- regression and host-test status;
- dependency/stacking and mergeability status;
- recommendation: `READY_FOR_OWNER_DECISION`, `CHANGES_REQUIRED`, or `BLOCKED`.

Only an explicit owner instruction naming the PR or otherwise unambiguously authorizing that specific merge permits the merge action. Examples of valid authorization: “PR #123 را ادغام کن” or “اجازه ادغام همین PR را می‌دهم.”

The following are **not** authorization: “ادامه بده”، “بررسی کن”، “خوبه”، a previous authorization for another PR, or an authorization issued before the current head SHA changed.

Immediately before merging, ChatGPT must re-fetch the PR and verify that:
1. the PR is still open and targets the intended base;
2. the head SHA is unchanged from the reviewed SHA;
3. all required checks are completed/success on that exact SHA;
4. no new review findings or unresolved required threads appeared;
5. dependencies and mergeability remain valid.

If the head SHA changes, required checks become stale, a conflict appears, or new material findings arise, the prior merge authorization is no longer valid; ChatGPT must re-review and ask again.

After a permitted merge, ChatGPT must verify the merge commit SHA, resulting `main` head, and available post-merge checks. It must not claim post-merge Green when evidence is unavailable.

## 5. Live GitHub configuration observed on 2026-11-15

The active repository ruleset `Min` (ID `24680937`) applies to `~DEFAULT_BRANCH` (`main`) and was observed with:

- enforcement: `active`;
- required approving review count: `0`;
- stale reviews dismissed on push: `true`;
- required conversation resolution: `true`;
- required status checks in strict mode: `runtime-tests`, `test`, and `Mandatory Bug Hunt`;
- deletion and non-fast-forward protections enabled;
- no bypass actors; the connected owner identity reported `current_user_can_bypass=never`;
- allowed merge methods: `squash` and `rebase`.

The repository metadata reported `allow_auto_merge=false`.

**Important verification limitation:** the connected GitHub App integration cannot read the legacy branch-protection endpoint because it lacks the required repository `Administration: read` permission. Consequently, this inspection confirms the active repository ruleset but does **not** prove that no additional legacy branch-protection rule applies. Do not change or delete protections based on an assumption. The owner should restore/re-authorize the GitHub connection with the required read permission, or inspect Settings → Rules → Rulesets and Settings → Branches directly.

## 6. Guardrails

- Never bypass branch rules, fabricate an approval, use a second owner identity to simulate independent review, or weaken CI to force a merge.
- Never merge solely because CI is green.
- Never auto-merge or merge without the per-PR owner authorization described above.
- Never change repository settings, rulesets, collaborators, secrets, or branch protections without a separate explicit owner instruction.
- Preserve immutable Golden DWG fixtures and all existing architecture-core boundaries.
- Treat unavailable evidence as unknown, not as success.

## 7. Operational checklist

- [ ] Live PR metadata and exact SHA fetched.
- [ ] Full diff reviewed.
- [ ] Architecture, security, tests, dependencies, and regression reviewed.
- [ ] Required exact-head CI checks completed/success.
- [ ] Host-specific tests accurately marked, including `NOT_RUN` where applicable.
- [ ] Review findings recorded in GitHub without misrepresenting AI comments as approval.
- [ ] Owner receives the complete decision report.
- [ ] Explicit authorization for this exact PR/head received.
- [ ] Final pre-merge SHA and gates rechecked.
- [ ] Merge performed only after authorization.
- [ ] Merge commit, new `main` SHA, and post-merge evidence verified.

---

This policy records the repository owner's decision. It does not itself create a GitHub approval, alter branch protections, grant new connector permissions, or authorize merging this policy PR.
