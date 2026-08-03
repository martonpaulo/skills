# Third-party notices

## mattpocock/skills (productivity/writing-great-skills)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/productivity/writing-great-skills`
- **Imported revision:** `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT

No upstream file is vendored. Upstream's `GLOSSARY.md` was not imported. `VALIDATION.md` is
original to this collection and has no upstream counterpart.

### What was adapted

Predictability as the reason skills exist, choosing the invocation policy deliberately rather than
by default, writing model-facing descriptions around distinct triggers with no synonym
duplication, progressive disclosure of reference material into linked files so the common path
stays small, keeping each meaning in a single place, and hunting no-ops sentence by sentence.

### What changed

**Reference became a workflow.** Upstream is entirely reference, by its own description. This
version is an ordered workflow around an explicit skill contract: objective, prerequisites,
invocation, workflow, safety boundaries, completion criteria, and validation. It ends by running
checks and reviewing the diff, which upstream does not do.

**The theoretical vocabulary was dropped.** Upstream builds a defined vocabulary in `GLOSSARY.md`
and uses it throughout: context load versus cognitive load, the information hierarchy as a ladder,
branches, leading words, router skills, and a failure-mode taxonomy of premature completion,
duplication, sediment, sprawl, no-op, and negation. That material teaches skill design well but
costs context on every run of a skill that mostly needs to produce a correct file. The practices it
justifies are kept; the terminology is not.

**Safety and cross-reference checks were added.** The skill now requires stating destructive,
publishing, Git, data, and scope limits specific to the skill being written, verifying that every
referenced skill is actually installed, and avoiding tool-specific instructions unless the skill
genuinely requires that tool. Upstream covers none of these.

**`VALIDATION.md` is new.** Structural and behavioral checks for a finished skill, written for this
collection.

### A deliberate divergence

Upstream's `Negation` failure mode argues against steering by prohibition and recommends prompting
the positive instead. This collection does the opposite in one specific place: skills that touch
destructive operations, credentials, publishing, or production code carry explicit `Must not`
lists. A guardrail that can be misread as a suggestion is not a guardrail. Upstream allows for this
by permitting a prohibition as a hard guardrail; here that exception is the standing rule for
safety boundaries and the positive framing is used everywhere else.
