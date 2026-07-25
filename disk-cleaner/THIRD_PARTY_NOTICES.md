# Third-party notices

## disk-cleaner

- **Upstream repository:** https://github.com/gccszs/disk-cleaner
- **Imported revision:** `b8e02ce23c3c05c9aea3f70810e83418794a49f6`
- **Imported on:** 2026-07-25
- **Original authors:** Disk Cleaner Contributors
- **License:** MIT, full text in `LICENSE`, preserved unchanged.

The `diskcleaner/` package and the `scripts/` runners originate from that project's
`skills/disk-cleaner/` directory.

### What was adapted

**Documentation rewritten.** `SKILL.md` was replaced. The upstream version was a 1,473-line
feature catalogue with an emoji policy, marketing copy, and sample "multi-agent" code calling a
`Anthropic().agent.create` API that does not exist. The replacement is an audit-first workflow
with explicit safety boundaries. The scan-sizing decision tree (sample first, choose mode from
the estimate) and the mandatory dry-run before deletion are kept from upstream; they are the
genuinely good ideas in it.

**Audit workflow added.** `references/audit-report.md` and `references/macos-developer.md` are
new. They come from the owner's own macOS audit prompt: read-only first pass, no `sudo`,
metadata-only inspection, risk/recreatability/recommendation classification, no double counting,
suspected leftovers labelled by confidence, and a phased plan that is proposed rather than
executed. Upstream had no equivalent.

**Safety hardened.**
- `scripts/clean_disk.py` no longer lists `~/Library/Application Support/MobileSync/Backup`
  (iOS device backups) as a cleanable cache location. Upstream did, which put irreplaceable
  user data one `--force` away from deletion.
- `diskcleaner/config/defaults.py` gained a protected set covering credentials and keys
  (`~/.ssh`, `~/.gnupg`, `~/.aws`, `~/.kube`, keychains), personal libraries (Photos, Mail,
  Messages, MobileSync), and cloud-synced folders (iCloud Drive, `CloudStorage`, Dropbox,
  Google Drive, OneDrive), plus protected patterns for `.env`, `.pem`, `.key`, `.p12`,
  `.keychain`, and `.mobileprovision` files.

**Translated to English.** User-facing strings and comments in `platforms/macos.py`,
`platforms/linux.py`, `platforms/windows.py`, `core/classifier.py`, `core/smart_cleanup.py`,
`core/process_manager.py`, and `optimization/concurrency.py` were Chinese upstream. This
collection is English-only.

### What was removed

| Removed | Reason |
| --- | --- |
| `scripts/analyze_progressive.py` | Broken upstream: imports `init_console` from `skill_bootstrap`, which does not define it. `analyze_disk.py --progressive` covers the same need. |
| `scripts/interactive_wizard.py`, `diskcleaner/core/interactive.py` | Interactive TTY prompts an agent cannot drive; overlaps the workflow in `SKILL.md`. |
| `scripts/scheduler.py` | Installs cron/launchd jobs. Out of scope, and this skill does not set up background execution. |
| `scripts/organize_files.py`, `diskcleaner/core/organizer.py`, `diskcleaner/core/rules/` | Moves the user's files into new folder structures. A different responsibility from reclaiming space. |
| `scripts/package_skill.py`, `scripts/test_wizard.py` | Upstream release tooling. |
| `INSTALL.md`, `UNIVERSAL_INSTALL.md`, `NO_PYTHON_GUIDE.md`, `AGENT_QUICK_REF.txt`, `README.md`, `docs/` | Installation and marketing docs for a standalone distribution. This skill lives in one place. |

`references/temp_locations.md` is kept from upstream, unchanged.
