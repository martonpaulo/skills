---
name: domain-model
description: Clarify ambiguous domain terminology, states, rules, entities, and relationships when code, documentation, or requested behavior use inconsistent or overloaded language.
metadata:
  scope: project
  role: foundation
  mutation: docs
---

# Domain Model

Use this skill only when domain language or rules are ambiguous, contradictory, or consequential. Merely reading existing terminology does not require this skill.

## Workflow

1. Inspect repository guidance and existing glossaries, diagrams, decisions, code, tests, and public behavior relevant to the terms in question.
2. Compare requested behavior and documentation with the actual code. Surface contradictions instead of silently choosing one source.
3. Distinguish entities, value concepts, states, transitions, rules, ownership, and relationships only as far as the current ambiguity requires.
4. Prefer precise existing project terminology. When a term is overloaded, propose a canonical meaning and identify the concepts that need separate names.
5. Validate the model with concrete scenarios and edge cases.
6. If durable glossary changes are useful, update the path configured by repository guidance or default to `CONTEXT.md`.

## Glossary boundary

Create no glossary for a codebase without meaningful domain language. When one is useful, follow [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md) and keep it limited to canonical vocabulary, rules, states, and relationships. Exclude implementation plans, task lists, temporary notes, and specifications.

Assume one context unless the repository already shows clear, meaningful context boundaries. Preserve its existing multi-context structure when present.

## Consequential decisions

Create or propose an ADR only when a decision is difficult to reverse, surprising without context, and based on a real tradeoff. Follow repository conventions or [ADR-FORMAT.md](ADR-FORMAT.md). Most terminology clarifications do not need an ADR.

## Completion

The work is complete when the material ambiguity is resolved or explicitly remains open, contradictions are visible, and any durable edits contain only canonical domain knowledge.
