---
status: learning-prototype
tested_scope: model-design
last_verified: 2026-09-09
---

# Evidence-based maturity model

## Principle

Do not assign one maturity score to an entire organization. Assess each capability against its intended target. A small development subscription might need a different target from a regulated production platform.

## Levels

| Level | Name | Evidence pattern |
|---:|---|---|
| 0 | Unknown / ad hoc | Scope, owner, method, or evidence is missing |
| 1 | Visible | Current state is inventoried with known coverage and limitations |
| 2 | Defined | Outcome, control, ownership, process, and target are documented |
| 3 | Repeatable | Versioned implementation and representative tests produce consistent results |
| 4 | Operated | Monitoring, remediation, exceptions, service levels, and cost are sustained |
| 5 | Evidence-driven | Outcomes, friction, economics, and risk evidence regularly change or retire controls |

Higher is not automatically better. The target should reflect risk, scale, economics, and organizational need.

## Capability scorecard

| Capability | Level 1 evidence | Level 3 evidence | Level 5 evidence |
|---|---|---|---|
| Governance ownership | Named stakeholders and current RACI | Decisions follow an operated lifecycle | Outcome and service data change priorities and authority |
| Resource organization | Visible hierarchy and subscription owners | Versioned vending and placement tests | Hierarchy evolves from observed control and workload needs |
| Identity and access | Role inventory with scope and coverage | Group-based, narrow, tested, reviewed access | Access patterns and incident evidence drive simplification |
| Policy lifecycle | Assignment and exemption inventory | Policy as code, tests, preview, audit and canary | Effectiveness, friction, and false positives drive retirement or redesign |
| Inventory and evidence | Timestamped queries and unknowns | Repeatable collectors and schemas | Evidence quality and reconstruction metrics improve the system |
| Security posture | Visible findings and ownership | Integrated response and exemption workflow | Risk outcomes and control overlap change investment |
| FinOps | Cost views, allocation gaps, budgets | Action ownership and verified optimization | Unit economics and governance cost shape architecture |
| Observability | Signal inventory and retention | Tested alerts and response service levels | Signal value, false positives, and cost drive collection changes |
| Exceptions | Visible waivers | Bounded, approved, expiring, monitored records | Patterns change standards, paved roads, or risk appetite |
| Delivery and IaC | Deployment ownership is known | Reviewed code, preview, canary, rollback | Lead time, failures, and outcomes continuously improve delivery |

## Assessment fields

For each capability, record:

- current level and evidence links;
- target level and business reason;
- scope and exclusions;
- confidence: high, medium, low, or unknown;
- most material gap;
- next smallest validation action;
- owner and review date; and
- what evidence would lower the score.

## Anti-gaming rules

- Tool deployment without ownership or operation does not establish maturity.
- A dashboard without known scope and freshness does not establish visibility.
- A policy assignment count does not establish effectiveness.
- Automation that cannot be rolled back is not mature.
- More controls do not imply better governance.
- Compliance percentage must retain exemptions, not-applicable cases, unknown scope, and data limitations.
- A score without a linked artifact or observation remains an opinion.
