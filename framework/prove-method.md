---
status: learning-prototype
tested_scope: method-design
last_verified: 2026-09-09
---

# The PROVE governance method

## Purpose

PROVE is the Lab's original operating loop for turning an agent or cloud-governance concern into a bounded, testable, and economically accountable decision. It is an operating method, not an upstream AGT API.

For the current runnable exercise, follow the [agent governance decision](templates/agent-governance-decision.example.json): profile a cloud-operations assistant, resolve tool authority and cost, operationalize the YAML host, verify execution/evidence, and evolve from observed results. The older metadata-query example remains supplementary Azure background.

```text
Profile → Resolve → Operationalize → Verify → Evolve
   ↑                                      ↓
   └──────────────────────────────────────┘
```

It is intentionally a loop. Governance assumptions, Azure capabilities, business priorities, workload behavior, threats, regulations, and costs change.

## 1. Profile

Understand the decision before selecting technology.

### Questions

- Which business outcome, obligation, or risk matters?
- Who benefits, and who owns the consequence?
- What estate and workload classes are in scope?
- What is the current baseline and confidence?
- Which facts are observed, source-supported, assumed, or unknown?
- What existing controls, policies, access, tooling, and teams already operate?

### Required output

- Problem and outcome statement.
- Accountable business or risk owner.
- Scope hypothesis and exclusions.
- Evidence coverage and unknowns.
- Initial value, feasibility, risk, adoption, and economics view.

### Failure signal

The team starts debating Azure Policy effects or IaC tools before it can explain the business consequence.

## 2. Resolve

Convert the problem into explicit choices and authority.

### Questions

- What risk tolerance or outcome threshold applies?
- What technology-neutral control objective is needed?
- What is the smallest effective scope?
- Which team can decide, implement, fund, operate, test, and accept exceptions?
- What alternatives have less friction or lower lifecycle cost?
- What evidence would change the decision?

### Required output

- Governance Decision Contract in `proposed` state.
- Control objective and options considered.
- Decision rights and exception authority.
- Proposed success, scale, stop, and reversal gates.
- Economic hypothesis without fabricated precision.

### Failure signal

The control exists because it is available or fashionable, not because its outcome, owner, and applicability are resolved.

## 3. Operationalize

Implement the smallest viable control through supported mechanisms and a safe delivery path.

### Questions

- Can a current built-in capability meet the objective?
- Should the mechanism be policy, access, configuration, monitoring, process, or a combination?
- Which scope, parameters, effects, identities, and dependencies are required?
- How will the change be validated, previewed, canaried, and rolled back?
- How will teams request help or an exception?

### Required output

- Reviewed implementation design and source/version references.
- Positive, negative, not-applicable, exception, and failure tests.
- Least-privilege identity plan.
- Audit-first deployment sequence.
- Monitoring, response, rollback, and teardown plan.

### Failure signal

An enforcement change is approved without representative tests, an impact view, or a rollback owner.

## 4. Verify

Determine whether the control operated as intended and was worth its consequences.

### Questions

- Did the mechanism evaluate and enforce the intended condition?
- Was inventory coverage complete enough for the decision?
- What false positives, false negatives, exceptions, and failures occurred?
- Did application health or delivery experience degrade?
- Can another reviewer reconstruct the decision and result?
- What did the control cost, and what benefit was actually observed?

### Required output

- Timestamped evidence with scope and limitations.
- Test, workload-health, and rollback results.
- Exception and remediation posture.
- Governance-cost and delivery-friction record.
- Observed outcome and confidence.

### Failure signal

The team reports a compliance percentage without explaining permissions, freshness, applicability, exemptions, or business effect.

## 5. Evolve

Use evidence to scale, narrow, automate, redesign, or retire.

### Questions

- Should exposure expand, pause, or reverse?
- Do exception patterns reveal a bad control or missing paved road?
- Can the control be simplified or replaced with a native capability?
- Has a platform, threat, regulation, price, or business change altered the decision?
- Is the control's lifecycle value still greater than its cost and friction?

### Required output

- Scale, revise, hold, rollback, or retire decision.
- Updated contract, control version, and source review.
- New review date and event triggers.
- Public learning lesson using synthetic or sanitized evidence.

### Failure signal

Controls accumulate indefinitely because no owner is measured on simplification or retirement.

## The Governance Decision Contract

The contract is the thread across all five phases. Its minimum content is:

| Domain | Required decision |
|---|---|
| Problem | Outcome, risk, beneficiary, baseline, and evidence status |
| Scope | Azure level, included and excluded classes, and criticality |
| Control | Objective, type, mechanism, version, and parameters |
| Accountability | Risk owner, control owner, operator, exception authority, assurance |
| Evidence | Sources, freshness, limitations, tests, retention |
| Rollout | Stage, gates, rollback trigger, stop rule, owner |
| Economics | Cost, friction, benefit classification, and validation status |
| Review | Last and next review plus event triggers |

Use the [JSON schema](schemas/governance-decision-contract.schema.json) and [synthetic example](templates/governance-decision-contract.example.json).

## Quality rules

- Use `unknown` rather than inventing a value.
- Use roles instead of personal names in public examples.
- Never put secrets or sensitive environment identifiers in a contract.
- Treat targets as proposed until a baseline and pilot validate them.
- Keep cash savings, cost avoidance, capacity release, revenue enablement, and risk reduction separate.
- A contract does not authorize an Azure change; organizational change approval remains separate.
