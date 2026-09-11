# Run the actual released AGT wrapper

This optional example uses Microsoft's `agent-governance-toolkit-core==4.1.0` package. It complements the [main learning lab](../../README.md) by exercising the real `agentmesh.governance.govern()` wrapper against an in-memory synthetic catalog. The package installation needs internet access; the example itself uses no model, provider credential or Azure resource.

## Install and run

Use Python 3.11 or newer. Run these commands from the repository root. The separate environment keeps the released toolkit's dependencies separate from the simulator.

Windows PowerShell:

```powershell
py -3 -m venv .venv-agt
.\.venv-agt\Scripts\python.exe -m pip install -r examples/upstream-agt/requirements.txt
.\.venv-agt\Scripts\python.exe examples/upstream-agt/run.py
```

macOS or Linux:

```bash
python3 -m venv .venv-agt
.venv-agt/bin/python -m pip install -r examples/upstream-agt/requirements.txt
.venv-agt/bin/python examples/upstream-agt/run.py
```

The script resolves [policy.yaml](policy.yaml) relative to itself. It checks the installed toolkit version and exits unsuccessfully if any expected outcome fails.

## Expected result

```text
ALLOW read_catalog: handler executed once; synthetic items=1
DENY delete_catalog: handler not executed; rule=deny-destructive-actions
DENY shell_exec: handler not executed; rule=deny-destructive-actions
DENY unknown_action: handler not executed; rule=default-deny
PASS: actual AGT 4.1.0; 1 allow, 3 denials, 1 handler execution
```

The assertions check both the decision and the side effect: only the permitted request reaches the handler. `shell_exec` is a test action name; this example contains no shell execution implementation. The catalog returns one fixed synthetic record.

AGT 4.1.0 may also emit an `agentmesh-platform is deprecated` warning when importing `agentmesh`. That warning was observed even with the correct consolidated `agent-governance-toolkit-core` package installed. The example preserves the warning and verifies the distribution version explicitly.

## Follow the control

Read [run.py](run.py) alongside [policy.yaml](policy.yaml):

1. The host creates a callable and supplies an agent identifier.
2. `govern()` loads the YAML using AGT's AgentMesh policy engine.
3. The read rule permits one request; a named rule denies destructive and shell requests.
4. `default_action: deny` blocks an unrecognized action.
5. `GovernanceDenied` prevents the handler from running for each blocked request.

The identifier is a local label supplied by trusted host code; this example does not authenticate a remote identity. The wrapper governs calls made through `guarded`. A caller that can invoke the underlying function directly or change the policy can bypass this boundary. A real service must control credentials, direct access and policy ownership.

## Version and scope

This example uses the released AgentMesh wrapper schema, `apiVersion: governance.toolkit/v1`. It does not use the simulator's policy schema or the newer native ACS manifest format. The [AGT reference](../../docs/agt-reference.md) explains those differences and the current development transition.

The package version is pinned; its transitive dependencies remain resolved according to the upstream package's constraints. A deployment should produce its own reviewed dependency lock and vulnerability assessment.

Observed validation on 2026-09-11: Windows, CPython 3.11.9, `agent-governance-toolkit-core` 4.1.0, PyYAML 6.0.3 and Pydantic 2.13.5. A fresh isolated installation completed, `run.py` produced the expected five lines and exited with code 0, and `python -m pip check` reported no broken requirements. Linux and macOS commands are provided but were not executed in this validation.

The verified scope is this synchronous wrapper, YAML policy and four synthetic requests. It does not validate native ACS, cryptographic identity, approvals, sandbox isolation, provider billing, Azure deployment or Codex/Gemini integration. Use the main lab's separate MCP instructions for the CLI exercise.

This is original example code using the public API documented in the [v4.1.0 wrapper source](https://github.com/microsoft/agent-governance-toolkit/blob/0de71ca6c95cf8b9b975ac96f48eaa7826bbe258/agent-governance-python/agent-mesh/src/agentmesh/governance/govern.py) and [policy parser](https://github.com/microsoft/agent-governance-toolkit/blob/0de71ca6c95cf8b9b975ac96f48eaa7826bbe258/agent-governance-python/agent-mesh/src/agentmesh/governance/policy.py). Both this original example and Microsoft's separate upstream package use MIT licenses with their respective copyright notices. See the [project license](../../LICENSE.md) and [third-party notices](../../THIRD-PARTY-NOTICES.md).
