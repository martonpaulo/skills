---
name: handoff
description: Write a compact durable handoff containing the exact context, decisions, modified files, verification, risks, and next action another agent or later session needs to continue safely.
argument-hint: "Focus or topic for the next session"
disable-model-invocation: true
metadata:
  scope: project
  role: authoring
  mutation: docs
  upstream: https://github.com/mattpocock/skills
  upstream-author: Matt Pocock
  upstream-path: skills/productivity/handoff
  upstream-revision: ed37663cc5fbef691ddfecd080dff42f7e7e350d
  upstream-checked: 2026-08-03
  version: mattpocock-personal.1
---

# Handoff

Create a durable continuation note only when the user invokes this skill.

## Destination

Use the repository's configured handoff path when available. Otherwise:

- inside a repository: `.scratch/handoffs/<timestamp>-<topic>.md`;
- outside a repository: `~/tools/handoffs/<timestamp>-<topic>.md`.

Use a sortable local timestamp and a short descriptive slug. Create the destination directory only when writing the handoff.

## Required content

- goal;
- current state;
- decisions already made;
- assumptions and constraints;
- relevant files and symbols;
- files modified;
- commands and tests run;
- test results;
- known failures, risks, or uncertainty;
- Git status and branch when relevant;
- exact next action.

Keep the document compact and operational. Reference existing artifacts instead of copying them or the full conversation. Redact credentials, secrets, and unnecessary personal information. If suggested skills would materially help, name only skills from this personalized collection.

## Completion

Report the absolute handoff path and confirm that the next action is specific enough to execute safely.
