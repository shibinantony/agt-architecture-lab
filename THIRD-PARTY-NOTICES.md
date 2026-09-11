# Third-party notices

Original code, documentation, schemas, templates and examples in this repository are licensed under the [MIT License](LICENSE.md), copyright 2026 Shibin Antony. This includes the independently written policy emulator and the small example that calls Microsoft's public AGT API.

Third-party packages are installed from their package distributions; their source and binaries are not vendored in this repository. Each package retains its own copyright notices and license. The direct dependencies below were checked against installed distribution metadata on 2026-09-11.

| Package | Version | Used for | Declared license | Upstream reference |
|---|---|---|---|---|
| PyYAML | 6.0.3 | Reading lab YAML | MIT | [Versioned package](https://pypi.org/project/PyYAML/6.0.3/), [source](https://github.com/yaml/pyyaml) |
| MCP Python SDK | 1.30.0 | Optional MCP server and client tests | MIT | [Versioned source](https://github.com/modelcontextprotocol/python-sdk/tree/v1.30.0) |
| jsonschema | 4.26.0 | Development-time decision schema validation | MIT | [Versioned package](https://pypi.org/project/jsonschema/4.26.0/), [source](https://github.com/python-jsonschema/jsonschema) |
| Microsoft Agent Governance Toolkit core | 4.1.0 | Separate actual-AGT example | MIT | [Release source and license](https://github.com/microsoft/agent-governance-toolkit/tree/0de71ca6c95cf8b9b975ac96f48eaa7826bbe258), [example scope](examples/upstream-agt/README.md) |

This table describes direct dependencies, not every transitive package in a resolved environment. If distributing an environment, container, binary or vendored dependency tree, include the licenses and notices required by that complete distribution. The repository currently distributes original source and dependency requirements, not a bundled runtime.

Microsoft's AGT is a separate project. The lab does not copy its implementation into the emulator, and the original lab YAML is not an AGT/ACS manifest. The upstream example invokes the installed AGT package. See the [AGT reference](docs/agt-reference.md) for source and version attribution.

Linked vendor documentation, specifications, product names and trademarks remain subject to their owners' terms. The lab's MIT License does not relicense those materials or imply endorsement. No vendor logos or copied third-party diagrams are distributed. See [NOTICE.md](NOTICE.md).

The GitHub Actions workflow references GitHub-maintained checkout, Python setup and artifact-upload actions by commit. Those actions execute separately under their upstream terms; their implementations are not copied into this source tree.
