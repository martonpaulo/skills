---
name: skill-authoring
description: Create, review, or simplify Agent Skills with precise triggers, focused workflows, explicit safety boundaries, useful completion criteria, valid frontmatter, and minimal unnecessary context.
disable-model-invocation: true
metadata:
  scope: meta
  role: authoring
  mutation: write
  upstream: https://github.com/mattpocock/skills
  upstream-author: Matt Pocock
  upstream-path: skills/productivity/writing-great-skills
  upstream-revision: ed37663cc5fbef691ddfecd080dff42f7e7e350d
  upstream-checked: 2026-08-03
  version: mattpocock-personal.1
---

# Skill Authoring

Use this user-invoked skill to create a new Agent Skill or improve an existing one. Optimize for predictable behavior, narrow responsibility, and low context cost.

## Workflow

1. Inspect the existing skill, supporting files, nearby skills, and repository guidance. Preserve useful behavior and identify stale references before editing.
2. Define the skill contract:
   - **Objective:** the single outcome the skill owns.
   - **Prerequisites:** evidence, files, tools, or state required to begin.
   - **Invocation:** who should trigger it and under what narrow conditions.
   - **Workflow:** ordered actions that materially change agent behavior.
   - **Safety boundaries:** destructive, publishing, Git, data, and scope limits specific to the skill.
   - **Completion criteria:** observable conditions for a finished run.
   - **Validation:** structural and behavioral checks for the skill itself.
3. Choose invocation policy:
   - **Model-invoked:** omit `disable-model-invocation`; write a narrow description containing positive trigger conditions and explicit non-triggers when accidental activation is plausible.
   - **User-invoked:** set `disable-model-invocation: true`; write a concise human-facing description.
4. Put the common workflow in `SKILL.md`. Move branch-specific reference material to clearly named
   supporting files only when that reduces the context needed for ordinary runs. If the skill is
   self-contained, create a zero-byte `references/.keep` as the repository's Antigravity
   compatibility shim; remove the marker when real reference files are added.
5. When the skill is adapted from someone else's work, record its provenance. See [Provenance](#provenance).
6. Remove no-op instructions, promotional prose, stale assumptions, and generic rules already owned by repository guidance. Keep each meaning in one place.
7. Use cross-skill references only for real dependencies, and verify that every referenced skill is installed. Avoid tool-specific instructions unless the skill genuinely requires that tool.
8. Add examples only when they materially disambiguate behavior. Keep them short and adaptable.
9. Run the checks in [VALIDATION.md](VALIDATION.md) and review the final diff.

## Provenance

An adapted skill pins its upstream with a commit and a date, never a branch name. A branch moves and the claim silently becomes false.

```yaml
metadata:
  upstream: https://github.com/owner/repo   # repository URL, not a /tree/<branch>/ deep link
  upstream-author: Author Name
  upstream-path: skills/engineering/thing   # omitted when the skill is the repository root
  upstream-revision: <full 40-character SHA in the upstream repository>
  upstream-checked: <YYYY-MM-DD>
```

The five fields travel together and answer two different questions.

`upstream-revision` answers what changed. It is the SHA in the **upstream** repository, not the SHA of the local baseline import commit, which is what makes drift measurable:

```bash
gh api "repos/<owner>/<repo>/commits?path=<upstream-path>&since=<date>" --jq 'length'
```

`upstream-checked` answers whether the skill is stale. It is the date of the last comparison against upstream, not the import date. Comparing and finding nothing changed advances this date on its own, with no other edit; a check that finds nothing is still worth recording, because only a recent date can answer the question.

Alongside the fields, write `THIRD_PARTY_NOTICES.md` naming the repository, the pinned revision, the author, the license, and specifically what was adapted, what changed, and what was deliberately not carried. Keep the upstream `LICENSE` when code is vendored. An upstream that publishes no license can still be adapted for personal use: say so plainly in the notice, attribute the author, and do not extend this repository's license over it.

When a skill draws on several upstreams, the frontmatter names the primary one and `THIRD_PARTY_NOTICES.md` is authoritative for the full set, pinning each separately.

A skill written from scratch carries no `upstream-*` fields.

## Completion

The skill is complete when its name and directory match, invocation is correct, references resolve, steps and boundaries are operational, completion is checkable, provenance is pinned when the skill is adapted, and unnecessary context has been removed.
