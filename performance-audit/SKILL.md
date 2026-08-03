---
name: performance-audit
description: Audit a project for evidence-backed performance, responsiveness, memory, storage, and resource-cost findings at low, medium, or high depth. Use only when the user explicitly invokes $performance-audit for a read-only cost review of a codebase, a path, or a named hot path. Not for optimizing anything, not for diagnosing one reported slowdown, which belongs to diagnose-bug, and not for correctness, structure, or interface findings, which belong to their own audits.
argument-hint: "[low|medium|high] [scope]"
disable-model-invocation: true
metadata:
  scope: project
  role: audit
  mutation: temporary
---

# Performance Audit

Find where this project spends time, memory, and storage it does not need to spend, and rank the
findings by what the user actually feels.

One rule separates this audit from guessing: **a cost claim that has not been measured is not a
finding, it is a profiling plan.** Code that looks expensive is a candidate. A candidate becomes a
finding when a concrete cost pattern is traced on a path that really executes, and it becomes
`Verified` only when something measured it. Everything else is reported as `Needs profiling`, with
the exact measurement that would settle it.

## Depth

Take the first argument as the depth and the rest as the scope. Default to `medium`.

| Depth | Coverage | Finding cap |
| --- | --- | --- |
| `low` | The single hot path with the most user exposure | 5 |
| `medium` | Every hot path identified in step 2, plus memory and storage growth | 10 |
| `high` | Medium, plus resource lifecycle, background and scheduled work, and cross-path root causes | 15 |

Depth narrows coverage. It never lowers the evidence bar, and it never turns a `Needs profiling`
candidate into a confirmed finding.

## 1. Establish the cost model

Before reading code, state what has to be fast **in this project** and what does not. A batch job
and an interactive editor fail in different ways, and a finding that ignores the difference is
noise.

Settle four things from the repository itself, and say which are inferred:

- **The budget**: what the user waits for, and roughly how long is acceptable. Startup, first
  meaningful output, a keystroke, a request, a full run.
- **The scale**: the input size the project is actually built for. An O(n²) loop over a bounded
  configuration is not a finding.
- **The constrained resource**: time, memory, storage, battery, network, or cost per call. Projects
  usually have one that dominates.
- **The existing evidence**: benchmarks, profiles, timing logs, performance tests, load tests, or
  issues reporting slowness. Read them before forming your own opinion.

If the project already documents performance requirements, they override every inference here.

## 2. Map the hot paths

A hot path is code that runs often, runs on something the user waits for, or runs over the largest
input. Identify them from the code, not from file names.

Start with the classes of path that exist in nearly every project, and keep only the ones that are
real here:

- the startup or cold-start path
- the path the user waits on most often, whichever it is for this project
- whatever renders, serializes, or emits a repeated element, once per element
- the most frequent write, sync, or persistence path
- work that runs on a timer, a subscription, an observer, or a background schedule

For each hot path you keep, write down its entry point, what it calls, and where it touches the
network, the disk, the database, or the main or UI thread. This map is the unit of analysis for the
rest of the audit, and it belongs in the report even where no finding attaches to it.

Where the project has a rendering or reactive layer, the state that invalidates it is part of the
path. State held higher in the tree than the thing it changes is a cost pattern, not a style
choice.

## 3. Apply the cost patterns

Read [cost-patterns.md](references/cost-patterns.md) and apply it to the mapped paths. It is
language-neutral; translate each pattern into the project's own runtime, framework, and idiom
rather than importing another ecosystem's vocabulary.

Two guards apply to every candidate:

- **Do not infer cost from a name.** A function called `cache`, `fast`, `sync`, or `lazy` proves
  nothing. Read what it does.
- **Do not call something slow because it is complex.** Complexity without a traced cost pattern on
  a path that executes is a `module-design` question, not a performance finding.

## 4. Assign confidence honestly

| Confidence | Meaning |
| --- | --- |
| `Verified` | Measured, or proven by a deterministic trace over a known input size |
| `Likely` | The cost pattern and the path are traced, but the magnitude is unmeasured |
| `Needs profiling` | The pattern is real and the path executes, but whether it matters depends on a measurement nobody has taken |
| `Unknown` | The evidence is incomplete. Report as an open question, never as a finding |

Severity and confidence stay independent. A path that can grow storage without bound is severe and
unmeasured at the same time, and downgrading it to medium because nobody profiled it hides it.

Use the collection's severity scale, `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, so `project-audit` can
rank these findings against the other lenses without translating a second scale.

## 5. Measure only what is safe

You may run a measurement the project already provides, an existing benchmark, performance test, or
profiling command, when it runs locally without installing dependencies, contacting production,
mutating repository files, or using real credentials or personal data. Prefer read-only and
no-cache modes. If a command's side effects are unclear, do not run it, and report the measurement
as the one that would settle the finding.

Never write a new benchmark here. Writing one is implementation work, and a benchmark authored to
confirm the finding that motivated it proves very little. Output goes to a uniquely named system
temporary directory, is reported, and is removed before completion.

## Audit independence

Each run is independent. Ignore earlier conversation context, previous conclusions of your own, and
any report, artifact, or generated output from a previous audit run. They are prior opinion, not
evidence, and an audit that reads its own last report will confirm it. Read the code, the tests, and
real measurement output only.

## Report

1. **Scope and coverage**: depth, the exact boundary audited, the cost model with its inferences
   marked, the hot paths mapped, and what was left unexamined. Never imply full coverage from a
   sample.
2. **Hot path maps**: for every path kept in step 2, its entry point, the work it performs, and its
   contact with the network, disk, database, or main thread. Include paths where nothing was found.
3. **Ranked findings**: one table with the location, the cost pattern, the evidence, the input size
   or frequency that makes it matter, the user-visible consequence, severity, confidence, and the
   smallest correction.
4. **Growth risks**: anything unbounded over time rather than slow right now. Caches without
   eviction, logs without rotation, state that only accumulates, retained references. These are the
   findings a snapshot profile never catches.
5. **Profiling plan**: for every `Needs profiling` and `Likely` finding, the smallest measurement
   that would confirm or reject it. The tool, the exact flow to exercise, the metric to read, and
   what result would mean the finding is wrong.
6. **Do not touch yet**: paths where a change is high-risk, where the measurement must come first,
   or where a correctness question outranks the cost question.
7. **Start here**: the single finding to act on first, and why it outranks the rest.

Every finding names a concrete location. Report no finding that rests on code you did not read.

## Boundaries

This audit inspects and reports. It never edits code, tests, configuration, or documentation, never
optimizes anything, never creates issues, branches, commits, or pull requests, and never writes a
benchmark.

- **Fixing a specific reported slowdown** is `diagnose-bug`, which reproduces one concrete defect.
  This skill searches for cost the user has not reported yet.
- **A structural cause behind several findings** is `architecture-review` or `module-design`. Name
  the route; do not perform it.
- **Framework or platform behavior a finding depends on** must be verified through `apple-docs` for
  Apple platforms or `deep-docs` elsewhere. If authoritative behavior cannot be established,
  downgrade the candidate rather than guessing.

Turning a selected finding into work is `issue-capture`, one issue at a time.

## Completion

The audit is complete when the cost model is explicit, the hot paths are mapped and reported
including the clean ones, every finding names a location and a traced cost pattern, every unmeasured
claim carries the measurement that would settle it, growth risks are separated from current
slowness, coverage is honest about what went unexamined, and nothing was mutated.
