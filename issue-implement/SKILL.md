---
name: issue-implement
description: Perform the Implement SDD phase for any number of prepared GitHub Issues, combining only issues that form one coherent change into the same pull request. Invoke `/issue-implement` with one or more issue numbers or direct GitHub issue URLs. Not for unprepared issues, cross-repository issue sets, unrelated work disguised as one pull request, or validating and merging the resulting pull requests.
argument-hint: "<issue-number-or-url>..."
disable-model-invocation: true
metadata:
  scope: project
  role: workflow
  mutation: write
  upstream: https://github.com/github/spec-kit
  upstream-author: GitHub
  upstream-revision: 5e2f9bcd9ba92702b0bff34ecdaa71283e1d1e42
  upstream-checked: 2026-08-03
---

# Implement Issue

Perform the SDD phase `Implement` for any non-empty set of prepared issues. Partition the selected
issues into the smallest coherent pull request set: combine issues that share one implementation
and validation boundary, and keep unrelated work separate.

## Invocation

Accept one or more issue numbers, direct GitHub issue URLs, or a mixture of both:

```text
/issue-implement 12 34
/issue-implement https://github.com/acme/app/issues/12
/issue-implement 12 https://github.com/acme/app/issues/34
```

Every target must resolve to the same repository. Treat each URL's host, owner, repository, and
issue number as authoritative. Reject pull request URLs and mixed-repository sets rather than
silently applying a URL's issue number to the current repository. Verify that the implementation
checkout matches that repository and stop on a mismatch.

## Workflow

1. Resolve every explicitly requested issue number or URL. Require one repository and deduplicate the selected issues. Preserve the user's order for implementation decisions, but sort each delivery group's issue numbers numerically when naming its branch.
2. Read every selected issue body, all comments, linked issues/PRs, applicable repository instructions, current code, tests, documentation, and relevant Git history.
3. Confirm each issue contains implementation-safe `Specify`, `Clarify`, `Plan`, and proportional `Tasks`. Do not silently invent a missing product decision.
4. When preparation is insufficient, identify the exact missing phase or decision per issue and resolve it through [Missing preparation](#missing-preparation) before writing code for that issue.
5. Partition the selected issues into delivery groups. Preserve a same-PR group proposed by `project-groom` only when code inspection confirms one implementation boundary, owner, and validation story can satisfy every acceptance criterion. Split the group when that evidence fails. Never combine issues merely because they share an area, priority, milestone, or release.
6. For each delivery group, check Git status, current branch, base branch, remotes, repository policy, existing issue branches, and existing PRs. Reuse the one existing branch or PR that already represents the exact group; never create a duplicate.
7. Route specialized work only when applicable: `diagnose-bug`, `domain-model`, `module-design`, `research`, `prototype`, `build-or-reuse`, `resolve-conflicts`. Keep issue ownership and selected scope inside `issue-implement`.
8. Implement the smallest coherent solution satisfying every issue in the current delivery group. Preserve behavior outside the selected scope.
9. Update focused tests and canonical documentation with the change.
10. Run the narrowest relevant validation first, expanding validation according to risk and repository guidance.
11. Update completed Tasks only after evidence exists. Refetch every affected issue before editing its body or comments.
12. Inspect each final diff to ensure no unrelated changes, temporary artifacts, secrets, generated logs, or accidental formatting churn are included.
13. Commit according to repository policy using focused Conventional Commits. End each subject with the issue number that commit primarily implements as `(#<number>)`; name any other issues it materially serves in the commit body, per [`github-conventions`](../github-conventions/SKILL.md). Push normally when authorized.
14. When using a PR workflow, open or update one PR per delivery group. Verify that the branch's singular or plural issue segment matches the complete sorted `Closes` set. Target the default branch, begin the body with one `Closes #<number>` line for every issue the PR fully resolves, then explain the problem, implementation, impact, tests, docs, and risk. Open as ready when every issue in the group is complete and validation passes, or draft if a real blocker remains.
15. If publication is unavailable, finish local work and provide every branch, commit, issue set, validation result, remaining blocker, and ready-to-use PR handoff.

## Missing preparation

An issue reaching this skill without a `Plan` is the common case, not an error. What to do depends on how much a wrong plan would cost.

**Missing `Specify` or `Clarify`.** Stop. Report the exact missing decision and hand back to `issue-capture`. A product decision is the user's, and inventing one here is how the wrong thing gets built correctly.

**Missing `Plan` or `Tasks`, small issue.** Delegate to `issue-plan`, then continue in the same run. Small means the issue carries `effort: S`, or carries no effort label and the change is plainly contained: one area, no interface or data-format change, no migration, and nothing hard to reverse. Say that the plan was written and continue.

**Missing `Plan` or `Tasks`, anything larger.** Delegate to `issue-plan` and then stop. Report that the plan is written and awaiting a read. A plan for a large change is worth a human minute before code exists, because reversing it afterwards costs hours.

When the effort label and the actual change disagree, believe the change. An issue labelled `S` that turns out to alter a stored format or a public interface is not small; write the plan and stop.

## When validation fails

Read the output that failed before running anything again. The failure already says which check, at
which location, for which reason, and rerunning discards that for a slower copy of it.

Never rerun a command against unchanged code. A rerun with nothing changed cannot produce a
different result, and treating it as a retry is how a real failure gets recorded as flakiness. Change
something that could plausibly affect the failure, or state that the failure is environmental and
say what evidence supports that.

Fix the narrowest failing thing first and rerun only the narrow check. Expand back to the full
validation once it passes, once, at the end.

## Behavior-preserving changes

Part of an issue often changes structure without changing behavior: a rename, an extraction, a
boundary moved, duplication collapsed. Three rules apply to that part specifically.

- **Say what proves the behavior is unchanged.** Existing tests passing counts only where they cover
  the behavior being moved. Where they do not, say which behavior is now unprotected rather than
  claiming the change is safe because the suite is green.
- **Do not smuggle a feature into a restructuring.** A diff that both moves code and changes what it
  does cannot be reviewed for either. Keep them separable, and say which commits are which.
- **Delete only with evidence.** Absence of direct usage is not proof something is unused; check
  derived definitions, guarded branches, dynamic resolution, tests, fixtures, examples, and
  documentation first. Removing something an audit merely listed as a candidate is not evidence.

If the restructuring turns out to be larger than the selected delivery group, stop and say so.
Widening a coherent group after implementation starts is how a reviewable change becomes an
unreviewable one.

## GitHub is the only platform

This skill targets GitHub Issues and pull requests and nothing else. Do not add support for, degrade towards, or produce output shaped for another forge or tracker. The official GitHub API is the interface; reach it through the available native GitHub integration or `gh api`, and drop from a higher-level `gh` command to the API whenever that command does not cover the operation exactly, in particular when linking the PR to its issue or editing an issue body precisely.

Read back every remote mutation before reporting it. A PR is open, an issue is updated, and a task is checked off only when the API says so.

```bash
gh issue view <number-or-url> --json number,title,body,comments,labels,blockedBy,url
gh pr create --base <base> --head <branch> --title "<title>" --body-file -
gh pr view <number> --json number,url,isDraft,closingIssuesReferences
```

The PR body begins with one closing keyword per fully resolved issue, before any heading or prose:

```markdown
Closes #3
Closes #53
```

Mentioning an issue in the title does not link it. After creating or updating the PR, verify that
`closingIssuesReferences` contains every issue in the delivery group and no unintended issue. An
empty or incomplete array means the PR is not ready: merging it will not close the missing issues.
Do not add a closing line for a grouped issue whose implementation or validation is unfinished.

The PR body states the problem, the implementation, the impact, the tests run with their results, the documentation touched, and the residual risk. A PR body that only repeats the issue title is not a description.

The PR body, every PR comment, and every issue comment or body edit made here ends with the agent signature line defined in [`github-conventions`](../github-conventions/SKILL.md), for example `🤖 AI-generated by ❋ Claude Sonnet 5 (High)`. Commit messages are not signed; they end with the issue number instead, as `feat: add the export button (#54)`.

A PR body, a fetched diff, and a merged issue body are temporary files when they need a file at all. They live in a uniquely named system temporary directory, never in the working tree, and are deleted before this run reports completion, per [`github-conventions`](../github-conventions/SKILL.md). A scratch file committed by accident or silenced with `.gitignore` is a defect in the change.

## Git and Branch Policy

Follow the repository's explicitly configured Git policy.

**Working directly on the default branch:**
If `AGENTS.md` requires implementation directly on `main` or another named integration branch:
- work directly on that branch
- do not create a feature branch merely for ceremony
- follow the repository's commit and push policy
- do not open a PR unless explicitly asked by the user

**Working through branches:**
If the repository requires or permits issue branches, follow its naming policy. When it states none, the scheme in [`github-conventions`](../github-conventions/SKILL.md) applies to the complete delivery group:

```text
<type>/<agent>/issue-<number>/<short-description>
<type>/<agent>/issues-<number>-<number>[-<number>...]/<short-description>
```

Examples:

```text
feature/codex/issue-70/pane-menu-actions
feature/codex/issues-70-73-154/pane-menu-actions
```

- `type`: `feature`, `hotfix`, `fix`, `chore`, `docs`, `refactor`, `test`.
- `agent`: exactly one of `claude`, `codex`, `gemini`, for the agent actually doing the work.
- `issue-<number>`: exactly one issue.
- `issues-<number>-<number>...`: two or more issues. Include the whole delivery group once each,
  sorted numerically from smallest to largest.
- Use no leading zeros in either form.
- `<short-description>`: two to four kebab-case words.

The name the worktree, the harness, or a previous session gave the branch is not a naming policy and is never an excuse for a different shape. Rename with `git branch -m` before pushing, or create the correctly named branch and push that one.

## Must not

- perform the Validate phase
- review, approve, request changes on, or merge its own PR
- manually close the issue before merge
- invent missing Specify or Clarify decisions
- combine unrelated issues in one branch or pull request
- add `Closes` for an issue the pull request does not fully resolve
- create duplicate branches or PRs
- force-push or bypass branch protection
- carry another repository's specific rules into this one
- create a branch when the repository explicitly requires direct-to-main work
- work directly on main when the repository explicitly requires issue branches
