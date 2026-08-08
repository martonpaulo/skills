---
name: issue-review
description: Perform the Validate SDD phase for one open GitHub pull request against every issue it closes. Invoke `/issue-review` with an issue number or direct issue URL to resolve its PR, a direct PR URL, or `pr <pull-request-number-or-url>` for an explicit PR target. A bare number always means an issue; the `pr` prefix is required only for a PR number. Not for loose diffs, partial review, or reviewing several pull requests at once.
argument-hint: "<issue-number-or-url> | pr <pr-number-or-url> | <pr-url>"
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

Perform the SDD phase `Validate` for exactly one pull request. Verification means ensuring the
implementation satisfies every issue the PR closes, follows repository instructions, preserves
outside behavior, has sufficient tests and evidence, and introduces no blocking defects.

## Invocation

Accept these issue and pull request forms:

```text
/issue-review 123
/issue-review https://github.com/acme/app/issues/123
/issue-review pr 456
/issue-review https://github.com/acme/app/pull/456
/issue-review pr https://github.com/acme/app/pull/456
```

- Treat `123` as issue `#123`, then resolve the unique open PR that closes it.
- Treat an `/issues/123` URL as that exact issue, including its repository.
- Treat `pr 456`, a `/pull/456` URL, or `pr <pull-url>` as that exact pull request.
- Never probe both namespaces or reinterpret a bare number as a PR when issue resolution fails.
- Reject an issue URL after `pr`, malformed URLs, and URLs whose path is neither `/issues/N` nor `/pull/N`.

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

1. Parse the invocation before any lookup. Resolve a bare number or `/issues/` URL as an issue and find its unique open closing PR. Resolve `pr <number-or-pull-url>` or a direct `/pull/` URL as that exact PR. Treat a URL's repository as authoritative. Stop on a malformed, missing, closed, or ambiguous target per [github-api.md](references/github-api.md). Record the current head SHA before reviewing.
2. Read the PR title, body, base/head branches, full commit list, complete diff, changed files in context, all issue comments, reviews, inline comments, review threads, and unresolved conversations. Verify that the body starts with one `Closes #N` line per closing issue and that the PR targets the default branch.
3. Read every issue in `closingIssuesReferences` and all of its comments. Reconstruct each controlling `Specify`, `Clarify`, `Plan`, and `Tasks`. An empty closing set is a blocking contract defect. For issue-form invocation, the supplied issue missing from that set is also blocking.
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

The review body, every inline comment, every thread reply, and every fallback comment ends with the agent signature line defined in [`github-conventions`](../github-conventions/SKILL.md), for example `🤖 AI-generated by ❋ Claude Sonnet 5 (High)`.

A large diff or patch worth keeping on disk, and the review JSON itself, go in a uniquely named system temporary directory, never in the reviewed repository, and are deleted before this run reports completion, including when the review was refused or abandoned, per [`github-conventions`](../github-conventions/SKILL.md). This skill leaves the working tree exactly as it found it.

### When GitHub refuses the review event

GitHub rejects a formal `APPROVE` on a PR the same account authored, and may refuse a review event for other reasons. That refuses the event, never the publication. Post the same content as a PR comment whose first line is the verdict, `Approved ✅`, `Requested Changes 🔄` or `Commented 💬`, with each finding naming its file and line because a plain comment cannot anchor to the diff.

Then report what actually happened: findings published as a comment, formal event refused and why, and which separate reviewer action remains. Ending a review with nothing published because the API refused the event is a failed review, not a limitation. [`github-conventions`](../github-conventions/SKILL.md) holds the full rule.

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

Approve only when the PR satisfies every issue in `closingIssuesReferences`, all required
acceptance criteria are met, no demonstrated blocking defect remains, repository rules are
followed, validation is sufficient, and unresolved threads do not represent blocking work. Do not
withhold approval for optional improvements.

## Request Changes criteria

Request changes when at least one demonstrated blocking issue remains. Do not request changes for personal preferences, optional refactors, stylistic differences handled by tooling, unverified future enhancements, or questions answerable from the repository.

## Merge and auto-merge safety

After submitting `APPROVE`, refetch the PR.
Merge immediately or enable auto-merge only when:
- the current head SHA is exactly the reviewed SHA
- the PR is not a draft
- the PR targets the default branch and `closingIssuesReferences` contains every intended issue
- all required checks passed, or auto-merge can safely wait for them
- no blocking review threads remain
- no required reviewer is missing
- GitHub reports the PR as mergeable/safely auto-mergeable
- the repository permits the chosen merge method and the account is authorized
- no administrator bypass is required
- the user did not request `--no-merge`

Merge with all commits preserved, per [`github-conventions`](../github-conventions/SKILL.md):

```bash
gh pr merge <number> -R <repository> --merge --delete-branch
```

Never `--squash`. If the repository's settings permit no method that preserves the commits, stop before merging and report the setting rather than squashing to get the PR closed.

Immediately after a successful merge, read every recorded closing issue back. If GitHub did not
auto-close one, close it as `completed` and verify it is closed. This fallback is allowed only
after the PR reports a successful merge and only for an issue the reviewed PR fully satisfied.
Report a merge as incomplete when any intended issue remains open or its closure cannot be
verified.

Never merge after `REQUEST_CHANGES`, approve one SHA and merge another, bypass checks, dismiss valid reviews merely to merge, change production code, commit fixes, close an issue before merge, or claim a formal approval when GitHub rejected it.

If GitHub prevents self-approval, publish the verdict as the comment described above, state what separate reviewer action is required, and do not claim the formal approval was submitted. When remote access is unavailable entirely, review locally and report findings without claiming published comments or approvals. Read the submitted review back before reporting success; a verdict is published only when the API says it is.

For a diff that is not yet a pull request, use `review-changes` instead. This skill needs exactly
one open pull request, at least one issue it closes, and a place to publish the verdict.
