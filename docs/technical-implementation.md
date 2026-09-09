---
status: learning-prototype
tested_scope: design-only
last_verified: 2026-09-09
---

# Technical implementation guide

## Current boundary

This guide defines the intended implementation path. The repository currently contains no Azure deployment package and has not been validated against a tenant. Commands capable of changing Azure are deliberately excluded from v0.1.

## Reference stack

| Concern | Initial choice | Reason |
|---|---|---|
| Knowledge and decisions | Markdown and Mermaid | Reviewable, portable, and readable by leadership and engineering |
| Decision contract | JSON plus JSON Schema | Machine validation and language-neutral integration |
| Local orchestration | PowerShell 7 | Common in Azure platform teams and cross-platform |
| Read-only inventory | Azure Resource Graph / KQL | Efficient queries across authorized subscriptions |
| Azure interface | Azure CLI | Scriptable and works with interactive or federated identity |
| Policy | Native Azure Policy resources; optional EPAC evaluation | Avoid inventing a policy engine |
| Infrastructure as code | Decision pending: Bicep or Terraform | Must match target audience and operating model |
| CI/CD | GitHub Actions, later | Review, schema validation, IaC build, fixtures, and gated deployment |
| Pipeline identity | OpenID Connect / workload identity, later | Avoid stored client secrets |
| Cost insights | Cost Management and optional Microsoft FinOps toolkit integration | Compose supported capabilities rather than fork them |

## Planned repository layers

```text
framework/        original method, contracts, schemas, and templates
toolkit/queries/  read-only inventory and evidence queries
infrastructure/   future policy and IaC packages
scripts/          future collectors and report generators
tests/            local contract, fixture, and repository tests
examples/         synthetic estates and expected reports
docs/             executive, architecture, operations, and learning material
```

## Prerequisites by mode

### Local learning

- Git.
- PowerShell 7 recommended; Windows PowerShell can run the current repository check.
- A JSON-aware editor.
- No Azure access.

### Read-only assessment

- An explicitly approved sandbox scope.
- Azure CLI and Resource Graph extension where required.
- Azure `Reader` at only the intended scope.
- Optional Cost Management Reader or Security Reader only when the approved assessment requires those signals.
- A local output path excluded from Git.

### Future sandbox policy pilot

- Separate change authorization.
- A deployment identity scoped to the sandbox.
- Permission to validate and assign only the approved policy resources.
- A separate remediation identity if modify or deploy-if-not-exists is tested.
- Infrastructure-as-code toolchain selected and pinned.
- A documented rollback and evidence-retention path.

## Stage 0 — establish the contract

1. Copy the [Governance Decision Contract example](../framework/templates/governance-decision-contract.example.json).
2. Replace synthetic values with a non-sensitive learning scenario.
3. Validate the JSON structure against the [schema](../framework/schemas/governance-decision-contract.schema.json).
4. Keep `evidence_status` as `assumption` until an observation supports the claim.
5. Name the business risk owner, control owner, platform operator, and exception authority.
6. Set a proposed rollout, rollback trigger, stop rule, and review date.

The current repository test parses JSON and checks local Markdown links:

```powershell
./tests/Test-Repository.ps1
```

## Stage 1 — read-only discovery

The collector planned for v0.1 must perform only query operations. Its output should include:

- query and tool version;
- tenant and subscription coverage expressed without publishing identifiers;
- caller permission boundary;
- collection start and end time;
- result count and pagination state;
- source freshness or known indexing delay;
- inaccessible scopes and failed queries;
- sanitized findings; and
- a content hash for repeatability.

Initial queries appear under [toolkit/queries](../toolkit/queries/README.md). Until tenant validation is completed, paste them into Azure Resource Graph Explorer in a sandbox and inspect results manually. Do not interpret zero rows as proof of compliance without validating access and query applicability.

## Stage 2 — select controls

For each risk:

1. Define a technology-neutral control objective.
2. Search current built-in Azure Policy definitions and supported platform capabilities.
3. Record why a built-in, configuration, process, access control, alert, or custom policy is appropriate.
4. Define scope, parameters, exclusions, and affected workload classes.
5. Specify compliant, noncompliant, not-applicable, exempt, stale-data, and unavailable-service tests.
6. Estimate operating cost and workload friction.
7. Define evidence and remediation ownership.

Do not copy a built-in policy into this repository merely to make it appear complete. Reference official identifiers and versions when implementation begins.

## Stage 3 — policy as code

The future implementation should maintain separate artifacts for:

- definitions;
- initiatives;
- assignments and parameters;
- exemptions;
- remediation configuration;
- scope topology; and
- expected tests.

Minimum pull-request gates:

| Gate | Required result |
|---|---|
| Schema and syntax | All JSON, Bicep, Terraform, and metadata validate |
| Source and version | Built-in or custom provenance is explicit |
| Scope diff | Reviewers can see added, changed, and removed assignments |
| Infrastructure preview | `what-if` or `plan` is attached and reviewed |
| Policy behavior | Positive, negative, exemption, and not-applicable fixtures pass |
| Permission diff | New deployment or remediation permissions are justified |
| Blast radius | Affected subscriptions, regions, resource types, and workloads are estimated |
| Economics | Monitoring, remediation, and delivery-friction impact is stated |
| Rollback | Reversal steps and owner are defined before approval |

## Stage 4 — safe deployment

Use the sequence recommended by Microsoft's Azure Policy safe-deployment guidance:

```text
static validation
  → sandbox assignment with audit or disabled enforcement
  → compliance and application-health review
  → narrow canary
  → expanded audit coverage
  → selective enforcement canary
  → staged enforcement
```

At every stage:

- validate both policy results and application health;
- preserve a known-good version;
- expand exposure only after a named reviewer approves the evidence;
- keep an exception route ready;
- stop on unexpected denials, modification, remediation, or telemetry gaps; and
- reconcile orphaned assignments and identities after rollback.

## Stage 5 — remediation

Evaluation and remediation are different risk events. A policy can correctly identify a gap while its remediation performs an unsafe change.

- Test remediation independently in a disposable or representative environment.
- Use the narrowest role and scope for the managed identity.
- Estimate the number and type of resources to be changed.
- Define concurrency, throttling, failure handling, and retry behavior.
- Record before-and-after state and affected resource count.
- Never grant broad permissions solely to make a remediation task succeed.
- Obtain a separate approval for changes that can interrupt or recreate resources.

## Stage 6 — evidence and operations

A control enters operations only when it has:

- named business, control, platform, remediation, and exception owners;
- a supported definition and assignment version;
- monitoring and alert routing;
- evidence freshness and retention rules;
- remediation and incident service levels;
- an exemption review cadence;
- lifecycle cost and friction measures;
- rollback and retirement criteria; and
- a platform-change revalidation trigger.

## Secrets and identities

- Do not store Azure credentials in GitHub secrets when workload identity federation can be used.
- Do not use personal credentials for unattended automation.
- Separate pull-request validation from deployment permission.
- Protect production environments with explicit approvals.
- Record object and role identifiers through configuration without publishing real tenant values in examples.
- Rotate or remove identities when a pilot ends.

## Deployment stacks caution

Deployment stacks can manage resource lifecycle and deny settings. They can also act on resources that become unmanaged. Any future use must:

- pin and review the intended scope;
- test known limitations;
- list resources to be owned;
- default the first lab to detach rather than delete;
- require a reviewed deletion plan before destructive `actionOnUnmanage` behavior; and
- test removal and rollback in sandbox.

## Exit criteria before any limited pilot

- The local fixture suite is deterministic.
- The read-only collector reports coverage and unknowns correctly.
- No output contains secrets or unapproved environment identifiers.
- Every control has a decision contract and named owner.
- Representative policy fixtures pass.
- Preview, canary, rollback, and teardown have been exercised.
- Remediation permissions have an independent review.
- Evidence retention and operating cost are approved.
- Workload owners understand the impact and exception path.
- The release is labelled `sandbox-validated`, not `production-ready`.
