---
status: source-register
last_verified: 2026-09-11
owner: Shibin Antony
---

# Source register

## Use

This register records the primary public sources behind current platform statements. A link is not an endorsement of the Lab, and a source does not validate the Lab's original methods. Recheck sources before implementation because Azure services, policy definitions, limits, prices, licensing, previews, and retirement dates change.

## AGT and executable lab references

The project now studies agent runtime governance. AGT stands for **Agent Governance Toolkit**. The lab's own policy schema and implementation are explained separately from upstream APIs. Version-specific source findings are in the [AGT reference](agt-reference.md); execution evidence is in [validation](validation.md).

| Subject | Primary source | What it establishes | Checked |
|---|---|---|---|
| Microsoft AGT | [Official repository](https://github.com/microsoft/agent-governance-toolkit) | Project identity and entry point to source, examples and releases | 2026-09-11 |
| Released AGT API | [v4.1.0 source](https://github.com/microsoft/agent-governance-toolkit/tree/0de71ca6c95cf8b9b975ac96f48eaa7826bbe258) | Release-specific package and wrapper interface | 2026-09-11 |
| ACS transition | [Pinned breaking changes](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/BREAKING_CHANGES.md) | Current development APIs and schemas differ from older releases | 2026-09-11 |
| MCP transport | [Protocol architecture](https://modelcontextprotocol.io/docs/learn/architecture) | Client/server tool discovery and invocation | 2026-09-11 |
| Python MCP | [SDK v1.30.0](https://github.com/modelcontextprotocol/python-sdk/tree/v1.30.0) | API version pinned by the optional lab server | 2026-09-11 |
| Codex CLI | [Official MCP documentation](https://developers.openai.com/codex/mcp) | Stdio registration and TOML configuration; checked alongside installed CLI help | 2026-09-11 |
| Gemini CLI | [Official MCP documentation](https://geminicli.com/docs/tools/mcp-server/) | Project MCP configuration, commands and trust setting; installed help checked | 2026-09-11 |
| AI gateway | [API Management capabilities](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities) | Mediation and controls for routed AI traffic; availability varies by capability/tier | 2026-09-11 |

Revalidate when the pinned SDK, CLI, adapter, policy format or deployment topology changes. Checking a link does not mean the complete upstream stack was executed. The original Azure sources below retain their original review dates unless separately refreshed.

## Azure platform background

| Area | Primary source | Claim supported | Checked | Revalidation trigger |
|---|---|---|---|---|
| Cloud governance | [Build a cloud governance team](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/govern/build-cloud-governance-team) | Governance is continuous, cross-functional work with explicit authority, risk, policy, and monitoring responsibilities | 2026-09-09 | CAF Govern restructure or material guidance change |
| Governance catalog | [Azure governance documentation](https://learn.microsoft.com/en-us/azure/governance/) | Azure governance is a portfolio including Management Groups, Policy, Resource Graph, and Cost Management rather than a first-party product named “Azure Governance Toolkit” | 2026-09-09 | Catalog rename or new product announcement |
| Landing zones | [What is an Azure landing zone?](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/) | Current model includes a platform landing zone and application landing zones; accelerators or custom implementation are options | 2026-09-09 | Reference-architecture change |
| Management groups | [Management-group design](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups) | Use management groups for common governance requirements, keep hierarchy reasonably flat, and limit broad inherited assignments | 2026-09-09 | Limit or design guidance change |
| Subscriptions | [Subscription organization](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-subscriptions) | Subscriptions are important management, scale, and workload boundaries | 2026-09-09 | Landing-zone design change |
| Subscription vending | [Subscription vending guidance](https://learn.microsoft.com/en-us/azure/architecture/landing-zones/subscription-vending) | Repeatable subscription distribution is part of platform operation at scale | 2026-09-09 | Architecture guidance change |
| Azure Policy | [Azure Policy overview](https://learn.microsoft.com/en-us/azure/governance/policy/overview) | Policy evaluates resource state using definitions, initiatives, assignments, effects, and compliance results | 2026-09-09 | Policy model or terminology change |
| Policy as code | [Design Azure Policy as Code workflows](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/policy-as-code) | Policy resources should use source control, testing, deployment workflow, and compliance gates | 2026-09-09 | Workflow guidance change |
| Safe policy rollout | [Safe deployment of Azure Policy assignments](https://learn.microsoft.com/en-us/azure/governance/policy/how-to/policy-safe-deployment-practices) | Policy assignments should use progressive exposure, audit/overrides, automated checks, and health validation | 2026-09-09 | Safe-deployment model change |
| Policy exemptions | [Azure Policy exemption structure](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/exemption-structure) | Exemptions support scoped metadata, category, and expiration | 2026-09-09 | Schema or feature change |
| RBAC | [Azure RBAC overview](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview) | A role assignment combines principal, role definition, and scope | 2026-09-09 | Authorization model change |
| RBAC practices | [Azure RBAC best practices](https://learn.microsoft.com/en-us/azure/role-based-access-control/best-practices) | Use least privilege, limited owners, groups, and careful custom roles | 2026-09-09 | Best-practice update |
| Privileged access | [Microsoft Entra PIM](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-configure) | PIM provides time- and approval-based privileged role activation, reviews, notification, and audit history; licensing applies | 2026-09-09 | Licensing or feature change |
| Inventory | [Azure Resource Graph overview](https://learn.microsoft.com/en-us/azure/governance/resource-graph/overview) | Resource Graph queries authorized Azure resources at scale, is permission-trimmed, and has indexing latency and throttling considerations | 2026-09-09 | Query, consistency, retention, or quota change |
| Resource changes | [Resource Graph change analysis](https://learn.microsoft.com/en-us/azure/governance/resource-graph/changes/resource-graph-changes) | Resource change data supports recent change investigation with a bounded queryable history | 2026-09-09 | Retention or availability change |
| Cost operations | [Plan to manage Azure costs](https://learn.microsoft.com/en-us/azure/cost-management-billing/understand/plan-manage-costs) | Cost analysis, budgets/alerts, tags, and regular review support cost management | 2026-09-09 | Cost Management behavior or scope change |
| Cost data | [Understand Cost Management data](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data) | Tags and cost data have coverage, freshness, and historical limitations | 2026-09-09 | Export, latency, tag, or agreement change |
| Budgets | [Create and manage Azure budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets) | Budgets provide notifications and do not themselves stop resources or consumption | 2026-09-09 | Budget action behavior change |
| FinOps | [FinOps Framework](https://learn.microsoft.com/en-us/cloud-computing/finops/framework/finops-framework) | Microsoft guidance organizes FinOps capabilities around shared accountability and an Inform, Optimize, Operate lifecycle | 2026-09-09 | Framework version change |
| FinOps governance | [FinOps policy and governance](https://learn.microsoft.com/en-us/cloud-computing/finops/framework/manage/governance) | Start with goals and audit, then expand policy coverage safely and measure value | 2026-09-09 | Capability guidance change |
| FinOps tooling | [Microsoft FinOps toolkit](https://github.com/microsoft/finops-toolkit) | A Microsoft open-source toolkit already provides cost-management and optimization solutions that this Lab should integrate with rather than recreate | 2026-09-09 | License, architecture, or project status change |
| Security posture | [Defender for Cloud overview](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction) | Defender for Cloud supplies posture and workload-protection capabilities with plan-dependent features | 2026-09-09 | Plan, pricing, or capability change |
| Security benchmark | [Microsoft Cloud Security Benchmark](https://learn.microsoft.com/en-us/security/benchmark/azure/introduction) | MCSB provides prescriptive security recommendations for cloud environments | 2026-09-09 | Benchmark version change |
| Monitoring | [Azure Monitor overview](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview) | Azure Monitor provides observability capabilities and multiple data stores and experiences | 2026-09-09 | Architecture or pricing change |
| Diagnostic settings | [Diagnostic settings](https://learn.microsoft.com/en-us/azure/azure-monitor/platform/diagnostic-settings) | Resource logs require explicit routing through diagnostic settings for selected destinations | 2026-09-09 | Collection model or supported destination change |
| Bicep | [What is Bicep?](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview) | Bicep is a declarative Azure IaC language with modules and change preview through what-if | 2026-09-09 | Language or support change |
| Deployment stacks | [Create and deploy deployment stacks](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-stacks) | Deployment stacks support resource lifecycle management and deny settings; unmanage actions require care | 2026-09-09 | Behavior or known limitations change |
| Blueprints retirement | [Azure Blueprints overview](https://learn.microsoft.com/en-us/azure/governance/blueprints/overview) | Blueprints entered phased retirement on 2026-07-31 and is scheduled to retire on 2027-01-31; migration points to deployment stacks and template specs | 2026-09-09 | Retirement date or migration guidance change |
| EPAC | [Enterprise Azure Policy as Code](https://github.com/Azure/enterprise-azure-policy-as-code) | An existing Azure open-source solution manages enterprise Policy as Code; integration should be evaluated before rebuilding similar orchestration | 2026-09-09 | Project status, license, or desired-state behavior change |
| AGT origin | [Microsoft Agent Governance Toolkit announcement](https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/) | Microsoft introduced Agent Governance Toolkit for agent runtime governance; it is the subject of this companion lab | 2026-09-11 | Project rename or status change |
| AGT mark | [Agent Governance Toolkit charter](https://github.com/microsoft/agent-governance-toolkit/blob/main/CHARTER.md) | The official charter states that “Agent Governance Toolkit” and “AGT” are trademarks | 2026-09-09 | Charter change |
| Microsoft names | [Microsoft trademark and brand guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks) | Microsoft provides restrictions and attribution requirements for use of its brand assets | 2026-09-09 | Legal-guidance change |

## Original propositions—not vendor facts

The following are original project proposals and are not claims made by Microsoft:

- the PROVE governance loop;
- the Governance Decision Contract;
- the control IDs and evidence chain in this repository;
- the maturity and executive scorecards;
- the proposed rollout, scale, stop, and economics models; and
- the proposed repository architecture and roadmap.
