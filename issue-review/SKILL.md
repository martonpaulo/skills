---
name: issue-review
description: Perform the Validate SDD phase for exactly one pull request. Triggers when the user provides a PR number/URL to review.
disable-model-invocation: true
license: MIT
metadata:
  scope: project
  role: audit
  mutation: write
  upstream: https://github.com/NousResearch/hermes-agent
  upstream-author: Hermes Agent
  upstream-path: skills/github/github-code-review
  upstream-revision: cc4cab2f592e60a197e796506de9168f74baf3ea
  upstream-checked: 2026-08-03
  version: hermes-personal.1
---

# Code Review

Perform the SDD phase `Validate` for exactly one pull request. Verification means ensuring the implementation satisfies the linked issue, follows repository instructions, preserves outside behavior, has sufficient tests/evidence, and introduces no blocking defects.

## Sources of truth

When these disagree, the higher one wins:

1. the direct review request;
2. the linked issue, its approved specification, and its acceptance criteria;
3. the most specific applicable repository instructions;
4. the root `AGENTS.md`;
5. relevant ADRs and architecture, design, domain, API, security, testing, and process documentation;
6. existing code behavior, tests, history, and established patterns.

Expose contradictions between them. Do not silently resolve a conflict by picking whichever source makes the PR look correct, and do not treat older documentation as authoritative over an accepted issue that deliberately replaces it.

Distinguish verified facts, reasonable inferences, and unknowns in everything published. Never claim that evidence was inspected, a command ran, or a check passed when it did not.

## Workflow

1. Resolve the exact repository and PR. Record the current head SHA before reviewing.
2. Read the PR title, body, base/head branches, full commit list, complete diff, changed files in context, all issue comments, reviews, inline comments, review threads, and unresolved conversations.
3. Read every explicitly linked issue and all of its comments. Reconstruct the controlling `Specify`, `Clarify`, `Plan`, and `Tasks`.
4. Read root and applicable nested `AGENTS.md` files, relevant architecture, design, API, domain, security, test, and process documentation.
5. Inspect callers, tests, types, configuration, history, blame, and established patterns needed to evaluate the change.
6. Run relevant local validation when practical. Inspect failed remote checks to determine if they are introduced by the PR, pre-existing, flaky, environmental, or unrelated.
7. Apply the `grilling` investigation discipline before asking anything.
8. Comment only when there is a demonstrated defect, regression, security vulnerability, missing behavior, explicit rule violation, material ambiguity, or to respond to an existing review thread.
9. Every blocking finding must include affected file/line, concrete failure/risk, evidence, violated requirement/rule, and minimum required correction. Anchor it to the exact line in the diff, not to a prose description of where it is.
10. Recheck the head SHA before submitting the review. If changed materially, inspect new changes.
11. Submit exactly one formal final verdict: `APPROVE` or `REQUEST_CHANGES`. Do not use `COMMENT` as the final verdict.

## GitHub is the only platform

This skill targets GitHub and nothing else. Do not add support for, degrade towards, or produce output shaped for GitLab, Bitbucket, Gitea, or any other forge. If the repository is not on GitHub, say so and stop.

## Publishing the review through the API

Findings are published as one formal review through the official GitHub API, pinned to the reviewed SHA, carrying its inline comments and its verdict in the same request. Not as loose issue comments, and not as a chat summary that claims to be a review.

Read [github-api.md](references/github-api.md) for the exact commands: reading the PR and its unresolved review threads, posting the review with anchored inline comments, replying inside an existing thread, and reading the verdict back.

Two rules bind every comment:

- **Anchor it.** A finding about a line is attached to that line through the API. Writing "line 84 should change" in a summary body, when the API could have attached that text to line 84, is a defect in the review.
- **Earn it.** Each comment states the failure, the evidence, the violated rule or requirement, and the minimum correction. Silence on a hunk means it was read and found sound.

When a finding concerns code the PR did not touch, the API will reject the anchor. Put it in the review body naming the file and line, rather than forcing an anchor.

### Do not publish

- a personal preference, an optional refactor, or unrelated cleanup;
- a speculative future problem with no concrete failure path;
- a stylistic difference, a formatting nit, or anything the project's tooling already enforces;
- a dependency upgrade or a missing feature the PR was never asked to deliver;
- praise, a generic summary, a restatement of what the code or the PR does;
- a question the repository, the linked issue, or the PR already answers.

Never invent a finding to produce output. A review that meets no threshold publishes no defect comment, and approving with an empty body is the correct result.

### Say what fails

A finding a reader cannot act on is not a finding. These are not review comments:

> This may cause problems. Consider improving this. This could be cleaner. You might want to add tests.

Each names a feeling, not a failure. State what breaks, under which input or condition, and why that matters. If you cannot name the condition, you have a suspicion, not a finding: verify it or drop it.

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

If GitHub prevents self-approval, report the verdict, state what separate reviewer action is required, and do not claim approval was submitted. When remote access is unavailable, review locally and report findings without claiming published comments/approvals. Read the submitted review back before reporting success; a verdict is published only when the API says it is.

For a diff that is not yet a pull request, use `review-changes` instead. This skill needs a PR to review and a place to publish the verdict.
