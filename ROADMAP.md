# Roadmap

The roadmap advances by evidence, not by date alone.

## Phase 0 — Foundation

**Goal:** establish a safe, independent project boundary.

- [x] Product scope and non-goals
- [x] Executive brief
- [x] PROVE method and Governance Decision Contract schema
- [x] Source register and freshness rules
- [x] Initial control, challenge, FinOps, and maturity models
- [x] Confidentiality, trademark, contribution, and license boundaries
- [ ] Final project-name clearance
- [ ] Intentional public code and documentation license decision

## Phase 1 — v0.1 read-only governance baseline

**Goal:** produce a repeatable baseline without changing Azure.

- [x] Initial Resource Graph inventory and tag queries
- [ ] Synthetic estate fixture
- [ ] PowerShell 7 assessment command
- [ ] Normalized evidence snapshot schema
- [ ] Human-readable baseline report
- [ ] Permission and coverage reporting
- [ ] Sanitization tests
- [ ] Offline fixture tests
- [ ] Reader-only sandbox validation

**Exit gates:** zero Azure writes; incomplete scope is visible; outputs contain no secrets or real identifiers; the same fixture produces the same result; every recommendation maps to evidence, an owner, and a validation action.

## Phase 2 — v0.2 audit-only sandbox canary

**Goal:** test a small guardrail set safely.

- [ ] Choose Bicep or Terraform reference path and record the decision
- [ ] Add policy-as-code validation
- [ ] Prefer built-in policy definitions where suitable
- [ ] Validate `what-if` or `plan` output
- [ ] Assign only audit or disabled enforcement at narrow sandbox scope
- [ ] Test exceptions, rollback, and teardown
- [ ] Measure false positives, application impact, and operating effort

**Exit gates:** representative tests pass; deployment and rollback identities are least-privileged; no broad assignment; evidence is reconstructable; workload owner approves the observed impact.

## Phase 3 — v0.3 exceptions and evidence operations

**Goal:** make the control lifecycle operable.

- [ ] Machine-readable exemption record and expiry checks
- [ ] Evidence correlation and retention design
- [ ] Policy-version monitoring
- [ ] Remediation workflow with narrow permissions
- [ ] Support service levels and escalation path
- [ ] Control-owner review cadence

## Phase 4 — v0.4 FinOps integration

**Goal:** govern both cloud cost and governance cost.

- [ ] Allocation and tag-quality scorecard
- [ ] Budget and anomaly response contract
- [ ] Advisor recommendation realization tracking
- [ ] Microsoft FinOps toolkit integration pattern
- [ ] Unit-economics example using synthetic data
- [ ] Governance cost and delivery-friction ledger

## Phase 5 — limited multi-subscription pilot

**Goal:** test portability and operating ownership with explicit authorization.

- [ ] Nonproduction multi-subscription scope
- [ ] Subscription-vending integration pattern
- [ ] Progressive policy exposure
- [ ] Quarterly control review
- [ ] Sanitized public lessons and observed limitations

## Later candidates

- Optional Bicep and Terraform adapters
- Defender for Cloud and Azure Monitor evidence adapters
- Policy Insights queries and dashboards
- Deployment stacks evaluation with safe unmanage defaults
- Regulatory control mappings with explicit non-certification boundary
- Community examples after contribution and license decisions

## Maturity labels

Use only these labels until a future decision changes them:

- `concept`
- `learning-prototype`
- `locally-tested`
- `sandbox-validated`
- `limited-pilot`

Do not use `production-ready`, `certified`, or `compliant` for this project without independently defined and evidenced criteria.
