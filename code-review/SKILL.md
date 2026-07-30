---
name: code-review
description: Perform the Validate SDD phase for exactly one pull request. Triggers when the user provides a PR number/URL to review.
disable-model-invocation: true
license: MIT
metadata:
  scope: project
  role: audit
  mutation: write
  upstream: https://github.com/NousResearch/hermes-agent/tree/main/skills/github/github-code-review
  upstream-author: Hermes Agent
  version: hermes-personal.1
---

# Code Review

Perform the SDD phase `Validate` for exactly one pull request. Verification means ensuring the implementation satisfies the linked issue, follows repository instructions, preserves outside behavior, has sufficient tests/evidence, and introduces no blocking defects.

## Workflow

1. Resolve the exact repository and PR. Record the current head SHA before reviewing.
2. Read the PR title, body, base/head branches, full commit list, complete diff, changed files in context, all issue comments, reviews, inline comments, review threads, and unresolved conversations.
3. Read every explicitly linked issue and all of its comments. Reconstruct the controlling `Specify`, `Clarify`, `Plan`, and `Tasks`.
4. Read root and applicable nested `AGENTS.md` files, relevant architecture, design, API, domain, security, test, and process documentation.
5. Inspect callers, tests, types, configuration, history, blame, and established patterns needed to evaluate the change.
6. Run relevant local validation when practical. Inspect failed remote checks to determine if they are introduced by the PR, pre-existing, flaky, environmental, or unrelated.
7. Apply the `grilling` investigation discipline before asking anything.
8. Comment only when there is a demonstrated defect, regression, security vulnerability, missing behavior, explicit rule violation, material ambiguity, or to respond to an existing review thread.
9. Every blocking finding must include affected file/line, concrete failure/risk, evidence, violated requirement/rule, and minimum required correction.
10. Recheck the head SHA before submitting the review. If changed materially, inspect new changes.
11. Submit exactly one formal final verdict: `APPROVE` or `REQUEST_CHANGES`. Do not use `COMMENT` as the final verdict.

## Approval criteria

Approve only when the PR satisfies the controlling issue, required acceptance criteria are met, no demonstrated blocking defect remains, repository rules are followed, validation is sufficient, and unresolved threads do not represent blocking work. Do not withhold approval for optional improvements.

## Request Changes criteria

Request changes when at least one demonstrated blocking issue remains. Do not request changes for personal preferences, optional refactors, stylistic differences handled by tooling, unverified future enhancements, or questions answerable from the repository.

## Merge and auto-merge safety

After submitting `APPROVE`, refetch the PR.
Merge immediately or enable auto-merge only when:
- the current head SHA is exactly the reviewed SHA
- the PR is not a draft
- all required checks passed, or auto-merge can safely wait for them
- no blocking review threads remain
- no required reviewer is missing
- GitHub reports the PR as mergeable/safely auto-mergeable
- the repository permits the chosen merge method and the account is authorized
- no administrator bypass is required
- the user did not request `--no-merge`

Never merge after `REQUEST_CHANGES`, approve one SHA and merge another, bypass checks, dismiss valid reviews merely to merge, change production code, commit fixes, or claim a formal approval when GitHub rejected it.

If GitHub prevents self-approval, report the verdict, state what separate reviewer action is required, and do not claim approval was submitted. When remote access is unavailable, review locally and report findings without claiming published comments/approvals.
