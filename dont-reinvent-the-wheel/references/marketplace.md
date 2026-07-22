# Optional Commercial Source Marketplace Review

Use this reference only when a commercial source-code product is genuinely plausible for the detected stack, capability, source-ownership requirements, integration model, security posture, and license needs.

Skip this review by default for domain-specific business logic, internal services, libraries, developer tooling, infrastructure code, native applications without a relevant marketplace, small isolated features, security-sensitive systems, and enterprise systems where provenance or licensing creates unacceptable risk.

## Candidate checks

When a marketplace candidate is relevant, verify from documentation and source-access terms:

- actual stack and supported framework versions;
- source-code availability and encrypted or inaccessible components;
- extension points, documented APIs, webhooks, embeds, and authentication model;
- dependency age, update history, support status, and security posture;
- license fit, SaaS use, client use, multi-tenant use, and redistribution restrictions;
- export, migration, rollback, and vendor-exit paths;
- customization and glue code still required.

Never infer integration capability from screenshots, demos, or marketing text. Reject or downgrade candidates with stale frameworks, unclear licenses, unverifiable APIs, weak update history, poor export paths, or integration work that exceeds the custom baseline.

Marketplace products are optional candidates, never a required gate or privileged category.
