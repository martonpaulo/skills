---
name: apple-docs
description: Research authoritative, version-aware Apple platform documentation for Swift, SwiftUI, UIKit, AppKit, Foundation, macOS, iOS, Xcode, Apple SDKs, Swift Evolution, compiler behavior, HIG, WWDC, signing, entitlements, capabilities, sandboxing, notarization, privacy manifests, distribution, and platform release changes. Use when implementation correctness depends on Apple API behavior, lifecycle, availability, deprecation, SDK or Xcode version, deployment target, platform conventions, or official guidance. In existing projects, detect Xcode, Swift, SDK, platform, dependencies, and deployment targets first. Prefer official Apple and Swift sources and clearly label forum discussions and community notes as secondary. Do not use for purely algorithmic Swift questions or non-Apple documentation.
license: MIT
allowed-tools: "Bash(python3:*)"
metadata:
  scope: project
  role: foundation
  mutation: none
  author: Patrick Ahrentløv
  version: 1.5.0-personal.1
---

# Apple Docs

Answer Apple development documentation questions with version and project context. Use this skill for authoritative lookups, not ordinary implementation, broad architecture, general product research, or purely algorithmic Swift work.

## Workflow

1. In an existing project, run `detect_apple_project_context()` first. Record resolved and unresolved Xcode, Swift, SDK, platform, deployment-target, dependency, entitlement, sandbox, capability, and signing context.
2. Define the exact documented behavior to verify. Include the relevant version, platform, and deployment target.
3. Use the highest-authority applicable source:
   1. official Apple documentation and release notes;
   2. official Apple or Swift source repositories;
   3. accepted Swift Evolution proposals;
   4. official WWDC pages and transcripts;
   5. Apple Developer Forums or Swift Forums, labeled secondary;
   6. community WWDC notes or summaries, labeled community.
4. Prefer documentation compatible with the detected context. State availability, deprecation, minimum version, fallback needs, and unresolved context explicitly.
5. Return a concise answer with source links or identifiers. Separate public API contracts from source implementation details, forum guidance, local Xcode additional documentation, and community notes.

Do not present a Swift Evolution pitch, forum statement, community note, or undocumented implementation detail as guaranteed public API behavior.

## Runner

This skill requires local shell execution and Python 3.10 or newer. `allowed-tools` is optional compatibility metadata; agents that do not interpret it should invoke the runner with their normal shell tool:

```bash
python3 scripts/run.py "result = detect_apple_project_context()" --project-path /path/to/project --pretty
```

Submitted code cannot import modules, read arbitrary files, launch subprocesses, or access the network directly. It can call only the registered documentation APIs. It must assign a JSON-serializable final value to `result`.

Use small queries and filter before returning data. Read [sandbox.md](references/sandbox.md) and [security.md](references/security.md) when changing or diagnosing the runner.

## APIs and references

- Project context and local Xcode documentation: [project-context.md](references/project-context.md)
- Apple API documentation: [apple-docs.md](references/apple-docs.md)
- Swift Evolution and forums: [swift-evolution.md](references/swift-evolution.md)
- Apple and Swift source: [swift-repos.md](references/swift-repos.md)
- Compiler internals: [compiler.md](references/compiler.md)
- HIG: [hig.md](references/hig.md)
- WWDC: [wwdc.md](references/wwdc.md)
- Legacy Documentation Archive: [archive.md](references/archive.md)
- Xcode releases: [xcode-releases.md](references/xcode-releases.md)
- Distribution, signing, and privacy: [distribution.md](references/distribution.md)
- Authority and cache behavior: [source-authority.md](references/source-authority.md), [cache.md](references/cache.md)

## Safety and completion

Context detection is read-only: do not build, sign, archive, update dependencies, execute project scripts, or modify the project. Local Xcode APIs search only expected installed-Xcode documentation folders and never accept arbitrary paths from sandbox code.

The lookup is complete when the answer identifies the applicable documentation and version, reports compatibility and uncertainty, labels source authority, and returns only the evidence needed for the task.
