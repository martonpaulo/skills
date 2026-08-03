# Discovery and Verification Sources

Use only the sources relevant to the detected stack and capability. No category is mandatory.

## Source roles

- **Primary sources:** official documentation, specifications, source repositories, release notes, changelogs, package registries, security advisories, pricing pages, license terms, and vendor integration documentation. Use these to validate claims.
- **Discovery sources:** search engines, curated lists, product directories, comparison sites, and marketplace catalogs. Use these to find candidates, then verify them.
- **Sentiment sources:** issue trackers, discussions, forums, community posts, and reviews. Use these for risk signals such as support quality, migration pain, pricing changes, or missing features; verify consequential claims where possible.

Check publication, release, and update dates. Prefer current primary evidence over stale summaries. Stop searching once the available evidence supports a defensible candidate set.

## Relevant ecosystems

Detect the project before choosing sources. Relevant ecosystems may include:

- npm, Maven Central, Gradle plugins, NuGet, PyPI, RubyGems, Packagist, crates.io, Go modules, Swift Package Manager, CocoaPods, and pub.dev;
- Docker Hub, GHCR, Helm, Terraform Registry, and Ansible Galaxy;
- AWS, Azure, and Google Cloud marketplaces;
- Atlassian Marketplace, Slack Marketplace, Shopify App Store, WordPress plugins, VS Code Marketplace, and Chrome Web Store.

Search only ecosystems that fit the actual stack. Treat Java and Spring, React and Next.js, React Native, Flutter, Swift and Apple platforms, backend services, infrastructure, CLI tooling, and general full-stack applications as first-class contexts.

## Verification

Verify the claims that affect the decision: functional fit, versions, supported platforms, APIs or extension surfaces, release activity, maintenance, advisories, license, pricing, data handling, export, and deprecation. State unverified facts explicitly.
