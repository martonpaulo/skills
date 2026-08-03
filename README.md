# Agent Skills

> My personal collection of [Agent Skills](https://code.claude.com/docs/en/skills), ready for any
> skill-aware coding agent.

Most of these started as someone else's open source skill. Every one has been rewritten for how
I actually work: less process, narrower triggers, tighter safety.

**🙏 Every upstream project is credited in the tables below, with a link.** If a skill is useful
to you, the credit belongs to its original author.

> [!NOTE]
> Public so the work is inspectable, but tuned to one person. **Fork it, don't depend on it.**

---

## 🧭 How this is organized

Two independent axes. **Scope** is where a skill acts. **Role** is what it does in the flow.
Frequency is deliberately not a category: `resolve-conflicts` can go months unused and is still
a workflow.

| Scope | Acts on | Configured by `setup-agent-docs`? |
| --- | --- | --- |
| `project` | A codebase | Yes |
| `personal` | My machine and my life | No, on purpose |
| `meta` | The skills and the agent setup themselves | Not applicable |

A repository has no business configuring conventions for a skill that cleans my disk. The two
`meta` skills are listed under **Project skills** below, because that is where they run.

| Role | What it means |
| --- | --- |
| **Setup** | Prepares an environment or agrees a convention. Runs once in a while. |
| **Foundation** | A reusable capability other skills delegate part of their work to. |
| **Workflow** | One concrete task, with a start, a process and a finish. |
| **Audit** | Inspects what already exists and ranks findings. Proposes, does not implement. |
| **Authoring** | Produces a durable artifact as its main output. |
| **Utility** | An operational task outside any project. |

Both axes live in frontmatter, alongside a third property that is easy to get wrong by reading
prose alone:

```yaml
metadata:
  scope: project
  role: audit
  mutation: docs
```

`mutation` is how far a skill may go: `none`, `temporary` (disposable files, all reported),
`docs` (documentation only, never production code), `write` (project code or configuration),
`approval-gated` (nothing at all without a confirmed per-item decision).

Directories stay flat. The taxonomy is metadata, not a path, so every skill directory remains
copyable on its own.

---

## 🛠️ Project skills

### Setup

| Skill | Invocation | Writes | What it does | Upstream |
| --- | --- | --- | --- | --- |
| [`setup-agent-docs`](setup-agent-docs/) | Model or user | `docs` | Configure optional **per-repository paths** for glossaries, ADRs, research, handoffs and prototypes. | [mattpocock/skills → setup-matt-pocock-skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/setup-matt-pocock-skills) |
| [`setup-project`](setup-project/) | User | `write` | Bootstrap or align a repository's **identity, operating rules, Git policy, public metadata and applicable project foundations**. | Written for this collection. |

### Foundations

Reusable capabilities. Invocable directly, but their real job is being delegated to.

| Skill | Invocation | Writes | What it does | Upstream |
| --- | --- | --- | --- | --- |
| [`apple-docs`](apple-docs/) | Model or user | `none` | Version-aware **Apple platform documentation**: Apple docs, Swift Evolution, Xcode and project context, local Xcode docs, HIG, WWDC, release notes, signing and distribution. | [Ahrentlov/apple-docs-skill](https://github.com/Ahrentlov/apple-docs-skill) |
| [`context7`](context7/) | Model or user | `none` | **Quick library documentation** from the Context7 index through its CLI: resolve a library ID, then query one topic. Version-aware, and honest about being an index rather than a source. | [upstash/context7 → context7-cli](https://github.com/upstash/context7/tree/master/skills/context7-cli) |
| [`deep-docs`](deep-docs/) | Model or user | `none` | Version-aware **documentation research** for non-Apple frameworks, SDKs, APIs, CLIs and platforms, with source-linked evidence. | Written for this collection. Architecture adapted from [apple-docs-skill](https://github.com/Ahrentlov/apple-docs-skill) and [appledeepdoc-mcp](https://github.com/Ahrentlov/appledeepdoc-mcp) |
| [`domain-model`](domain-model/) | Model or user | `docs` | Clarify **contradictory domain terminology**, states, rules and relationships. | [mattpocock/skills → domain-modeling](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling) |
| [`grilling`](grilling/) | Model or user | `none` | The shared **interview discipline**: one decision at a time, always with a recommendation. | [mattpocock/skills → grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling) |
| [`prototype`](prototype/) | Model or user | `temporary` | Run a **disposable experiment** when executing code beats discussing it. | [mattpocock/skills → prototype](https://github.com/mattpocock/skills/tree/main/skills/engineering/prototype) |
| [`research`](research/) | Model or user | `docs` | Answer a technical or product question from **current primary sources**. | [mattpocock/skills → research](https://github.com/mattpocock/skills/tree/main/skills/engineering/research) |

### Workflows

| Skill | Invocation | Writes | What it does | Upstream |
| --- | --- | --- | --- | --- |
| [`backlog-curator`](backlog-curator/) | User | `write` | **Review the GitHub Issue backlog**: detect duplicates, obsolete issues, and delegate missing SDD phases. Ends on a Mermaid graph of the blocking order. | [github/gh-aw](https://github.com/github/gh-aw) (behavioral ref) |
| [`debug`](debug/) | Model or user | `write` | **Diagnose a hard bug**: reproduce, hypothesize, find the root cause, minimal fix, verify. | [mattpocock/skills → diagnosing-bugs](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs) |
| [`dont-reinvent-the-wheel`](dont-reinvent-the-wheel/) | Model or user | `none` | **Build or reuse?** Decide whether one capability should use an existing feature, a native capability, a dependency, a service, or custom code. | [felinto-dev/felinto-skills → dont-reinvent-the-wheel](https://github.com/felinto-dev/felinto-skills/tree/main/.agents/skills/dont-reinvent-the-wheel) |
| [`grill`](grill/) | User | `none` | **Pressure-test a plan** through a focused interview. Writes nothing. | [mattpocock/skills → grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) |
| [`implement-issue`](implement-issue/) | User | `write` | **Implement exactly one prepared GitHub Issue** by writing code, tests, and documentation. | [martonpaulo/tabelo](https://github.com/martonpaulo/tabelo), [openclaw/openclaw](https://github.com/openclaw/openclaw), [github/spec-kit](https://github.com/github/spec-kit) |
| [`module-design`](module-design/) | Model or user | `write` | Improve **module boundaries**, interfaces, dependency direction, cohesion and test seams. | [mattpocock/skills → codebase-design](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design) |
| [`resolve-conflicts`](resolve-conflicts/) | Model or user | `write` | Resolve a **merge, rebase or cherry-pick** by reconstructing the intent of both sides. | [mattpocock/skills → resolving-merge-conflicts](https://github.com/mattpocock/skills/tree/main/skills/engineering/resolving-merge-conflicts) |

### Audits

Read what exists, rank what is worth fixing, change nothing on their own.

| Skill | Invocation | Writes | What it does | Upstream |
| --- | --- | --- | --- | --- |
| [`architecture-review`](architecture-review/) | User | `docs` | Assess a codebase and **rank architecture improvements** against concrete code evidence. | [mattpocock/skills → improve-codebase-architecture](https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture) |
| [`bug-hunter`](bug-hunter/) | User | `temporary` | Find **verified functional, logic, runtime and security bugs** through an adversarial audit; never fixes them. | [codexstar69/bug-hunter](https://github.com/codexstar69/bug-hunter) |
| [`code-review`](code-review/) | User | `write` | **Validate exactly one pull request** against the controlling issue and repository rules. | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent), [SpillwaveSolutions/pr-reviewer-skill](https://github.com/SpillwaveSolutions/pr-reviewer-skill) |
| [`product-audit`](product-audit/) | User | `none` | Audit **UI, UX, accessibility and copy** at routed `low`, `medium` or `high` depth; never implements findings. | [jakubkrehel/skills](https://github.com/jakubkrehel/skills), [content-designer/ux-writing-skill](https://github.com/content-designer/ux-writing-skill), [Thecsiz/ux-critique](https://github.com/Thecsiz/ux-critique) |

### Authoring

| Skill | Invocation | Writes | What it does | Upstream |
| --- | --- | --- | --- | --- |
| [`capture-issue`](capture-issue/) | Model or user | `write` | **Convert a problem or request** into one canonical GitHub Issue (Specify, Clarify). | Written for this collection. |
| [`grill-and-document`](grill-and-document/) | User | `docs` | The `grill` interview, but **preserves** canonical domain language and consequential decisions. | [mattpocock/skills → grill-with-docs](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs) |
| [`handoff`](handoff/) | User | `docs` | Write a compact **continuation note** for another agent or a later session. | [mattpocock/skills → handoff](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) |
| [`plan-issue`](plan-issue/) | User | `write` | **Plan the implementation and tasks** for exactly one GitHub Issue. | [obra/superpowers](https://github.com/obra/superpowers) |
| [`skill-authoring`](skill-authoring/) | User | `write` | Create, review or simplify **Agent Skills**. | [mattpocock/skills → writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills) |

---

## 🏠 Personal skills

All `utility`. They act on my machine and my life, never on a repository.

| Skill | Invocation | Writes | What it does | Upstream |
| --- | --- | --- | --- | --- |
| [`disk-cleaner`](disk-cleaner/) | Model or user | `approval-gated` | **Audit a machine for reclaimable disk space**: caches, build artifacts, dependency stores, duplicates, leftovers from removed apps. Classifies everything by risk, cleans only what was approved. | [gccszs/disk-cleaner](https://github.com/gccszs/disk-cleaner) |
| [`grey-market`](grey-market/) | Model or user | `none` | **Find digital products far below the official price** in regional markets, through community sources instead of ordinary search. Locates sellers, never transacts. | [felinto-dev/felinto-skills → grey-market](https://github.com/felinto-dev/felinto-skills/tree/main/.agents/skills/grey-market) |

---

## ⚡ Invocation

**Model or user**
: The agent may load it on its own when the description matches, and I can invoke it by name.
Descriptions are narrow, with explicit non-triggers, so they stay quiet during ordinary work.
This also includes narrow child workflows that an already user-invoked parent explicitly delegates.

**User**
: By name only (`disable-model-invocation: true`). Broad reviews, interviews and file-writing
workflows that should never start on their own.

---

## 🔗 How they relate

Cross-references exist only where the dependency is real.

```mermaid
flowchart LR
  setup-project --> setup-agent-docs
  setup-project --> grilling
  setup-project -.current external evidence.-> research
  setup-project -.version-specific Apple setup.-> apple-docs
  setup-project -.version-specific non-Apple setup.-> deep-docs
  grill --> grilling
  grill-and-document --> grilling
  grill-and-document --> domain-model
  architecture-review --> module-design
  bug-hunter --> apple-docs
  bug-hunter --> deep-docs
  bug-hunter -.selected finding to fix.-> debug
  dont-reinvent-the-wheel --> research
  dont-reinvent-the-wheel --> prototype
  research --> apple-docs
  research --> deep-docs
  research --> context7
  debug --> deep-docs
  deep-docs -.Apple questions.-> apple-docs
  deep-docs -.an indexed snippet is enough.-> context7
  context7 -.Apple questions.-> apple-docs
  context7 -.an authoritative source is needed.-> deep-docs
  capture-issue --> grilling
  capture-issue -.when applicable.-> domain-model
  capture-issue -.when applicable.-> research
  plan-issue -.when Specify or Clarify is incomplete.-> capture-issue
  plan-issue -.when consequential decisions remain.-> grilling
  plan-issue -.when applicable.-> domain-model
  plan-issue -.when applicable.-> module-design
  plan-issue -.when applicable.-> research
  plan-issue -.when applicable.-> prototype
  plan-issue -.when applicable.-> dont-reinvent-the-wheel
  implement-issue -.when applicable.-> debug
  implement-issue -.when applicable.-> domain-model
  implement-issue -.when applicable.-> module-design
  implement-issue -.when applicable.-> research
  implement-issue -.when applicable.-> prototype
  implement-issue -.when applicable.-> dont-reinvent-the-wheel
  implement-issue -.when applicable.-> resolve-conflicts
  code-review -.investigation discipline.-> grilling
  backlog-curator --> capture-issue
  backlog-curator --> plan-issue
  backlog-curator -.for unresolved consequential conflicts.-> grilling
```

<details>
<summary>Conditional edges, spelled out</summary>

- `setup-project` delegates optional glossary, ADR, research, handoff and prototype path
  selection to `setup-agent-docs` after establishing the repository's root guidance. It uses
  `grilling` for the one-time setup decisions, `research` only for current external evidence,
  and `apple-docs` or `deep-docs` only for version-specific configuration.
- `architecture-review` reaches for `domain-model` or `grilling` only when the review actually
  needs them.
- `bug-hunter` routes versioned Apple behavior to `apple-docs` and other framework or library
  behavior to `deep-docs`; it hands a user-selected confirmed finding to `debug` only in a
  separate implementation task.
- `dont-reinvent-the-wheel` reaches for `grilling` when unresolved requirements would change the
  decision, and for `architecture-review` only on an explicitly requested broad reuse audit.
- `research`, `debug` and `dont-reinvent-the-wheel` route to `apple-docs` or `deep-docs` only
  when the answer depends on documented behavior.
- `context7` and `deep-docs` trade in both directions. Context7 is an index of other people's
  documentation, so it is the fast path for a library's current API, and `deep-docs` takes over
  whenever the conclusion has to be traced to an official versioned source, or the library is
  not indexed at all.
- `capture-issue` routes to `domain-model` or `research` only when existing ambiguity or missing evidence prevents capturing the issue.
- `plan-issue` delegates to `capture-issue` if the Specify/Clarify foundation is incomplete, and conditionally routes to specialized design/prototype skills when needed.
- `implement-issue` routes to specialized work skills (e.g., `debug`, `resolve-conflicts`) when they directly apply to implementing the single prepared issue.
- `backlog-curator` delegates missing phases for an issue to `capture-issue` or `plan-issue`.

</details>

---

## 📦 Using one elsewhere

Every skill directory is self-contained. Copy the one you want into your agent's or your
project's skills directory. Conventions for changing anything here live in
[AGENTS.md](AGENTS.md).

> [!WARNING]
> **Do not run `npx skills update` on these.** It would overwrite the personalization. Review
> upstream changes and port over only what is worth having.

### Sync all skills

The commands link every top-level skill directly into the corresponding agent directory, so
repository changes are available immediately without copying files. They are safe to run
repeatedly and can be called from any working directory:

```sh
/path/to/skills/sync-skills
/path/to/skills/sync-agents
/path/to/skills/sync-claude
```

`sync-skills` updates both `~/.agents/skills` and `~/.claude/skills`; the other two commands update
only their named destination. Use `--dry-run` to preview any command. Existing real files and
directories are reported as conflicts and left untouched.

To make the combined command available in zsh, link it from a directory already on `PATH`:

```sh
mkdir -p ~/.local/bin
ln -s /path/to/skills/sync-skills ~/.local/bin/sync-skills
```

---

## 📄 License

The original work here (the personalization, the docs, the references) is
[MIT licensed](LICENSE).

That grant covers my work only. Vendored upstream code keeps its own license, and it does not
extend to `dont-reinvent-the-wheel` or `grey-market`, whose upstream publishes no license at
all. [NOTICE.md](NOTICE.md) says exactly what applies to what.
