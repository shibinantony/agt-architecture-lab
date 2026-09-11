# Governance exception record template

## Request

| Field | Entry |
|---|---|
| Exception ID | [Stable ID] |
| Control ID and version | [Reference] |
| Requested scope | [Smallest exact scope; use synthetic identifiers publicly] |
| Requester role | [Role] |
| Business owner | [Role] |
| Risk owner | [Role] |
| Requested start | [YYYY-MM-DD] |
| Requested expiry | [YYYY-MM-DD] |
| Business need | [Why the standard cannot currently be met] |

## Assessment

- Applicability confirmed by: [Role and evidence]
- Risk created by the exception: [Impact and likelihood]
- Alternatives considered: [Comply, narrow, redesign, delay, or stop]
- Compensating control: [Owner, operation, test, and evidence]
- Financial and delivery impact: [Cost, avoidance, friction]
- Dependencies and downstream effects: [Systems and teams]

## Decision

| Field | Entry |
|---|---|
| Decision | [Approve / reject / revise] |
| Decision authority | [Role] |
| Decision date | [YYYY-MM-DD] |
| Approved scope | [Exact bounded scope] |
| Effective date | [YYYY-MM-DD] |
| Expiry date | [YYYY-MM-DD] |
| Conditions | [Required evidence, milestones, or limits] |
| Azure exemption reference | [Reference; no real ID in public examples] |
| Agent / tool / action digest | [Exact runtime request and policy version, when relevant] |
| Approval expiry and replay control | [One-time authorization scope and trusted verifier] |

An Azure Policy exemption and an agent-action approval are separate decisions. This template documents authority; it is not an executable approval token.

## Monitoring and closure

| Review item | Owner | Frequency or date | Evidence |
|---|---|---|---|
| Compensating control operates | | | |
| Scope remains correct | | | |
| Risk has not increased | | | |
| Remediation plan progresses | | | |
| Renewal or closure decision | | | |

Renewal is a new decision with current evidence, not an automatic date extension.
