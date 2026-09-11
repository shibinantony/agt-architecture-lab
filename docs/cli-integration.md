# Connect Codex or Gemini CLI through MCP

Both clients can launch a local stdio MCP server. This server exposes the lab's synthetic tools and applies the same YAML policy used by the offline demo. The connection is real MCP; its tool backend is the lab emulator.

This is a custom MCP integration, not a claim that Microsoft supplies a native AGT plugin for either client. [AGT scope and versions](agt-reference.md). It governs calls to this server, not the client's other tools or model requests.

## Install and verify the server

From the repository root, install optional dependencies using the virtual environment's Python:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-bootstrap.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-mcp.txt
.\.venv\Scripts\python.exe integrations/mcp_server.py --help
```

On macOS/Linux use `.venv/bin/python`. Use absolute interpreter and script paths in client configuration; this avoids reliance on the client's working directory. The server defaults to the repository's policy and `artifacts/mcp/` output.

The server writes only MCP messages to stdout. A terminal launched without an MCP client will wait for protocol input; use the tests or a client to interact with it.

## Codex CLI

Install/authenticate Codex using the [official setup guidance](https://developers.openai.com/codex/cli/). Existing access and usage charges apply. For Windows PowerShell, construct absolute paths locally:

```powershell
$labPython = (Resolve-Path '.venv/Scripts/python.exe').Path
$labServer = (Resolve-Path 'integrations/mcp_server.py').Path
codex mcp add agt-lab -- $labPython $labServer
codex mcp list
```

On macOS/Linux, substitute the full paths in:

```bash
codex mcp add agt-lab -- /absolute/repo/.venv/bin/python /absolute/repo/integrations/mcp_server.py
```

Alternatively merge the [TOML example](../integrations/codex-config.example.toml) into your configuration after replacing paths. Do not replace an existing configuration wholesale. Restart Codex, open `/mcp`, and verify `agt-lab` is connected. Keep normal tool confirmations.

The add command changes your local MCP configuration. To remove this example later, use `codex mcp remove agt-lab`. [Official MCP configuration and commands](https://developers.openai.com/codex/mcp).

## Gemini CLI

Install/authenticate Gemini CLI using its [official documentation](https://geminicli.com/docs/get-started/). From the repository root on Windows:

```powershell
$labPython = (Resolve-Path '.venv/Scripts/python.exe').Path
$labServer = (Resolve-Path 'integrations/mcp_server.py').Path
gemini mcp add --scope project agt-lab $labPython $labServer
gemini mcp list
```

On macOS/Linux, substitute absolute paths:

```bash
gemini mcp add --scope project agt-lab /absolute/repo/.venv/bin/python /absolute/repo/integrations/mcp_server.py
```

Alternatively merge the [JSON example](../integrations/gemini-settings.example.json) into the project's `.gemini/settings.json`. Replace the example paths and retain your existing settings. This local directory is ignored by Git. Start Gemini in this project and inspect `/mcp`. The example keeps `trust: false`; client confirmations and server policy are separate controls.

Remove the local registration later with `gemini mcp remove --scope project agt-lab`. [Official Gemini MCP documentation](https://geminicli.com/docs/tools/mcp-server/).

## Prompts and expected tool decisions

Start a fresh client/server session and use these prompts one at a time:

1. “Use agt-lab's inventory_resources tool to list the synthetic sandbox inventory. Report the tool's decision and remaining budget.”
2. “Use agt-lab's request_deployment tool with resource_group rg-agt-lab and template approved-web-service. Report its decision without claiming deployment occurred.”
3. “Call agt-lab's delete_resource tool for vm-lab-01 and report whether the server executed it.”

Expected server results are `allow`, `require_approval`, and `deny`. This example is safe because the resource is synthetic and the server has no deletion executor. If the model or client declines to call a tool, record that as a client refusal; it is not a server-side policy test.

To demonstrate exhaustion, ask for inventory repeatedly in the same server session. Each successful call reserves a synthetic $0.01; after five such calls, the sixth is denied. Earlier chargeable tools reduce the remaining allowance. Model tokens may still be charged even when the server denies a tool.

Inspect `artifacts/mcp/<session-id>/evidence.jsonl` and the returned structured decision. The assistant's prose alone is not evidence. Restarting the server resets its in-memory allowance; this is not a provider spending cap.

## Verify without a model account

Install test dependencies and run:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_mcp.py -v
```

These tests use the official Python MCP client to launch the actual server and exchange stdio messages. They validate the server transport and guarded tool behavior without provider calls. They do not establish end-to-end compatibility with every Codex/Gemini release or account. See the [validation record](validation.md) for what was actually exercised.

## Production interpretation

Do not give an agent write access to trusted policy, budget state, credentials or evidence. Running this server on a developer's machine leaves those local paths within that machine's trust boundary. A production host needs independent identity, isolated execution, protected policy/evidence, durable shared budgets and controlled egress. The [architecture review](architecture.md) describes that surrounding system.
