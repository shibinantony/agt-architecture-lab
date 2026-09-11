---
status: learning-prototype
tested_scope: role-based-curriculum-design
last_verified: 2026-09-11
---

# Learning paths: from a first policy decision to an adoption decision

Start with the official [Microsoft Agent Governance Toolkit (AGT) repository](https://github.com/microsoft/agent-governance-toolkit) to identify the project. This independent lab provides a small original emulator and a separate [released-AGT example](../examples/upstream-agt/README.md). Begin with the emulator's Azure inventory task, then compare its policy decisions with the real wrapper. Agent actions, evidence, and operating choices are the subject.

The paths below produce different artifacts. Engineers run and challenge the controls; architects establish where they apply; directors establish who operates them; CXOs decide whether the outcome warrants investment. Time estimates are suggestions, not prerequisites or completion claims.

| Audience | Suggested time | Start here | Artifact |
|---|---|---|---|
| Beginner engineer | 30–60 minutes | First decision exercise below | Annotated local decision trail |
| Intermediate engineer | 60–90 minutes | Policy-change exercise | Compared runs and a policy review note |
| Advanced engineer | 2–3 hours | Boundary and failure exercise | Threat/failure test matrix and integration evidence |
| Architect | 60–90 minutes | Architecture review exercise | Integration diagram and decision record |
| Director / platform leader | 45–60 minutes, then pilot planning | [Operating model](operating-model.md) | Ownership, service measures, and adoption backlog |
| CXO / business sponsor | 20–30 minutes | [Executive brief](../EXECUTIVE-BRIEF.md) | Fund, learn further, or defer decision |

## Beginner engineer: explain one action

**Prerequisite:** complete the Python setup in the [lab guide](lab-guide.md). Run commands from the repository root. The examples use `python` in the activated environment; if activation is unavailable, substitute `.\.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on macOS/Linux. No model account or Azure subscription is needed for this exercise.

1. Read [lab/policy.yaml](../lab/policy.yaml). Locate the default decision, permitted environment and resource group, tool decisions, and session budget.
2. Predict what an inventory request, a deletion request, and a deployment request should do.
3. Run the offline scenario:

   ```shell
   python -m lab demo --output artifacts/beginner
   ```

4. Open `summary.md`, `summary.json`, and `evidence.jsonl` in the generated session directory under `artifacts/beginner`. Match each prediction to the actual decision and reason.
5. Find the budget-exhaustion case. Explain why a permissible tool can still be refused after earlier calls consume the allowance.

**Expected result:** permitted fixture work returns results; deletion is denied; deployment stops at `require_approval`; an additional cost-bearing request is denied when the allowance is exhausted. The evidence remains local and synthetic.

**Checkpoint:** in your own words, explain “the model requests; policy decides; the tool executes only permitted work.” Identify which file records the decision, and why approval-pending does not mean the deployment happened.

## Intermediate engineer: change one rule and explain the effect

**Prerequisite:** complete the beginner exercise and understand YAML indentation.

1. Copy `lab/policy.yaml` to `lab/policy.exercise.yaml` using your editor. Change only `controls.max_session_cost_usd` from `0.05` to `0.02`; retain the original for comparison.
2. Predict whether the original sequence of $0.01 inventory, $0.02 estimate, and $0.02 report calls can complete within one session.
3. Run the same scenario with the changed policy:

   ```shell
   python -m lab demo --policy lab/policy.exercise.yaml --output artifacts/intermediate
   ```

4. Compare evidence with the beginner run. Separate decisions caused by budget from decisions caused by tool policy, environment, resource scope, or classification.
5. Restore the copied budget to `0.05`, change `tools.inventory_resources.decision` to `deny`, and run again into a separate output directory. Review how one policy edit affects useful work and subsequent budget consumption.
6. Write a review note with objective, changed fields, expected behavior, observed results, user impact, and rollback to the original policy. Link it to the [Governance Decision Contract](../framework/templates/agent-governance-decision.example.json).

**Expected result:** the lower allowance prevents the original three successful calls; the explicit inventory denial prevents that tool's execution. Each run starts a fresh session, so these comparisons do not establish a persistent daily spending cap.

**Checkpoint:** another engineer can explain each changed decision from the policy and evidence. They can also identify why editing trusted policy is an administrative action and not something an agent should be free to do.

## Advanced engineer: challenge the boundary

**Prerequisite:** complete the previous exercises and read [technical implementation](technical-implementation.md). The optional CLI-client exercise also needs a separately configured client and may incur provider usage.

1. Review the demo's out-of-scope, classification, unknown-tool, and forged-input cases. Trace each request to its policy check and evidence result. Distinguish tested cases from broader untested attack classes.
2. Follow the [lab guide](lab-guide.md) to connect either Codex or Gemini CLI through the optional MCP server. Request inventory, then request deletion. Keep the server's returned decisions and session evidence as the proof, not just the assistant's narrative.
3. Draw the boundary around this MCP server. List shell execution, other MCP servers, direct cloud credentials, and model calls that can occur elsewhere. Do not test real deletion; document how production credentials and network rules would prevent an alternate route.
4. Build a failure matrix covering malformed policy, evidence-write failure, concurrent spending, process restart, duplicate requests, approval expiry, and a policy change between review and execution. Mark each as tested, unsupported by the lab, or requiring a production design.
5. Run the [released-AGT example](../examples/upstream-agt/README.md) in its separate environment. It pins `agent-governance-toolkit-core==4.1.0` and expects one allowed request, three denials, and exactly one handler execution. Compare its YAML schema, host enforcement, identity assumptions, and evidence with the emulator. The wrapper example was verified on Windows/Python 3.11.9; record your own platform and result. Review the newer ACS path in the [AGT reference](agt-reference.md) as a separate experiment; these YAML formats are not interchangeable.

**Expected result:** evidence for the exercised guarded tools plus an explicit gap list. The emulator does not become an enterprise identity service, durable approval system, model gateway, or distributed budget ledger when connected to a client.

**Checkpoint:** a reviewer can distinguish the emulator run, a live client-to-lab run, the verified released-AGT wrapper example, and a newer ACS experiment. The wrapper's four exercised requests do not establish provider integration or ACS compatibility; record any experiment you did not run as unperformed.

## Architect: place the control in the real system

1. Read the [architecture](architecture.md). Sketch user, agent/client, model provider or gateway, policy boundary, approval authority, tool service, Azure/data systems, identity, and evidence store.
2. Annotate every trust boundary with credentials, permitted data, enforcement owner, and an alternate path. Identify which proposed operations require Azure RBAC, Azure Policy, agent policy, content safeguards, or more than one layer.
3. Walk one permitted inventory request and one sensitive write from intent to evidence. Explain what happens if policy evaluation, approval, the tool, or logging fails.
4. Add model and tool budget ownership using the [FinOps guide](finops.md). Separate forecast alerts from pre-execution admission and from invoice reconciliation.
5. Record the smallest pilot scope, upstream version to validate, unacceptable gaps, rollback/containment owner, and evidence required before expansion.

**Expected output:** one annotated diagram and an architecture decision record. **Checkpoint:** every consequential action has a defined enforcement point, identity, failure behavior, and owner; bypass paths have a documented disposition.

## Director and CXO: turn the evidence into a decision

Directors complete the [adoption exercise](operating-model.md#directors-adoption-exercise): establish a baseline, assign decision rights and support, propose acceptance gates, and present the 30 / 60 / 90-day plan. The output is an operable pilot proposal, including the people and review capacity it requires.

CXOs read the [executive brief](../EXECUTIVE-BRIEF.md), choose a bounded pilot, further learning, or deferral, and record the reason. Require an accepted-result measure, full cost per result, risk owner, stop rule, and date for the next decision. A passing demo justifies learning confidence; a funded scale decision needs measured workload outcomes.

**Checkpoint for both:** distinguish observed local behavior, source-supported upstream capabilities, proposed enterprise design, and measured business benefit. No claim of ROI or production coverage follows solely from this repository.

## Keep each lesson evidence-based

Apply [PROVE](../framework/prove-method.md) across the paths: Profile the problem; Resolve the control and authority; Operationalize a bounded implementation; Verify results and economics; Evolve based on evidence.

Label artifacts as proposed, source-supported, fixture-tested, sandbox-observed, pilot-observed, or revalidated. Include scope, date, version, expected/actual result, limitations, owner, and next action. The [maturity model](maturity-model.md) helps assess the missing capabilities without turning lab completion into a production-readiness score.
