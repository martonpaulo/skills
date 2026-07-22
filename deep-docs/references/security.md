# Security model

Sandboxed query code is untrusted. AST validation rejects imports, dangerous built-ins, dunder introspection, and missing `result`. The child runs in a separate Python process with restricted built-ins, an isolated temporary directory, a minimal environment, time and output limits, and resource limits where supported. It has only JSON IPC access to registered documentation APIs.

AST validation is defense in depth, not the sole boundary. Never expose generic network, filesystem, import, subprocess, `open`, `eval`, `exec`, or attribute-introspection APIs to submitted code.

Host-side HTTPS providers enforce:

- HTTPS-only URLs;
- exact provider-owned hostnames;
- DNS resolution with private, loopback, link-local, multicast, reserved, and unspecified addresses rejected;
- redirect revalidation;
- connection/read timeouts and redirect limits;
- response-size and content-type limits;
- no `file://`, `ftp://`, local socket, or arbitrary host access.

The local CLI provider uses argument arrays, `shell=False`, a fixed executable allowlist, fixed help/version argument tuples, a sanitized environment, a timeout, and output limits. It does not run package installation, project scripts, builds, deploys, migrations, or mutation commands.
