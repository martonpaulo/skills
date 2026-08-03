# Focused Reuse Audit

Use this reference only when the user explicitly requests a reuse audit, replacement audit, or audit of custom capabilities that might use native or maintained solutions. Do not start a whole-application audit merely because no specific capability was provided.

## Workflow

1. Detect the stack from manifests, lockfiles, framework and platform configuration, infrastructure, deployment files, and current dependencies.
2. Identify custom capabilities with meaningful maintenance, security, operational, or non-differentiating cost.
3. Cite repository evidence using file paths and symbols.
4. Classify only high-value opportunities:
   - keep custom because it is differentiating, domain-specific, or already simpler;
   - use an existing project or native capability;
   - evaluate a maintained external candidate;
   - defer because evidence or requirements are insufficient.
5. Prioritize by expected payoff, migration risk, confidence, and approximate effort.
6. Produce recommendations, not automatic rewrites.

Preserve domain-specific and differentiating code. For each replacement opportunity, apply the replacement-safety rules in [scorecard.md](scorecard.md).

If findings expand beyond focused reuse decisions into boundaries, ownership, coupling, or broader restructuring, recommend `architecture-review`. That skill owns the broad assessment; `build-or-reuse` owns individual reuse decisions.

## Output

Report the detected stack, repository evidence, highest-value opportunities, areas to keep custom, risks, confidence, and next verification step. Keep the list short enough to investigate responsibly.
