---
status: learning-prototype
tested_scope: runtime-boundary-and-adoption-risk-analysis
last_verified: 2026-09-11
---

# Agent governance challenges and trade-offs

The central review question is whether every consequential action reaches an effective control with trusted context and usable evidence. This independent lab makes that question concrete for a small set of synthetic tools. For an actual deployment, review [Microsoft AGT's security guidance](https://github.com/microsoft/agent-governance-toolkit/blob/main/SECURITY.md), select an upstream version, and test the full architecture.

## Runtime and integration risks

| Risk / early signal | Lab behavior or limitation | Production response and owner |
|---|---|---|
| Identity spoofing: request contains `role`, `actor`, or a claimed environment | Unknown argument fields are denied; identity is still a trusted fixture, not authenticated identity | Verify credentials and delegated authority outside model-controlled input; security / IAM |
| Scope or classification spoofing: request tries another resource group or labels restricted data as public | Direct resource lookup uses fixture metadata; inventory filters scope/classification | Derive scope and classification from trusted sources, and test stale metadata; data / platform |
| Unknown or changed tools: a familiar name hides new behavior | Unknown tool names are denied; handlers are fixed local code | Review tool manifests, implementation changes, schemas, and downstream authority; tool owner |
| YAML ambiguity: duplicate fields, unknown controls, permissive defaults, or invalid costs | Strict startup validation refuses these configurations | Protect policy publication, pin schema/runtime versions, and test migrations; control owner |
| Approval confusion: assistant says an operation was approved | `require_approval` never executes; there is no approval executor | Bind an authorized approval to exact action, arguments, environment, expiry, and one-time use; approval owner |
| Client shell or other tools bypass the gate | Only requests reaching this runtime are governed | Restrict credentials, network routes, tool availability, and filesystem authority; platform / security |
| Agent can change policy or evaluator | Local files and in-process objects are outside the untrusted JSON-input boundary | Separate administration and execution trust; isolate service and deployment identities; platform |
| Budget evasion through caller prices or concurrent calls | Costs come from validated policy; one runtime lock serializes check, charge, and execution | Test reservations and concurrency across all instances; FinOps / gateway |
| Restart or another process restores spending allowance | Each new runtime starts a fresh counter and evidence session | Persist shared period/workload budgets and reconcile in-flight work; FinOps / platform |
| Tool is denied but model spending continues | No model metering or model-route enforcement is implemented | Bound model output, retries, loops, fallbacks, and provider-facing usage; model gateway owner |
| Evidence sink fails before dispatch | Session closes and handler is not entered | Define fail-closed operation, recovery capacity, and incident routing; evidence platform |
| Evidence sink fails after dispatch | Handler may have completed; session closes and reports uncertainty | Reconcile the external outcome before retrying; use idempotency and recovery procedures; incident owner |
| Audit file is edited, removed, or partially lost | Local JSONL is unsigned/editable; policy hash alone does not prove integrity | Use independent storage, access control, integrity checks, missing-event detection, and retention; evidence / assurance |
| Unlimited denied requests grow evidence or queues | Teaching runtime has no service-wide admission/rate limit | Bound request size, rate, queue depth, log volume, and retention; platform / observability |
| Prompt injection or hostile tool output changes agent intent | Deterministic checks cover the listed action properties, not general content safety | Test model, content, data-egress, tool-result, and action boundaries together; security / agent owner |

AGT's upstream security guidance recommends separating policy execution from a compromised agent's process and using an external evidence store that agents cannot alter. This lab's shared local environment illustrates why those boundaries need deliberate design. [Upstream threat model and operator guidance](https://github.com/microsoft/agent-governance-toolkit/blob/main/SECURITY.md).

## Engineering trade-offs to review

| Choice | Benefit | Cost or failure to address |
|---|---|---|
| Fail closed when authority or evidence is unavailable | Avoids work whose authorization cannot be established | Availability and recovery become part of the control's operating cost |
| Require human approval for sensitive work | Introduces business judgment at a meaningful point | Queues, timeout, fatigue, replay, and unclear authority can undermine it |
| Serialize local check and execution | Makes one session's cumulative budget easy to reason about | Does not coordinate multiple processes and limits throughput |
| Retain minimal audit fields | Reduces disclosure of arbitrary prompts, arguments, and exceptions | Less context for investigations; decide which safe output references are necessary |
| Use an original small emulator | Makes policy decisions and failures inspectable without cloud access | Cannot establish compatibility, performance, or coverage of the upstream toolkit |
| Add a real tool adapter | Tests behavior closer to the business workflow | Adds credentials, real side effects, external failure modes, and reconciliation work |

The local audit trail retains decision and execution status. Full report findings are returned to the caller; they are not automatically a retained report archive. A missing completion record must not be interpreted as proof that no action ran.

## Release and organizational risks

| Risk / early signal | Response | Owner |
|---|---|---|
| Source drift: a README example, package, schema, and installed release disagree | Record commit/version, follow version-matched instructions, inspect breaking changes, and rerun representative tests before rollout | Dependency / platform owner |
| Naming confusion: readers treat this companion as the Microsoft product | Identify Microsoft AGT as the subject, link [the official repository](https://github.com/microsoft/agent-governance-toolkit), and distinguish local implementation from upstream behavior | Repository owner |
| False denials or excessive approvals frustrate users | Measure task completion, false-denial rate, review time, and exception demand; revise overly broad rules | Governance product owner |
| Agent adoption has no support or risk owner | Establish mandate, escalation, on-call response, and revocation before expanding scope | Director / sponsor |
| “Passed the lab” becomes “production secure” or “compliant” | Preserve tested scope and evidence state; use independent challenge and the [maturity model](maturity-model.md) | Assurance / risk |
| Synthetic savings become a business-case fact | Measure accepted outcomes and full costs, reconcile billing, and distinguish recommendations from realized value | FinOps / business owner |
| Public examples expose client or tenant information | Keep teaching fixtures synthetic; classify and restrict real inventory, identities, topology, and cost data | Data / repository owner |
| Exceptions or controls persist without review | Assign expiry, owner, usage review, and retirement triggers | Control / exception owner |

Use the [upstream changelog](https://github.com/microsoft/agent-governance-toolkit/blob/main/CHANGELOG.md), [breaking changes](https://github.com/microsoft/agent-governance-toolkit/blob/main/BREAKING_CHANGES.md), and this repository's [source register](source-register.md) as review inputs. A newer source claim is not a substitute for observing the installed version.

## Azure platform supplement

| Risk | Review action | Owner |
|---|---|---|
| Broad or inherited permissions permit work outside the intended scope | Inspect effective access and inheritance; separate discovery from mutation credentials | IAM / platform |
| Resource policy or remediation disrupts existing workloads | Baseline first, test representative workloads, stage exposure, review remediation permissions, and exercise recovery | Control / workload |
| Inventory omits resources or lags a recent change | State visible versus expected scope and freshness; reconcile important results with an authoritative source | Evidence owner |
| Cost reports lag work or omit allocation context | Record billing period, agreement, shared-cost method, and unresolved differences | FinOps |
| Budget alerts are mistaken for a hard spending cap | Design any stop/degrade action separately with authority and workload-criticality checks | FinOps / workload |
| Logs, security services, and review queues cost more than the claimed benefit | Include platform and human operating cost in the value ledger | Product / finance |

These risks remain even when agent policy behaves correctly. Azure RBAC grants scoped permissions, Azure Policy governs supported resource properties/actions, and Resource Graph returns a permission-dependent, eventually consistent view. [RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview), [Azure Policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview), [Resource Graph](https://learn.microsoft.com/en-us/azure/governance/resource-graph/overview). The [FinOps guide](finops.md) explains cost and budget limitations.

## Gate for expanding a pilot

For each added tool or scope, record its business outcome, smallest effective authority, trusted inputs, alternate paths, failure behavior, representative tests, evidence, full cost, and containment owner. Close or explicitly accept material gaps through the [operating model](operating-model.md). Expand only when useful outcomes and operational evidence justify the remaining risk and burden.
