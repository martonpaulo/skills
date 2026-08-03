# Dependency Graph

The closing output of every curation pass: one Mermaid block, then a short legend. It encodes
blocking order and nothing else.

## Block structure

```
%%{init: {"flowchart": {"curve": "linear", "nodeSpacing": 40, "rankSpacing": 60}}}%%
flowchart TD
```

- `flowchart TD`, never `LR`.
- No `%%` comments anywhere in the block. The `%%{init}%%` line above is a configuration
  directive, not a comment, and stays.
- Strip accents and diacritics from every label. They break the import in some renderers.
- Node id is `N<zero-padded number>`.

## Node label

Four lines, separated by `<br/>`. `\n` does not break lines in a Mermaid label; `<br/>` does.

```
N091[["#091<br/>Workspace passa a aceitar de um a quatro panes<br/>effort: L<br/>priority: P1"]]
```

- Line 1: the number, zero-padded to three digits (`#003`, `#021`, `#245`). Past three digits,
  every digit is kept as it is (`#2952`).
- Line 2: a short description written by the agent in the language of the conversation, saying
  what the issue *does* rather than repeating its title.
- Line 3: `effort: <value>`, using the repository's own scale.
- Line 4: `priority: <value>`, using the repository's own scale.

Drop line 3 or line 4 entirely when the repository does not track that field. Never invent a
value, and never substitute a guess for a missing one.

## Links

One `click N<zero-padded number> "<issue url>" _blank` line per node, after the `classDef`
lines, matching the node ids exactly. Mermaid
links the whole node, not a fragment of the label, so the number cannot carry the link on its
own. Anchor tags inside a label are ignored under the default `securityLevel` and must not be
used.

## Edges

- Solid `-->` only for real blocking order: the source must land before the target.
- Dashed `-.->` with an inline label only for cycles that must be broken before anyone starts:
  `N073 -.->|"cycle, #070 lists Move pane but #073 says it comes after #070"| N070`.
- Nothing else becomes an edge. Coordination, overlap, supersession, duplicates, conflicts and
  umbrella issues belong in the written report; as edges they make the graph unreadable.
- Never add an edge to make the graph connected.

## Shape

- `[[ ]]` waits for nobody.
- `[ ]` has something in front of it.
- No emoji or symbol markers inside labels. They disappear on render.

A fully isolated issue is `[[ ]]` like any other issue that waits for nobody. It needs no extra
marking: no arrow points at it and none leaves it.

The side bars of `[[ ]]` show clearly on the darker fills and get faint on the palest one, so
the shape is a reinforcement rather than the primary signal. That is acceptable, because the
pale end of the ramp is exactly where a node has no dependents and the absent arrows already
say it.

## Color

Color encodes **how many issues depend on it**, never how many it waits for. It has to read as
an ordered scale at a glance, so it walks one continuous path, green to teal to blue to indigo
to purple, getting darker at every step, with the border thickening along with it. Two channels
in the same direction, which survives a grayscale print and a dark theme:

```
classDef d0 fill:#cdeac0,stroke:#7cb342,stroke-width:1px,color:#1b5e20
classDef d1 fill:#8ed3b8,stroke:#2e9e75,stroke-width:2px,color:#0b3d2e
classDef d2 fill:#4fb3c9,stroke:#0f7f96,stroke-width:2px,color:#053540
classDef d3 fill:#2b6cb0,stroke:#174e7c,stroke-width:3px,color:#ffffff
classDef d4 fill:#3b4b9e,stroke:#1f2a6b,stroke-width:3px,color:#ffffff
classDef d5 fill:#5b2a86,stroke:#37134f,stroke-width:4px,color:#ffffff
```

Two constraints hold whatever the palette:

- **Lightness only ever decreases.** A step that is lighter than the one before it destroys the
  ordering, however pleasant the hue.
- **The bottom step still has to be a color.** Near-white and light grey wash out against a
  white page and read as "unstyled" rather than as "zero".

Avoid the red and amber family here. It reads as severity, not as quantity, and the backlog
already has priority for that.

Collapse the unused steps and always land the darkest class on the highest count actually
present, so the top of the scale is the root of the backlog rather than a fixed number. The
legend states the exact count behind each step it used.

## Grouping

No subgraphs at all: not by area, not by epic, not by milestone, and not for the free issues
either. Every node sits loose on the canvas.

Issues with no dependency in either direction are always included and never filtered out. They
need no box and no caption, because having no edge attached is already the whole statement.

## Legend

Two or three lines of prose after the block, in this order:

1. what the shape means,
2. the color scale with the exact dependent count of each step,
3. where to start: the root that unblocks the most, and any cycle that has to be broken first.

Nothing longer. The findings are already in the report above it.

## When the graph gets too big

Simplify the single graph instead of splitting it: remove everything that is not a blocking
dependency and shorten the labels. Never emit a high-level graph plus per-component graphs.
