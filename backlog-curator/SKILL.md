---
name: backlog-curator
description: Maintain the quality, consistency, and implementability of the repository's GitHub Issue backlog. Detects duplicates, obsolete issues, and delegates missing SDD phases to flow-capture-issue or plan-issue. Closes with a Mermaid graph of the blocking order across open issues.
disable-model-invocation: true
metadata:
  scope: project
  role: workflow
  mutation: write
  upstream: https://github.com/github/gh-aw
  upstream-author: GitHub
  upstream-revision: 5adcdb6d4ec153409feab88c1688a9929fa07008
  upstream-checked: 2026-08-03
---

# Backlog Curator

Maintain the quality, consistency, and implementability of the repository's GitHub Issue backlog. Operates across issues but delegates individual SDD phase work.

## Workflow

1. Read repository instructions, issue templates, existing labels, milestones, open issues, relevant recent closed issues, linked PRs, project documentation, and current code when necessary to verify obsolescence or dependencies.
2. Build a backlog map containing type, area, priority, effort, SDD phase completeness, dependencies, blockers, overlap, conflicts, linked implementation, and possible obsolescence.
3. Use the repository's existing metadata taxonomy. Do not create a new label system without explicit authorization. When the repository has no convention of its own, audit against the taxonomy `flow-capture-issue` documents: closed value sets for `type:`, `priority:` and `effort:`, an open set for `area:`.
4. Detect strong duplicates, partial duplicates, overlapping scope, missing dependencies, conflicting requirements, stale decisions, issues already implemented, obsolete issues, and issues with missing Specify, Clarify, Plan, or Tasks.
5. Refetch each issue before mutation to preserve concurrent edits and provenance.
6. Apply low-risk metadata changes only when evidence is clear. Add dependency and coordination links when supported.
7. Use `grilling` for consequential conflicts that evidence cannot resolve.
8. Delegate missing `Specify` or `Clarify` to `flow-capture-issue`. Delegate missing `Plan` or `Tasks` to `plan-issue`.
9. Keep comments sparse. Prefer updating the canonical issue body. Use comments for provenance, explicit supersession, duplicate resolution, cross-issue coordination, and unresolved human decisions.
10. Close every pass with the dependency graph described in [DEPENDENCY-GRAPH.md](DEPENDENCY-GRAPH.md), covering the open issues the pass considered and reflecting the links applied during it.

## Duplicate handling

1. Select the canonical issue based on completeness, history, active references, and scope.
2. Copy all unique requirements, evidence, decisions, dependencies, and acceptance criteria into the canonical issue.
3. Preserve attribution and link to the source issue.
4. Comment on the duplicate explaining the canonical issue. Comment on the canonical issue when provenance is not otherwise clear.
5. Close the duplicate with reason `duplicate`. Never delete it.

## Obsolete issue handling

Close an issue as obsolete only when supported by concrete evidence (e.g. merged implementation, explicitly superseding decision, removal of feature). Age alone is never evidence of obsolescence.

## Must not

- implement code
- create implementation branches or PRs
- perform code review
- approve or merge PRs
- delete issues
- close issues merely because they are old
- invent product decisions
- create generic Plan and Tasks for every issue in one pass
- silently resolve contradictory requirements
- overwrite recent human edits
- create labels without authorization

## GitHub is the only platform

This skill targets GitHub Issues and nothing else. Do not add support for, degrade towards, or produce output shaped for another tracker.

Read [github-api.md](references/github-api.md) for the exact commands. Two of them change the quality of a pass:

- `blockedBy` and `blocking` on `gh issue view --json` are GitHub's own issue dependencies and are the source of truth for the blocking order. Read them before believing any sentence in a body that claims one.
- `closedByPullRequestsReferences` is real evidence that an issue is already implemented, which is one of the few valid grounds for closing it as obsolete.

Every mutation is verified by reading it back. A label, link, edit, or closure counts as applied only when the API reports it, never because a command exited zero.

A pass that changes nothing posts nothing. Do not comment to announce that the backlog was reviewed.

## Fallback

When GitHub access is unavailable, accept a supplied issue export or issue list, produce an ordered mutation plan, and do not claim any labels, comments, edits, closures, or links were applied. Still emit the dependency graph, omitting the `click` lines when issue URLs are unknown.
