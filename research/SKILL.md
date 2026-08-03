---
name: research
description: Research a technical or product question using high-trust primary sources when a decision depends on current documentation, external evidence, compatibility details, standards, or verified behavior.
metadata:
  scope: project
  role: foundation
  mutation: docs
  upstream: https://github.com/mattpocock/skills
  upstream-author: Matt Pocock
  upstream-path: skills/engineering/research
  upstream-revision: ed37663cc5fbef691ddfecd080dff42f7e7e350d
  upstream-checked: 2026-08-03
  version: mattpocock-personal.1
---

# Research

Use this skill when external evidence or current documentation materially affects a decision. For questions answerable from the local codebase alone, inspect the code directly.

For a build-versus-reuse decision, gather and verify external evidence here while `build-or-reuse` owns the recommendation.

Use `apple-docs` for authoritative Apple development documentation, `deep-docs` for precise version-aware software documentation, and `context7` when an indexed snippet of a library's current API settles the point. This skill retains broader external investigation, comparisons, current events, product questions, academic evidence, and questions spanning multiple source types.

## Workflow

1. Define the question, decision it informs, and any version, platform, or date constraints.
2. Search primary sources first: official documentation, specifications, standards, source code, release notes, first-party APIs, and original research.
3. Verify information that may have changed. Record source dates and applicable versions when they matter.
4. Cross-check consequential claims against a second authoritative source or the referenced implementation when practical.
5. Separate the result into:
   - confirmed facts supported by sources;
   - reasonable inferences, labeled as such;
   - uncertainty, conflicts, or missing evidence.
6. Return a concise answer with citations or precise source references.

## Persistence

Return findings in the conversation by default. Persist them only when they are likely to be reused or the user requests a durable artifact. Follow an existing repository convention; otherwise use `docs/research/<descriptive-topic>.md`. Create the directory only when writing the document.

## Completion

Research is complete when the decision-relevant claims are cited, current where necessary, and explicit about remaining uncertainty. Do not modify production code as part of research.
