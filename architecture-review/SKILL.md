---
name: architecture-review
description: Review an existing codebase for high-value architectural improvements, using concrete code evidence to identify weak boundaries, shallow modules, duplication, coupling, scattered responsibilities, and unstable seams.
disable-model-invocation: true
metadata:
  scope: project
  role: audit
  mutation: docs
  upstream: https://github.com/mattpocock/skills
  upstream-author: Matt Pocock
  upstream-path: skills/engineering/improve-codebase-architecture
  upstream-revision: ed37663cc5fbef691ddfecd080dff42f7e7e350d
  upstream-checked: 2026-08-03
  version: mattpocock-personal.1
---

# Architecture Review

Perform a broad, evidence-based assessment only when the user invokes this skill. This skill produces recommendations; it does not refactor the codebase.

For an explicitly requested broad reuse or replacement audit, use `build-or-reuse` for individual candidate decisions while this skill retains ownership of broader architectural findings.

## Workflow

1. Establish the requested scope and read repository guidance plus relevant architecture documentation. Documentation is useful when present but is never a prerequisite.
2. Inspect source code, tests, call sites, dependency direction, and recent change patterns where history is relevant.
3. Apply `module-design` criteria to boundaries, interfaces, dependency direction, ownership, test seams, cohesion, and coupling.
4. Use `domain-model` only when inconsistent terminology, business rules, or domain boundaries materially affect the architecture.
5. Identify concrete findings. Each finding must cite files and symbols and explain the observed cost rather than relying on a generic preference.
6. Rank findings by impact, confidence, effort, implementation risk, and expected payoff. Prefer a few high-value findings over an exhaustive catalog.
7. Write a concise Markdown report in the conversation unless the user requests a file or repository guidance specifies a review location.

## Removal is a claim that needs evidence

Absence of direct usage is not evidence that something is unused. Before recommending that a module,
type, abstraction, or dependency be removed, check derived definitions built on it, guarded branches
for a platform, environment, or feature flag, dynamic resolution that assembles the name at runtime,
tests, fixtures, examples, and documentation, and consumers outside this repository when anything
here is published. Say which of those you checked.

A candidate that survives all of them is a removal recommendation. A candidate that fails one is a
dependency, not dead weight. A candidate you could not fully trace is reported as uncertain, never
as safe to delete.

## Report shape

For each finding include:

- evidence: files, symbols, and behavior;
- problem and practical consequence;
- recommended boundary or responsibility change;
- impact, confidence, effort, risk, and payoff;
- validation needed before implementation.

End with the strongest recommendation and why it should come first. Apply `grilling` only when a material architectural decision cannot be resolved from code or existing guidance.

## Safety and completion

Do not implement a recommendation until the user explicitly selects it. The review is complete when every recommendation is evidence-backed, ranked, and scoped, and uncertainty is visible.
