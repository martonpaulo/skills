---
name: debug
description: Diagnose a non-trivial bug through reproduction, evidence gathering, hypothesis testing, root-cause analysis, a minimal fix, and regression verification. Use when the cause is not already obvious.
metadata:
  scope: project
  role: workflow
  mutation: write
  upstream: https://github.com/mattpocock/skills
  upstream-author: Matt Pocock
  upstream-path: skills/engineering/diagnosing-bugs
  upstream-revision: ed37663cc5fbef691ddfecd080dff42f7e7e350d
  upstream-checked: 2026-08-03
  version: mattpocock-personal.1
---

# Debug

Use this discipline for difficult bugs, intermittent failures, and performance regressions. For a local failure with an already-proven cause, use the normal implementation workflow.

When a hypothesis depends on documented API behavior, version compatibility, deprecation, configuration semantics, or migration changes, use `apple-docs` for Apple development or `deep-docs` elsewhere. This skill retains ownership of reproduction, diagnosis, and the fix.

## Workflow

1. Inspect the relevant code, call sites, tests, logs, and recent changes before editing.
2. Reproduce the reported symptom or gather the strongest available concrete evidence. Confirm that the evidence matches the user's bug rather than a nearby failure.
3. Reduce the scenario while preserving the failure when practical. Record the smallest reliable reproduction command or procedure.
4. Separate symptoms from possible causes. Write explicit, falsifiable hypotheses and rank them by evidence.
5. Test one hypothesis at a time with targeted instrumentation, controlled inputs, a debugger, a profiler, or a focused test. Remove temporary instrumentation afterward.
6. Identify the root cause and make the smallest correct fix. Avoid batches of speculative or unrelated changes.
7. Add a regression test at the closest stable behavioral seam when practical.
8. Run the focused reproduction or test first, then broader relevant anti-regression checks.

## Evidence gaps

If reproduction is impossible, report what was tried, what evidence is missing, and what artifact or access would improve confidence. Do not present a hypothesis as a confirmed cause.

## Completion

Claim the bug is fixed only when the original symptom no longer reproduces, focused verification passes, broader checks show no relevant regression, and temporary debugging changes are gone. Report the root cause, fix, commands run, results, and residual uncertainty.
