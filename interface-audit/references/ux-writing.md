# UX Writing Pass

Use this reference at `medium` and `high` depth after the core pass. Review the complete flow vocabulary and state copy, not isolated strings in a vacuum.

## Establish the content system

1. Inspect nearby product copy, terminology, localization resources, and any voice or content guide.
2. Identify the user's goal, current knowledge, likely emotional state, and the stakes of the interaction.
3. Evaluate copy as purposeful, concise, conversational, and clear. Do not optimize one quality by damaging another.
4. Preserve intentional brand voice unless it causes ambiguity, inconsistency, translation risk, exclusion, or an inappropriate tone for the stakes.

## Review by element

- **Titles and headings:** orient the user and describe the current task or content.
- **Buttons and menu actions:** use a specific verb and object when needed; consequential confirmations repeat the consequence instead of relying on `OK`, `Yes`, or `Submit`.
- **Links:** describe the destination or result and remain understandable out of context.
- **Forms:** keep visible labels, use placeholders only as format examples, explain constraints before failure when practical, and place recovery text beside the problem.
- **Errors:** state what failed, preserve known facts, avoid blame or false certainty, and give the next available action. Do not guess a cause.
- **Empty and no-result states:** distinguish first use, user-cleared content, filters/search, permission, offline, and load failure; orient the user and provide a proportionate exit or next step.
- **Success and status:** confirm the result with enough specificity to remove doubt; avoid celebration that is disproportionate to the event.
- **Settings and permissions:** label the enabled state plainly, explain the user benefit before a permission request, and make consequences and reversibility clear.
- **Onboarding:** move toward first value, reveal complexity progressively, keep optional steps skippable, and use one vocabulary for advancing and finishing.

## Accessibility and localization

- Prefer plain, familiar words and direct sentence structure without flattening necessary domain language.
- Avoid idioms, culture-bound humor, unnecessary gender, device-specific verbs when multiple inputs are supported, and sentences assembled from fragments around variables.
- Check pluralization, interpolation, truncation, text expansion, bidirectional text, and screen-reader clarity when the implementation is available.
- Do not assign a reading grade, comprehension rate, or character benchmark unless the product defines it or the claim is independently verified for this audience.

## Finding contract

For every writing finding include:

- the complete current text and location;
- the complete proposed replacement in the product's language;
- the user's task or state;
- the comprehension, recovery, trust, accessibility, or consistency cost;
- any localization or implementation verification still required.

Consolidate repeated terminology or capitalization drift into one systemic finding. Do not rewrite copy that is already clear merely to impose a preferred voice.
