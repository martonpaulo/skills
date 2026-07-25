# Agent Skills

My personal collection of [Agent Skills](https://code.claude.com/docs/en/skills) — 18 skills
that any skill-aware coding agent can load. Most started life as someone else's open-source
skill; every one has been rewritten for how I actually work. **Every upstream project is
credited below, with a link. If a skill is useful to you, the credit belongs to its original
author.**

The repository is public so the work is inspectable and reusable, but it is tuned to one
person's setup. Fork it rather than depending on it.

## How it is wired up

The repository *is* the canonical skills directory:

```
~/.agents/skills -> ~/Tools/skills      # universal Agent Skills path
~/.claude/skills/<skill> -> ../../.agents/skills/<skill>
```

Agents that read the universal `~/.agents/skills` path pick up every skill automatically. Agents
with their own directory get a symlink per skill.

To use a single skill somewhere else, copy its directory into that project's or that agent's
skills directory — each one is self-contained.

## Two kinds of skill

**Project skills** apply to a codebase: designing it, debugging it, researching how its
dependencies behave, resolving its merge conflicts. These are the ones `setup-agent-docs`
configures conventions for.

**Personal skills** apply to me and my machine, not to any repository. They are excluded from
project setup on purpose — a repository has no business configuring conventions for them.

## Project skills

| Skill | Invocation | What it does | Upstream |
| --- | --- | --- | --- |
| [`apple-docs`](apple-docs/) | Model or user | Version-aware Apple platform documentation research: Apple docs, Swift Evolution, Xcode and project context, local Xcode docs, HIG, WWDC, release notes, distribution and signing. | [Ahrentlov/apple-docs-skill](https://github.com/Ahrentlov/apple-docs-skill) |
| [`architecture-review`](architecture-review/) | User | Assess an existing codebase and rank architecture improvements against concrete code evidence. | [mattpocock/skills → improve-codebase-architecture](https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture) |
| [`debug`](debug/) | Model or user | Diagnose a non-trivial bug: reproduce, form hypotheses, find the root cause, make the minimal fix, verify. | [mattpocock/skills → diagnosing-bugs](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs) |
| [`deep-docs`](deep-docs/) | Model or user | Version-aware documentation research for non-Apple frameworks, SDKs, libraries, APIs, CLIs, and platforms, with source-linked evidence. | Written for this collection; security and provider architecture adapted from [Ahrentlov/apple-docs-skill](https://github.com/Ahrentlov/apple-docs-skill) and [Ahrentlov/appledeepdoc-mcp](https://github.com/Ahrentlov/appledeepdoc-mcp) |
| [`domain-model`](domain-model/) | Model or user | Clarify contradictory domain terminology, states, rules, and relationships. | [mattpocock/skills → domain-modeling](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling) |
| [`dont-reinvent-the-wheel`](dont-reinvent-the-wheel/) | Model or user | Decide whether one specific capability should reuse an existing feature, a native platform capability, a dependency, an open-source project, a service — or be built. | [felinto-dev/felinto-skills → dont-reinvent-the-wheel](https://github.com/felinto-dev/felinto-skills/tree/main/.agents/skills/dont-reinvent-the-wheel) |
| [`grill`](grill/) | User | Pressure-test a plan through a focused interview, writing no files. | [mattpocock/skills → grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) |
| [`grill-and-document`](grill-and-document/) | User | Same interview, but preserves canonical domain language and genuinely consequential decisions. | [mattpocock/skills → grill-with-docs](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs) |
| [`grilling`](grilling/) | Model or user | The shared interview discipline: one decision at a time, always with a recommendation. | [mattpocock/skills → grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling) |
| [`handoff`](handoff/) | User | Write a compact continuation note for another agent or a later session. | [mattpocock/skills → handoff](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) |
| [`module-design`](module-design/) | Model or user | Improve module boundaries, interfaces, dependency direction, cohesion, and test seams. | [mattpocock/skills → codebase-design](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design) |
| [`prototype`](prototype/) | Model or user | Run a disposable experiment when executing code answers the question faster than discussing it. | [mattpocock/skills → prototype](https://github.com/mattpocock/skills/tree/main/skills/engineering/prototype) |
| [`research`](research/) | Model or user | Answer a technical or product question from current, high-trust primary sources. | [mattpocock/skills → research](https://github.com/mattpocock/skills/tree/main/skills/engineering/research) |
| [`resolve-conflicts`](resolve-conflicts/) | Model or user | Resolve an in-progress merge, rebase, or cherry-pick by reconstructing the intent of both sides. | [mattpocock/skills → resolving-merge-conflicts](https://github.com/mattpocock/skills/tree/main/skills/engineering/resolving-merge-conflicts) |
| [`setup-agent-docs`](setup-agent-docs/) | User | Configure optional per-repository paths for glossaries, ADRs, research notes, handoffs, and prototypes. | [mattpocock/skills → setup-matt-pocock-skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/setup-matt-pocock-skills) |
| [`skill-authoring`](skill-authoring/) | User | Create, review, or simplify Agent Skills. | [mattpocock/skills → writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills) |

## Personal skills

Not project skills. `setup-agent-docs` deliberately ignores them.

| Skill | Invocation | What it does | Upstream |
| --- | --- | --- | --- |
| [`disk-cleaner`](disk-cleaner/) | Model or user | Audit a personal machine for reclaimable disk space — caches, build artifacts, dependency stores, duplicates, leftovers from removed apps — classify every candidate by risk, and clean only what was explicitly approved. | [gccszs/disk-cleaner](https://github.com/gccszs/disk-cleaner) |
| [`grey-market`](grey-market/) | Model or user | Find digital products sold well below the official price in regional markets, through community sources rather than ordinary search. Locates sellers; never transacts. | [felinto-dev/felinto-skills → grey-market](https://github.com/felinto-dev/felinto-skills/tree/main/.agents/skills/grey-market) |

## Invocation

**Model or user** — the agent may load the skill on its own when the description matches, and I
can also invoke it by name. Descriptions are written narrowly, with explicit non-triggers, so
they do not fire during ordinary work.

**User** — invoked by name only (`disable-model-invocation: true`). These are broad or
file-writing workflows that should never start on their own.

## How the skills relate

Cross-references only exist where the dependency is real:

- `grill` → `grilling`
- `grill-and-document` → `grilling`, `domain-model`
- `architecture-review` → `module-design`; `domain-model` or `grilling` only when the review
  actually needs them
- `dont-reinvent-the-wheel` → `research` for external evidence · `grilling` when unresolved
  requirements would change the decision · `prototype` when practical fit must be validated ·
  `architecture-review` only for an explicitly requested broad reuse audit
- `deep-docs` → hands Apple documentation to `apple-docs`
- `research` → `apple-docs` or `deep-docs` when the question is documentation precision
- `debug` → `apple-docs` or `deep-docs` when a hypothesis depends on documented behavior

## Repository layout

```
<skill>/
├── SKILL.md                 # required: frontmatter + workflow
├── references/              # optional: loaded only when the workflow needs them
├── scripts/                 # optional: executable helpers
├── agents/openai.yaml       # optional: agent-specific metadata
├── LICENSE                  # when upstream code is vendored
└── THIRD_PARTY_NOTICES.md   # when upstream code is vendored or adapted
```

Conventions for changing anything here live in [AGENTS.md](AGENTS.md).

## Credits and licensing

These are personalized forks, not mirrors. Behavior was deliberately changed — corporate
process, ticket and tracker workflows, required subagents, and vendor lock-in were removed, and
safety boundaries were tightened. Bugs in this collection are mine, not the upstream authors'.

| Upstream project | Author | License | Used by |
| --- | --- | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Matt Pocock | MIT | The 13 engineering and productivity skills above |
| [Ahrentlov/apple-docs-skill](https://github.com/Ahrentlov/apple-docs-skill) | Patrick Ahrentløv | MIT | `apple-docs`, `deep-docs` |
| [Ahrentlov/appledeepdoc-mcp](https://github.com/Ahrentlov/appledeepdoc-mcp) | Patrick Ahrentløv | MIT | `deep-docs` (architecture reference only) |
| [felinto-dev/felinto-skills](https://github.com/felinto-dev/felinto-skills) | felinto-dev | not stated upstream | `dont-reinvent-the-wheel`, `grey-market` |
| [gccszs/disk-cleaner](https://github.com/gccszs/disk-cleaner) | Disk Cleaner Contributors | MIT | `disk-cleaner` |

Each vendored skill keeps its upstream `LICENSE` and a `THIRD_PARTY_NOTICES.md` recording the
imported revision and exactly what was changed.

Do not update these skills with `npx skills update` — it would overwrite the personalization.
Review upstream changes and port over only what is worth having.
