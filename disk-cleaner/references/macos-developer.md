# macOS developer machine

Locations and read-only commands for auditing a Mac used for software development. Generic
scanners miss most of this, because the space sits in per-tool caches and per-project build
output rather than in one big directory.

Only inspect what exists. If a tool is not installed, record `not found` and move on.

## Read-only commands

Safe to run during an audit. Nothing here modifies state.

```
sw_vers                                    # macOS version
df -h                                      # capacity, used, free per volume
diskutil info /                            # volume detail, purgeable space
du -sh <dir>                               # size of a directory
find <dir> -type d -name node_modules      # locate artifacts
stat -f '%m %N' <path>                     # last modification time
tmutil listlocalsnapshots /                # Time Machine local snapshots
xcode-select -p                            # active developer directory
xcrun simctl list                          # simulators, runtimes, devices
brew list ; brew list --cask               # installed formulae and casks
HOMEBREW_NO_AUTO_UPDATE=1 brew cleanup -n  # what cleanup WOULD remove
HOMEBREW_NO_AUTO_UPDATE=1 brew autoremove --dry-run
npm config get cache ; yarn cache dir ; pnpm store path ; bun pm cache
docker system df -v ; docker images ; docker ps -a ; docker volume ls
pkgutil --pkgs                             # installed packages
plutil -p <plist>                          # selective plist read
```

Never run: `rm`, `mv`, `trash`, `find -delete`, `brew cleanup` without `-n`, `brew uninstall`,
`npm/yarn/pnpm cache clean`, `docker system prune`, `xcrun simctl delete`,
`tmutil deletelocalsnapshots`, `git clean`, `git gc`, `gradle clean`, `mvn clean`,
`defaults write/delete`, `chmod`, `chown`, `chflags`, or anything under `sudo`.

Do not scan `/System` aggressively.

## Where to look

### General

`~`, `~/Desktop`, `~/Downloads`, `~/Documents`, `~/Movies`, `~/Pictures`, `~/.Trash`,
`~/Library`, `/Applications`, `~/Applications`, `/Library/Application Support`,
`/Library/Caches`, `/Library/Logs`, `/opt/homebrew`, `/usr/local`.

Common project roots: `~/Developer`, `~/Projects`, `~/Code`, `~/Workspace`, `~/Documents`,
`~/Desktop`.

### Caches and logs

| Path | What it is |
| --- | --- |
| `~/Library/Caches` | Per-application caches. Often the single largest reclaimable area. |
| `/Library/Caches` | System-wide caches. |
| `~/.cache` | XDG-style cache used by cross-platform tools. |
| `~/Library/Logs`, `/Library/Logs` | Application logs. |
| `~/Library/Application Support/CrashReporter`, `~/Library/DiagnosticReports` | Crash reports. |
| `~/Library/Saved Application State` | Window/state restore data. Low value, low risk. |

### Xcode and Apple platforms

| Path | What it is | Notes |
| --- | --- | --- |
| `~/Library/Developer/Xcode/DerivedData` | Intermediate build products, indexes | Rebuilds automatically. Low risk, usually large. |
| `~/Library/Developer/Xcode/Archives` | Shipped/archived builds | Needed to re-symbolicate crash reports. Review first. |
| `~/Library/Developer/Xcode/iOS DeviceSupport` | Symbols per connected device OS version | Old OS versions are safe once no device runs them. |
| `~/Library/Developer/CoreSimulator/Devices` | Simulator devices and their data | Deleting loses simulator app state. |
| `~/Library/Developer/CoreSimulator/Caches` | Downloaded runtimes | Re-downloadable, often several GB. |
| `~/Library/Developer/Xcode/UserData/Previews` | SwiftUI preview data | Regenerated. |

### JavaScript

Per-project: `node_modules`, `.next`, `dist`, `build`, `out`, `.turbo`, `.parcel-cache`,
`.vite`, `coverage`, `.cache`.

Global stores: `~/.npm`, `~/.yarn`, `~/.pnpm-store`, `~/.bun`, `~/.deno`, `~/.nvm`.

A `node_modules` beside a lockfile is low risk, `npm ci` restores it exactly. Without a
lockfile it is medium risk, because the restored tree may differ.

### JVM

`~/.m2/repository`, `~/.gradle/caches`, `~/.gradle/wrapper`, `~/.sdkman`, and per-project
`target`, `build`, `.gradle`, `android/build`.

### Python, Rust, Go, Ruby

`~/Library/Caches/pip`, `~/.pyenv`, `~/.rbenv`, `~/.cargo/registry`, `~/go/pkg/mod`, and
per-project `.venv`, `venv`, `__pycache__`, `.pytest_cache`, `.tox`.

### iOS/native dependency managers

Per-project `Pods`, `Carthage/Build`, `ios/build`; global `~/Library/Caches/CocoaPods`.

### Homebrew

`/Library/Caches/Homebrew` and `~/Library/Caches/Homebrew` hold downloads; `Cellar` under
`/opt/homebrew` (Apple Silicon) or `/usr/local` (Intel) holds the installs themselves. Use the
dry-run commands above to see what `brew cleanup` and `brew autoremove` would remove.

### Containers and VMs

`~/Library/Containers/com.docker.docker/Data` (Docker Desktop disk image, often tens of GB and
does not shrink on its own), Parallels, UTM, VMware, VirtualBox images, Android emulator images
under `~/.android/avd`.

Report `docker system df -v` totals. Never prune.

### Backups and snapshots

`~/Library/Application Support/MobileSync/Backup` (iOS device backups), `.ipsw` files, old
`iOS DeviceSupport`, Time Machine local snapshots. All are report-only.

## Leftovers from removed applications

Compare what is installed (`/Applications`, `~/Applications`, `/System/Applications`, Homebrew
casks) with what still has state in:

`~/Library/Application Support`, `~/Library/Preferences`, `~/Library/Caches`,
`~/Library/Containers`, `~/Library/Group Containers`, `~/Library/Saved Application State`,
`~/Library/LaunchAgents`, `/Library/Application Support`, `/Library/LaunchAgents`,
`/Library/LaunchDaemons`.

For launch agents and daemons, read only `Label`, `Program`, `ProgramArguments`, and
`RunAtLoad`, and check whether the referenced binary exists. Do not dump whole plists, they can
contain secrets.

| Plist | Label | Target binary | Exists? | Likely app | Risk | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |

## Never clean automatically

`~/.ssh`, `~/.gnupg`, `~/.aws`, `~/.kube`, `~/Library/Keychains`, Photos library, Mail,
Messages, iCloud Drive (`~/Library/Mobile Documents`), `~/Library/CloudStorage`, Dropbox,
Google Drive, OneDrive, application databases, iOS backups, VM images, and any project folder
without a backup. These are protected in `diskcleaner/config/defaults.py` and must also be
respected by any direct shell command.
