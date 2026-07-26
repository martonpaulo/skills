# Resolving libraries and writing queries

## Step 1: resolve the library ID

```bash
ctx7 library react "how to clean up useEffect with async operations"
ctx7 library prisma "how to define one-to-many relations with cascade delete"
```

Both arguments matter. The name narrows the index; the query ranks the matches and disambiguates libraries that share a name.

Each result carries:

| Field | Use it for |
| --- | --- |
| Context7-compatible library ID | The `/org/project` identifier passed to `ctx7 docs`. |
| Title and description | Confirming this is the library the project actually depends on. |
| Code Snippets | Documentation coverage. A near-empty entry will not answer a specific question. |
| Source Reputation | `High`, `Medium`, `Low`, or `Unknown`. Prefer the official project's own entry. |
| Benchmark Score | Index quality, 100 being the maximum. |
| Versions | Present only for some entries, and the source of the version-pinned ID. |

The same library commonly appears several times: the project's own repository, a scraped documentation website, and localized mirrors. Prefer the entry that matches the upstream project, not a mirror, unless the mirror is clearly better indexed.

If the user already supplied an ID in `/org/project` or `/org/project/version` form, skip this step.

## Version-specific IDs

When the resolution output lists versions, append the closest one to the project's installed version:

```bash
ctx7 docs /react/react "useEffect cleanup with async"
ctx7 docs /react/react/v19.2.7 "useEffect cleanup with async"
```

Two limits are worth stating in the answer:

- Only some entries carry a version list at all. Without one, the query hits whatever the index holds, which tracks the project's default branch rather than any release.
- The `Source:` URLs in the output can point at the default branch even for a version-pinned query. Treat them as provenance for the snippet, not as proof of what that version shipped. When that distinction decides the outcome, escalate to `deep-docs`.

## Step 2: query the documentation

```bash
ctx7 docs /vercel/next.js "how to add authentication middleware to app router"
```

One topic per call. A query spanning several concepts dilutes the ranking and returns something shallow about each.

| | Query |
| --- | --- |
| Good | `"how to set up authentication with JWT in Express"` |
| Good | `"React useEffect cleanup function with async operations"` |
| Too vague | `"auth"`, `"hooks"` |
| Too broad | `"routing and auth and caching in Next.js"` |

Output mixes titled code snippets carrying a language-tagged block with prose explanations. Both include a `Source:` URL.

An unknown or misspelled ID fails immediately rather than falling back to a search, and a missing leading `/` is the usual cause.

## Machine-readable output

`--json` works on both commands and is the right choice when the result feeds a script rather than a person:

```bash
ctx7 library zod "schema refinement" --json
```

The library objects expose `id`, `title`, `description`, `branch`, `lastUpdateDate`, `state`, `totalTokens`, `totalSnippets`, `stars`, `trustScore`, `benchmarkScore`, and `versions`. `lastUpdateDate` is the honest way to judge how current an entry is; a stale index is a reason to escalate rather than to caveat.

Plain output is already clean outside a TTY, so piping to `head` or `grep` needs no extra flag.
