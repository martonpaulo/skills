# Third-party notices

## mattpocock/skills (engineering/setup-matt-pocock-skills)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/engineering/setup-matt-pocock-skills`
- **Imported revision:** `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT

No upstream file is vendored. None of upstream's seed templates were imported.

### What was adapted

The shape of the setup: explore the repository's current state before proposing anything, reuse
what already exists rather than assuming, present a draft before writing, ask only about what
exploration did not settle, record the result as one block in the repository's agent guidance,
update that block in place instead of appending a duplicate, and stay safe to run again.

### What was removed

Most of upstream's subject matter. It configures an issue tracker (GitHub, GitLab, local markdown,
or freeform), a five-label triage vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`,
`ready-for-human`, `wontfix`), and a domain-doc layout, then writes `docs/agents/issue-tracker.md`,
`docs/agents/triage-labels.md`, and `docs/agents/domain.md` from seed templates.

This collection may not require an issue tracker, tickets, labels, or a backlog as a precondition
for any skill, so none of that is configured here. The seed templates
(`issue-tracker-github.md`, `issue-tracker-gitlab.md`, `issue-tracker-local.md`,
`triage-labels.md`, `domain.md`) were not imported.

What remains is only the optional artifact paths: domain glossary, ADRs, research notes, handoffs,
and prototypes.

### What changed

**`AGENTS.md` is preferred, not `CLAUDE.md`.** Upstream edits `CLAUDE.md` when it exists and falls
back to `AGENTS.md`. This collection treats `AGENTS.md` as canonical and makes `CLAUDE.md` a
symbolic link to it, so the preference is reversed. `.gemini/rules/agents.md` is also recognized as
active guidance.

**Model-invocable on purpose.** Upstream is user-invoked. This version omits
`disable-model-invocation` because `project-setup` calls it as its final documentation step, and
the skill states that the parent's already-explicit setup request is what authorizes it and that
it authorizes nothing broader.

**Personal skills are explicitly out of scope.** The skill states that `disk-cleaner` and
`grey-market` act on the user's machine rather than a repository and never get paths, conventions,
or guidance configured for them. A repository has no authority over personal machine maintenance.

**No empty scaffolding.** Directories and files are created only when something is actually written
to them.
