# Personal Engineering Skills

These are personalized forks for practical use across coding agents. They preserve engineering discipline while avoiding organization-specific process dependencies.

## Available skills

| Skill | Invocation | Purpose |
| --- | --- | --- |
| `architecture-review` | User | Assess an existing codebase and rank evidence-backed architecture improvements. |
| `debug` | Model or user | Diagnose a non-trivial bug through reproduction, hypotheses, a minimal fix, and verification. |
| `domain-model` | Model or user | Clarify contradictory domain terminology, states, rules, and relationships. |
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

## Renamed from upstream

| Upstream | Personal name |
| --- | --- |
| `prototype` | `prototype` |
| `research` | `research` |
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
