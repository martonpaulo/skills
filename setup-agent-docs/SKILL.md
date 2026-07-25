---
name: setup-agent-docs
description: Configure lightweight per-repository conventions for optional domain glossaries, ADRs, research notes, handoffs, and disposable prototypes without setting up trackers, tickets, labels, or backlog workflows.
disable-model-invocation: true
---

# Setup Agent Docs

Run this user-invoked setup once per repository when the user wants explicit paths for artifacts written by the project skills in this collection. It must remain safe to run again.

Scope: only project skills produce repository artifacts. Personal-use skills such as `disk-cleaner` and `grey-market` operate on the user's machine, not on a repository, never configure paths, conventions, or guidance for them.

## Workflow

1. Inspect existing guidance and conventions before proposing anything:
   - `AGENTS.md`
   - `CLAUDE.md`
   - `CONTRIBUTING.md`
   - existing architecture and documentation directories
   - existing glossary, ADR, research, handoff, and prototype paths
2. Reuse established paths where they are clear. Ask only which still-unconfigured artifact types the user actually wants.
3. Suggested defaults when no convention exists:
   - domain glossary: `CONTEXT.md`
   - ADRs: `docs/adr/`
   - research: `docs/research/`
   - handoffs: `.scratch/handoffs/`
   - prototypes: `.scratch/prototypes/`
4. Show the short configuration block before writing it.
5. Record only selected conventions in existing repository guidance. Prefer `AGENTS.md`; use `CLAUDE.md` when it is the repository's active agent guidance. If neither exists, create `AGENTS.md` only with the user's selected conventions.
6. If a `## Agent skill paths` section already exists, update it in place. Preserve surrounding content and remove entries the user no longer wants.

Example block:

```markdown
## Agent skill paths

- Domain glossary: `CONTEXT.md` (optional; create only when useful)
- Research notes: `docs/research/` (create only when persisting research)
- Handoffs: `.scratch/handoffs/`
- Prototypes: `.scratch/prototypes/`
```

## Safety and completion

Do not create empty files or directories. Do not introduce process configuration unrelated to these optional artifact paths. Setup is complete when the selected paths appear once in the active guidance file and a second run would update rather than duplicate the block.
