---
name: disk-cleaner
description: Audit a personal computer for reclaimable disk space and, only after explicit approval, clean it. Covers caches, logs, build artifacts, dependency stores, duplicates, stale downloads, package-manager leftovers, simulator and container data, and residue from uninstalled apps. Always starts read-only, classifies every candidate by risk and recreatability, and never deletes anything without a confirmed decision. Use when the user asks what is filling their disk, wants a cleanup plan, or asks to free space on their machine. Do not use for cleaning a project's working tree during normal development, for diagnosing application bugs, or for any repository-level task.
license: MIT
allowed-tools: "Bash(python3:*)"
metadata:
  upstream: https://github.com/gccszs/disk-cleaner
  upstream-author: Disk Cleaner Contributors
  version: 2.2.0-personal.1
---

# disk-cleaner

Personal-machine disk space skill. It answers two questions, in this order:

1. What is actually taking up space, and how risky is each item to remove?
2. Which of those items should be removed now, and what proves it worked?

This is a personal skill, not a project skill. It operates on the user's machine, not on a
repository under development.

## Safety boundaries

These are absolute. They hold even if the user asks for speed.

- **Audit before action.** The first pass is always read-only. No deletion, move, copy, or
  configuration change happens during it.
- **No `sudo`, ever.** Do not request an administrator password and do not work around
  permissions. Record `Permission denied` as a limitation and continue.
- **No blind deletion.** `clean_disk.py` defaults to `--dry-run`. Run the preview, show it,
  and only pass `--force` after the user confirms that specific scope.
- **Never delete on the user's behalf**: Trash contents, Time Machine snapshots, iOS or app
  backups, virtual machine images, Docker volumes, credentials, or anything under
  `~/.ssh`, `~/.gnupg`, `~/.aws`, `~/Library/Keychains`, Photos/Mail/Messages libraries, or a
  cloud-synced folder. Report them; let the user act.
- **Privacy.** Read metadata only: path, size, timestamps, file type, owning app. Do not open
  documents, photos, mail, message stores, browser history, `.env` files, or anything that may
  hold a secret. Partially mask a filename that looks sensitive but matters by size.
- **No GUI.** Do not use `open`, do not launch applications.
- **Report honestly.** Suspected leftovers of an uninstalled app are *suspicions*, not facts.
  Label confidence. Never claim space was freed without re-measuring.

## Workflow

### 1. Frame the request

Establish the target path (default: the user's home directory), whether this is an audit or an
approved cleanup, and how much time the user will accept. If the machine is a developer
machine, read `references/macos-developer.md` before scanning — it lists the toolchain
locations that generic scanners miss.

### 2. Size the job before scanning it

Always sample first. A full scan of a large volume can take hours.

```bash
python3 scripts/analyze_disk.py --sample --path ~ --json
```

Use `estimated_time_seconds` from the result to pick the mode:

| Estimate | Mode | Command |
| --- | --- | --- |
| < 30 s | Full scan | `analyze_disk.py --path <path>` |
| 30–120 s | Time-limited | `analyze_disk.py --path <path> --time-limit 60` |
| > 120 s | Progressive | `analyze_disk.py --path <path> --progressive --time-limit 60` |

Tell the user the expected duration before starting, and never leave them without feedback for
more than two minutes. Partial results from an interrupted scan are still useful — say they are
partial.

### 3. Audit read-only

Combine the scripts with direct read-only inspection. Cover, at minimum:

- Disk totals: capacity, used, free, purgeable.
- Largest directories in `~` and in `~/Library`.
- Caches, logs, and crash reports.
- Development artifacts: dependency directories, build output, package-manager stores,
  simulator and emulator data, container images.
- Duplicates and large stale files, old installers, forgotten downloads.
- Residue from applications that no longer exist.
- Local backups and snapshots — for reporting only.

`references/macos-developer.md` has the macOS paths and the safe read-only commands.
`references/temp_locations.md` has the cross-platform cache and temp locations.

### 4. Classify every candidate

Do not present a raw size list. Every item gets three labels, defined in
`references/audit-report.md`:

- **Risk** — Low, Medium, High.
- **Recreatability** — Easy, Moderate, Hard.
- **Recommendation** — one of the fixed set (Safe to clean, Good candidate but review first,
  Keep, Do not touch, Investigate manually, Back up first, Depends on whether still in use).

Avoid double counting: when a parent directory and a child both appear, say which total
contains the other, and count the space once in the summary.

### 5. Report

Follow the structure in `references/audit-report.md`. Write the report in the language the user
is writing in, in plain terms — this is a report for a person deciding what to delete, not a
tool dump. Sizes in MB or GB. Order by impact within each risk level. End with a phased plan
that has not been executed.

### 6. Clean only what was approved

For each approved phase:

```bash
python3 scripts/clean_disk.py --cache --logs --dry-run   # preview, always first
python3 scripts/clean_disk.py --cache --logs --force     # only after explicit confirmation
```

Prefer a targeted path (`--path`) over a broad category when the audit identified a specific
offender. For toolchain caches, prefer the tool's own command (`brew cleanup`, `npm cache
clean --force`, `docker system prune`) and tell the user what it will do — but only run it when
the user asked for that cleanup.

Afterwards, re-measure free space and report actual versus estimated savings.

## Scripts

Run them from the skill root; they locate the bundled `diskcleaner` package themselves.
Requires Python 3.7+ and nothing else — no pip install.

| Script | Purpose | Notable flags |
| --- | --- | --- |
| `check_skill.py` | Verify the package works in this environment | — |
| `analyze_disk.py` | Size analysis | `--sample`, `--progressive`, `--file-limit`, `--time-limit`, `--deep-scan`, `--find-duplicates`, `--json` |
| `find_duplicates.py` | Duplicate detection by hash | `--strategy {adaptive,fast,accurate}`, `--all`, `--json` |
| `analyze_growth.py` | Growth trend over captured snapshots | `--capture`, `--history`, `--cleanup DAYS` |
| `monitor_disk.py` | Usage against warning/critical thresholds | `--warning`, `--critical`, `--alerts-only` |
| `clean_disk.py` | Deletion, **dry-run by default** | `--dry-run`, `--force`, `--temp`, `--cache`, `--logs`, `--downloads DAYS`, `--path` |

Script output is intentionally ASCII-only so it survives non-UTF-8 consoles. Do not add emoji
to script output. Your own report to the user is free-form.

If Python is unavailable, fall back to read-only shell inspection (`df`, `du`, `find`, `stat`)
and say that the scripted analysis was skipped.

## Completion criteria

An audit is done when every large consumer is categorized, classified, and explained; the
conservative savings estimate counts no space twice; uncertain items are marked uncertain; and
a phased plan exists that nobody has executed.

A cleanup is done when only approved items were removed, nothing on the protected list was
touched, and free space was re-measured and reported.

## Attribution

Adapted from [gccszs/disk-cleaner](https://github.com/gccszs/disk-cleaner) (MIT). See
`THIRD_PARTY_NOTICES.md` for what was changed.
