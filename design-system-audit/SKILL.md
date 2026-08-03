---
name: design-system-audit
description: Audit whether a codebase expresses one visual system, covering design-token ownership, hardcoded visual values that bypass the tokens, near-duplicate components that should be one composed component, and tokens that are stale or carry no meaning. Use only when the user explicitly invokes $design-system-audit for a read-only review of a project's tokens, styling layer, or component library. Not for judging the interface as a user experiences it, which belongs to interface-audit, and not for implementing tokens, extracting components, or choosing a design direction.
argument-hint: "[low|medium|high] [scope]"
disable-model-invocation: true
metadata:
  scope: project
  role: audit
  mutation: none
---

# Design System Audit

Judge whether the code expresses one visual system or several.

`interface-audit` judges the interface as a user perceives it: does this screen work. This audit
judges how that appearance is expressed in code: is there one owner for each visual decision, or is
the same decision restated in forty places with slightly different values. A product can look
perfectly consistent today and still fail this audit, and that is exactly the interesting case,
because it means consistency is being maintained by hand and will drift the moment nobody is
looking.

The unit of analysis is the **visual decision**: a color, a spacing step, a radius, a type style, a
duration, an elevation, a border. Every one of them has exactly one place it should be decided, and
this audit finds the ones that have zero or many.

## Depth

Take the first argument as the depth and the rest as the scope. Default to `medium`.

| Depth | Coverage | Finding cap |
| --- | --- | --- |
| `low` | Token bypass on the surfaces with the most reuse | 5 |
| `medium` | Low, plus token ownership, stale tokens, and duplicate components | 10 |
| `high` | Medium, plus naming coherence, state and theme coverage, and cross-surface root causes | 15 |

Depth narrows coverage. It never lowers the evidence bar and never relaxes the deletion-safety rule.

## 1. Locate the system

Find where visual decisions are supposed to live before judging where they actually live. Read what
the repository documents about its design system first; a documented convention always overrides an
inference made here.

The system may be a token file, a theme object, CSS custom properties, a style sheet, a constants
namespace, a component library, or a framework's own theming layer. Name what it is in this project.

Two outcomes are legitimate and both are reportable:

- **A system exists.** Map it: where decisions are declared, how they are consumed, and which layers
  are allowed to declare new ones.
- **No system exists.** Do not treat that as fifty findings. Report the de-facto system instead: the
  values that already repeat across the codebase and would become the tokens. That inventory is the
  finding, and it is worth more than a list of every literal.

## 2. Classify ownership

Read [token-rules.md](references/token-rules.md) and classify what the system declares. The four
categories that matter are primitive, semantic, component-scoped, and stale.

Two guards:

- **Do not infer a token's purpose from its name or namespace.** Read the call sites. A token named
  for a color that is used exclusively for a disabled state is a semantic token with the wrong name,
  which is a different finding from an unused primitive.
- **A token that only aliases another token of the same layer, adding no meaning, is not a token.**
  It is an extra hop that makes the system look richer than it is.

## 3. Find the bypass

A bypass is a visual decision made outside the system: a literal color, spacing value, radius,
duration, font size, opacity, border width, or breakpoint written where a token should have been
consumed.

Search for the literals rather than reading files end to end. What matters is not the count but the
pattern:

- **A repeated literal is one finding, not many.** Twelve places using the same undeclared value are
  one missing token with twelve call sites. Report it that way.
- **A near-miss is worse than a bypass.** Values that are almost but not quite a declared token are
  the strongest evidence that the system is not being consumed, and they are invisible to a reader
  looking at any single file.
- **Distinguish the layers.** A literal inside a token declaration is where literals belong. The same
  literal inside a feature view is the finding.
- **Some literals are correct.** A one-off value that genuinely belongs to a single component, and
  that nothing else should ever match, is not a bypass. Say why it is exempt rather than reporting
  it and letting the reader work it out.

## 4. Find the duplicate components

Things that are visually the same should be one component composed differently, not several
components that happen to agree.

Look for components that render the same structure with different props, differ only in a value
that could be a parameter, or were plainly copied and then diverged. Report each cluster once, with
the members, what actually differs between them, and what the composed component would take as its
parameters.

The reverse finding is also real and easier to miss: one component with a growing set of boolean
flags controlling unrelated appearances. That is several components wearing one name, and splitting
it is the correction.

Prefer the platform's own primitive over a custom component that reimplements it. A custom control
earns its place through a behavior the primitive does not have, never through appearance alone.

## 5. Verify deletion safety

**Absence of direct usage is not evidence that something is unused.** Before recommending that any
token, component, or style be deleted, check every one of these and say which you checked:

- derived declarations that consume it, including tokens defined in terms of it
- platform, theme, locale, or feature-flag guarded branches
- previews, stories, examples, fixtures, and documentation
- tests, including snapshots
- dynamic construction: names assembled at runtime from strings, maps, or configuration
- consumers outside this repository, when the system is published or shared

A candidate that survives all of them is a deletion recommendation. A candidate that fails any of
them is a dependency, not a corpse. A candidate you could not fully trace is reported as
`Unknown`, never as safe to delete.

## Audit independence

Each run is independent. Ignore earlier conversation context, previous conclusions of your own, and
any report or generated artifact from a previous audit run. Read the declarations, the call sites,
and the documented conventions only.

## Report

1. **Scope and coverage**: depth, the exact boundary audited, what the design system is in this
   project, and what was left unexamined.
2. **System map**: where visual decisions are declared, which layers may declare new ones, and how
   the layers compose. Include this even when the finding list is short.
3. **Ranked findings**: one table with the visual decision at stake, the location of the
   declaration and of the call sites, the evidence, the consequence if the pattern spreads,
   severity, confidence, and the smallest correction.
4. **Bypass clusters**: repeated literals and near-misses grouped by the decision they express, each
   with the token that should own it and every call site.
5. **Composition candidates**: component clusters that should become one, with what differs and what
   the parameters would be.
6. **Cleanup candidates**: with the deletion-safety checks that were run for each, and a separate
   list of candidates that could not be fully traced.
7. **Start here**: the single correction to make first, and why it outranks the rest.

Use `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` so `project-audit` can rank these against the other lenses.
Severity here is about how far the inconsistency will spread and how much it will cost to unwind,
not about how ugly it looks.

Every finding names a concrete location. Report no finding that rests on code you did not read.

## Boundaries

This audit inspects and reports. It never edits code, tokens, styles, components, or documentation,
never extracts a component, never deletes a token, and never creates issues, branches, commits, or
pull requests.

- **Whether the interface works for a user** is `interface-audit`. A contrast failure, an unreadable
  label, or a missing state is its finding, not this one.
- **Whether a boundary is right** is `module-design`. This audit reports that a decision has no
  owner; where the owner should live is that question.
- **Choosing the design direction** belongs to the product owner. This audit never recommends a
  different palette, type scale, or visual language. It reports that the project has more than one.

Turning a selected finding into work is `issue-capture`, one issue at a time. A report of twelve
bypass clusters is not a mandate for twelve issues.

## Completion

The audit is complete when the design system is named and mapped, every bypass is grouped by the
decision it expresses rather than listed per line, duplicate components are clustered with their
real differences, every deletion candidate carries its safety checks, exempt literals are explained
rather than omitted, coverage is honest about what went unexamined, and nothing was mutated.
