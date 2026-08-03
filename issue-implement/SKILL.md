---
name: issue-implement
description: Perform the Implement SDD phase for exactly one prepared issue. Triggers when the user provides an issue number/URL to implement.
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

Perform the SDD phase `Implement` for exactly one prepared issue.

## Workflow

1. Resolve the current repository and exact issue.
2. Read the issue body, all comments, linked issues/PRs, applicable repository instructions, current code, tests, documentation, and relevant Git history.
3. Confirm the issue contains implementation-safe `Specify`, `Clarify`, `Plan`, and proportional `Tasks`. Do not silently invent a missing product decision.
4. When preparation is insufficient, identify the exact missing phase or decision and resolve it through [Missing preparation](#missing-preparation) before writing any code.
5. Check Git status, current branch, base branch, remotes, repository policy, existing issue branches, and existing PRs.
6. Route specialized work only when applicable: `debug`, `domain-model`, `module-design`, `research`, `prototype`, `dont-reinvent-the-wheel`, `resolve-conflicts`. Keep issue ownership and scope inside `issue-implement`.
7. Implement the smallest coherent solution satisfying the issue. Preserve behavior outside scope.
8. Update focused tests and canonical documentation with the change.
9. Run the narrowest relevant validation first, expanding validation according to risk and repository guidance.
10. Update completed Tasks only after evidence exists. Refetch the issue before editing its body or comments.
11. Inspect the final diff to ensure no unrelated changes, temporary artifacts, secrets, generated logs, or accidental formatting churn are included.
12. Commit according to repository policy using focused Conventional Commits. Push normally when authorized.
13. When using a PR workflow, open a PR that targets the correct base branch, links the issue, and explains the problem, implementation, impact, tests, docs, and risk. Open as ready when validation passes, or draft if a real blocker remains.
14. If publication is unavailable, finish local work and provide branch, commit, validation results, remaining blockers, and a ready-to-use PR handoff.

## Missing preparation

An issue reaching this skill without a `Plan` is the common case, not an error. What to do depends on how much a wrong plan would cost.

**Missing `Specify` or `Clarify`.** Stop. Report the exact missing decision and hand back to `issue-capture`. A product decision is the user's, and inventing one here is how the wrong thing gets built correctly.

**Missing `Plan` or `Tasks`, small issue.** Delegate to `issue-plan`, then continue in the same run. Small means the issue carries `effort: S`, or carries no effort label and the change is plainly contained: one area, no interface or data-format change, no migration, and nothing hard to reverse. Say that the plan was written and continue.

**Missing `Plan` or `Tasks`, anything larger.** Delegate to `issue-plan` and then stop. Report that the plan is written and awaiting a read. A plan for a large change is worth a human minute before code exists, because reversing it afterwards costs hours.

When the effort label and the actual change disagree, believe the change. An issue labelled `S` that turns out to alter a stored format or a public interface is not small; write the plan and stop.

## GitHub is the only platform

This skill targets GitHub Issues and pull requests and nothing else. Do not add support for, degrade towards, or produce output shaped for another forge or tracker. The official GitHub API is the interface; reach it through the available native GitHub integration or `gh api`, and drop from a higher-level `gh` command to the API whenever that command does not cover the operation exactly, in particular when linking the PR to its issue or editing an issue body precisely.

Read back every remote mutation before reporting it. A PR is open, an issue is updated, and a task is checked off only when the API says so.

```bash
gh issue view <number> --json number,title,body,comments,labels,blockedBy,url
gh pr create --base <base> --head <branch> --title "<title>" --body-file -
gh pr view <number> --json number,url,isDraft,closingIssuesReferences
```

The link between a PR and its issue is made by a closing keyword in the PR body (`Closes #<number>`), not by mentioning the number in the title. Verify it landed: `closingIssuesReferences` must contain the issue. An empty array means the PR is not linked and merging it will not close the issue.

The PR body states the problem, the implementation, the impact, the tests run with their results, the documentation touched, and the residual risk. A PR body that only repeats the issue title is not a description.

## Git and Branch Policy

Follow the repository's explicitly configured Git policy.

**Working directly on the default branch:**
If `AGENTS.md` requires implementation directly on `main` or another named integration branch:
- work directly on that branch
- do not create a feature branch merely for ceremony
- follow the repository's commit and push policy
- do not open a PR unless explicitly asked by the user

**Working through branches:**
If the repository requires/permits issue branches, follow its naming policy. Fallback naming:
`type/agent/issue-NNN/short-description`
(e.g., `feature/claude/issue-024/add-button`).
- `type`: `feature`, `hotfix`, `fix`, `chore`, `docs`, `refactor`, `test`.
- `agent`: the acting agent identifier.
- `issue-NNN`: zero-padded issue number.

## Must not

- perform the Validate phase
- review, approve, request changes on, or merge its own PR
- manually close the issue before merge
- invent missing Specify or Clarify decisions
- implement multiple unrelated issues
- create duplicate branches or PRs
- force-push or bypass branch protection
- carry another repository's specific rules into this one
- create a branch when the repository explicitly requires direct-to-main work
- work directly on main when the repository explicitly requires issue branches
