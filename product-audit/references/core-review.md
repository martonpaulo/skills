# Core Product Review

Use this reference at every depth. Judge the product against its users, platform, stage, and established system before applying general preferences.

## Experience and task flow

- Identify the primary task and the intended first, second, and third actions. Flag hierarchy only when it competes with or obscures that path.
- Check whether labels, grouping, order, and affordances match the user's likely mental model and use the same concepts consistently across the flow.
- Trace every in-scope interaction through idle, active, loading, success, empty, error, disabled, and recovery states when those states can occur.
- Check system feedback, reversibility, interruption and re-entry, destructive consequences, and ownership handoffs. Do not invent states the product model does not require.
- Prefer one systemic finding for a shared component, token, or rule over repeated leaf-level symptoms.

## Layout and visual communication

- Check grouping, shared alignment edges, visual hierarchy, information density, progressive disclosure, and the distinction between controls and static content.
- Stress the layout against supported viewport changes, text expansion, dynamic data, zoom, safe areas, and right-to-left direction when relevant and observable.
- Evaluate typography, color, icons, surfaces, and motion by the meaning they communicate, not by a preferred aesthetic. Preserve deliberate platform conventions and established tokens when they remain usable.
- Treat visual polish as secondary to task, structure, semantics, feedback, and recovery. A different visual taste is not a finding.

## Accessibility

- Inspect semantic roles, accessible names and descriptions, heading and reading order, form labels and errors, keyboard reachability, focus visibility and movement, and screen-reader state announcements when evidence allows.
- Check target size and spacing, contrast, non-color cues, reduced motion, zoom/text resizing, and alternative content. Use the project's platform and accessibility requirements when documented.
- Never infer semantic or keyboard compliance from appearance alone. Never infer contrast from source tokens when compositing or runtime themes determine the rendered pair.
- Treat an inaccessible core task as `HIGH`; calibrate narrower failures by reach and consequence.

## Interface copy

- Check that actions use specific verbs, links name destinations, terms remain consistent, controls describe the state or action accurately, and consequential choices state their outcome.
- Errors must identify what failed and offer a realistic recovery path. Empty states must orient the user and offer a relevant next step when one exists.
- Match the product's existing voice and localization model. Cleverer or shorter wording is not automatically better.

## Evidence discipline

- Cite the current implementation or rendered state precisely and explain the user-visible consequence.
- Separate observed behavior from inferred risk. A source-only concern that depends on runtime is `Likely` at most until verified.
- Record unavailable states and tools in coverage. Do not convert missing evidence into a negative finding.
- Consolidate by root cause and prefer high-leverage recommendations that fit the existing system.
