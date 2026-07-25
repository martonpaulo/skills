# Audit report structure

Use this when producing a disk audit. Write in the user's language. Sizes in MB or GB. Every
table is for a person deciding what to delete, so explain jargon inline.

## Classification vocabulary

### Risk

| Level | Meaning |
| --- | --- |
| Low | Cache, log, build output, or dependency that is clearly regenerated automatically. |
| Medium | Probably regenerated, but removal costs a re-download, a re-login, a re-index, or a rebuild. |
| High | May hold personal data, configuration, backups, history, or state that cannot be recovered. |

### Recreatability

| Level | Meaning |
| --- | --- |
| Easy | The system, app, or package manager recreates it with no action from the user. |
| Moderate | Requires reinstalling dependencies or reconfiguring something. |
| Hard | Depends on a backup, personal data, or manual state. |

### Recommendation

Use exactly one of: `Safe to clean`, `Good candidate but review first`, `Keep`, `Do not touch`,
`Investigate manually`, `Back up first`, `Depends on whether still in use`.

### Confidence (for suspected leftovers)

`High`, `Medium`, `Low`. A missing application is evidence, not proof. Never report a suspicion
as a certainty.

## Sections

### 1. Executive summary

| Metric | Value | Note |
| --- | ---: | --- |

At minimum: total capacity, free space now, count and total of low-risk candidates, of
medium-risk candidates, of high-risk items, the top five opportunities, a conservative savings
estimate, and a potential savings estimate that needs manual review.

The conservative estimate includes only low-risk items and counts no space twice.

### 2. Ranked cleanup candidates

| # | Category | Path / item | Size | Risk | Recreatable | Why it is here | In plain terms | Recommendation |
| ---: | --- | --- | ---: | --- | --- | --- | --- | --- |

Order: low risk with large size, then medium risk with large size, then high-risk items for
review only.

### 3. Appears safe to clean

Low-risk items only.

| Item | Path | Size | Why it looks safe | How it would come back | Note |
| --- | --- | ---: | --- | --- | --- |

### 4. Needs review

| Item | Path | Size | Risk | What could be lost | Question to answer first |
| --- | --- | ---: | --- | --- | --- |

### 5. Suspected leftovers of removed apps

| Likely app | Leftover found | Path | Size | Evidence | Confidence | Risk | Recommendation |
| --- | --- | --- | ---: | --- | --- | --- | --- |

Evidence worth citing: the application is absent from `/Applications`, `~/Applications`, and the
package manager; the directory has not been modified in a long time; a launch agent points at a
binary that does not exist.

### 6. Projects with large dependencies or build output

| Project | Path | Dependencies | Builds/caches | Total candidate | Last modified | Recreatable | Risk | Recommendation |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |

Heuristics: untouched for more than 180 days is a strong candidate; 90 to 180 days deserves
review; modified in the last 30 days should usually be kept. A dependency directory with a
lockfile is low risk; without one it is medium risk. Build output is generally low risk.

### 7. Platform developer data

Xcode derived data, archives, device support, simulators and runtimes, Android AVDs, and similar.

| Item | Path | Size | What it is | When it is usually safe to clear | Risk | Note |
| --- | --- | ---: | --- | --- | --- | --- |

### 8. Package managers

| Tool | Item | Read-only command used | Size / result | Risk | Recommendation |
| --- | --- | --- | ---: | --- | --- |

### 9. Containers, VMs, and large images

| Item | Type | Size | Last used, if known | Risk | Recommendation |
| --- | --- | ---: | --- | --- | --- |

### 10. Large files for manual review

| File | Path | Size | Type | Last modified | Risk | Recommendation |
| --- | --- | ---: | --- | --- | --- | --- |

### 11. Do not touch without a backup

| Item | Path | Size | Why it is off limits |
| --- | --- | ---: | --- |

Always includes, when present: Photos library, Mail, Messages, Keychains, iCloud Drive,
Dropbox/Google Drive/OneDrive folders, app databases, project folders with no backup,
`~/.ssh`, `~/.gnupg`, `~/.aws`, config directories holding tokens, and containers of apps still
in use.

### 12. Suggested plan

Phases, described but **not executed**.

| Phase | Estimated savings | Risk | What to check first |
| --- | ---: | --- | --- |

A typical order: low-risk caches and build output; then stale projects; then suspected
leftovers; then high-impact items such as backups, containers, VMs, and simulators.

### 13. Commands run

| Command | Purpose | Changed anything? |
| --- | --- | --- |

During an audit, the last column is `No` for every row.

### 14. Limitations

State what could not be inspected: permission-denied areas, tools that are not installed,
uncertain results, anything skipped for privacy, and any remaining risk of double counting.
