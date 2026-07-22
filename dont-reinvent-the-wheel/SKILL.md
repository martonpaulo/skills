---
name: dont-reinvent-the-wheel
description: Evaluate whether a specific requested software capability should use an existing project feature, native platform capability, maintained dependency, open-source project, external service, hybrid approach, or custom implementation. Use for explicit build-versus-reuse decisions or when evaluating replacements for one identified custom capability. Do not use for general research, architecture reviews, codebase-wide audits, implementation work, debugging, or requirements interviews.
---

# Don't Reinvent the Wheel

Decide whether one specific software capability should be reused, integrated, bought, adapted, or built from scratch. Keep custom implementation as a real option; reuse is valuable only when total cost and risk are lower.

Do not interrupt ordinary implementation for small utilities, domain-specific business logic, or choices the user has already settled. Use judgment based on likely effort, maintenance burden, risk, differentiation, and reversibility.

## Workflow

### 1. Identify the capability

Establish:

- the specific capability being evaluated;
- must-have behavior and non-negotiable constraints;
- the relevant stack, deployment context, and data boundary;
- whether the capability is product differentiation or table stakes.

Use explicit assumptions for small uncertainties. If unresolved requirements would materially change the candidate set or decision, use or recommend `grilling`; do not reproduce an interview workflow here.

### 2. Inspect the repository first

When repository context is available, inspect manifests, lockfiles, current dependencies, framework and platform configuration, infrastructure and deployment configuration, existing abstractions, and code that may already provide the capability. Never recommend adding what the project already has.

### 3. Consider the option ladder

Evaluate in this default order:

1. existing project capability;
2. native language, framework, SDK, database, cloud, or platform capability;
3. current dependency already installed;
4. maintained package or library;
5. maintained open-source or self-hosted project;
6. external service or SaaS;
7. hybrid approach;
8. custom implementation.

This is a heuristic, not a rule. Prefer custom work when it is simpler, safer, domain-specific, strategically differentiating, or avoids excessive integration complexity.

Detect the actual stack before external discovery. Read [discovery-sources.md](references/discovery-sources.md) only when external candidates or current ecosystem facts need investigation.

### 4. Verify external evidence

Use or recommend `research` when the decision depends on current candidates, APIs, compatibility, maintenance, releases, advisories, pricing, licenses, deprecation, or platform support. `dont-reinvent-the-wheel` owns the decision; `research` owns deeper external evidence gathering.

When formal skill invocation is unavailable, apply the same evidence standard directly: use current web research when available, prefer primary sources, verify important claims, check dates, and separate confirmed facts from inference and uncertainty. Community sources may reveal candidates or risks, but verify consequential claims through primary sources when possible. When web access is unavailable, state that current external facts remain unverified.

Never fabricate a package, API, price, license, compatibility claim, security status, or maintenance signal.

Use `apple-docs` to verify whether an Apple platform already provides the capability. Use `deep-docs` to verify native, framework, SDK, API, or version-specific capabilities elsewhere. This skill retains ownership of the build-versus-reuse decision.

Read [marketplace.md](references/marketplace.md) only when commercial source-code products are genuinely plausible for the detected stack, capability, ownership requirements, integration model, security posture, and license needs.

### 5. Compare with custom implementation

Always retain custom implementation as the baseline. Compare only criteria material to the decision, including:

- code and glue work still required;
- migration and rollback work;
- operational ownership and upgrade burden;
- security, privacy, license, and pricing implications;
- vendor or project health and lock-in;
- data ownership, export, and exit path;
- long-term maintenance;
- strategic differentiation.

Read [scorecard.md](references/scorecard.md) for material comparisons, confidence, effort sizing, optional scoring, and replacement safety. A failed must-have requirement disqualifies a candidate regardless of its aggregate score.

If practical fit remains the strongest uncertainty—such as undocumented behavior, performance, SDK ergonomics, UI embedding, migration complexity, glue code, framework compatibility, or native-platform support—recommend `prototype`. Do not build the experiment as part of this decision unless the user separately requests implementation and that workflow takes over.

### 6. Lead with the decision

Use exactly one decision label:

- `Use existing project capability`
- `Use native platform capability`
- `Use maintained dependency`
- `Use open-source or self-hosted solution`
- `Use external service`
- `Use hybrid approach`
- `Prototype before deciding`
- `Build custom`
- `Insufficient evidence`

Read [recommendation.md](references/recommendation.md) for concise and detailed output shapes. Use the smallest candidate set and output that support a defensible decision.

## Explicit reuse audits

Read [reuse-audit.md](references/reuse-audit.md) only when the user explicitly requests a reuse audit, replacement audit, or audit of custom capabilities. For a broad codebase-wide audit, use or recommend `architecture-review`; apply this skill only to the individual build-versus-reuse decisions inside that broader review.

## Safety and completion

Do not change production code, remove existing behavior, purchase a product, or start a migration as part of this decision. Replacement remains unapproved until must-have behavior, migration, rollback, licensing, security, and exit paths are verified.

The decision is complete when it states the option, rationale, main tradeoff, confidence, material assumptions, and any verification still required.
