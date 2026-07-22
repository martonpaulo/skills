# Project context and local Xcode documentation

Use these APIs before answering version-sensitive behavior in an existing Apple project.

## `detect_apple_project_context(path=".")`

Returns best-effort Xcode and Swift versions, installed SDK identifiers, projects and workspaces, target platforms, deployment targets, Swift Package and CocoaPods locks, signing-related build settings, entitlements, capabilities, App Sandbox state, and unresolved fields.

The configured project root comes from `scripts/run.py --project-path`. `path` may select only that root or a descendant. Detection uses read-only file parsing plus fixed commands: `xcodebuild -version`, `swift --version`, and `xcodebuild -showsdks`. It never builds, signs, archives, updates dependencies, or executes project scripts.

## Local Xcode additional documentation

- `list_xcode_documentation_sources()` lists installed Xcode applications that contain the expected `AdditionalDocumentation` resource.
- `search_local_xcode_docs(query, xcode_version=None, limit=20)` searches document names and content.
- `fetch_local_xcode_doc(name, xcode_version=None, max_chars=10000)` returns one capped document.

The APIs discover only `Xcode*.app` bundles under configured application roots and only their expected documentation subdirectory. Sandbox code supplies an opaque Xcode source/version and a document name, never a filesystem path. Names containing traversal or separators are rejected.

Treat this material as `local_xcode_additional_documentation`. It may describe SDK implementation guidance or additional local notes; it is not automatically a public API contract. The APIs degrade to empty results when Xcode or the additional documentation directory is unavailable.
