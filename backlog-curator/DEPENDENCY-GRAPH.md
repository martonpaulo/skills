# Dependency Graph

The closing output of every curation pass: one Mermaid block, then a short legend. It encodes
blocking order and nothing else.

## Block structure

```
%%{init: {"flowchart": {"curve": "linear", "nodeSpacing": 40, "rankSpacing": 60}}}%%
flowchart TD
```

- `flowchart TD`, never `LR`.
- No `%%` comments inside the block.
- Strip accents and diacritics from every label. They break the import in some renderers.
- Node id is `N<issue number>`.
- Node label is `#<number> · <short phrase> · <effort>`. The phrase is written by the agent in
  the language of the conversation and says what the issue *does*, rather than repeating its
  title. Drop the effort segment when the repository does not track effort.
- One `click N<number> "<issue url>" _blank` line per node, after the `classDef` lines.

## Edges

- Solid `-->` only for real blocking order: the source must land before the target.
- Dashed `-.->` with an inline label only for cycles that must be broken before anyone starts:
  `N73 -.->|"cycle, #70 lists Move pane but #73 says it comes after #70"| N70`.
- Nothing else becomes an edge. Coordination, overlap, supersession, duplicates, conflicts and
  umbrella issues belong in the written report; as edges they make the graph unreadable.
- Never add an edge to make the graph connected.

## Shape

- `[[ ]]` waits for nobody.
- `[ ]` has something in front of it.
- No emoji or symbol markers inside labels. They disappear on render.

## Color

Color encodes **how many issues depend on it**, never how many it waits for. Use plain colors
that any renderer accepts, through `classDef`:

```
classDef d0 fill:#eeeeee,stroke:#9e9e9e,stroke-width:1px,color:#212121
classDef d1 fill:#a5d6a7,stroke:#388e3c,stroke-width:1px,color:#1b5e20
classDef d2 fill:#ffb74d,stroke:#e65100,stroke-width:2px,color:#3e2723
classDef d3 fill:#ffab40,stroke:#bf360c,stroke-width:2px,color:#3e2723
classDef d4 fill:#e53935,stroke:#b71c1c,stroke-width:3px,color:#ffffff
```

Grey is zero, then one step per dependent count. Collapse unused steps and keep the strongest
red for the highest count actually present, so the scale always ends on the root of the backlog.

## Grouping

- No subgraphs by area, epic or milestone. They are the main source of unreadability.
- Exactly one subgraph, `direction LR`, holding every issue with no dependency in either
  direction, titled so it reads as "can start at any time".
- Isolated issues are always included, never filtered out. Being free to start is the signal.

## Legend

Two or three lines of prose after the block, in this order:

1. what the shape means,
2. the color scale with the exact dependent count of each step,
3. where to start: the root that unblocks the most, and any cycle that has to be broken first.

Nothing longer. The findings are already in the report above it.

## When the graph gets too big

Simplify the single graph instead of splitting it: remove everything that is not a blocking
dependency and shorten the labels. Never emit a high-level graph plus per-component graphs.
