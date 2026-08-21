---
name: issue-plan
description: Complete the Plan and Tasks SDD phases for exactly one GitHub Issue. Triggers when the user asks to plan an issue, or when delegated by project-groom or issue-implement. Invoke manually as `/issue-plan <issue-number-or-url>`; direct GitHub issue URLs are accepted. Not for planning several issues, implementing code, or handling non-GitHub trackers.
argument-hint: "<issue-number-or-url>"
metadata:
  scope: project
  role: authoring
  mutation: write
  upstream: https://github.com/obra/superpowers
  upstream-author: obra
  upstream-path: skills/writing-plans
  upstream-revision: 44c9b2d6e889982ac18c27d05a19fefe335194e1
  upstream-checked: 2026-08-03
  version: superpowers-personal.1
---

# Plan Issue

Complete the SDD phases `Plan` and `Tasks` for exactly one GitHub Issue.

## Invocation

Accept either an issue number in the current repository or a direct GitHub issue URL:

```text
/issue-plan 123
/issue-plan https://github.com/acme/app/issues/123
```

Treat a URL's host, owner, repository, and issue number as the exact target. Reject pull request
URLs and never replace the URL's repository with the current working repository. Before inspecting
local code, verify that the checkout matches the URL repository; stop on a mismatch unless the
exact checkout is available.

## Workflow

1. Accept exactly one issue number or direct issue URL and resolve that exact target.
2. Read the issue title and body, every issue comment, linked issues, linked PRs, applicable `AGENTS.md`, code, tests, documentation, and relevant history.
3. Reconstruct the canonical `Specify` and `Clarify` contract. Do not assume the newest comment automatically overrides older content. Look for explicit decisions, confirmations, and supersession.
4. If `Specify` or `Clarify` is materially incomplete, delegate to `issue-capture` or stop with an exact preparation gap.
5. Inspect the current code instead of trusting stale file lists in the issue.
6. Use `grilling` only for unresolved consequential choices.
7. Route to `domain-model`, `module-design`, `research`, `prototype`, or `build-or-reuse` only when their exact triggers apply.
8. Update the canonical issue with `Plan` and proportional `Tasks`. Verify that every acceptance criterion, dependency, and major risk is covered.
9. Refetch the issue before writing to avoid overwriting concurrent edits.

## Plan content

Include when applicable:
- chosen approach
- important rejected alternatives
- architecture and ownership boundaries
- affected modules and responsibilities
- interfaces and contracts
- data and state flow
- compatibility and migration concerns
- accessibility, security, and failure behavior
- documentation updates
- dependencies and coordination
- risks and regression areas
- validation and test strategy
- implementation sequence

## Task sizing

Planning is where the size becomes knowable, so apply the issue's `effort:` label once the Plan
exists, using the repository's own scale or the closed set `issue-capture` documents. An issue
sized `XL` is a prompt to check whether it should be split before Tasks are written.

Use repository labels or conventions when available. Fallback behavior:

- **Small**: Do not add a separate Tasks checklist that merely repeats the Plan. The Plan itself must be directly executable.
- **Medium**: Add a short, ordered checklist. Each item must represent a coherent, verifiable result.
- **Large**: Add complete, ordered Tasks. Include relevant files or ownership areas, dependencies, required tests, and validation. Make each task independently reviewable where practical.

Do not use placeholders such as `TBD`, `handle edge cases`, or `add tests`.

## Must not

- modify production code
- create a branch, commit, push, or open a PR
- implement the issue
- re-ask resolved questions
- invent a technical plan without inspecting the repository
- turn reversible implementation details into unnecessary user questions

## GitHub and Fallback Behavior

This skill targets GitHub Issues and nothing else. Do not add support for, degrade towards, or produce output shaped for another tracker. The official GitHub API is the interface; reach it through the available native GitHub integration or `gh api`, and drop from a higher-level `gh` command to the API whenever that command does not cover the operation exactly.

Read the whole issue, including its relationships, before planning anything:

```bash
gh issue view <number-or-url> --json number,title,body,state,labels,comments,blockedBy,blocking,parent,subIssues,url
```

`blockedBy` is GitHub's own dependency data. An issue blocked by unfinished work cannot be planned as if it were independent.

Write `Plan` and `Tasks` into the canonical body, then read it back:

```bash
gh issue edit <number-or-url> --body-file -            # replaces the whole body
gh issue edit <number-or-url> --add-label "effort:M"
gh issue view <number-or-url> --json body,labels
```

The rewritten body, and any comment posted alongside it, ends with the agent signature line defined in [`github-conventions`](../github-conventions/SKILL.md), for example `🤖 AI-generated by ❋ Claude Sonnet 5 (High)`. When merging into an existing body, replace the signature already there rather than stacking a second one under it.

Merging a body usually needs the old text on disk. Keep that file in a uniquely named system temporary directory and delete it before this run reports completion, including when the edit failed, per [`github-conventions`](../github-conventions/SKILL.md).

`--body-file -` replaces the entire body, so refetch immediately before writing and merge the new sections into the existing content by hand. Never claim an issue or comment was published on the strength of the command alone. When remote access is unavailable, continue locally when safe, produce a ready-to-publish artifact, and state which remote actions were not performed.
