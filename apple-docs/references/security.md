# Sandbox security

Submitted query code is untrusted. The runner applies defense in depth:

1. AST validation rejects imports, dangerous built-ins, dunder access, and code without a `result` assignment.
2. A separate Python process runs with restricted built-ins, an isolated temporary working directory, a minimal environment, timeout, output cap, and resource limits where the platform supports them.
3. The child can call only named documentation APIs through JSON IPC. It has no generic filesystem, network, or subprocess API.
4. Host APIs validate inputs, constrain paths and domains, cap results, and serialize responses before returning them.

AST validation is not the sole security boundary. Resource limits differ across operating systems, so the subprocess, API allowlist, timeouts, and output limits remain required. Never add `open`, imports, arbitrary attribute introspection, generic subprocess execution, generic URL fetching, or arbitrary path access to the sandbox namespace.
