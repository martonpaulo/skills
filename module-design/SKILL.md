---
name: module-design
description: Design or improve module boundaries, interfaces, dependency direction, cohesion, coupling, test seams, and responsibility ownership when a code change exposes unclear or unstable structure.
metadata:
  scope: project
  role: workflow
  mutation: write
  upstream: https://github.com/mattpocock/skills
  upstream-author: Matt Pocock
  upstream-path: skills/engineering/codebase-design
  upstream-revision: ed37663cc5fbef691ddfecd080dff42f7e7e350d
  upstream-checked: 2026-08-03
  version: mattpocock-personal.1
---

# Module Design

Use these criteria when a module's responsibilities, interface, dependencies, or test seams are unclear. Adapt them to the repository's language, framework, and established architecture.

## Workflow

1. Inspect callers, implementation, tests, data flow, lifecycle, and existing conventions.
2. State the behavior the module should own and the knowledge callers should not need.
3. Map dependencies and direction: which dependencies are stable, which vary, and which side should own the abstraction.
4. Consider at least two plausible designs when the boundary is consequential. See [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md).
5. Compare designs by interface size, cohesion, coupling, locality, dependency direction, testability, migration risk, and fit with the codebase.
6. Recommend the smallest design that gives clear ownership and a stable behavioral seam.

## Decision criteria

- Prefer a deep module: substantial behavior behind a small, stable interface.
- Keep behavior and the state or rules it governs local when that improves understanding.
- Put tests at stable behavioral seams so internal refactoring does not rewrite them.
- Inject dependencies when substitution, isolation, or lifecycle ownership requires it; avoid indirection that has only one fixed implementation and no testing value.
- Make dependency direction reflect ownership of policy rather than incidental call direction.
- Avoid abstractions that merely rename or forward calls.
- Reduce scattered business rules and parallel sources of truth.
- Preserve familiar repository vocabulary. Names such as service, component, API, manager, and helper are normal; criticize them only when they conceal unclear responsibility.

These are decision criteria, not universal laws. A small function, local helper, framework component, or direct dependency may be the best design.

## Framework fit

Apply the same criteria using native conventions: Spring services and beans, React or Next.js components and hooks, Swift types and protocols, or equivalent structures in other ecosystems. Do not force one ecosystem's layering or terminology onto another.

For dependency categories and test strategies, see [DEEPENING.md](DEEPENING.md).

## Completion

A design recommendation is complete when ownership, interface, dependencies, test seam, migration scope, tradeoffs, and repository fit are explicit.
