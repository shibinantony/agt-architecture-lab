---
status: learning-prototype
tested_scope: assessment-model-design
last_verified: 2026-09-11
---

# Evidence-based agent governance maturity

Assess a specific agent workflow and its control boundary. A local lab, an Azure platform, and a production agent fleet have different scopes. Completing this repository demonstrates learning and local behavior; it does not establish organization-wide maturity or certify [Microsoft AGT](https://github.com/microsoft/agent-governance-toolkit).

## Levels

| Level | Name | Evidence required |
|---:|---|---|
| 0 | Unknown / ad hoc | Scope, owner, method, or evidence is missing |
| 1 | Visible | Agents, tools, identities, costs, and data paths are inventoried with known gaps |
| 2 | Defined | Outcome, policy, owner, approval authority, and target are documented |
| 3 | Repeatable | Versioned implementation and representative tests reproduce decisions in the assessed environment |
| 4 | Operated | Monitoring, incident response, approvals, exceptions, service measures, and costs are sustained |
| 5 | Evidence-driven | Outcomes, friction, economics, and incidents regularly change or retire controls |

Choose a target appropriate to risk and operating scale. A higher score without a better outcome is not an investment case.

## Capability assessment

| Capability | Visible evidence | Repeatable evidence | Evidence-driven practice |
|---|---|---|---|
| Business ownership | Workflow purpose and accountable owner | Decision rights used in actual changes | Outcome evidence changes funding and priorities |
| Tool and model inventory | Agent, tool, provider, credential, and data-path list | Inventory reconciled with deployed configuration | Unused capabilities and risky paths are removed |
| Action control | Known allow, deny, and approval cases | Positive, negative, malformed-input, and bypass tests | Incident and false-denial patterns improve policy |
| Identity and access | Credential owners and reachable scopes | Least-privilege access and revocation tested | Access shrinks or changes with observed need |
| Human approval | Named authority and action classes | Exact request binding, expiry, replay prevention, and timeout tested | Approval burden and outcomes improve delegated authority |
| Execution containment | Known process, network, and filesystem boundaries | Alternative routes and credential escape tested | Threat findings change isolation and tool design |
| Audit and evidence | Known record fields, location, and gaps | Request-to-result correlation and failure recovery tested | Reconstruction time, retention cost, and incident needs improve collection |
| AI and cloud economics | Model, tool, infrastructure, and people costs visible | Budget reservations, concurrency, retries, and billing reconciliation tested | Accepted-task economics changes architecture and model routing |
| Reliability | Dependencies and fallback behavior listed | Policy outage, tool failure, kill switch, and recovery tested | Incident evidence and service measures change design |
| Adoption and exceptions | Users, training needs, and waivers visible | Support, expiry, escalation, and exception reviews operate | Repeated friction changes the supported workflow |
| Azure platform governance | Landing-zone, RBAC, policy, and cost controls inventoried | Resource controls and agent controls tested together | Overlap and gaps change platform investment |

## Worked assessment: completing this lab

After running the offline demo and reviewing its artifacts, an engineer can claim observed decisions for the supplied synthetic requests. They can record a repeatable local test for that narrow policy implementation. They cannot infer authenticated enterprise identities, tamper-resistant storage, live approvals, distributed budgets, or protection of the client's other tools.

For example, record action control as “repeatable for the supplied local scenarios; deployment and bypass coverage unknown.” Keep enterprise identity and operational response “unassessed” until evidence exists. Do not average these into a misleading “production ready” score.

The separate [AGT source-snapshot exercise](../examples/upstream-agt/README.md) targets development commit `0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf` with core metadata version 5.0.0. A successful assertion run means one allowed request, three denied requests, and one handler execution. Use the [validation record](validation.md) for actual platform/results, and record the source commit as well as the package version. This distinct wrapper test scope does not raise the maturity of enterprise identity, approvals, distributed accounting, ACS integration, or production operations.

## Assessment record

For each capability, record current level, evidence links, tested environment, exclusions, confidence, target and business reason, most material gap, next validation action, owner, and review date. State what evidence would lower the score.

An architect should review boundary and failure evidence; a director should confirm operating capacity; the business owner should decide whether the next investment is worthwhile. Use the [role exercises](learning-path.md) and [operating model](operating-model.md) to produce the missing artifacts.

## Rules against inflated scores

- Installation, policy counts, and dashboards do not establish effectiveness.
- Source-supported vendor capabilities are not observations in your deployment.
- A passed synthetic scenario does not prove general resistance to bypass or prompt injection.
- A denied action is not evidence that the same action was unreachable through every other path.
- Budget decisions need a stated unit, scope, lifecycle, and reconciliation method.
- Automation requires a tested containment and recovery process.
- A score without dated, scoped evidence remains an opinion.
