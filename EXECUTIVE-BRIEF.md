---
status: learning-prototype
tested_scope: executive-decision-design
last_verified: 2026-09-11
owner: Shibin Antony
---

# Executive brief: Microsoft Agent Governance Toolkit (AGT) — Architecture Review & Hands-on Lab

This is an independent companion to Microsoft's [Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit), the upstream project for governing AI agent actions. Azure is the example enterprise environment. The repository provides an original teaching emulator, a separate [AGT source-snapshot exercise](examples/upstream-agt/README.md), and an adoption framework. The two examples have distinct implementations and validation scopes.

## The business decision

Choose whether one bounded agent workflow merits a measured pilot. A useful first candidate is an assistant that reviews an Azure inventory, estimates cost, and drafts a governance report. Give it explicit permission to inspect approved data, prevent destructive operations, and route sensitive actions to a human decision.

The funding question is: **can a controlled agent produce an accepted business result with less effort and acceptable risk, total cost, and operating burden?** Installing a toolkit does not answer that question.

| Choice | When it fits | Evidence to require |
|---|---|---|
| Run a bounded pilot | A repeatable workflow has a business owner, an approved dataset, and a measurable baseline | Accepted-result rate, full operating cost, control coverage, exception demand, and rollback exercise |
| Continue offline learning | The team needs to understand tool boundaries, YAML policies, or evidence before selecting a workload | Completed [role exercises](docs/learning-path.md) and a reviewed architecture |
| Defer this use case | Risk exceeds delegated authority, benefits are weak, or ownership is absent | Recorded reason, cheaper alternatives, and a specific reconsideration trigger |

## What the demonstration makes concrete

Run the [hands-on lab](docs/lab-guide.md) or have an engineer present its evidence. A YAML policy evaluates tool requests before execution. The demo exercises allowed work, denied work, a request requiring approval, and a synthetic tool-budget limit, then writes audit and summary artifacts.

That lets leadership examine a decision trail: requested action, applicable policy, decision, outcome, and budget effect. The default run uses fixtures and makes no cloud or model calls. Its results demonstrate local policy behavior; they do not measure production incident reduction, provider spending, or ROI.

The separate AGT exercise targets a pinned development snapshot whose core package reports version 5.0.0; it is not a released-package installation. Its assertions require one permitted request to execute and three denied requests to remain outside the handler. See the [validation record](docs/validation.md) for the tested platform and results. These four synthetic requests address wrapper behavior, not production readiness, ACS conformance, or an end-to-end model-provider integration.

The optional MCP route lets a configured Codex or Gemini CLI client request these guarded tools. Its boundary is those tools. Other shell commands, connections, credentials, and model requests require their own controls. See the [architecture](docs/architecture.md) for the full integration and bypass paths.

## What changes in the enterprise architecture

Place agent governance between the agent's proposed action and the business tool that can carry it out. Combine it with identity and access controls, network restrictions, a model gateway, content safeguards, approval services, and durable evidence storage. Azure Policy governs supported Azure resource properties and actions; agent policy evaluates actions at integrated agent/tool boundaries, including non-Azure tools. Each has a distinct owner and scope. [Azure Policy overview](https://learn.microsoft.com/en-us/azure/governance/policy/overview).

The [upstream AGT repository](https://github.com/microsoft/agent-governance-toolkit) is the source for its actual implementation and supported integrations. Use this lab to understand the design questions, then validate a selected upstream version against the intended workload.

## Benefits to measure

| Value hypothesis | Pilot measure | What would weaken the case |
|---|---|---|
| Less repetitive review work | Median human minutes per accepted report, including corrections | Review and approval time exceeds the baseline |
| More consistent control decisions | Positive, negative, and bypass test outcomes for the selected tools | Work can reach the target through an unguarded route |
| Faster evidence preparation | Time for an independent reviewer to reconstruct a sampled action | Logs lack policy identity, result, scope, or retention |
| Better spending discipline | Total cost per accepted task, retry rate, and reconciled budget variance | Tool limits hide growing model, infrastructure, or support costs |
| Safer expansion of agent access | Number and severity of uncovered action paths and unresolved exceptions | Permissions grow faster than coverage and operating capacity |

These are hypotheses. A blocked synthetic action is an observed local decision, not a prevented production incident. An estimated Azure saving is a recommendation until an approved change produces a verified financial outcome.

## Accountability and investment

Name a business owner for the outcome and residual risk, a platform owner for the tool boundary and availability, a security owner for identity and abuse controls, and a FinOps owner for allocation and reconciliation. The governance product owner coordinates policy changes, support, training, and adoption; assurance independently challenges the evidence. The [operating model](docs/operating-model.md) defines decision rights.

Fund the complete service: engineering, model consumption, gateway and compute, logs and retention, human approval, support, incident response, and maintenance. Model fees can continue even when a tool is denied. The [FinOps guide](docs/finops.md) separates these costs and provides a worked, fictional example.

## A 30 / 60 / 90-day pilot plan

| Period | Director's deliverable | Gate for the next stage |
|---|---|---|
| Days 0–30 | Select one workflow; baseline time, cost, quality, and failure modes; complete the local lab; name owners and budgets | Scope, data handling, expected benefit, and acceptance criteria are explicit |
| Days 31–60 | Validate the selected upstream version in a controlled environment; test allowed and denied actions, approval expiry, bypasses, unavailable dependencies, and budget exhaustion | Representative evidence supports the tool boundary, support process, and rollback |
| Days 61–90 | Operate a limited pilot; sample decisions; reconcile usage; measure accepted outcomes, friction, incidents, and exceptions | Decide scale, revise, hold, or stop using the agreed baseline |

Pilot targets are proposals until owners agree them. A lab completion is not authorization for cloud access or production enforcement.

## The scale decision pack

Request one [Governance Decision Contract](framework/templates/agent-governance-decision.example.json), an [architecture review](docs/architecture.md), a cost-and-value ledger, representative test evidence, and an operating owner. Apply the original [PROVE method](framework/prove-method.md): Profile the outcome, Resolve authority, Operationalize the control, Verify evidence, and Evolve from results.

Scale only when the accepted outcome improves, coverage and limitations are understood, financial evidence reconciles, and the team can support and reverse the service. Hold or stop when false denials, approval queues, missing evidence, bypasses, or total cost undermine the case. This lab makes those choices reviewable; it does not make them on behalf of the organization.
