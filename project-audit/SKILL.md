---
name: project-audit
description: Run the applicable audits across a whole project and consolidate their findings into one ranked list, so bugs, architecture and interface problems compete on the same scale instead of arriving as separate reports. Use only when the user explicitly invokes $project-audit for a broad read-only health check at low, medium or high depth. Not for auditing one file or one pull request, not for implementing any finding, and not as a substitute for invoking a single audit directly when only one lens applies.
argument-hint: "[low|medium|high] [scope]"
disable-model-invocation: true
metadata:
  scope: project
  role: audit
  mutation: temporary
---

# Project Audit

Run the audits that actually apply to this project and merge their output into one ranked list.

The individual audits already exist and are good at their own lens. What none of them can do is
tell you what to fix first, because each ranks only within itself: `bug-hunter` returns severities,
`architecture-review` returns payoffs, `interface-audit` returns user consequences, and three
ordered lists are not an answer. Producing the single order is this skill's whole job.

## Depth

Take the first argument as the depth and the rest as the scope. Default to `medium`.

| Depth | Lenses | Consolidated cap |
| --- | --- | --- |
| `low` | The one or two lenses with the most exposure, on the primary path only | 8 |
| `medium` | Every applicable lens, on the highest-risk complete areas | 15 |
| `high` | Every applicable lens across the stated scope, plus cross-lens root causes | 25 |

Depth narrows coverage. It never relaxes the evidence bar: a finding that would not survive in its
own audit does not survive here either.

## 1. Decide which lenses apply

Inspect the project first, then pick. Running a lens that cannot apply wastes a pass and pads the
report.

| Lens | Delegate to | Applies when |
| --- | --- | --- |
| Behavioral defects | `bug-hunter` | Always, for any project with executable logic |
| Structure and boundaries | `architecture-review` | More than a handful of modules, or churn concentrated in one area |
| Interface and copy | `interface-audit` | The project has a user interface, CLI output, or user-facing copy |
| Documentation truth | direct inspection | `AGENTS.md`, README, or guidance claims behavior the code contradicts |

State which lenses you selected and which you skipped, each with the reason. A CLI with no UI does
not get an interface audit, and saying so is part of the report.

`architecture-review` applies `module-design`'s criteria for boundaries, cohesion and dependency
direction; do not invoke `module-design` separately here.

## 2. Run each lens under its own contract

Delegate. Do not reimplement an audit's method, relax its evidence threshold, or keep a finding it
would have dismissed. Each delegated audit keeps its own rules about what counts as verified and
what must be reported as a coverage gap.

Run them independently so one lens's conclusions cannot seed another's. If independent agents are
available and the user wants them, the lenses may run in parallel as read-only agents; that is an
optimization, and a single sequential pass must produce the same report.

## 3. Consolidate

This is the step that justifies the skill.

1. **Merge duplicates across lenses.** The same root cause often surfaces three times: a defect in
   `bug-hunter`, a boundary problem in `architecture-review`, and a broken state in
   `interface-audit`. Merge them into one finding, name the root cause, and list every symptom with
   the lens that found it. A cause that shows up in three lenses is more important than any of its
   three reports suggested, and that is exactly what separate reports hide.
2. **Rank on one scale.** Order by user or data consequence first, then reachability, then
   confidence, then the cost of fixing it. A confirmed data-loss path outranks an elegant
   architectural payoff; a speculative refactor outranks nothing.
3. **Keep severity and confidence independent.** A severe finding with weak evidence is severe and
   uncertain, not downgraded to medium.
4. **Say what to do first, and why that one.** One recommendation, with the reason it leads.

## Report

1. **Scope and coverage:** depth, the exact boundary audited, the lenses run, the lenses skipped
   with reasons, and what was left unexamined. Never imply full coverage from a sample.
2. **Ranked findings:** one table across all lenses, each row naming the finding, the originating
   lens or lenses, the location, the evidence, the consequence, severity, confidence, and the
   smallest correction.
3. **Cross-lens root causes:** findings that merged, with every symptom and the lens that saw it.
4. **Per-lens coverage gaps:** what each audit could not verify, kept in its own words.
5. **Start here:** the single recommendation to act on first, and why it outranks the rest.

## Boundaries

This audit inspects and reports. It never edits code, tests, configuration, or documentation,
never creates issues, branches, commits or pull requests, and never fixes a finding.

Three things people expect here and that do not belong:

- **Fixing a defect** is `debug`, in a separate task, after the owner selects a finding.
- **Deciding to replace a capability** is `dont-reinvent-the-wheel`, once a finding has made the
  case that something should be replaced.
- **Interviewing the owner** is `grilling`. This skill reads evidence; it does not resolve product
  decisions, and a finding that depends on one is reported as exactly that.

Turning a selected finding into work is `issue-capture`, one issue at a time. Do not bulk-create
issues from an audit; a report of fifteen findings is not a mandate for fifteen issues.

Temporary work stays in a uniquely named system temporary directory and is removed and reported
before completion.

## Completion

The audit is complete when the selected lenses ran under their own contracts, the skipped ones are
named with reasons, duplicates across lenses are merged under their root cause, every finding is
ranked on one scale with evidence and location, coverage is honest about what went unexamined, and
nothing was mutated.
