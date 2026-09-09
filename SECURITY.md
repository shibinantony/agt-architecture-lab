# Security policy

## Current support boundary

This repository is a learning prototype. It has no supported production release and should not be used as an authority to deploy controls into an Azure environment.

## Reporting a security concern

Do not open a public issue containing a secret, real tenant identifier, exploitable configuration, client information, or other sensitive data. When the repository is published, the owner must configure a private vulnerability-reporting channel before accepting security reports.

Until that channel exists, remove sensitive details and contact the repository owner through a private, previously verified route.

## Repository safety rules

- Never commit credentials, tokens, certificates, private keys, connection strings, or real environment exports.
- Treat inventory, role assignments, policy assignments, cost data, and architecture output as potentially sensitive.
- Run future Azure collectors with the minimum read permission required.
- Use a separate, narrowly scoped identity for any future deployment or remediation.
- Require explicit review for commands capable of creating, changing, or deleting Azure resources.
- Default examples to synthetic data and non-destructive behavior.
- Record destructive semantics, including deployment-stack or desired-state cleanup behavior, before enabling them.
