---
name: skill-authoring
description: Create, review, or simplify Agent Skills with precise triggers, focused workflows, explicit safety boundaries, useful completion criteria, valid frontmatter, and minimal unnecessary context.
disable-model-invocation: true
metadata:
  scope: meta
  role: authoring
  mutation: write
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
4. Put the common workflow in `SKILL.md`. Move branch-specific reference material to clearly named supporting files only when that reduces the context needed for ordinary runs.
5. Remove no-op instructions, promotional prose, stale assumptions, and generic rules already owned by repository guidance. Keep each meaning in one place.
6. Use cross-skill references only for real dependencies, and verify that every referenced skill is installed. Avoid tool-specific instructions unless the skill genuinely requires that tool.
7. Add examples only when they materially disambiguate behavior. Keep them short and adaptable.
8. Run the checks in [VALIDATION.md](VALIDATION.md) and review the final diff.

## Completion

The skill is complete when its name and directory match, invocation is correct, references resolve, steps and boundaries are operational, completion is checkable, and unnecessary context has been removed.
