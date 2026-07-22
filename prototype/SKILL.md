---
name: prototype
description: Build a small disposable experiment when executing code is the fastest reliable way to answer a concrete technical, behavioral, integration, state-management, or UI question. Do not use for normal production implementation.
---

# Prototype

Use a prototype only when a small executable experiment will produce better evidence than more discussion or ordinary implementation work.

A prototype may validate the practical fit of a candidate selected during a `dont-reinvent-the-wheel` decision; that skill retains ownership of the comparison and recommendation.

## Workflow

1. State the single question being tested.
2. Define the observable result that would answer it, including what would falsify the current assumption.
3. Inspect the relevant code, constraints, and existing tooling without changing production files.
4. Create the smallest experiment that exercises the uncertainty:
   - Inside a repository, use `.scratch/prototypes/<descriptive-slug>/` unless repository guidance configures another prototype path.
   - Outside a repository, create a uniquely named safe temporary workspace.
   - Reuse the project's runtime when practical, but keep the experiment isolated.
5. Run the experiment and record the actual observations. Adjust only when an observation reveals that the experiment cannot answer the stated question.
6. Report the answer, evidence, limitations, and every disposable file created.

Read [LOGIC.md](LOGIC.md) for logic, state, behavior, or integration experiments. Read [UI.md](UI.md) for visual or interaction experiments.

## Safety boundaries

- Never modify production files merely to make the prototype easier.
- Keep real data, credentials, and destructive integrations out of the experiment unless the question specifically requires a safe isolated substitute.
- Never silently integrate prototype code into production. Production adoption is separate implementation work with normal review and testing.
- Do not commit, publish, or push prototype artifacts unless the user explicitly requests it.

## Completion

The prototype is complete when the stated observation has answered the question or when the remaining evidence gap is explicit. Identify the disposable workspace so it can be removed safely.
