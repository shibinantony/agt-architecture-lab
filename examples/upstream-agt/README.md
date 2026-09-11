# Run the actual AGT wrapper from pinned source

This advanced, optional example builds Microsoft's AGT core from the immutable source commit `0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf` (package metadata version 5.0.0). It is a **development snapshot, not the PyPI 5.0.0 release**. It complements the [main learning lab](../../README.md) by exercising the real `agentmesh.governance.govern()` wrapper against an in-memory synthetic catalog. Installation needs internet access and native build tools; the example itself uses no model, provider credential or Azure resource.

## Install and run

Use a Linux development environment with Python 3.11+, Rust/Cargo and a C linker/build toolchain. Transitive ACS dependencies may compile native code. `rustc --version` and `cargo --version` must succeed before installation. Run from the repository root; the separate environment keeps the toolkit's dependencies out of the beginner simulator.

```bash
python3 -m venv .venv-agt
.venv-agt/bin/python -m pip install -r requirements-bootstrap.txt
.venv-agt/bin/python -m pip install -r examples/upstream-agt/requirements.txt
.venv-agt/bin/python -m pip check
.venv-agt/bin/python examples/upstream-agt/run.py
```

The script resolves [policy.yaml](policy.yaml) relative to itself. Before importing AGT, it checks the package version, installed source provenance and cryptography pin. It exits unsuccessfully if any expected outcome fails. The [Linux CI job](../../.github/workflows/repository-validation.yml) reproduces installation, checks the behavior and audits installed dependencies; use the run for the exact commit as evidence.

Windows/macOS source builds are not validated here. The Windows attempt failed during native ACS build metadata generation because Cargo was not available to the backend; it did not establish a working snapshot installation. Also, cryptography 49+ [removed 32-bit Windows and Intel macOS support](https://cryptography.io/en/latest/changelog/#v49-0-0). Do not downgrade dependencies to bypass these requirements. The [beginner emulator](../../docs/lab-guide.md) does not need this source build.

## Expected result

```text
ALLOW read_catalog: handler executed once; synthetic items=1
DENY delete_catalog: handler not executed; rule=deny-destructive-actions
DENY shell_exec: handler not executed; rule=deny-destructive-actions
DENY unknown_action: handler not executed; rule=default-deny
PASS: actual AGT development snapshot 0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf; package 5.0.0; 1 allow, 3 denials, 1 handler execution
```

The assertions check both the decision and the side effect: only the permitted request reaches the handler. `shell_exec` is a test action name; this example contains no shell execution implementation. The catalog returns one fixed synthetic record.

The `agentmesh` import may also emit a deprecation warning; warnings are not suppressed. The package and source checks distinguish this installation from a separately installed legacy package.

## Follow the control

Read [run.py](run.py) alongside [policy.yaml](policy.yaml):

1. The host creates a callable and supplies an agent identifier.
2. `govern()` loads the YAML using AGT's AgentMesh policy engine.
3. The read rule permits one request; a named rule denies destructive and shell requests.
4. `default_action: deny` blocks an unrecognized action.
5. `GovernanceDenied` prevents the handler from running for each blocked request.

The identifier is a local label supplied by trusted host code; this example does not authenticate a remote identity. The wrapper governs calls made through `guarded`. A caller that can invoke the underlying function directly or change the policy can bypass this boundary. A real service must control credentials, direct access and policy ownership.

## Version and scope

This example uses the AgentMesh wrapper schema, `apiVersion: governance.toolkit/v1`. It does not use the simulator's policy schema or the newer native ACS manifest format. Installing a transitive ACS package does not mean this example exercises its runtime. The [AGT reference](../../docs/agt-reference.md) explains those differences.

The source commit and cryptography 50.0.1 are pinned; other transitive dependencies remain resolved according to upstream constraints. This is not a complete dependency lock. A deployment must produce its own reviewed lock and assessment.

Why not install a released wheel? The publication audit found that core 4.1.0 requires cryptography below 49, and the PyPI core 5.0.0 wheel requires it below 50. [CVE-2026-69247](https://github.com/pyca/cryptography/security/advisories/GHSA-g6cj-pr64-35w5) is fixed in cryptography 50.0.0. The [selected unmodified source metadata](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/agent-governance-python/agent-governance-toolkit-core/pyproject.toml) permits versions below 51, so the normal resolver can install 50.0.1 without bypassing compatibility checks. Prefer a reviewed compatible release when one becomes available. See the [validation record](../../docs/validation.md) for observed platform results and the dated dependency audit.

The assertion scope is this synchronous wrapper, YAML policy and four synthetic requests. It does not validate native ACS, cryptographic identity, approvals, sandbox isolation, provider billing, Azure deployment or Codex/Gemini integration. Use the main lab's separate MCP instructions for the CLI exercise.

This is original example code using the public API in the [pinned wrapper source](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/agent-governance-python/agent-mesh/src/agentmesh/governance/govern.py) and [policy parser](https://github.com/microsoft/agent-governance-toolkit/blob/0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf/agent-governance-python/agent-mesh/src/agentmesh/governance/policy.py). Both this original example and Microsoft's separate upstream package use MIT licenses with their respective copyright notices. See the [project license](../../LICENSE.md) and [third-party notices](../../THIRD-PARTY-NOTICES.md).
