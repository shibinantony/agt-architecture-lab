"""Real SDK client/server stdio tests. No model subscription or cloud connection."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import asynccontextmanager
from datetime import timedelta
from pathlib import Path

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    raise unittest.SkipTest("Install requirements-mcp.txt to run real MCP transport tests")

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "integrations" / "mcp_server.py"


class MCPTransportTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.output = self.directory / "evidence"
        self.stderr = self.directory / "stderr.log"

    @asynccontextmanager
    async def client(self, *, module=False):
        arguments = ["-m", "integrations.mcp_server"] if module else [str(SCRIPT)]
        parameters = StdioServerParameters(
            command=sys.executable,
            args=[*arguments, "--output", str(self.output)],
            # Absolute script mode intentionally starts outside the repository.
            cwd=ROOT if module else self.directory,
        )
        with self.stderr.open("w", encoding="utf-8") as errors:
            async with stdio_client(parameters, errlog=errors) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream, read_timeout_seconds=timedelta(seconds=20)) as session:
                    initialized = await session.initialize()
                    self.assertEqual(initialized.serverInfo.name, "agt-architecture-lab")
                    self.assertIsNotNone(initialized.capabilities.tools)
                    yield session

    def payload(self, result):
        self.assertIsInstance(result.structuredContent, dict)
        self.assertEqual(len(result.content), 1)
        self.assertEqual(result.content[0].type, "text")
        self.assertEqual(json.loads(result.content[0].text), result.structuredContent)
        return result.structuredContent

    def evidence(self):
        paths = list(self.output.glob("*/evidence.jsonl"))
        self.assertEqual(len(paths), 1)
        return [json.loads(line) for line in paths[0].read_text(encoding="utf-8").splitlines()]

    async def test_real_stdio_discovery_execution_denial_approval_and_evidence(self):
        async with self.client() as session:
            discovered = await session.list_tools()
            tools = {tool.name: tool for tool in discovered.tools}
            self.assertEqual(set(tools), {"inventory_resources", "estimate_cost", "create_governance_report", "request_deployment", "delete_resource"})
            self.assertTrue(all(tool.inputSchema["additionalProperties"] is False for tool in tools.values()))
            inventory_result = await session.call_tool("inventory_resources", {})
            inventory = self.payload(inventory_result)
            self.assertFalse(inventory_result.isError)
            self.assertEqual(inventory["decision"], "allow")
            self.assertEqual(inventory["result"]["count"], 2)
            denied_result = await session.call_tool("delete_resource", {"resource_id": "vm-lab-01"})
            self.assertTrue(denied_result.isError)
            self.assertEqual(self.payload(denied_result)["execution"]["status"], "blocked")
            approval_result = await session.call_tool("request_deployment", {"resource_group": "rg-agt-lab", "template": "approved-web-service"})
            approval = self.payload(approval_result)
            self.assertTrue(approval_result.isError)
            self.assertEqual(approval["decision"], "require_approval")
            self.assertEqual(approval["execution"]["status"], "pending_approval")
            self.assertEqual(approval["session_id"], inventory["session_id"])
        events = self.evidence()
        self.assertEqual(len(events), 4)
        self.assertEqual(sum(event["phase"] == "execution" for event in events), 1)
        summary = json.loads(next(self.output.glob("*/summary.json")).read_text())
        self.assertEqual(summary["decision_counts"], {"allow": 1, "deny": 1, "require_approval": 1})
        self.assertEqual(summary["synthetic_cost_usd"], 0.01)
        self.assertEqual(self.stderr.read_text(), "")

    async def test_malformed_arguments_reach_runtime_and_secrets_do_not_leak(self):
        secret = "untrusted-secret-avoid-in-logs"
        async with self.client() as session:
            requests = [
                ("inventory_resources", {"actor": "admin", "cost_usd": 0, "prompt": secret}),
                ("estimate_cost", {"resource_id": [secret]}),
                ("estimate_cost", {}),
                ("inventory_resources", {"resource_group": "rg-production"}),
                ("estimate_cost", {"resource_id": "db-restricted-01"}),
                (secret, {}),
            ]
            expected_rules = ["argument_schema", "argument_schema", "argument_schema", "resource_scope", "data_classification", "default_deny"]
            for (tool, arguments), rule in zip(requests, expected_rules):
                result = await session.call_tool(tool, arguments)
                payload = self.payload(result)
                self.assertTrue(result.isError)
                self.assertEqual(payload["decision"], "deny")
                self.assertEqual(payload["rule"], rule)
                self.assertNotIn(secret, json.dumps(payload))
        events = self.evidence()
        self.assertEqual(len(events), 6)
        self.assertTrue(all(event["phase"] == "decision" for event in events))
        self.assertNotIn(secret, json.dumps(events))
        self.assertNotIn(secret, self.stderr.read_text())

    async def test_budget_accumulates_across_real_client_calls_and_module_entrypoint(self):
        async with self.client(module=True) as session:
            session_ids = set()
            for _ in range(5):
                result = await session.call_tool("inventory_resources", {})
                payload = self.payload(result)
                self.assertFalse(result.isError)
                session_ids.add(payload["session_id"])
            exhausted = await session.call_tool("inventory_resources", {})
            self.assertTrue(exhausted.isError)
            self.assertEqual(self.payload(exhausted)["rule"], "session_budget")
            forged = await session.call_tool("inventory_resources", {"budget_usd": 999, "reset_budget": True})
            self.assertEqual(self.payload(forged)["rule"], "argument_schema")
            still_exhausted = self.payload(await session.call_tool("inventory_resources", {}))
            self.assertEqual(still_exhausted["rule"], "session_budget")
            self.assertEqual(still_exhausted["session_spent_usd"], 0.05)
            self.assertEqual(len(session_ids), 1)
        self.assertEqual(len(self.evidence()), 13)

    def test_invalid_policy_exits_without_protocol_noise_or_secret_logging(self):
        secret = "private-value-that-must-not-appear"
        policy_path = self.directory / "invalid.yaml"
        policy_path.write_text(f"{secret}: first\n{secret}: second\n", encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--policy", str(policy_path), "--output", str(self.output)],
            cwd=self.directory,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stdout, "")
        self.assertIn("policy is invalid", completed.stderr)
        self.assertNotIn(secret, completed.stderr)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
