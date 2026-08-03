---
name: flow-define-product
description: Interview the owner to decide what a product is, who it serves, the job it does, and what it will deliberately never do, then record that as the durable definition every later decision is measured against. Use when starting a new project, when an existing one has no stated scope, or when repeated arguments about whether something belongs reveal that the boundary was never written down. Do not use for specifying one feature, planning an implementation, choosing a stack, or writing a marketing page.
disable-model-invocation: true
metadata:
  scope: project
  role: authoring
  mutation: docs
---

# Define Product

Decide what the product is and, just as deliberately, what it is not. The output is one short
document that later work is measured against: the description and topics `flow-setup-project`
needs, the boundary `flow-capture-issue` checks a request against, and the standard
`product-audit` audits the interface against.

This is the first step of the delivery flow. It defines the product, never the solution. No stack,
no architecture, no schema, no screens.

## Workflow

1. Inspect whatever already exists before asking anything: the README, any existing guidance, the
   code, the issues, and a landing page if there is one. An existing project usually has an
   implicit definition that only needs to be made explicit and consistent. Bring the contradictions
   you find into the interview rather than resolving them alone.
2. Run the interview through `grilling`, one decision at a time, each with a recommendation. Cover
   the sections below in order, because each constrains the next.
3. When a term turns out to be overloaded or contested, route to `domain-model` and keep its
   canonical meaning. Vocabulary belongs there, not here.
4. When a whole capability might not need building at all, route to `dont-reinvent-the-wheel`
   before it becomes part of the definition. A product defined around something it should have
   bought is expensive to undo.
5. Write the document, then read it back to the owner as a summary of what was decided and what
   was ruled out.

## What the definition contains

- **What it is.** One sentence a stranger understands, naming the thing and the job it does.
- **Who it is for.** The specific person and the situation they are in. "Everyone" is not an
  answer; it is the absence of one.
- **The job.** What that person is trying to get done, and how they cope today without this. If
  the current workaround is fine, say so; that is a finding, not a failure.
- **What it does.** The capabilities that make it worth using, at the level of outcomes rather
  than features.
- **What it will never do.** The explicit non-goals, each with the reason. This is the section that
  earns the document. A non-goal that carries no reason will be reopened in three months.
- **How you know it worked.** The observable signal that the product does its job, stated so that
  a later disagreement about success has an answer.
- **Constraints.** What is fixed and not up for negotiation: platform, privacy, budget, offline
  behavior, regulation, existing systems it must live with.

Include only the sections that carry a real decision. An empty heading is worse than an absent
one, because it looks answered.

## Boundaries

Do not turn this into a specification. It states what the product is; individual requirements,
acceptance criteria, and edge cases belong to `flow-capture-issue`.

Do not choose a technology, a framework, an architecture, or a data model. If a constraint truly
forces one, record the constraint and the reason, not the choice.

Do not write marketing copy. This document is read by the owner and by agents, and both need a
statement that can be checked, not one that persuades.

Do not create issues, branches, or code.

## Where it goes

Use the path repository guidance configures, or `docs/product.md` when it configures none. Create
the file only when there is something decided to write in it.

`setup-agent-docs` records the path when the owner wants it somewhere else. This skill normally
runs before that, so choosing the default now and recording it later is the expected order.

## Completion

End by listing the first issues the definition implies, in the order they would have to happen,
with a one-line reason each. Do not create them; `flow-capture-issue` owns that, one at a time, and
it is the natural next step.

The definition is complete when a stranger could tell from it whether a proposed feature belongs,
every non-goal carries its reason, the constraints are the real ones rather than assumed ones, and
nothing in it commits to a solution.
