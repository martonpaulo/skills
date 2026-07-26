# AGENTS.md

Guidance for agents working **on** this repository. It is not a skill and is not loaded as one.

## What this is

A personal collection of Agent Skills. Every skill is either a personalized fork of an open
source skill or written for this collection. Personalization is the point: upstream is a
starting position, not a spec.

## Taxonomy

Every skill is classified on two independent axes, declared in frontmatter and mirrored by the
[README.md](README.md) catalog.

**`scope`** is where the skill acts.

- `project` acts on a codebase.
- `personal` acts on the owner's machine or life. Never configured by `setup-agent-docs`, never
  referenced from repository conventions, never treated as part of a project workflow.
- `meta` acts on the skills and the agent setup themselves.

**`role`** is what the skill does in the flow.

- `setup` prepares an environment or agrees a convention.
- `foundation` is a reusable capability other skills delegate part of their work to.
- `workflow` performs one concrete task with a start, a process and a finish.
- `audit` inspects what exists and ranks findings, without implementing them.
- `authoring` produces a durable artifact as its main output.
- `utility` performs an operational task outside any project.

Frequency of use is not a category and must not become one. A skill invoked twice a year is
still whatever role it performs.

Roles overlap by design. When two fit, pick the one that describes the skill's **main output**:
`handoff` interviews nothing and produces a note, so it is `authoring`, not `workflow`.

**`mutation`** is a separate property, not a role. It states how far the skill may go:
`none`, `temporary` (disposable files, all reported), `docs` (documentation only, never
production code), `write` (project code or configuration), `approval-gated` (nothing without a
confirmed per-item decision). Declare the maximum the skill is permitted, not the common case.

Invocation is already expressed by `disable-model-invocation`, and effort levels by the skill's
own arguments. Neither is duplicated into `metadata`; a second copy is a drift bug.

## Hard rules

- **English only.** Skill content, frontmatter, documentation, filenames, comments, code, error
  messages, examples. The exception is a foreign-language search term or glossary entry that
  exists *because* it is foreign; those stay in the source language.
- **Credit upstream.** A skill derived from someone else's work carries its upstream `LICENSE`
  when code is vendored, plus a `THIRD_PARTY_NOTICES.md` naming the repository, the imported
  revision, the original author, the license, and specifically what was changed and removed.
  Update the README table and [NOTICE.md](NOTICE.md) too. Never present someone else's work as
  original.
- **Do not invent capabilities.** Do not document an API, a flag, or a behavior without running
  it. If an upstream script is broken, fix it or drop it. Never ship it documented as working.
- **No required ceremony.** No skill may require issue trackers, tickets, labels, backlogs,
  branches, pull requests, subagents, background execution, Docker, or a specific vendor. Those
  may be optional accelerators with a working fallback.
- **Preserve safety boundaries.** Never weaken an existing guard on destructive operations,
  commits, pushes, force-pushes, credentials, or production code. Tightening is welcome.
- **One responsibility per skill.** If a skill is growing a second job, that is a new skill or a
  cross-reference, not a longer `SKILL.md`.
- **Cross-reference only real dependencies**, and only to skills that exist here. A reference to
  an uninstalled or renamed skill is a bug.
- **Do not hardcode the shape of things.** Directory contents, the skill list, and counts all
  change. Read what is on disk instead of trusting a description of it, and avoid writing
  documentation that goes stale the next time a skill is added.

## Skill structure

`SKILL.md` is the only required file, and its frontmatter `name` must match the directory name
exactly. Everything else is optional and belongs inside the skill's own directory: reference
documents loaded on demand, executable scripts, agent-specific metadata, and the licensing and
attribution files required when upstream work is vendored.

Skill directories stay **flat**, one level under the repository root. Do not group them into
`audits/`, `workflows/` or any other folder: the taxonomy is metadata, and nesting would only
break paths, cross-references, and copying a single skill elsewhere.

Read a few existing skills before adding one. They are the current example of the shape, and
they are authoritative in a way this file cannot be.

### Frontmatter

```yaml
---
name: <matches the directory name>
description: <what it does, when to use it, and when NOT to>
disable-model-invocation: true   # user-invoked skills only
license: MIT                     # when upstream code is vendored
allowed-tools: "Bash(python3:*)" # when the skill ships executable scripts
metadata:
  scope: project | personal | meta
  role: setup | foundation | workflow | audit | authoring | utility
  mutation: none | temporary | docs | write | approval-gated
  upstream: <url>                  # when derived from someone else's skill
  upstream-author: <name>
  version: <upstream>-personal.N
---
```

`scope`, `role` and `mutation` are required on every skill and defined under
[Taxonomy](#taxonomy). A skill that ships its own effort or depth levels declares them where
they are actually implemented, through `argument-hint` and the workflow, not as inert metadata.

`description` is the whole triggering mechanism. Write narrow triggers and state the
non-triggers explicitly. A description that fires during ordinary implementation work is a
defect. User-invoked skills (broad reviews, interviews, file-writing workflows) set
`disable-model-invocation: true`. A narrow child workflow that must be called by an already
user-invoked parent leaves the field absent, names both the direct and delegated triggers in its
description, and may not exceed the mutation already authorized by the parent.

Note that the official skill validator predates `disable-model-invocation` and `argument-hint`
and rejects both. That is a validator limitation, not a reason to remove the fields.

### Content

Keep `SKILL.md` operational: purpose, workflow, safety boundaries, completion criteria. Push
detail into reference files so it loads only when needed. Prefer short instructions to
philosophy, and delete anything that duplicates another skill or restates a generic rule the
agent already follows.

## Adding or adapting a skill

1. Clone the upstream source to a temporary directory and read all of it, including the code and
   not just the docs.
2. If the repository is clean, commit the untouched import first as
   `chore: import <name> upstream baseline`. It makes the personalization diff reviewable.
3. Personalize: rewrite the description, strip ceremony and vendor lock-in, translate to
   English, tighten safety, drop broken or out-of-scope files.
4. Classify it: `scope`, `role` and `mutation`, decided from what the finished skill actually
   does rather than from what upstream called it.
5. Run whatever the skill ships: scripts, tests, diagnostics. Report what you actually ran.
6. Write `THIRD_PARTY_NOTICES.md` and keep the upstream `LICENSE`.
7. Update `README.md` (the table for its role, and the relationships) and `NOTICE.md`.
8. Commit with a focused message and push.

Installing a skill into a particular agent is the owner's local concern and is not tracked here.

## Validation before committing

- Every skill directory has a `SKILL.md` whose frontmatter `name` matches the directory.
- Every description states both triggers and non-triggers.
- Every skill declares `scope`, `role` and `mutation`, using only the documented values.
- The declared `mutation` is not narrower than what the skill's workflow actually permits.
- The invocation policy matches what the README claims.
- Every relative Markdown link resolves.
- No reference to a renamed, uninstalled, or upstream-only skill name.
- Python compiles (`python3 -m compileall -q <skill>`) and the skill's own tests pass.
- No file left with a non-English user-facing string.
- README tables match the skill directories actually on disk.

## Git

Commit only files related to the change at hand. Conventional-commit prefixes (`feat:`, `fix:`,
`refactor:`, `chore:`, `docs:`). Push to `origin main` when the work is complete and validated.
Never force-push. Keep `__pycache__` and editor scratch files out of commits; they are ignored.
