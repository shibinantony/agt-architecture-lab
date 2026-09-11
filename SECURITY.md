# Security and trust boundaries

This repository contains educational code, an original policy emulator, a local MCP server, and a separate pinned upstream AGT example. It has no supported production deployment.

## What the runnable lab protects

The emulator evaluates requests reaching its five-tool host. It rejects unsupported arguments and policy keys, limits fixture access, blocks denied/pending actions, applies a synthetic session allowance, and requires decision evidence before dispatch. See [tests](tests/) and [implementation](docs/technical-implementation.md).

Its configuration, process, fixture and filesystem are trusted. Local actor values are not authenticated identities. Budget state resets with a new runtime; evidence is editable. A coding client's shell, other MCP servers, direct credentials and model traffic are outside this boundary. Repeated denied requests can still consume memory, disk and client tokens; production ingress needs rate/size limits.

The upstream example validates only the installed AGT wrapper and supplied synthetic cases. It does not test the full toolkit's identity, isolation, approval, ACS or fleet capabilities. [Upstream example scope](examples/upstream-agt/README.md).

## Handling data and credentials

Use synthetic inputs. Do not commit provider keys, tokens, connection strings, real inventory, invoices, identity details, client/employer data or private conversation records. Generated sessions and local CLI settings are ignored by Git, but ignored files still need suitable local access controls.

The default demo and tests need no provider account or Azure access. Optional client sessions use the client's existing authentication and can incur provider usage. A real deployment needs independently protected credentials, policy, evidence and a reviewed operating model.

## Reporting

Do not disclose secrets or sensitive exploit/environment details in public issues. Use a previously verified private contact route to the repository owner. Do not assume GitHub private vulnerability reporting has been configured; verify availability before submitting details.

For upstream component vulnerabilities, follow the affected upstream project's security policy. Report the exact version and distinguish a lab defect from an upstream issue.
