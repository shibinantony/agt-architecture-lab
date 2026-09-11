# Roadmap

The current milestone is an executable learning companion to Microsoft Agent Governance Toolkit. Progress is measured by observed behavior in a stated scope.

## Delivered: local architecture review and lab

- Correct AGT naming, explicit Microsoft repository links and version-aware reference.
- Beginner, intermediate and advanced engineering exercises; architect, director and CXO routes.
- Original strict YAML policy emulator with synthetic tools, default denial, approval stops, scope/classification checks and a cumulative local allowance.
- Structured evidence, summaries and negative/concurrency/failure tests.
- Stdio MCP server and real protocol tests for client integration.
- Separate pinned actual Microsoft AGT 4.1.0 example with verified allow/deny behavior.
- Enterprise architecture, FinOps worked example, ownership, control catalog and agent decision contract.
- CI jobs for the emulator, MCP, documents, schema and upstream example.

See [validation](docs/validation.md) for local and CI evidence. Documentation of a design is not a completed deployment.

## Next: real client acceptance

Run the documented workflow through an authenticated Codex and Gemini CLI session. Preserve client version, requested tool, server evidence and account/model cost boundary. No universal client interception claim follows from this test.

**Exit gate:** a reviewer can distinguish client refusal, server denial, actual execution and provider usage.

## Next: upstream ACS evaluation

Choose a matching source/package/schema/adapter combination from the [upstream reference](docs/agt-reference.md). Exercise verdicts, transformed arguments, all bound intervention points, errors and upgrade compatibility in an isolated environment.

**Exit gate:** observed behavior for the selected API and workload; no mixing of released wrapper YAML with current ACS examples.

## Next: operated sandbox pilot

Add authenticated identity, protected policy/evidence, shared durable metering, independently verified approvals where needed, and isolated tool execution. Start with an approved read-only workflow. Exercise bypass, timeout, retry, logging outage, containment and recovery.

**Exit gate:** owned operations, accepted results, known coverage, measured cost/friction and reviewed residual risk.

## Later: scale and reuse

Integrate broader Azure controls, financial exports and enterprise evidence systems only after the pilot establishes need. Select intentional code/documentation licenses before changing reuse or contribution rights; current [license terms](LICENSE.md) remain in force.

Maturity labels are scoped: source-reviewed, fixture-tested, protocol-tested, upstream-example-tested, sandbox-observed and pilot-observed. None alone means production-ready.
