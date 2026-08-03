# Third-party notices

## mattpocock/skills (engineering/research)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/engineering/research`
- **Imported revision:** `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT

No upstream file is vendored. The 12-line original was rewritten.

### What was adapted

Primary sources over secondary write-ups, following every claim back to the source that owns it,
citing each claim, and matching the repository's existing convention for where such notes live.

### What changed

**Background agents are not required.** Upstream's first instruction is to spin up a background
agent so the user keeps working. This collection does not require background execution or
subagents, so the research runs in the current session.

**Persistence became conditional.** Upstream always writes a Markdown file. Here findings are
returned in the conversation by default and persisted only when they are likely to be reused or
the user asks, defaulting to `docs/research/<topic>.md` and creating the directory only when
actually writing.

**Evidence is graded.** Results are split into confirmed facts with sources, inferences labelled
as inferences, and remaining uncertainty or conflict. Consequential claims are cross-checked
against a second authoritative source. Source dates and applicable versions are recorded when they
matter. Upstream had none of this.

**Routing to the documentation specialists.** The skill now defers to `apple-docs`, `deep-docs`,
and `context7` where they own the question, and keeps broader investigation, comparisons, and
multi-source questions for itself.

**A boundary was added.** Research does not modify production code.
