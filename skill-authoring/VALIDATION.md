# Skill Validation

## Frontmatter

- `SKILL.md` begins with valid YAML frontmatter.
- `name` exactly matches the directory name.
- `description` is concise and accurately states the trigger.
- User-invoked skills set `disable-model-invocation: true`.
- Model-invoked skills omit that field.
- Optional fields are supported and useful.

## Content

- The skill has one clear objective.
- Prerequisites, workflow, safety boundaries, completion criteria, and validation are present where relevant.
- Steps are actionable and ordered; completion is observable.
- Likely accidental triggers have explicit non-trigger guidance.
- Generic repository rules and duplicated meanings are removed.
- Supporting files are relevant and reachable from a precise context pointer.
- Examples clarify a real ambiguity.

## Provenance

Skip this section only for a skill written entirely from scratch.

- `THIRD_PARTY_NOTICES.md` exists and names the repository, revision, author, and license.
- The five `upstream-*` fields are present, with a full 40-character SHA and an ISO date.
- `upstream` is a repository URL, not a `/tree/<branch>/` deep link. No branch name stands in for a revision anywhere.
- `upstream-revision` is the SHA in the upstream repository, not the local baseline commit.
- The notice says what was adapted, what changed, and what was deliberately not carried, and every claim in it matches the files actually present.
- The upstream `LICENSE` is kept when code is vendored, and an unlicensed upstream is stated as such rather than covered by this repository's grant.
- `NOTICE.md` and the README list this skill consistently.

## References and safety

- Every relative link resolves.
- Every named skill or external tool is available or explicitly optional.
- Old names and stale workflows are absent.
- Git, publishing, destructive actions, secrets, and production changes have boundaries proportional to the skill's risk.

## Final review

Read the skill as a coding agent: verify that it can determine when to start, what to do, when to stop, and what it must leave untouched. Search the full skill directory for stale names after renames.
