---
status: learning-prototype
tested_scope: curriculum-design
last_verified: 2026-09-09
---

# Public learning path

## Method

Each sprint begins with a leadership or operating decision and produces one reusable artifact. Use the five lenses from the source CXO Learning Log:

- **Value:** which measurable outcome changes?
- **Feasibility:** are platform, data, skills, access, and operations viable?
- **Risk:** what could the workload or the control harm?
- **Adoption:** will teams use the governed path correctly?
- **Economics:** does confidence-adjusted benefit justify lifecycle cost and friction?

Separate assumptions from observed evidence and keep source dates and revalidation triggers.

## Eight learning sprints

| Sprint | Executive question | Technical focus | Reusable output |
|---:|---|---|---|
| 1 | What does cloud governance enable, and who owns it? | CAF Govern, operating model, risk appetite | Governance charter and RACI |
| 2 | How should the estate be divided for control and autonomy? | Management groups, subscriptions, landing zones, vending | Scope decision and hierarchy rationale |
| 3 | Who and what can act, where, and for how long? | Entra identities, Azure RBAC, PIM, managed identities | Privileged-access decision contract |
| 4 | Which risks justify technical guardrails? | Azure Policy definitions, initiatives, effects, exemptions | Initial control catalog |
| 5 | How do we change governance without harming workloads? | Policy as code, IaC, preview, canary, rollback | Safe rollout and test plan |
| 6 | Can we see and prove the current state? | Resource Graph, Policy Insights, Monitor, evidence model | Read-only baseline and limitations |
| 7 | Is governance improving cloud economics? | Cost Management, budgets, allocation, Advisor, unit economics | FinOps scorecard and value ledger |
| 8 | Should we scale, revise, or stop? | Integrated sandbox review | Executive decision pack and public lesson |

## Lesson structure

Every lesson should answer:

1. What decision is being learned?
2. What is the business problem without product names?
3. What is the core insight?
4. What did primary sources establish?
5. What remains an assumption or design proposition?
6. What options and trade-offs were evaluated?
7. What artifact was created?
8. How was it tested, and in what scope?
9. What failed, surprised, or remains unknown?
10. What is the next evidence action and owner?

## Evidence ladder

Label claims with the strongest achieved state:

| State | Meaning |
|---|---|
| Proposed | An original idea or target without validation |
| Source-supported | A primary source supports the platform fact |
| Fixture-tested | A local synthetic test passed |
| Sandbox-observed | Behavior was observed in a named, nonproduction scope |
| Limited-pilot observed | Behavior was observed across an approved limited pilot |
| Revalidated | A material change triggered and passed a new review |

Do not promote a claim because it sounds plausible.

## Publication checklist

- [ ] Uses a business decision rather than a feature summary.
- [ ] States tested scope and date.
- [ ] Separates Microsoft facts, original proposals, assumptions, and observations.
- [ ] Uses only primary sources for current technical claims.
- [ ] Contains no employer, client, tenant, identity, cost, or security information.
- [ ] Shows advantages, disadvantages, and failure modes.
- [ ] Includes ownership, economics, and workload impact.
- [ ] Defines scale, stop, and reversal criteria.
- [ ] Links the reusable artifact.
- [ ] Adds source freshness and a revalidation trigger.
