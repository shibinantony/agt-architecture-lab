# Technical implementation

The runnable implementation is a Python 3.11+ policy emulator around five synthetic tools, with an optional MCP server for Codex and Gemini CLI. Start with the [lab walkthrough](lab-guide.md); use this page to review behavior and extension points.

## Files and responsibilities

| File | Responsibility |
|---|---|
| [lab/policy.yaml](../lab/policy.yaml) | Original, versioned lab policy; trusted local actor, scope, decisions and synthetic cost |
| [lab/runtime.py](../lab/runtime.py) | Strict policy loading, argument validation, decisions, tool dispatch, budget and evidence |
| [lab/fixtures/resources.json](../lab/fixtures/resources.json) | Four synthetic resources across two scopes and three classifications |
| [lab/__main__.py](../lab/__main__.py) | Offline demo and single-call command |
| [integrations/mcp_server.py](../integrations/mcp_server.py) | Stdio MCP interface using the same runtime |
| [tests/test_lab.py](../tests/test_lab.py) | Negative, budget, concurrency, policy and evidence failure cases |
| [tests/test_mcp.py](../tests/test_mcp.py) | Actual subprocess/stdio discovery and calls using the MCP client SDK |
| [requirements.txt](../requirements.txt) | Core dependency pin |
| [requirements-mcp.txt](../requirements-mcp.txt) | Optional MCP dependency pin |
| [requirements-dev.txt](../requirements-dev.txt) | Test dependencies |

The MCP dependency intentionally uses the maintained v1 SDK API at `mcp==1.30.0`. Version 2 is a different API; upgrades require migration and protocol tests. [Official SDK v1 source](https://github.com/modelcontextprotocol/python-sdk/tree/v1.30.0). Direct dependencies are pinned; this is not a platform-independent lock of every transitive dependency.

The separate [actual AGT example](../examples/upstream-agt/README.md) uses Microsoft's core 4.1.0 package and its AgentMesh wrapper policy in an isolated environment. Its allow/deny assertions are executed independently; it is not the implementation behind this MCP server.

## Enforcement order

The runtime validates a known tool and its arguments, evaluates trusted actor/environment and resource scope/classification, checks the configured decision, and admits allowed work within the remaining budget. Unknown tools and removed tool rules deny. Unsupported request properties cannot override identity, cost, budget or approvals.

The exact rule order is implemented in `GovernanceRuntime._evaluate`; an invalid request can fail before reaching a later policy check. Use the returned rule/reason to explain a result instead of inferring the cause from the last policy field you changed.

Allowed execution follows a durable decision append, a synthetic cost reservation, the handler, and a completion append. A denied or approval-required call never enters a handler. A pre-execution evidence-write failure stops execution. A completion-write failure closes that runtime and reports uncertainty; it cannot undo a completed action. Here the allowed handlers only compute/read synthetic data.

## YAML contract

`schema_version: agt-architecture-lab/v1` identifies this repository's format. The loader rejects missing/unknown fields, duplicate keys, aliases, invalid types, non-finite or negative costs, unsupported decisions, and unsafe attempts to enable deployment/deletion.

| Section | Interpretation |
|---|---|
| `actor` | Trusted local fixture identity; not authenticated Entra identity |
| `environment` | Trusted local fixture environment |
| `controls.allowed_*` | Explicit permitted roles, environments, resource groups and classifications |
| `controls.default_decision` | Must be `deny` |
| `controls.max_session_cost_usd` | Synthetic allowance for one runtime instance |
| `tools.<name>.decision` | `allow`, `deny`, or `require_approval`, subject to the tool's safety constraints |
| `tools.<name>.cost_usd` | Trusted synthetic charge, reserved for admitted execution |

A changed policy is loaded only into a new runtime; the existing process keeps its validated policy snapshot. Its SHA-256 digest records which input file produced the decisions. A digest in an editable local file does not prove tamper resistance.

## Evidence contract

Each runtime creates a unique directory under the selected output parent. `evidence.jsonl` contains decision and execution records; `summary.json` and `summary.md` contain totals and limitations. Session/event identifiers, UTC timestamps, policy digest, rule, reason, status and synthetic cost let a reviewer correlate an allowed request with its completion.

Evidence minimizes raw arguments; it is not a transcript of prompts, secrets or returned resource data. Tool response payloads are returned to the caller, while evidence records decision/execution status. Protect real payloads and request metadata separately if adapting the lab.

The default demo has 10 decisions and 3 execution completions: **13 JSONL records**. Do not count completion records as additional tool decisions.

## Budget semantics and limits

The three allowed demo calls reserve $0.01 + $0.02 + $0.02 = $0.05. The next inventory request is denied. All amounts are fictional tool charges; the resource's monthly estimate and the client's model bill are different quantities.

The lock serializes calls within one runtime instance. New instances and restarts start fresh budgets. The budget is not shared across processes, clients or tenants. Local evidence does not restore budget state. A real solution needs atomic reservations in a trusted shared store, usage reconciliation, retry/idempotency design, cancellation semantics and accountable owners. [FinOps design](finops.md).

## Approval and bypass boundaries

`require_approval` means the proposal stops. There is no approval-granting tool, verified approver identity, approved-execution path, deployment backend or delete handler. An agent cannot approve itself by passing an extra field. A production approval must bind approver, action digest, policy version, scope, expiry and replay protection before a separate executor acts.

MCP exposes only this tool boundary. A client's shell, another server, direct Azure access and model API traffic stay outside it. The host filesystem and Python process are trusted in this teaching setup; arbitrary code in that process could change its state. [Architecture](architecture.md) shows the additional isolation and credential boundaries.

## Extension sequence

1. Add a synthetic behavior and adversarial tests before introducing an external operation.
2. Select a pinned upstream AGT/ACS host interface and map this lab's controls explicitly. Do not send the lab YAML to an upstream parser.
3. Derive identity from authenticated transport/workload context; derive scope and cost from trusted services.
4. Add shared metering, durable evidence and independently verified approval where required.
5. Wire a read-only sandbox adapter with least privilege and reconcile its coverage.
6. Test transport, denial-before-side-effect, timeout, retry, evidence outage and rollback in that actual environment.

The original [decision schema](../framework/schemas/governance-decision-contract.schema.json) remains available. The [agent-specific example](../framework/templates/agent-governance-decision.example.json) links the current lab to ownership and rollout. Azure queries remain supplementary and have not been executed against a tenant as part of this rework.
