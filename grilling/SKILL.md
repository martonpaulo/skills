---
name: grilling
description: Interview the user one decision at a time to resolve material uncertainty in a plan or design before implementation. Use only when unresolved choices could significantly affect behavior, scope, architecture, data, security, compatibility, or user experience.
metadata:
  scope: project
  role: foundation
  mutation: none
  upstream: https://github.com/mattpocock/skills
  upstream-author: Matt Pocock
  upstream-path: skills/productivity/grilling
  upstream-revision: ed37663cc5fbef691ddfecd080dff42f7e7e350d
  upstream-checked: 2026-08-03
  version: mattpocock-personal.1
---

# Grilling

Use this discipline to pressure-test a plan or design when important choices remain. Skip it when the task is concrete, low-risk, local, and reversible.

## Interview loop

1. Inspect the codebase, documentation, and environment first. Answer factual questions from evidence instead of asking the user.
2. Map the unresolved decisions and their dependencies. Start with prerequisites that constrain later choices.
3. Ask exactly one question at a time and wait for the answer.
4. Explain why the question matters when that is not obvious.
5. Offer a recommended answer with concise reasoning and the key tradeoff.
6. Update the shared understanding after each answer, then ask the next material question.

Focus on decisions that materially affect behavior, scope, architecture, data, security, compatibility, user experience, or irreversible cost. Use established project conventions for reversible preferences instead of questioning the user.

Stop when the remaining uncertainty can be handled by reasonable, reversible implementation choices. Do not continue for exhaustiveness.

## Recording what the interview settles

By default the outcome is the summary below and nothing else. Two answers earn a durable artifact,
and both belong to `domain-model`: a term that became canonical, and a decision that is hard to
reverse, surprising without context, and the result of a real tradeoff. Route there as the
interview settles them rather than at the end, so nothing survives only in the conversation.

Create no other artifact. An interview does not open issues, write plans, or produce
work-management records, whatever the caller intends to do afterwards.

## Completion

Conclude with a concise shared-understanding summary, assumptions, constraints, decisions, and any unresolved choices. Do not start implementation.
