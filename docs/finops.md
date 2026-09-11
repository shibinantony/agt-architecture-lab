---
status: learning-prototype
tested_scope: economic-model-design-and-synthetic-example
last_verified: 2026-09-11
---

# FinOps for governed agent workloads

Measure the cost of obtaining an accepted business result. An agent can consume model tokens, retry tools, hold approvals open, and produce logs even when its final task fails. Agent governance should make those decisions visible and bounded; the economics also need finance ownership and billing reconciliation.

This guide is an original companion to [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit). Its enterprise controls are design requirements to evaluate, not claims that this local emulator implements a production billing platform.

## Keep the cost boundaries explicit

| Boundary | What consumes resources | Where a production limit belongs | What this lab does |
|---|---|---|---|
| Model / provider | Input, output, additional reasoning or cached usage where billed, retries, fallback models | Authorized model gateway or provider-facing application with usage accounting | Makes no model calls; does not count tokens or enforce provider budgets |
| Tool execution | Queries, jobs, paid APIs, execution time | Guarded tool service before work is admitted | Applies fixed fictional USD costs and a per-session limit |
| Azure workload | Compute, storage, network, managed services | Resource configuration, workload design, financial review, and separately designed automation | Reads synthetic fixtures and returns illustrative estimates |
| Governance service | Gateway, policy evaluation, evidence storage, monitoring, support, review | Platform budgets, retention policy, capacity planning, operating ownership | Writes local evidence and summaries |

The cost returned by `estimate_cost` describes a synthetic Azure resource. The `cost_usd` charged to call that tool is a separate teaching value. Neither is an invoice or current Azure price.

## Run the budget exercise

After [setup](lab-guide.md), run:

```shell
python -m lab demo
```

Open the session's `summary.md` and `evidence.jsonl` beneath `artifacts/lab`. The supplied [lab policy](../lab/policy.yaml) sets `max_session_cost_usd: 0.05` and these fictional tool charges:

| Allowed operation | Synthetic charge | Cumulative charge for these three calls |
|---|---:|---:|
| `inventory_resources` | $0.01 | $0.01 |
| `estimate_cost` | $0.02 | $0.03 |
| `create_governance_report` | $0.02 | $0.05 |

The next otherwise allowed $0.01 call exceeds that session limit and is denied. Denied and approval-pending calls do not execute or consume the lab's tool budget. These values illustrate admission control, not measured consumption. A new process/session starts a new budget: restarting the CLI is not a way to enforce a daily or organization-wide spending cap.

**Checkpoint:** identify the record that explains the budget denial, distinguish tool charge from the returned Azure estimate, and explain why a Codex or Gemini client could still incur model usage after the denial.

## A worked AI cost example

All numbers below are fictional teaching assumptions, with no association to any provider's current pricing. Assume input costs $2 per million tokens and output costs $8 per million tokens, without cached or other separately billed categories.

```text
First attempt: 6,000 input + 1,000 output tokens
  = (6,000 × $2 + 1,000 × $8) / 1,000,000 = $0.020

Retry: 3,000 input + 500 output tokens
  = (3,000 × $2 + 500 × $8) / 1,000,000 = $0.010

Monthly model cost: 1,000 first attempts + 200 retries
  = 1,000 × $0.020 + 200 × $0.010 = $22
```

Suppose human review accepts 800 reports. A fictional monthly cost ledger is:

| Category | Assumed cost |
|---|---:|
| Model usage, including retries | $22 |
| Tool hosting and gateway | $50 |
| Evidence storage and monitoring | $8 |
| Platform support and policy maintenance | $120 |
| Human review and approval | $400 |
| Allocated build cost for this month | $100 |
| **Total** | **$700** |

Cost per accepted report is **$700 / 800 = $0.875**. Dividing only model cost by all 1,000 attempts would hide failures and most operating cost. Compare $0.875 with a measured baseline at the same quality and scope before claiming value. The lab's fictional $0.05 tool allowance is not added to this ledger as if it were a real bill.

## From a local allowance to a production budget

The [AGT reference](agt-reference.md) distinguishes upstream cost-governance designs from the emulator's admission check. The separate source-pinned wrapper exercise checks allow/deny behavior, with observed results in the [validation record](validation.md); it does not validate AGT cost accounting or provider metering.

The following is a proposed production design, beyond the lab's fixed per-process counter:

1. **Allocate:** bind workload, cost center, environment, trusted actor, provider/model, and budget period to the request. Decide how shared costs are allocated.
2. **Reserve before dispatch:** estimate the bounded maximum charge and atomically reserve it against shared remaining budget. Concurrent requests must not each spend the same remaining balance.
3. **Execute within limits:** constrain output, tool duration, retries, parallel calls, and fallback routes. A denied tool can still be preceded or followed by a billed model request.
4. **Reconcile actual usage:** replace the reservation with reported usage and release the unused portion. Record rate version, currency, usage dimensions, provider request ID, and task correlation.
5. **Handle uncertainty:** timeouts do not prove that nothing was billed. Keep ambiguous reservations pending investigation; use idempotency and bounded retries to avoid duplicate actions and charges.
6. **Close the financial period:** compare gateway/tool usage to provider exports and invoices, explain differences, allocate shared costs, and carry unresolved discrepancies to an owner.

This budget reservation is an accounting hold, distinct from purchasing Azure reservations or savings plans. Commitments require a separate demand and utilization decision. A distributed cap also needs persistent state and controls over alternate credentials and routes; a local YAML limit cannot supply those properties.

Azure budgets notify when thresholds are met; they do not themselves stop consumption. Design any automatic action separately with criticality, authority, and recovery in view. [Microsoft budget guidance](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets).

Cost records can arrive after the operation and remain estimates before invoicing. Resource tags do not cover all usage, and a current resource inventory is not the same population as historical billed usage. Preserve these limitations when reconciling. [Microsoft Cost Management data guidance](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data).

## Reporting and ownership

Use the Inform, Optimize, Operate cycle to connect visibility with accountable action. [Microsoft's FinOps framework guidance](https://learn.microsoft.com/en-us/cloud-computing/finops/framework/finops-framework).

| Report | Owner | Review and action |
|---|---|---|
| Cost per accepted task, quality, and human review minutes | Workload owner | Weekly: redesign wasteful loops and verify task usefulness |
| Tokens, retries, fallback usage, reservation age, budget denials | Model / tool platform owner | Daily during pilot: investigate amplification and stale holds |
| Allocated spend, invoice variance, shared cost, forecast | FinOps / finance | Monthly: reconcile and adjust budgets |
| Approval queues, false denials, evidence volume, support effort | Governance product owner | Weekly/monthly: change costly controls or operating capacity |
| Realized value, adverse effects, and investment case | Business owner with finance | Pilot gate/quarterly: scale, revise, hold, or stop |

Track cash savings, cost avoidance, released capacity, delivery improvement, and risk reduction separately. Recommendations are potential value; a blocked synthetic action is not a financial saving. Recognize implemented changes only after evidence and finance review, and do not count the same benefit twice.

Keep provider price, agreement, currency, model/version, effective date, and usage categories in a maintained rate table outside this fictional example. Revalidate when pricing, model routing, workload demand, or billing terms change. The [operating model](operating-model.md) identifies decision rights; the [executive brief](../EXECUTIVE-BRIEF.md) turns the ledger into an investment decision.
