---
status: source-reviewed-and-wrapper-tested
tested_scope: upstream-source-review-and-version-specific-wrapper-synthetic-smoke-test
last_verified: 2026-09-11
---

# Microsoft Agent Governance Toolkit: the upstream reference

**AGT means Agent Governance Toolkit.** The official project is [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit). Microsoft introduced it as runtime governance for autonomous AI agents. An agent proposes an action; application code checks the action against policy before a tool performs it. This is the subject of this architectural review and lab. [Microsoft announcement](https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/).

Azure governance is the surrounding cloud discipline: resource organization, identity, infrastructure policy, monitoring and financial accountability. AGT adds controls to agent execution within that environment. Calling the upstream project “Azure Governance Toolkit” would obscure this distinction. See the [integration architecture](architecture.md) for how both layers work together.

This repository is an independent educational companion. Its original simulator demonstrates selected governance ideas; an [optional upstream example](../examples/upstream-agt/README.md) exercises Microsoft's wrapper from a pinned development snapshot. It is a native-build exercise, not the beginner setup. The [upstream charter](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/CHARTER.md) identifies the project, MIT license and Microsoft marks. See our [project notice](../NOTICE.md) for attribution.

## Read the right version

The source review on 2026-09-11 found important differences between GitHub release metadata, PyPI distributions and development code:

| Reference | Observed version | How to use it |
|---|---|---|
| [Latest GitHub release](https://github.com/microsoft/agent-governance-toolkit/releases/tag/v4.1.0) | `v4.1.0`, published 2026-06-09 | Historical release/API reference; not the current lab installer |
| [Release source](https://github.com/microsoft/agent-governance-toolkit/tree/0de71ca6c95cf8b9b975ac96f48eaa7826bbe258) | `0de71ca6c95cf8b9b975ac96f48eaa7826bbe258` | Immutable source reference for the release |
| [PyPI core distribution](https://pypi.org/project/agent-governance-toolkit-core/5.0.0/) | `5.0.0` | Newer than the GitHub release metadata; its cryptography upper bound still excludes the patched version |
| [Reviewed development source](https://github.com/microsoft/agent-governance-toolkit/tree/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf) | `0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf`, core source metadata `5.0.0` | Current optional example pin; differs from the same-numbered PyPI wheel and permits cryptography 50.0.1 |
| [ACS Python package metadata](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/policy-engine/sdk/python/pyproject.toml) | `agent-control-specification` source version `0.3.1b1`, Python 3.11+ | A different package/version from the toolkit release; source metadata alone does not establish an installed wheel version |

The [upstream README](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/README.md) describes Public Preview status. Treat a release, a package version, a policy schema and a source commit as four separate identifiers. Record all four in a real evaluation. A successful lab run establishes the behavior of this lab; it does not establish production readiness for every upstream component.

The publication audit found that released core 4.1.0 requires cryptography below 49 and PyPI core 5.0.0 requires it below 50. The [PKCS#7 advisory](https://github.com/pyca/cryptography/security/advisories/GHSA-g6cj-pr64-35w5) is fixed in cryptography 50.0.0. The selected source permits versions below 51; the optional example pins 50.0.1 and retains normal dependency resolution. It also introduces native ACS build dependencies. See the [setup and limitations](../examples/upstream-agt/README.md) before choosing this development-source exercise.

## What the components do

These are upstream responsibilities, not features automatically provided by the local simulator:

| Component or concern | Role in an agent system | Architectural question |
|---|---|---|
| Agent OS and the policy runtime | Connect agent execution to policy checks | Does the tool invocation actually pass through the enforcement point? |
| Agent Control Specification, ACS | Evaluate a snapshot at a declared intervention point and return a verdict | Do manifest bindings match the adapter's actual snapshot fields? |
| AgentMesh | Agent identity, delegation and trust relationships | Who authenticates the caller and limits delegated authority? |
| Runtime and sandbox integration | Apply execution limits and connect to isolation mechanisms | Which restrictions are enforced by application code, and which by the OS or container? |
| MCP gateway and adapters | Mediate supported tool interfaces | Can a client reach the same capability through another server or shell? |
| Audit and evidence | Record decisions and their context | Can reviewers correlate policy, request, execution and outcome? |
| Agent SRE | Reliability, operational budgets and response controls | Who reacts to a runaway workflow or a failing dependency? |

The [upstream architecture and security boundaries](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/docs/ARCHITECTURE.md) describe these components. The [ACS Python SDK](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/policy-engine/sdk/python/README.md) describes the actual host and adapter interfaces. Select the components needed for a workload and verify their behavior together.

## YAML formats are different contracts

“A YAML policy” does not identify an executable format. The consumer determines the schema and behavior:

| Format | Recognizable fields | Consumer and boundary |
|---|---|---|
| This lab's policy | Its own documented schema, identity, tool and budget settings | The original simulator in this repository; educational and intentionally small |
| AgentMesh wrapper policy | `apiVersion: governance.toolkit/v1`, `name`, `default_action`, `rules`, string `condition` and `action` | `agentmesh.governance.govern()` and its own policy implementation |
| Native ACS manifest | `agent_control_specification_version`, `policies`, `intervention_points`, `policy_target`, `tools` | `agent_control_specification.AgentControl` plus the configured policy dispatcher |
| Older Agent OS policy documents | Pre-ACS rule models and their adapters | Version-specific legacy APIs; current development code removes these surfaces |

The [released AgentMesh parser](https://github.com/microsoft/agent-governance-toolkit/blob/0de71ca6c95cf8b9b975ac96f48eaa7826bbe258/agent-governance-python/agent-mesh/src/agentmesh/governance/policy.py) and [current ACS example manifest](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/examples/acs-email-tool/manifest.yaml) demonstrate the difference. Copying a file between these consumers does not make it compatible. An unsupported key must not be mistaken for an active control.

In the reviewed development source, ACS is the policy runtime and the former Agent OS rule model is removed. The separate AgentMesh wrapper still exists. Read the [native policy contract](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/docs/specs/AGENT-OS-POLICY-ENGINE-1.0.md) and the [breaking-change record](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/BREAKING_CHANGES.md) before choosing or migrating an API.

## Two upstream examples to study

For historical comparison, the [v4.1.0 wrapper source](https://github.com/microsoft/agent-governance-toolkit/blob/0de71ca6c95cf8b9b975ac96f48eaa7826bbe258/agent-governance-python/agent-mesh/src/agentmesh/governance/govern.py) exposes `govern(callable, policy=..., agent_id=...)`; denied calls raise `GovernanceDenied` before the wrapped function runs. The [release package metadata](https://github.com/microsoft/agent-governance-toolkit/blob/0de71ca6c95cf8b9b975ac96f48eaa7826bbe258/agent-governance-python/agent-governance-toolkit-core/pyproject.toml) places that implementation in core 4.1.0 and requires Python 3.11+. This older distribution is not the recommended installer because of the dependency issue above.

The [local upstream example](../examples/upstream-agt/README.md) now supplies an isolated source-build setup, an original YAML policy and a self-checking script. It checks the exact source origin as well as package versions, then expects one permitted request to execute and three denied requests never to reach the handler. The [validation record](validation.md) distinguishes the original Windows 4.1.0 smoke test, the failed Windows native-source installation, and the current Linux CI gate. This is an AgentMesh wrapper exercise, not validation of the newer ACS execution path or a provider-backed session.

For the newer ACS host model, the [pinned email-tool walkthrough](https://github.com/microsoft/agent-governance-toolkit/tree/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/examples/acs-email-tool) is especially instructive. It uses synthetic recipients and a local stand-in for sending email. The example demonstrates allow, argument transformation and deny without a model credential. Its setup builds the SDK from the same repository checkout; source builds require the native build toolchain. Keep the checkout and example at the same commit.

The sequence in its [host code](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/examples/acs-email-tool/run.py) is:

1. Load the manifest and a custom dispatcher into `AgentControl`.
2. Create a `HostSession` and submit a `pre_tool_call` snapshot.
3. Inspect `result.verdict.decision.permits`.
4. If transformation is required, use `transformed_policy_target` as the tool arguments.
5. Invoke the tool only after the permitted decision, then record the completed call.

The newer ACS example was source-reviewed for this guide; its native runtime was not executed in this validation. The source-pinned AgentMesh wrapper example and the original simulator have separate test scopes. The [technical guide](technical-implementation.md) identifies the executable paths and tests provided here.

## Migration details that change outcomes

The reviewed [breaking-change record](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/BREAKING_CHANGES.md) includes several behavior changes worth testing explicitly:

- Current hosts use `AgentControl` and `HostSession`; the intermediate `agt.policies` wrapper is removed.
- Every intervention point evaluated by the chosen adapter needs a manifest binding. An unconfigured point is denied.
- `HostSession` and agent adapters use nested tool-result fields such as `$.tool_result.value`; other entry points can still have different shapes.
- Tool-call budget accounting changed from including the proposed call to counting already completed calls. Recheck boundary cases when migrating limits.
- Approval timeout configuration belongs to the host session; a similarly named manifest field does not automatically configure it.

Test the exact adapter and package combination. Checking that YAML parses is insufficient: a binding can resolve to the wrong object and change the decision.

## What the simulator teaches, and where the mapping ends

| Lab concept | Upstream connection | What still needs a real integration |
|---|---|---|
| A policy check before a synthetic tool executes | AGT host enforcement and ACS `pre_tool_call` | A reviewed adapter around every consequential operation |
| Allowed and denied tool requests | Policy decisions and fail-closed handling | Full policy semantics, version migration and workload-specific tests |
| A configured caller identity | Identity-aware authorization | Authentication, signed identity, delegated authority and lifecycle management |
| An approval-required outcome | Upstream approval/escalation mechanisms | An authenticated approver, action binding, expiry and replay protection |
| Synthetic budget accounting | Cost-aware governance | Provider usage metering, shared durable budgets and invoice reconciliation |
| A decision record | Audit and evidence systems | Protected retention, external integrity verification and operational review |
| An MCP client calling the lab server | Governance at a tool boundary | Coverage of all client capabilities and prevention of alternate access paths |

This mapping is an architectural comparison, not an assertion that the simulator implements AGT APIs, ACS conformance, cryptographic trust, agent isolation or all upstream guardrails.

There is also a specific cost-model distinction. [AGT's accepted cost-governance design](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/docs/adr/0012-cost-governance-observability-policies.md) describes observing costs after execution, issuing soft-cap alerts and blocking subsequent actions after a hard cap. The crossing action can therefore overshoot. A lab check against an estimated cost before execution is a different educational mechanism. Neither synthetic accounting nor a delayed cloud budget alert is proof of a provider-wide spending cap. The [FinOps guide](finops.md) explains how to reconcile these controls.

## Architectural review questions

Before adopting an upstream component in a real system, establish the following:

- The host, adapter, SDK and policy versions are compatible and reproducible.
- The trusted code owns policy, identity, cost inputs and tool credentials; the model cannot supply its own authorization.
- Every privileged action crosses an enforced boundary, including alternative tools, delegated agents and direct network access.
- Pre-action denial prevents the side effect. Post-action filtering can suppress a result but cannot undo an action that already happened.
- Approval and exception records bind to the exact action and expire; a role name typed into a prompt is not approval.
- Evidence reaches an appropriately protected store with a known failure and retention policy.

AGT's application middleware operates inside the application's trust boundary. Host isolation, least-privilege credentials and network controls remain part of the overall design. Similarly, adding this lab as an MCP server governs calls to that server; it does not intercept every operation a coding assistant can perform. These boundaries are central to the [reference architecture](architecture.md), [control catalog](control-catalog.md) and [learning path](learning-path.md).
