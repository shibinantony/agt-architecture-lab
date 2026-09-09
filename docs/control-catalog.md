---
status: learning-prototype
tested_scope: design-only
last_verified: 2026-09-09
---

# Initial control catalog

## Use

This catalog defines technology-neutral control objectives and minimum evidence. It is not a regulatory checklist and does not claim that every control applies to every environment. Each adopted control requires its own Governance Decision Contract, local risk basis, implementation, tests, and owner.

| ID | Control objective | Typical Azure mechanism | Minimum evidence | Example test | Primary owner |
|---|---|---|---|---|---|
| GEL-ORG-01 | Every governed subscription has an approved purpose, owner, workload class, criticality, and lifecycle state | Subscription vending metadata, management-group placement, tags or registry | Intake decision, current owner, scope, review date | Sample new, transferred, sandbox, and decommissioned subscriptions | Platform owner |
| GEL-ORG-02 | Management-group placement reflects common control needs and is not changed without impact review | Management Groups and reviewed IaC | Before/after inheritance map, approval, deployment result | Move a synthetic subscription and compare effective policy/RBAC | Platform architect |
| GEL-IAM-01 | Privileged access is least-privileged, scoped, time-bound where supported, and reviewed | Entra groups, Azure RBAC, PIM, access reviews | Role, principal type, scope, assignment state, review result | Find standing broad roles, direct user assignments, and expired eligibility | IAM owner |
| GEL-IAM-02 | Automation identities are separated by validation, deployment, and remediation responsibility | Managed identities, workload identity, Azure RBAC | Identity-to-operation map, role assignments, credential method | Verify collector cannot write and remediator cannot exceed control scope | Platform and IAM owners |
| GEL-POL-01 | Every policy assignment maps to an approved risk, owner, version, scope, parameters, and test | Azure Policy, Git, optional EPAC | Decision contract, definition ID/version, assignment diff, test result | Trace a sampled assignment from risk to current evidence | Control owner |
| GEL-POL-02 | Policy changes use progressive exposure and application-health gates | Audit/disabled effects, overrides, resource selectors, CI/CD | Preview, canary stages, expected results, approvals, rollback | Introduce compliant and noncompliant fixtures at each tier | Platform owner |
| GEL-EXC-01 | Every exception is justified, bounded, owned, monitored, and time-limited | Azure Policy exemptions plus repository record | Control reference, scope, reason, approver, compensating control, expiry | Test expired, over-broad, wrong-control, and missing-owner cases | Exception authority |
| GEL-INV-01 | Governance inventory declares scope, permissions, freshness, pagination, failures, and unknowns | Azure Resource Graph and collector metadata | Coverage statement, timestamps, query version, counts, failures | Remove access to one scope and verify it becomes unknown | Evidence owner |
| GEL-FIN-01 | Cloud cost is allocated using approved dimensions and known gaps are visible | Cost Management scopes, tags, tag inheritance, cost allocation | Allocation method, coverage, unallocated/shared cost, freshness | Test unsupported, missing, invalid, and late tag data | FinOps owner |
| GEL-FIN-02 | Budgets and anomalies route to an accountable owner and produce a documented decision | Cost Management budgets, forecast and anomaly alerts | Alert, owner, response, disposition, outcome | Trigger or simulate threshold and verify routing and decision | FinOps and workload owners |
| GEL-FIN-03 | Optimization value is recognized only after action and observed outcome | Azure Advisor, cost exports, action register | Recommendation, decision, implemented action, before/after measure | Sample rejected, implemented, reversed, and expired recommendations | FinOps owner |
| GEL-SEC-01 | Security-posture findings have scope, owner, severity, due date, exception, and evidence | Defender for Cloud and Microsoft Cloud Security Benchmark | Finding, affected scope, owner, disposition, retest | Sample high-severity and exempt findings through closure | Security owner |
| GEL-OBS-01 | Required governance and platform signals are collected, routed, retained, and costed | Activity logs, diagnostic settings, Azure Monitor, Log Analytics | Data source, alert route, retention, access, monthly cost | Disable a signal or action group and verify detection | Observability owner |
| GEL-CHG-01 | Upstream policy, API, pricing, licensing, preview, and retirement changes trigger impact review | Source register, dependency inventory, release monitoring | Change notice, affected artifacts, decision, due date | Simulate a built-in policy version or retirement notice | Product owner |
| GEL-EVD-01 | An independent reviewer can reconstruct each material control decision and operating result | Repository, Azure evidence sources, integrity metadata | Linked decision, deployment, result, exception, remediation, economics | Reconstruct a sampled control within the target service level | Assurance owner |
| GEL-RET-01 | Obsolete controls, identities, exceptions, data, and resources are retired safely | Git change, Azure deletion/detach workflow, retention process | Retirement approval, impact preview, teardown result, residual check | Retire a synthetic control and confirm no orphaned identity or cost | Platform owner |

## Control design fields

Every implemented control should define:

- business outcome or risk;
- control objective and type: preventive, detective, corrective, or directive;
- applicability and explicit non-applicability;
- Azure scope and inheritance;
- owner, operator, risk authority, and exception authority;
- supported mechanism and version;
- parameters, exclusions, dependencies, and failure mode;
- positive, negative, exception, stale-data, and service-failure tests;
- evidence source, freshness, access, integrity, and retention;
- finding severity and remediation service level;
- expected cost and delivery friction;
- rollout stage and last observed result;
- rollback trigger and procedure; and
- next review or retirement trigger.

## Mapping discipline

Use this chain:

```text
business outcome or risk
  → policy statement
  → control objective
  → implementation mechanism
  → evidence source
  → test
  → owner and response
```

Do not start with a regulatory label or Azure Policy initiative and assume every included definition is applicable. Document the local interpretation and evidence boundary.
