# Distribution, signing, and privacy lookups

Use current official Apple documentation and release notes for:

- code signing, certificates, provisioning profiles, entitlements, and capabilities;
- macOS App Sandbox and hardened runtime;
- notarization and distribution outside the Mac App Store;
- privacy manifests and required-reason APIs;
- App Store Review Guidelines and App Store Connect;
- build settings, SDK changes, and platform release notes.

Start with `detect_apple_project_context()` to identify relevant build settings, entitlements, target platforms, deployment targets, Xcode, and SDK context. Then search official Apple documentation and current release notes. App Store policies and distribution requirements change; verify their current wording and effective date rather than relying on remembered behavior.

There is no dedicated structured provider for every distribution topic. Use authoritative Apple pages directly and cite them. Do not infer entitlement, signing, notarization, privacy, or review behavior from an unrelated API page or community post.
