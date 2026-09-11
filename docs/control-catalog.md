---
status: learning-prototype
tested_scope: local-synthetic-controls-and-production-design
last_verified: 2026-09-11
---

# Agent governance control catalog

Use this catalog to connect a business risk to a policy, test, evidence, and accountable owner. The `LAB-*` identifiers belong to this independent teaching implementation. They are not Microsoft AGT control identifiers or a compliance certification.

Keep the implemented [emulator](../lab/runtime.py), the separate [released-AGT wrapper example](../examples/upstream-agt/README.md), and production control requirements distinct. The wrapper example has been tested with AGT 4.1.0 on Windows/Python 3.11.9: one allowed call and three denials, with only one handler execution. The controls below describe the emulator; they are not inferred properties of every upstream component. Select production components against their own configuration, integration, and [security guidance](https://github.com/microsoft/agent-governance-toolkit/blob/main/SECURITY.md).

## Implemented local controls

The policy is [lab/policy.yaml](../lab/policy.yaml). Tests named below are in [tests/test_lab.py](../tests/test_lab.py); names omit the `test_` prefix. All data and charges are synthetic, and actor/environment identity comes from trusted startup configuration.

| ID / objective | Implementation and focused test | Evidence to inspect | Accountable owner in a real service |
|---|---|---|---|
| LAB-POL-01: reject ambiguous policy | Strict schema rejects unknown/missing fields, duplicate keys, aliases, invalid money, and unsupported decisions; `PolicyValidationTests` | A rejected configuration produces a startup error before a runtime starts | Control owner |
| LAB-TOOL-01: default deny | Only catalogued tools can be selected; `removed_catalog_tool_and_unknown_tool_default_deny` | `rule: default_deny`, no handler result | Tool platform owner |
| LAB-CTX-01: trust server context | Role/environment come from policy; caller identity, cost, classification, and reset overrides are rejected; `caller_fields_cannot_forge_identity_cost_scope_or_reset_budget` and `trusted_role_and_environment_enforced` | `argument_schema`, `actor_role`, or `environment` denial | Security / IAM owner |
| LAB-SCOPE-01: constrain visible resources | Resource group and classification checks apply to inventory and direct lookup; `classification_and_scope_apply_to_inventory_and_direct_lookup` | Filtered inventory or `resource_scope` / `data_classification` denial | Data / workload owner |
| LAB-APR-01: hold sensitive operations | Deny and approval-pending requests never dispatch; destructive allow rules are invalid; `denied_and_approval_requests_never_enter_handlers` | `blocked` or `pending_approval`; zero execution charge; handler spy remains untouched | Approval authority / platform owner |
| LAB-FIN-01: bound session charges | Fixed trusted costs use decimal accounting and one runtime lock; `threads_cannot_overdraw_session_budget` | `session_budget` denial and total at or below the configured allowance | FinOps / platform owner |
| LAB-FIN-02: charge attempted execution | Handler failure retains its dispatch charge; `handler_failure_is_recorded_and_dispatch_cost_remains_charged` | Execution status `failed` and charged cost | Tool platform owner |
| LAB-EVD-01: record before execution | Decision append is flushed before dispatch; `audit_is_durable_before_handler_dispatch` and `audit_failure_blocks_execution_and_closes_session` | Decision event exists before handler; sink failure prevents dispatch and closes session | Evidence platform owner |
| LAB-EVD-02: report completion uncertainty | Completion-log failure closes session without pretending execution did not occur; `completion_audit_failure_does_not_claim_unexecuted_or_success` | Error, unhealthy audit state, consumed charge, no subsequent execution | Incident / evidence owner |
| LAB-DATA-01: minimize audit content | Only known fixture labels are retained; unknown values/fields and raw exceptions are excluded; `secrets_and_unrecognized_argument_names_are_not_in_evidence` | Redaction and absence of supplied secret marker | Data owner |

Run the [lab guide](lab-guide.md) for the demonstration and test commands. The normal demo contains ten decisions and three successful execution completions: thirteen JSONL records. Correlate decision and completion using `event_id`; use `policy_sha256` to identify the policy file. The hash identifies content but does not authenticate the policy or make the log resistant to editing.

The evidence records decision reasons and execution status, not complete returned inventory or report payloads. Detailed synthetic findings appear in the CLI/MCP response. A real evidence design must decide which outputs or references to retain, with data access and retention controls.

## Production controls to design and validate

These are requirements to assess with a selected upstream AGT version and the surrounding platform. They are not implemented by the local emulator.

| Objective | Required test and evidence | Owner |
|---|---|---|
| Authenticate agent and delegated authority | Forged, expired, revoked, and wrongly scoped credentials are rejected; record verified issuer and scope | Security / IAM |
| Prevent alternate execution paths | Shell, other MCP servers, direct credentials, and network routes cannot bypass required enforcement | Platform / security |
| Isolate policy administration | Agent cannot edit policy, replace code, mutate the running evaluator, or change trusted data | Platform / security |
| Bind human approval to the action | Wrong request, changed arguments, expiry, replay, and unauthorized approver fail; approved action has a linked decision | Approval service owner |
| Enforce shared financial limits | Atomic reservation, concurrent requests, restarts, retries, provider usage, and invoice reconciliation work across instances | FinOps / gateway owner |
| Protect evidence and recover failures | Access controls, integrity verification, retention, missing-event detection, and recovery are exercised | Evidence platform / assurance |
| Handle content and tool-result attacks | Sensitive content, hostile tool output, untrusted documents, and changed tool definitions are tested at the applicable boundaries | Security / agent owner |
| Operate and revoke the service | Policy outage, queue saturation, credential revocation, tool timeout, containment, and recovery are tested | Platform / incident owner |
| Manage release drift | Pinned AGT/provider/client versions, change review, migration, and representative regression evidence are maintained | Product / dependency owner |

## Azure platform supplement

Azure controls remain necessary when the protected tools reach Azure. Azure RBAC authorizes actions at resource scopes; Azure Policy evaluates supported resource properties and actions. Their controls complement the agent's integrated tool boundary. [Azure RBAC overview](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview), [Azure Policy overview](https://learn.microsoft.com/en-us/azure/governance/policy/overview).

The legacy `GEL-*` identifiers below retain useful Azure-oriented objectives from the earlier lab. They are supplementary design guidance, not controls deployed by the emulator.

| Legacy IDs | Platform objective | Minimum evidence / test | Owner |
|---|---|---|---|
| GEL-ORG-01 / 02 | Own each subscription and review hierarchy changes | Owner registry; before/after access and policy inheritance | Platform architect |
| GEL-IAM-01 / 02 | Scope privileged access; separate discovery and write identities | Effective permissions; collector cannot write; revocation test | IAM / platform |
| GEL-POL-01 / 02 | Link resource controls to risk; stage changes | Versioned assignment, representative tests, canary, rollback | Control owner |
| GEL-EXC-01 | Bound and expire exemptions | Scope, authority, compensating control, expiry, closure | Exception authority |
| GEL-INV-01 | Declare inventory coverage and freshness | Expected versus visible scope, pagination, missing-access test | Evidence owner |
| GEL-FIN-01 / 02 / 03 | Allocate, route cost signals, verify realized value | Cost mapping, alert disposition, implemented action and observed outcome | FinOps |
| GEL-SEC-01 / GEL-OBS-01 | Operate security findings and required signals | Finding disposition, signal outage test, retention and cost | Security / observability |
| GEL-CHG-01 / GEL-EVD-01 / GEL-RET-01 | Review change, reconstruct decisions, retire safely | Source/version review, sampled trace, removal and residual-cost check | Product / assurance / platform |

Resource Graph results depend on permissions and indexing freshness, so an empty query cannot establish absence of risk. [Resource Graph overview](https://learn.microsoft.com/en-us/azure/governance/resource-graph/overview). Cost alerts need a separate response design; see [FinOps](finops.md).

## Adopting a control

Create a [Governance Decision Contract](../framework/templates/agent-governance-decision.example.json) stating outcome, applicability, agent/tool and resource scope, authority, implementation version, evidence, failure behavior, tests, economics, rollout, and stop/reversal rule. Apply [PROVE](../framework/prove-method.md), then record the strongest achieved evidence state. A source-supported capability or passing fixture test must not silently become a production control claim.
