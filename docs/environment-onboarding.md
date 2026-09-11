# Environment onboarding

Choose the environment that matches the question you need to answer.

| Mode | Prerequisites | Cost / authority | Output |
|---|---|---|---|
| Offline lab | Python 3.11+, install core dependency | No cloud/model account | Synthetic decisions, reports and evidence |
| MCP protocol test | Optional MCP/test dependencies | Local subprocess only | Verified discovery and guarded calls |
| Codex or Gemini CLI | Installed, authenticated client plus MCP setup | Existing client/provider usage terms and charges | Client calls with server evidence |
| Actual upstream example | Separate pinned environment | Follow that example's dependencies | Evidence for that particular AGT API |
| Azure sandbox pilot | Named owner, reviewed design, approved scope and identity | Organization-specific access and cost | Observed external behavior and gaps |

## Local setup

Follow [the lab guide](lab-guide.md). Keep generated output in ignored `artifacts/`. If you use an environment activation step, choose the command for your shell; the documented full Python paths also work without activation.

No Azure login, provider API key, Docker, Node.js or CLI is required for the offline demo. Dependencies are downloaded during installation; afterward the demo operates locally.

## Add a coding client

Follow [CLI integration](cli-integration.md). Select one client first. Use absolute interpreter and server paths so launching from another working directory does not change the policy or fixture. Keep the normal client tool confirmations enabled.

Verify both an allowed and denied request using the server's evidence. Client statements alone are not proof that a call occurred. Distinguish a tool that was never requested, a client-side refusal, an MCP error and a policy denial.

## Prepare an enterprise pilot

Choose a single bounded workflow, such as reading sandbox inventory and producing a report. Record the business owner, data classification, allowed operations, identity source, expected usage, success measure and stopping conditions in a [decision contract](../framework/templates/agent-governance-decision.example.json).

Before replacing fixture handlers, review:

- Exact reachable tools and alternate paths, including direct shell/API access.
- Upstream AGT package, source, policy schema and adapter compatibility.
- Separate identities for discovery and any future deployment.
- Real scope/coverage, cost metering and rate limits.
- Evidence storage, retention, access and outage behavior.
- Approval verification, rollback and the team on call.

For an Azure read-only assessment, start with the narrowest suitable role and scope. [Azure Resource Graph examples](../toolkit/queries/README.md) are supplemental exercises. Visibility is authorization-dependent: incomplete access or failed collection is unknown, not proof of compliant or empty scope.

## Greenfield and existing environments

For greenfield work, align hosting, networking, identities and resource policy with the [Azure landing-zone model](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/). Decide the trusted tool boundary before distributing credentials to agents.

For an existing estate, map inherited policy, RBAC, current agents, MCP servers, deployment ownership and network routes first. Introduce runtime checks around a narrow workflow, measure false denials and task quality, and expand through reviewed canaries. Changing the agent layer does not automatically make existing platform controls adequate.

## Completion evidence

A local learner should be able to explain the demo's outcomes. A client integrator should retain server-side evidence for allow and deny. A pilot owner needs actual identity, isolation, failure, cost and operational evidence. These are separate maturity gates; see [validation](validation.md) and [maturity](maturity-model.md).
