---
name: architecture-review
description: Review an existing codebase for high-value architectural improvements, using concrete code evidence to identify weak boundaries, shallow modules, duplication, coupling, scattered responsibilities, and unstable seams.
disable-model-invocation: true
metadata:
  scope: project
  role: audit
  mutation: docs
---

# Architecture Review

Perform a broad, evidence-based assessment only when the user invokes this skill. This skill produces recommendations; it does not refactor the codebase.

For an explicitly requested broad reuse or replacement audit, use `dont-reinvent-the-wheel` for individual candidate decisions while this skill retains ownership of broader architectural findings.

## Workflow

1. Establish the requested scope and read repository guidance plus relevant architecture documentation. Documentation is useful when present but is never a prerequisite.
2. Inspect source code, tests, call sites, dependency direction, and recent change patterns where history is relevant.
3. Apply `module-design` criteria to boundaries, interfaces, dependency direction, ownership, test seams, cohesion, and coupling.
4. Use `domain-model` only when inconsistent terminology, business rules, or domain boundaries materially affect the architecture.
5. Identify concrete findings. Each finding must cite files and symbols and explain the observed cost rather than relying on a generic preference.
6. Rank findings by impact, confidence, effort, implementation risk, and expected payoff. Prefer a few high-value findings over an exhaustive catalog.
7. Write a concise Markdown report in the conversation unless the user requests a file or repository guidance specifies a review location.

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
