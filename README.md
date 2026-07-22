# Personal Engineering Skills

These 16 personalized forks are designed for practical use across coding agents. They preserve engineering discipline while avoiding organization-specific process dependencies.

## Available skills

| Skill | Invocation | Purpose |
| --- | --- | --- |
| `architecture-review` | User | Assess an existing codebase and rank evidence-backed architecture improvements. |
| `apple-docs` | Model or user | Perform authoritative, version-aware Apple development documentation research using Apple docs, Swift sources and proposals, Xcode context, local Xcode documentation, HIG, WWDC, release notes, and distribution guidance. |
| `debug` | Model or user | Diagnose a non-trivial bug through reproduction, hypotheses, a minimal fix, and verification. |
| `deep-docs` | Model or user | Perform authoritative, version-aware documentation research for non-Apple frameworks, SDKs, libraries, APIs, CLIs, platforms, and developer tools. |
| `domain-model` | Model or user | Clarify contradictory domain terminology, states, rules, and relationships. |
| `dont-reinvent-the-wheel` | Model or user | Evaluate whether a specific capability should reuse an existing project feature, native platform capability, maintained dependency, open-source project, external service, hybrid approach, or custom implementation. |
| `grill` | User | Pressure-test a plan through a focused interview without writing files. |
| `grill-and-document` | User | Pressure-test a plan while preserving canonical domain language and rare consequential decisions. |
| `grilling` | Model or user | Resolve material uncertainty one question at a time before implementation. |
| `handoff` | User | Write a compact continuation note for another agent or later session. |
| `module-design` | Model or user | Improve module ownership, interfaces, dependencies, cohesion, coupling, and test seams. |
| `prototype` | Model or user | Run a disposable experiment when execution is the best way to answer a concrete question. |
| `research` | Model or user | Verify technical or product questions against current, high-trust primary sources. |
| `resolve-conflicts` | Model or user | Resolve an active Git conflict by preserving the valid intent of both sides. |
| `setup-agent-docs` | User | Configure optional repository paths for glossaries, ADRs, research, handoffs, and prototypes. |
| `skill-authoring` | User | Create, review, or simplify focused Agent Skills. |

## Real dependencies

- `grill` uses `grilling`.
- `grill-and-document` uses `grilling` and `domain-model`.
- `architecture-review` uses `module-design`, and uses `domain-model` or `grilling` only when the review actually needs them.
- `dont-reinvent-the-wheel` uses `research` when external evidence is needed.
- `dont-reinvent-the-wheel` uses `grilling` when unresolved requirements materially affect the decision.
- `dont-reinvent-the-wheel` uses `prototype` when practical fit must be validated.
- `dont-reinvent-the-wheel` uses `architecture-review` only for an explicitly requested broad reuse audit.
- `deep-docs` defers Apple development documentation to `apple-docs`.
- `research` uses `apple-docs` for authoritative Apple documentation and `deep-docs` for precise version-aware software documentation.
- `debug` uses `apple-docs` or `deep-docs` when a bug depends on documented behavior.
- `dont-reinvent-the-wheel` uses `apple-docs` or `deep-docs` when native capability or version support must be verified.

## Upstream mapping

| Upstream | Personal name |
| --- | --- |
| `prototype` | `prototype` |
| `research` | `research` |
| `dont-reinvent-the-wheel` | `dont-reinvent-the-wheel` |
| `apple-developer-docs` | `apple-docs` |
| `appledeepdoc-mcp` | Architectural reference for `deep-docs`, not a runtime dependency |
| `improve-codebase-architecture` | `architecture-review` |
| `diagnosing-bugs` | `debug` |
| `domain-modeling` | `domain-model` |
| `codebase-design` | `module-design` |
| `grilling` | `grilling` |
| `setup-matt-pocock-skills` | `setup-agent-docs` |
| `resolving-merge-conflicts` | `resolve-conflicts` |
| `grill-me` | `grill` |
| `grill-with-docs` | `grill-and-document` |
| `handoff` | `handoff` |
| `writing-great-skills` | `skill-authoring` |

These are personalized forks. Do not blindly overwrite them with `npx skills update`; review upstream changes and port only useful behavior.
