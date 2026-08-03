---
name: grill-and-document
description: Start a focused one-question-at-a-time interview that also preserves resolved domain vocabulary and genuinely consequential architectural decisions without creating tickets or implementing the plan.
disable-model-invocation: true
metadata:
  scope: project
  role: authoring
  mutation: docs
  upstream: https://github.com/mattpocock/skills
  upstream-author: Matt Pocock
  upstream-path: skills/engineering/grill-with-docs
  upstream-revision: ed37663cc5fbef691ddfecd080dff42f7e7e350d
  upstream-checked: 2026-08-03
  version: mattpocock-personal.1
---

# Grill and Document

Apply `grilling` for the interview and `domain-model` for terminology, business rules, and domain decisions.

## Workflow

1. Inspect repository guidance and existing glossary or ADR conventions directly. Respect configured paths when present; otherwise use the defaults defined by `domain-model` only when an artifact becomes useful.
2. Ask one material question at a time through `grilling`.
3. When terminology becomes canonical, write the glossary entry promptly. Keep glossary content limited to domain vocabulary, states, rules, and relationships.
4. Record an ADR only when the resolved decision is difficult to reverse, surprising without context, and based on a real tradeoff.
5. Continue until the remaining uncertainty is reversible and implementation-safe.

Do not turn `CONTEXT.md` into a specification. Do not create planning or work-management artifacts, and do not start implementation after the interview.

## Completion

End with the agreed understanding, files written, unresolved decisions, and recommended next action.
