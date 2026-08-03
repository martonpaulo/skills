# Token Rules

Classification rules for the declarations a design system owns. "Token" here means any declared
visual decision, whatever the project calls it: a token, a variable, a custom property, a theme
entry, a constant, a style.

These are audit rules. They classify and judge what exists; they never authorize an edit.

## The four layers

| Layer | Holds | May contain a literal | Signature of a defect |
| --- | --- | --- | --- |
| Primitive | The raw scale: the palette, the spacing steps, the type ramp, the radius set | Yes, this is the only place literals belong | A feature consumes it directly, skipping the semantic layer |
| Semantic | What a value means in this product: the role, the state, the intent | Only where no primitive expresses it | It aliases another semantic entry, adding no meaning |
| Component-scoped | A decision that belongs to one component and composes semantic entries | No | It is consumed by a component other than its owner |
| Stale | Nothing any more | Not applicable | It is still exported, so it looks alive |

A healthy system reads downward: a component consumes semantic entries, semantic entries compose
primitives, primitives hold the literals. Every skipped step is a finding, and the most common one
by far is a feature reaching straight past the semantic layer into the palette.

## Naming

A name is a claim about meaning, and a wrong name costs more than a missing one, because it is
consumed in good faith.

- A semantic name states role, state, or intent, not appearance. A name that describes what the
  value looks like locks the system to the current design and becomes a lie the first time the
  design changes.
- Two names for the same decision is the same defect as two decisions under one name. Both mean the
  ownership is unresolved.
- A name that survived a change of meaning is worse than either. Check that each name still matches
  what its call sites use it for.

## What does not belong in the system

Non-visual product decisions frequently drift into a token file because it is a convenient place to
put a constant. They are not visual decisions and they do not belong there:

- limits, thresholds, counts, page sizes, timeouts, retry counts
- feature flags and capability switches
- copy, labels, and messages
- routes, keys, and identifiers

Report these as misplaced, name the owner they should have, and keep them separate from the visual
findings. They inflate the apparent size of the system and hide the tokens that matter.

## Judging whether a token earns its place

A declaration earns its place when it has meaning that its value does not: when a reader learns
something from the name that the literal would not have told them, or when changing it in one place
is supposed to change every consumer.

It does not earn its place when it only renames a literal used exactly once, only forwards to
another entry of the same layer, or exists because a naming convention demanded a full set and the
missing members were filled in.

Neither case is severe on its own. Both matter when they are the pattern, because a system nobody
can hold in their head stops being consulted, and the bypass findings follow directly from that.

## States and themes

A visual decision that has states is not one decision. Check that the system covers the states the
product actually has, and report the ones expressed ad hoc at the call site instead: hover, focus,
pressed, selected, disabled, loading, empty, error, destructive.

The same applies to every theme, appearance, or density the product ships. A token declared for one
of them and hardcoded for the others is a bypass with a longer fuse: it looks correct until someone
switches modes.

Where a state or a theme is expressed only by color, note it. Whether that fails a user is
`interface-audit`'s finding, not this audit's, but the missing non-color cue is visible from the
declarations and is worth routing.

## Evidence rules

- Read call sites before classifying. A declaration's layer is determined by how it is consumed, not
  by which file it sits in or what it is called.
- Group by the decision, not by the line. Twelve call sites of one missing token are one finding.
- Separate verified from inferred. A token whose consumers you could not fully enumerate is
  `Unknown`.
- Never recommend a deletion without the safety checks in the skill's step 5.
