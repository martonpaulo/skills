---
name: plan-issue
description: Complete the Plan and Tasks SDD phases for exactly one GitHub Issue. Triggers when the user provides an issue number/URL to plan, or when delegated by backlog-curator.
disable-model-invocation: true
metadata:
  scope: project
  role: authoring
  mutation: write
  upstream: https://github.com/obra/superpowers/tree/main/skills/writing-plans
  upstream-author: obra
  version: superpowers-personal.1
---

# Plan Issue

Complete the SDD phases `Plan` and `Tasks` for exactly one GitHub Issue.

## Workflow

1. Accept exactly one issue number or URL.
2. Read the issue title and body, every issue comment, linked issues, linked PRs, applicable `AGENTS.md`, code, tests, documentation, and relevant history.
3. Reconstruct the canonical `Specify` and `Clarify` contract. Do not assume the newest comment automatically overrides older content. Look for explicit decisions, confirmations, and supersession.
4. If `Specify` or `Clarify` is materially incomplete, delegate to `capture-issue` or stop with an exact preparation gap.
5. Inspect the current code instead of trusting stale file lists in the issue.
6. Use `grilling` only for unresolved consequential choices.
7. Route to `domain-model`, `module-design`, `research`, `prototype`, or `dont-reinvent-the-wheel` only when their exact triggers apply.
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
exists, using the repository's own scale or the closed set `capture-issue` documents. An issue
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

Use available native GitHub integration, authenticated `gh`, or the GitHub API. When remote access is unavailable, continue locally when safe, produce a ready-to-publish artifact, state which remote actions were not performed, and never claim an issue or comment was published.
