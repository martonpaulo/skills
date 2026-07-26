---
name: grilling
description: Interview the user one decision at a time to resolve material uncertainty in a plan or design before implementation. Use only when unresolved choices could significantly affect behavior, scope, architecture, data, security, compatibility, or user experience.
metadata:
  scope: project
  role: foundation
  mutation: none
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

## Completion

Conclude with a concise shared-understanding summary, assumptions, constraints, decisions, and any unresolved choices. Do not start implementation.
