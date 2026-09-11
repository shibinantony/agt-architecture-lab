"""Expose the offline governance lab through the MCP Python SDK's stdio transport.

Install requirements-mcp.txt first. This adapter governs its five published
tools only; it cannot intercept the client's other MCP, shell, or network tools.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Codex and Gemini may launch an absolute script path from another directory.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

try:
    import anyio
    import mcp.types as types
    from mcp.server.lowlevel import Server
    from mcp.server.stdio import stdio_server
except ImportError:
    raise SystemExit("MCP dependencies are missing. Install requirements-mcp.txt with the Python interpreter used to launch this server.") from None

from lab.runtime import AuditError, GovernanceRuntime, PolicyError, TOOL_DEFINITIONS


def _response(payload: dict, is_error: bool) -> types.CallToolResult:
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=json.dumps(payload, sort_keys=True, allow_nan=False))],
        structuredContent=payload,
        isError=is_error,
    )


def create_server(runtime: GovernanceRuntime) -> Server:
    server = Server(
        "agt-architecture-lab",
        version="0.1.0",
        instructions=(
            "Original offline AGT-inspired teaching lab. Resources, actor and costs are synthetic. "
            "Use only the listed tools for this exercise. Policy denials are final. "
            "A deployment request records pending approval and cannot execute. "
            "One server process shares one cumulative budget; restarting starts a new session."
        ),
    )
    unavailable = False

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [types.Tool(**definition) for definition in TOOL_DEFINITIONS]

    # Runtime validation is authoritative. Letting a schema adapter drop unknown
    # fields or reject before this callback would omit their governance evidence.
    @server.call_tool(validate_input=False)
    async def call_tool(name: str, arguments: dict | None) -> types.CallToolResult:
        nonlocal unavailable
        if unavailable:
            return _response({
                "error": "session_closed",
                "reason": "The session closed after an evidence or internal error; no further action was dispatched.",
                "session_id": runtime.session_id,
                "synthetic": True,
            }, True)
        try:
            result = runtime.call(name, arguments)
            runtime.write_summary()
            is_error = result["decision"] != "allow" or result["execution"]["status"] != "succeeded"
            return _response(result, is_error)
        except AuditError:
            unavailable = True
            # A completion append can fail AFTER the local handler. Never tell
            # the client that a failed audit proves there was no execution.
            return _response({
                "error": "audit_unavailable",
                "reason": "Evidence storage failed. A local action may have completed; this session is closed to further calls.",
                "execution": {"status": "unconfirmed"},
                "session_id": runtime.session_id,
                "synthetic": True,
            }, True)
        except Exception:
            unavailable = True
            # Raw exception text may contain caller input. Do not forward it.
            return _response({
                "error": "internal_error",
                "reason": "The local adapter failed and closed this session. Inspect its local evidence before retrying.",
                "execution": {"status": "unconfirmed"},
                "session_id": runtime.session_id,
                "synthetic": True,
            }, True)

    return server


async def serve(runtime: GovernanceRuntime):
    server = create_server(runtime)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Original offline governance lab over MCP stdio; no Azure credentials needed.")
    parser.add_argument("--policy", default=str(REPO_ROOT / "lab" / "policy.yaml"), help="Original lab YAML policy path (default is relative to this repository)")
    parser.add_argument("--output", default=str(REPO_ROOT / "artifacts" / "mcp"), help="Parent for a unique session evidence directory")
    args = parser.parse_args(argv)
    # SDK warnings can interpolate untrusted unknown tool names. Keep stderr
    # limited to our static operational messages and stdout strictly protocol.
    logging.getLogger("mcp").setLevel(logging.CRITICAL)
    try:
        runtime = GovernanceRuntime(Path(args.policy).resolve(), Path(args.output).resolve())
        runtime.write_summary()
        anyio.run(serve, runtime)
        return 0
    except PolicyError:
        print("Lab MCP server refused startup: policy is invalid or unreadable. No tool executed.", file=sys.stderr)
        return 1
    except AuditError:
        print("Lab MCP server stopped: evidence storage is unavailable. Inspect local evidence before retrying.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 0
    except Exception:
        print("Lab MCP server stopped after a local adapter or transport error. Inspect local evidence before retrying.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
