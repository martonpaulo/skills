# ADR Format

Follow the repository's existing ADR convention. If none exists, use the configured directory or `docs/adr/` and a descriptive sequential filename such as `0001-use-domain-events.md`.

```markdown
# Decision title

## Context

What constraint or tradeoff made a decision necessary.

## Decision

The chosen direction and the reason it fits the constraint.

## Consequences

The important benefits, costs, and follow-up constraints.
```

Add considered alternatives only when their rejection will matter to a future reader. Do not create an ADR unless the decision is hard to reverse, surprising without context, and based on a real tradeoff.
