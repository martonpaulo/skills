---
name: capture-issue
description: Convert a newly reported or discovered bug, defect, problem, or feature request into one canonical, implementation-ready GitHub Issue containing the Specify and Clarify phases. Do not trigger when the defect will be fixed immediately, an adequate issue exists, the user only wants an explanation, or the request is already in later phases.
metadata:
  scope: project
  role: authoring
  mutation: write
---

# Capture Issue

Convert a newly reported or discovered problem, bug, or feature request into one canonical, implementation-ready GitHub Issue containing the SDD phases `Specify` and `Clarify`.

## Workflow

1. Read repository instructions, issue templates, label conventions, documentation, code, tests, and relevant history.
2. Search open issues and relevant closed issues before creating anything.
3. Decide whether to update an existing canonical issue, comment with missing evidence, create a new issue, or produce a ready-to-post draft when GitHub writes are unavailable.
4. For bugs, investigate enough to capture:
   - observed behavior
   - expected behavior
   - reproduction steps
   - affected environment
   - version, commit, or branch when relevant
   - severity and impact
   - concrete evidence
   - validation already attempted
   - known workaround
   - blockers or dependencies
5. Apply `grilling` directly for material unresolved decisions. Do not route through `grill`, because `grill` is a manual conversational wrapper and does not create work artifacts.
6. Route to `domain-model` when domain terminology, states, rules, entities, or relationships are materially ambiguous.
7. Route to `research` when current external evidence affects the requested behavior.
8. Create or update exactly one canonical issue. Apply only existing, clearly applicable labels and metadata.
9. Refetch the issue before mutation when concurrent editing is possible.

## Specify Phase

Include only relevant sections, but cover:
- problem
- user or system impact
- current behavior
- expected outcome
- scope
- non-goals
- acceptance criteria
- evidence
- dependencies
- known constraints

## Clarify Phase

Preserve:
- resolved decisions
- assumptions
- constraints
- explicitly superseded decisions
- decisions inferred from existing repository contracts
- genuinely unresolved human choices

When comments supersede older issue content, make that relationship explicit rather than leaving contradictory requirements silently active.

## Must Not

- create Plan
- create Tasks
- implement code
- create a branch
- commit or push
- open a PR
- create duplicate issues
- create an issue for a defect fixed immediately
- invent behavior to fill missing requirements
- turn an unverified suspicion into a confirmed bug

## Shared investigation rule

Before asking the user a question:
1. Read the applicable root and nested `AGENTS.md` files.
2. Inspect relevant code, tests, documentation, configuration, history, linked issues, comments, reviews, and established patterns.
3. Distinguish verified facts, reasonable inferences, and unknowns.
4. Attempt to resolve the question from evidence.
5. Ask only when a material decision remains unresolved and cannot be settled safely from the repository.

Do not ask the user for information that the repository, GitHub history, or linked artifacts can answer.

## Shared GitHub and fallback behavior

GitHub is the preferred workflow, but do not falsely assume GitHub access is always available. Use, in order:
1. available native GitHub integration
2. authenticated `gh`
3. GitHub API when a required operation is not covered by a higher-level command
4. user-supplied issue, PR, diff, or repository context

When remote access is unavailable:
- continue locally when the task remains safe and meaningful
- produce a ready-to-publish artifact or exact handoff
- clearly state which remote actions were not performed
- never claim that an issue, PR, comment, review, approval, push, or merge happened
