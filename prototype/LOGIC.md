# Logic, State, and Integration Experiments

Use this shape when the uncertainty concerns behavior, state transitions, data shape, concurrency, performance characteristics, or an integration contract.

## Practical shapes

- A direct function harness with representative inputs and observable outputs.
- A small state machine or reducer driver for transition questions.
- A local fake or stub for an external boundary.
- A minimal benchmark for a specific performance claim.
- A protocol or serialization round trip for compatibility questions.

Keep inputs deterministic and expose the relevant state after each action. Prefer an existing test runner or script runtime, but place every new artifact in the prototype workspace. A prototype may include focused assertions when they make the answer unambiguous.

Use synthetic or disposable data. Connect to a real service only when that service is the uncertainty and a non-production environment is available.

Report the inputs, observed outputs, and the conclusion they support. If the result depends on an uncontrolled variable, say so.
