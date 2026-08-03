# Third-party notices

## mattpocock/skills (productivity/handoff)

- **Upstream repository:** https://github.com/mattpocock/skills
- **Upstream path:** `skills/productivity/handoff`
- **Imported revision:** `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- **Imported on:** 2026-07-22
- **Last checked against upstream:** 2026-08-03
- **Original author:** Matt Pocock
- **License:** MIT

No upstream file is vendored. The 16-line original was rewritten.

### What was adapted

Writing a document that lets a fresh agent continue the work, referencing existing artifacts by
path or URL instead of duplicating specs, plans, ADRs, issues, commits, and diffs, redacting
credentials and personal information, a suggested-skills section, user-invoked only, and treating
the argument as the next session's focus.

### What changed

**Destination.** Upstream writes to the operating system's temporary directory, explicitly not the
workspace. A handoff that the OS may delete is not durable, so this version writes to the
repository's configured handoff path, or `.scratch/handoffs/<timestamp>-<topic>.md` inside a
repository and `~/tools/handoffs/<timestamp>-<topic>.md` outside one, with a sortable timestamp
and a descriptive slug. The directory is created only when the handoff is actually written.

**Required content is enumerated.** Upstream describes the document as a summary of the
conversation. This version requires goal, current state, decisions made, assumptions and
constraints, relevant files and symbols, files modified, commands and tests run, test results,
known failures and risks, Git status and branch, and the exact next action. A summary of a
conversation is not the same artifact as an operational continuation note.

**Suggested skills are constrained.** Only skills that exist in this collection may be named.
Upstream could suggest anything, including skills the receiving agent does not have.

**Completion is checkable.** The skill reports the absolute path and confirms that the next action
is specific enough to execute safely.
