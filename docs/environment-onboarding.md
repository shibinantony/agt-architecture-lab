---
status: learning-prototype
tested_scope: process-design
last_verified: 2026-09-09
---

# Environment onboarding

## Choose the starting mode

| Mode | Azure access | Changes Azure? | Use when |
|---|---|---:|---|
| Local simulation | None | No | Learning, framework review, schema and fixture testing |
| Read-only assessment | Reader at approved sandbox scope | No | Establishing an inventory and evidence baseline |
| Audit-only sandbox pilot | Separate deployment identity | Yes, narrow and approved | Testing policy applicability and operational impact |

Start at the lowest mode that can answer the decision. Access to a production environment is not a shortcut for missing fixtures or ownership.

## Entry questionnaire

Answer these before requesting Azure access:

### Outcome and authority

- What business outcome, risk, or audit issue motivates the work?
- Who is accountable for the outcome and residual risk?
- Who can authorize read access, change, remediation, rollback, and public use of lessons?
- What is explicitly out of scope?

### Estate and criticality

- Which tenant, management group, subscription, or resource-group scope is intended?
- Is the environment sandbox, nonproduction, or production?
- Which workloads are business-critical, regulated, externally exposed, or difficult to interrupt?
- Who owns existing landing-zone and IaC deployments?

### Data and confidentiality

- Can inventory, role, policy, cost, security, or network information leave the tenant?
- Which identifiers must be hashed, generalized, or removed?
- Where may raw output be stored, who may read it, and when must it be deleted?
- Is public publication permitted only for synthetic examples?

### Operations and economics

- Who will triage findings and exceptions?
- What response times are realistic?
- Which monitoring, security, reporting, or retention features incur cost?
- What evidence will show value, friction, and stop conditions?

## Mode 1 — local simulation

1. Clone or copy the repository locally.
2. Run `./tests/Test-Repository.ps1`.
3. Read the [executive brief](../EXECUTIVE-BRIEF.md) and [architecture](architecture.md).
4. Copy the example Governance Decision Contract and change only synthetic values.
5. Walk through a scenario such as missing ownership metadata or excessive permanent access.
6. Identify assumptions, evidence required, appropriate Azure mechanisms, and reversal triggers.
7. Record the lesson using the [learning path](learning-path.md).

**Exit condition:** another reviewer can reconstruct the decision without Azure access.

## Mode 2 — read-only assessment

### Minimum preparation

- Use a sandbox subscription or other explicitly approved narrow scope.
- Obtain Azure `Reader` only at that scope.
- Add Cost Management Reader or Security Reader only if the approved questions require it.
- Use a named, non-shared identity with multifactor authentication.
- Confirm the output path is ignored by Git.
- Agree sanitization and deletion rules before collection.

### Collection sequence

1. Record the authenticated identity, intended scope, and collection time privately.
2. Verify that the caller can enumerate the exact expected subscriptions.
3. Run a simple resource count and compare it with a trusted portal view.
4. Test pagination and query failure behavior.
5. Run the inventory and tag-coverage queries.
6. Record inaccessible providers, scopes, tables, or role-dependent data.
7. Timestamp and hash raw output before transformation.
8. Generate a sanitized summary with no real names or identifiers for public learning.
9. Review findings with the platform and workload owners.
10. Delete or retain raw data according to the approved rule.

### Coverage rule

Use these result states:

| State | Meaning |
|---|---|
| Observed compliant | The applicable resource was visible and met the tested condition at the recorded time |
| Observed noncompliant | The applicable resource was visible and failed the tested condition |
| Exempt | An approved, valid, in-scope exception was found |
| Not applicable | The test does not apply and the basis is recorded |
| Unknown | Permissions, query failure, latency, or missing evidence prevents a conclusion |

Never collapse `unknown` into `compliant`.

## Mode 3 — audit-only sandbox pilot

This mode changes Azure and requires separate organizational approval.

1. Confirm the sandbox and affected workloads.
2. Create a decision contract for each proposed control.
3. Choose the current built-in definition or reviewed custom artifact.
4. Validate the infrastructure and policy code locally.
5. Review `what-if` or `plan` output.
6. Use a separate deployment identity with narrow scope.
7. Assign with audit or disabled enforcement.
8. Wait for and verify evaluation results; account for indexing and evaluation latency.
9. Test compliant, noncompliant, exempt, and unexpected workload cases.
10. Measure false positives, remediation effort, support demand, cost, and workload friction.
11. Exercise rollback and remove unused identities or assignments.
12. Decide whether to revise, hold, stop, or propose a canary enforcement test.

Audit mode can still create cost and operational work. It is not risk-free simply because it does not deny a deployment.

## Greenfield onboarding

- Begin with the current Azure Landing Zone conceptual architecture.
- Define the platform landing zone, application landing zones, subscription-vending path, hierarchy, and centralized capabilities.
- Decide which requirements genuinely need common inheritance.
- Validate controls before workloads depend on them.
- Keep sandbox and decommissioned paths explicit.
- Automate only after the manual decision flow is understood.

## Brownfield onboarding

Brownfield work begins with discovery, not reorganization.

- Inventory existing management groups, subscriptions, assignments, exemptions, RBAC, shared services, deployment ownership, and critical workloads.
- Identify resources managed by other IaC states, deployment stacks, or desired-state tools.
- Map policy effects inherited from every parent scope.
- Identify missing owners and operational dependencies.
- Establish an audit baseline before moving subscriptions or applying new controls.
- Use canary scopes that represent the estate without exposing critical workloads first.
- Treat changes to hierarchy, deny policy, modify policy, remediation, locks, role assignments, and deployment ownership as separate change decisions.

## Onboarding outputs

An onboarding package should contain:

- approved scope and exclusions;
- named owners and decision rights;
- permission and coverage statement;
- sanitized inventory baseline;
- initial control and exception register;
- risk, cost, and workload criticality profile;
- proposed sandbox tests;
- data handling and deletion rules;
- rollout, rollback, and stop gates; and
- unresolved questions.

## Readiness checklist

- [ ] Executive or risk owner is named.
- [ ] Platform and workload owners are involved.
- [ ] Scope and environment classification are explicit.
- [ ] Least-privilege access is approved.
- [ ] Raw output handling is approved.
- [ ] Public material will use synthetic or fully sanitized data.
- [ ] Query coverage and unknown states are reported.
- [ ] No write operation is hidden inside a read-only mode.
- [ ] Change, remediation, and rollback require separate authorization.
- [ ] Monitoring and operating cost are understood.
- [ ] Success, stop, and review dates are recorded.
