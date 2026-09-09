# Azure Resource Graph query pack

## Status

These queries are learning examples. They have received static review but have **not** been executed against an Azure sandbox in this repository's current version.

They perform read-only queries when pasted into Azure Resource Graph Explorer or invoked through an approved Resource Graph client. Query execution is authorization-trimmed and can return incomplete results when the caller lacks access.

## Queries

- [Resource inventory](resource-inventory.kql) — counts resources by subscription, type, and location.
- [Tag coverage](tag-coverage.kql) — lists resources missing one or more proposed allocation fields.

## Safe use

1. Use a sandbox and an explicitly approved Reader scope.
2. Confirm the caller can see the expected subscriptions.
3. Run a simple count and reconcile it with a trusted portal view.
4. Account for pagination, throttling, and indexing latency in any automation.
5. Treat inaccessible or failed scope as unknown.
6. Store raw results outside Git and sanitize all public examples.
7. Do not call tag presence “financially allocated” without validating values and Cost Management behavior.

## Planned validation

- Synthetic fixture equivalence.
- Azure portal Resource Graph Explorer run in one sandbox subscription.
- Azure CLI pagination and failure handling.
- Empty, inaccessible, recently changed, and high-row-count cases.
- Sanitization of identifiers and free-text tags.
