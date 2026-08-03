---
name: domain-model
description: Clarify ambiguous domain terminology, states, rules, entities, and relationships when code, documentation, or requested behavior use inconsistent or overloaded language.
metadata:
  scope: project
  role: foundation
  mutation: docs
  upstream: https://github.com/mattpocock/skills
  upstream-author: Matt Pocock
  upstream-path: skills/engineering/domain-modeling
  upstream-revision: ed37663cc5fbef691ddfecd080dff42f7e7e350d
  upstream-checked: 2026-08-03
  version: mattpocock-personal.1
---

# Domain Model

Use this skill only when domain language or rules are ambiguous, contradictory, or consequential. Merely reading existing terminology does not require this skill.

## Workflow

1. Inspect repository guidance and existing glossaries, diagrams, decisions, code, tests, and public behavior relevant to the terms in question.
2. Compare requested behavior and documentation with the actual code. Surface contradictions instead of silently choosing one source, and label each side as current behavior, current contract, or desired contract. Those three disagreeing is normal during a change; treating them as one is what produces a wrong model.
3. Distinguish entities, value concepts, states, transitions, rules, ownership, and relationships only as far as the current ambiguity requires. Separate them on two axes: what kind of concept it is, and how long it is meant to live. See [Data lifetime](#data-lifetime).
4. Prefer precise existing project terminology. When a term is overloaded, propose a canonical meaning and identify the concepts that need separate names.
5. Validate the model with concrete scenarios and edge cases.
6. If durable glossary changes are useful, update the path configured by repository guidance or default to `CONTEXT.md`.

## Data lifetime

Sort every piece of state into one of four kinds. Most arguments about what belongs in the model are really a disagreement about which of these something is:

- **Canonical.** The single source of truth. Losing it loses user work, so it survives reload, migration, and export.
- **Reconstructible projection.** Derived from canonical data and rebuildable at any time. It is a cache, and it must never be edited as if it were the original.
- **Transient state.** Alive only for the current session or interaction, such as an in-progress draft, a selection, or a pending validation result.
- **Local preference.** Belongs to this user on this machine, and never to the document. Two people opening the same thing may legitimately differ.

The glossary describes the canonical layer. A projection earns an entry only when it has its own name in the domain, and a preference never does; recording one there is how a display setting turns into a fake business rule.

Keep one owner for every rule and mapping. When a change replaces a model, delete the vocabulary and code paths it supersedes in the same change, so the old meaning cannot outlive the decision.

## Glossary boundary

Create no glossary for a codebase without meaningful domain language. When one is useful, follow [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md) and keep it limited to canonical vocabulary, rules, states, and relationships. Exclude implementation plans, task lists, temporary notes, and specifications.

Assume one context unless the repository already shows clear, meaningful context boundaries. Preserve its existing multi-context structure when present.

## Consequential decisions

Create or propose an ADR only when a decision is difficult to reverse, surprising without context, and based on a real tradeoff. Follow repository conventions or [ADR-FORMAT.md](ADR-FORMAT.md). Most terminology clarifications do not need an ADR.

## Completion

The work is complete when the material ambiguity is resolved or explicitly remains open, contradictions are visible, and any durable edits contain only canonical domain knowledge.
