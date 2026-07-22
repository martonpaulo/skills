# Decision Criteria and Safety

Use only the criteria material to the specific capability:

- functional fit and must-have behavior;
- current-stack compatibility;
- API, webhook, SDK, embed, or extension surface;
- remaining code and glue complexity;
- maintenance activity, maturity, and documentation;
- security, privacy, and data ownership;
- license, pricing, and operational burden;
- migration effort, lock-in, export, and exit path;
- performance, latency, and accessibility when relevant;
- code and maintenance avoided;
- strategic differentiation.

## Confidence

- `HIGH`: important claims are verified through primary sources; functional fit and integration are clear; maintenance, security, license, pricing, migration, and exit path are acceptable.
- `MEDIUM`: fit is probable, but one or two material unknowns still require verification or a prototype.
- `LOW`: evidence is weak; maintenance, integration, license, lock-in, export, compatibility, or security has major uncertainty.

Do not make a `LOW`-confidence candidate the primary recommendation. Use `Insufficient evidence` when no defensible decision can be made.

## Approximate effort

- `XS`: under 1 hour
- `S`: under 1 working day
- `M`: 1–3 working days
- `L`: 4–10 working days
- `XL`: more than 10 working days or involving multiple systems

State major assumptions when effort affects the decision. Do not imply precision without inspecting the integration context.

## Replacement safety

When evaluating replacement of existing custom code:

- inspect current behavior and map must-haves to candidate capabilities;
- identify behavior that would be lost or changed;
- preserve public interfaces unless migration is explicitly accepted;
- prefer existing and native capabilities before adding dependencies;
- reject candidates that fail a must-have requirement;
- reject replacement when remaining glue is more complex than the current implementation;
- keep differentiating product behavior custom;
- verify license compatibility, maintenance, deprecation, security, data ownership, and export;
- define migration, rollback, and exit paths;
- keep existing code until the replacement is verified.

Evaluate parity against must-have behavior and migration risk, not a universal percentage.

## Optional weighted scoring

Use weighting only when several viable candidates remain and the tradeoffs benefit from an explicit comparison. Choose weights from the actual priorities, show the assumptions, and avoid decimal precision. A failed must-have requirement overrides the total score; the score supports judgment but never determines it alone.
