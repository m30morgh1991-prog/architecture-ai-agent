# Pre-phase H100 coherence and governance audit — 2026-10-09

## Scope and verified repository point

- Repository: `m30morgh1991-prog/architecture-ai-agent`.
- Main at audit start: `2842cf2523fb9140b72f03a2311addf06c468af2` (PR #93 merge).
- Mainline workflow query and combined status returned no exposed checks for that merge commit. Therefore post-merge Green is not claimed.
- Preserved Golden DWGs must not be modified: `test-assets/golden-projects/bagheri7.dwg` and `test-assets/golden-projects/afifiiiii.end.edit3.dwg`.

## Findings and fixes in this audit branch

1. **Stale state documentation:** `PROJECT_STATE.md` and `MASTER_HANDOFF.md` still described PR #75 as the current point; the checklist still described PR #93 as in progress even though PR #93 was merged. Synced all three to the live main checkpoint and current open PR/gate states.
2. **Stacked-PR CI trigger mismatch:** PR CI Gate and Runtime Tests only ran for pull requests targeting `main`, while Bug Hunt already ran on all pull requests. Removed the target-branch filter from both PR triggers so stacked/dependency PRs can be tested without retargeting them merely to trigger CI. Push triggers remain main-only.
3. **Ruleset is not enforcing protections:** GET of `/repos/m30morgh1991-prog/architecture-ai-agent/rulesets/24680937` showed ruleset `Min` has `enforcement=disabled`, empty include/exclude ref targets, and `required_status_checks=[]`. Its configured review/check rules are therefore not active on main. The available GitHub connection permits reading but not writing rulesets; this is an explicit administrative blocker, not something this PR can claim to have fixed.
4. **Reviews absent:** PR #96, #97, #98, and #99 each have no submitted reviews recorded. Successful CI does not satisfy review approval.
5. **Scale/unit evidence boundary:** PR #98 is the prerequisite to PR #99. PR #99 must not merge first; after #98 merges, rebase/retarget #99 to updated main and rerun all gates on the final exact head.

## Exact-head evidence observed

| PR | Exact head | PR CI | Runtime | Bug Hunt | Review |
|---|---|---:|---:|---:|---|
| #93 (merged) | `26f1a0c9c0f47b3d8fa5f419f4a659c57b6e9d5e` | #289 success | #576 success | #246 success | Merged; post-merge Green not claimed |
| #96 | `1df773883036525e20c972815ac3a3410c00d7da` | #300 success | #587 success | #257 success | Missing |
| #97 | `25d57ef7e6b18f49228f9194b3991a92387cd04b` | #305 success | #592 success | #262 success | Missing |
| #98 | `7092f3cba6fc5b3f8747bbe78ff2e2976111ae1b` | #303 success | #590 success | #260 success | Missing; prerequisite |
| #99 | `c472396d5a3a984c8c134bb7f55d068326c4fc14` | #313 success | #600 success | #272 success | Missing; dependent on #98 |

## Required ruleset configuration before treating governance as enforced

1. Edit repository Settings → Rules → Rulesets → `Min`.
2. Set enforcement to **Active** and target `refs/heads/main` (or the UI's equivalent exact default-branch target).
3. Require pull requests before merging; require one approval from an independent authorized reviewer; dismiss stale approvals; require approval of the latest reviewable push; require conversation resolution.
4. Block branch deletion and force pushes. Keep bypass actors empty unless a deliberate documented exception is approved.
5. Require the three exact check runs from recent PR events: PR CI Gate, Runtime Tests, and Bug Hunt Gate. Confirm their exact job/check names in GitHub's rule editor before saving; do not guess names.
6. After saving, read the ruleset again and verify enforcement=active, main is targeted, and required checks are populated. Then verify an ordinary PR cannot merge without review and checks.

The current connection's read-only GitHub fetch endpoint cannot mutate ruleset settings; the above activation step must be completed by an authorized repository administrator in GitHub Settings.

## Fail-closed decisions retained

- H100 remains active; H101 remains locked.
- Recognized DWG unit metadata alone stays NEEDS_REVIEW; absent/unsupported/malformed evidence stays UNKNOWN; dimensions remain UNKNOWN without verified dimension-to-geometry association.
- Section marker presence does not prove direction, cut-plane endpoints, or view geometry; those remain UNKNOWN absent independent evidence.
- No Logical/Static PASS is promoted to Runtime or Visual PASS.
- No Golden DWG assets were changed.

## Gate to resume phases

Do not start H101 until the ruleset blocker is addressed, reviews/dependencies are handled, final exact-head checks pass after rebasing as needed, and H100 semantic Golden ground truth plus real-world transformed/defective fixtures satisfy UG-10.
