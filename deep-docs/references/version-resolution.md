# Version resolution

`detect_project_context()` reads supported manifests and lockfiles without running package managers or project scripts. It recognizes npm locks, Maven and Gradle declarations, Swift Package and CocoaPods locks, Python declarations and Poetry locks, Cargo manifests and locks, Go modules, .NET projects, container manifests, and relevant runtime pins.

For each dependency it keeps separate fields:

- `declared_version`: the manifest expression, which may be a range;
- `locked_version`: the exact lock value when available;
- `detected_runtime_version`: a safe local runtime value when actually queried;
- `resolved_version`: the strongest trustworthy exact value;
- `resolution`: `locked`, `declared_exact`, or `unresolved`.

Prefer a lock value over a declared range. Do not call a range an installed version. When lock, runtime, and requested versions disagree, report the conflict before choosing documentation.

An Xcode project, workspace, CocoaPods Apple project, or Apple platform declaration routes to `apple-docs`. A generic `Package.swift` alone does not prove Apple platform development.
