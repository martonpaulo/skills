# Issue Labels

The label taxonomy every issue skill reads and writes. A repository that already has its own
convention wins; this is the default when it has none, and the reference when its convention is
incomplete.

The point is sortable work. A backlog labelled only `bug` or `enhancement` cannot be ordered,
filtered or planned.

## Closed sets

No label may be created with a `type:`, `priority:` or `effort:` prefix outside the values
below. A value that seems to be missing is a conversation with the owner, not a new label.

### `type:` — required, exactly one

`bug` · `feature` · `improvement` · `refactor` · `maintenance` · `research` · `documentation`

No additions. `type: hotfix` is urgency, which `priority:` already carries.

### `priority:` — required, exactly one

`P0` · `P1` · `P2` · `P3`

No additions. `P4` is a backlog that has stopped ordering itself.

### `effort:` — at most one

`XS` · `S` · `M` · `L` · `XL`

An issue may carry no `effort:` label while it is still unestimated, and that absence is
meaningful: it says nobody has sized it yet. Once estimated it takes exactly one value, and
never a second one.

`effort: XL` is a signal to check whether the issue should be split before it is planned.

## Open set

### `area:` — one or more

Free values, drawn from the shape of the repository rather than from a fixed list. Typical
values in a front-end project: `grid`, `source-editor`, `formats`, `clipboard`,
`import-export`, `workspace`, `persistence`, `accessibility`, `design-system`, `performance`,
`documentation`, `tooling`.

Add an `area:` only when it is a filter somebody will use more than once. A label invented for a
single issue is noise with a colour.

## Rules

- The working default on any issue is `type` + `priority` + `effort` + `area`.
- Never label with bare `bug`, `feature` or `enhancement`. They carry no order.
- Never encode a dependency as a label. Dependencies are `Depends on #123` links and the
  dependency graph. A `blocked` label states the state, never who does the blocking.
- Never invent a value to avoid leaving a field empty. An absent `effort:` is honest; a guessed
  one is not.
