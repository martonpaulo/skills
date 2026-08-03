---
name: setup-agent-docs
description: Configure lightweight per-repository conventions for the optional product definition, domain glossaries, ADRs, research notes, handoffs, and disposable prototypes. Use when the user directly requests these artifact paths or when project-setup delegates this step after establishing root guidance. Do not use for complete project setup, ordinary documentation edits, personal-skill configuration, trackers, tickets, labels, or backlog workflows.
metadata:
  scope: meta
  role: setup
  mutation: docs
  upstream: https://github.com/mattpocock/skills
  upstream-author: Matt Pocock
  upstream-path: skills/engineering/setup-matt-pocock-skills
  upstream-revision: ed37663cc5fbef691ddfecd080dff42f7e7e350d
  upstream-checked: 2026-08-03
  version: mattpocock-personal.1
---

# Setup Agent Docs

Run this setup once per repository when the user wants explicit paths for artifacts written by the project skills in this collection. The product definition usually already exists by then, because `project-setup` runs before `project-setup`; record where it actually is rather than moving it. It may be invoked directly or as the delegated final documentation step of `project-setup`, and it must remain safe to run again.

Keep this skill model-invocable because `project-setup` calls it through the agent's skill tool. The already explicit parent setup request authorizes this narrow documentation step; it does not authorize any broader project mutation.

Scope: only project skills produce repository artifacts. Personal-use skills such as `disk-cleaner` and `grey-market` operate on the user's machine, not on a repository, never configure paths, conventions, or guidance for them.

## Workflow

1. Inspect existing guidance and conventions before proposing anything:
   - `AGENTS.md`
   - `CLAUDE.md`
   - `.gemini/rules/agents.md`
   - `CONTRIBUTING.md`
   - existing architecture and documentation directories
   - existing glossary, ADR, research, handoff, and prototype paths
2. Reuse established paths where they are clear. Ask only which still-unconfigured artifact types the user actually wants.
3. Suggested defaults when no convention exists:
   - product definition: `docs/product.md`
   - domain glossary: `CONTEXT.md`
   - ADRs: `docs/adr/`
   - research: `docs/research/`
   - handoffs: `.scratch/handoffs/`
   - prototypes: `.scratch/prototypes/`
4. Show the short configuration block before writing it.
5. Record only selected conventions in existing repository guidance. Prefer `AGENTS.md`; use `CLAUDE.md` or `.gemini/rules/agents.md` when it is the repository's active agent guidance. If none exists, create `AGENTS.md` only with the user's selected conventions.
6. If a `## Agent skill paths` section already exists, update it in place. Preserve surrounding content and remove entries the user no longer wants.

Example block:

```markdown
## Agent skill paths

- Product definition: `docs/product.md`
- Domain glossary: `CONTEXT.md` (optional; create only when useful)
- Research notes: `docs/research/` (create only when persisting research)
- Handoffs: `.scratch/handoffs/`
- Prototypes: `.scratch/prototypes/`
```

## Safety and completion

Do not create empty files or directories. Do not introduce process configuration unrelated to these optional artifact paths. Setup is complete when the selected paths appear once in the active guidance file and a second run would update rather than duplicate the block.
