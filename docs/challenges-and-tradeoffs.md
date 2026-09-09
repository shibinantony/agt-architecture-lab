---
status: learning-prototype
tested_scope: risk-analysis
last_verified: 2026-09-09
---

# Challenges and trade-offs

## Challenge register

| Challenge | Early signal | Mitigation | Primary owner |
|---|---|---|---|
| Product-name and acronym confusion | Users assume Microsoft ownership or confuse the project with Microsoft's Agent Governance Toolkit | Use a distinct project name, descriptive Azure subtitle, and non-affiliation notice | Repository owner |
| Brownfield disruption | Large noncompliant baseline or unknown deployment ownership | Discover first, map dependencies, audit, segment, and canary | Platform owner |
| Broad policy blast radius | One assignment affects many subscriptions or critical workloads | Limit root assignments, preview, use selectors/overrides where supported, stage exposure | Platform and control owners |
| Policy false positives | Compliant patterns are denied or reported incorrectly | Representative positive, negative, exception, and not-applicable tests | Control owner |
| Inherited-policy confusion | Teams cannot explain the effective assignment or parameter | Keep hierarchy flat, document parent scope, produce effective-scope views | Platform owner |
| Remediation privilege escalation | Managed identity needs broad write access | Separate remediation from evaluation, use narrow roles and scope, independently review | Security / IAM owner |
| Permanent exceptions | Waivers lack expiry or are repeatedly renewed | Require owner, reason, compensating control, expiry, usage and renewal evidence | Exception authority |
| Incomplete inventory | Results omit resources because the caller lacks access | Report expected versus visible scope and use `unknown` state | Assessment owner |
| Eventual consistency | Recent change is absent from Resource Graph or policy result | Timestamp, wait/retry, reconcile with authoritative source, document latency | Evidence owner |
| Query limits and pagination | Counts differ or only the first page is processed | Implement paging, throttling backoff, row reconciliation, and query tests | Toolkit engineer |
| Cost-data limitations | Recent charges, tags, credits, or shared costs do not reconcile | Record agreement, scope, freshness, tag inheritance, and allocation method | FinOps owner |
| Budget misconception | Stakeholders expect a budget to stop spend | State that budgets alert; design any automated response separately and safely | FinOps and workload owners |
| Telemetry cost growth | Log ingestion and retention rise without a use case | Data collection rules, tiering, sampling, retention review, cost owner | Observability owner |
| Security-plan cost | Paid capabilities are enabled without an owner or funding | Explicit plan selection, scope, benefit hypothesis, and cost review | Security and FinOps owners |
| Compliance overclaim | A green policy dashboard is called “compliant” | Distinguish configuration evidence from complete legal, process, and operating assurance | Risk and assurance |
| Desired-state deletion | A tool removes assignments or resources it considers unmanaged | Define ownership root, detect external management, detach first, review deletion plans | Platform owner |
| Deployment-stack cleanup | `actionOnUnmanage` deletes an important resource | Sandbox test, explicit ownership, safe default, protected destructive approval | Platform owner |
| Built-in policy evolution | Definition behavior or version changes unexpectedly | Track versions, review release changes, test upgrades progressively | Control owner |
| Platform retirement and preview | Design depends on retiring Blueprints or preview Service Groups | Exclude Blueprints from new work; isolate previews behind optional adapters | Architect |
| RBAC sprawl | Many direct assignments and standing owners | Group-based assignment, narrow scope, PIM, access review, break-glass control | IAM owner |
| Central bottleneck | Exception and onboarding queues grow | Product service levels, subscription vending, self-service evidence, federated owners | Governance product owner |
| Shadow IT | Teams bypass controls to deliver | Explain outcomes, provide a usable paved road, measure friction, improve controls | Sponsor and product owner |
| Confidentiality leakage | Public report contains names, IDs, costs, or topology | Synthetic fixtures, sanitization checks, private raw storage, publication review | Repository and data owners |
| Skills concentration | Only one engineer understands the toolkit | Documentation, paired reviews, learning sprints, runbooks, ownership rotation | Platform owner |
| Governance becomes a project | Controls have no review after initial launch | Named product owner, recurring metrics, event-driven review, retirement workflow | Executive sponsor |

## Specific technical cautions

### Audit is safer, not harmless

Audit assignments can create evaluation load, operational findings, monitoring cost, and remediation pressure. They can also produce misleading results if aliases, modes, applicability, permissions, or data latency are misunderstood.

### Deny changes the developer experience

Deny is useful when preventing a well-understood, high-confidence condition is better than remediating it later. It also creates immediate delivery failure. Error messages, owner routing, exceptions, and representative tests are part of the control.

### Modify and deploy-if-not-exists require identities

These effects can change resources and commonly require managed identities with specific permissions. Treat assignment creation, evaluation, and remediation as separate risk decisions.

### Hierarchy changes are operating-model changes

Moving a subscription changes inherited policy and possibly access. Model the effective before-and-after state; do not treat the move as administrative housekeeping.

### Resource Graph is a view, not a transaction log

Resource Graph is efficient for governance inventory, but results are authorization-trimmed and indexed with latency. Persist evidence intentionally if the review needs longer history or point-in-time reconstruction.

### Blueprints is not a foundation for new work

Microsoft states that Azure Blueprints is retiring on January 31, 2027, following phased retirement that began July 31, 2026. Use current infrastructure-as-code, template spec, and deployment-stack patterns after evaluating their own trade-offs.

## Organizational challenges

### Control without authority

A governance team that can identify risk but cannot resolve ownership, funding, or noncompliance will produce dashboards rather than outcomes. Define mandate and escalation before scaling tools.

### Authority without feedback

A central team that can enforce policy but does not measure workload impact will create brittle standards. Track false positives, onboarding time, support demand, and exception patterns.

### Evidence without interpretation

More telemetry does not automatically improve assurance. Define what decision each data source supports, how fresh it must be, who reviews it, and when it may be deleted.

### Efficiency without value

Reducing resource cost can harm performance, resilience, or security. Pair every cost decision with business outcome and quality constraints.

## Decision test

Before introducing or scaling a control, ask:

1. What measurable outcome or risk justifies it?
2. What lower-friction alternative was considered?
3. Is the chosen scope the smallest effective scope?
4. What could this control break?
5. How was representative behavior tested?
6. Who can approve and who can reverse it?
7. How will exceptions expire?
8. What evidence can be wrong, late, or incomplete?
9. What does the full lifecycle cost?
10. What observed result will cause scale, revision, or retirement?
