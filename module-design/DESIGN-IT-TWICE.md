# Compare Alternative Designs

Use this only for a consequential boundary where the first plausible interface may hide a poor tradeoff.

1. State the behavior, callers, dependencies, constraints, and compatibility requirements.
2. Sketch two or three materially different interfaces. Produce them sequentially or in parallel only when the current agent supports that safely; parallel execution is optional.
3. For each option, show a representative call site, owned behavior, dependency strategy, test seam, and migration cost.
4. Compare the options using the criteria in [SKILL.md](SKILL.md): interface size, ownership, cohesion, coupling, locality, dependency direction, testability, risk, and repository fit.
5. Recommend one option or a specific hybrid. Explain the rejected tradeoffs.

Stop once additional variants no longer expose a meaningful design difference.
