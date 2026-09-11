"""Offline command-line entry point. No credentials or model client required."""

import argparse
import json
import sys

from .runtime import AuditError, GovernanceRuntime, PolicyError


def demo(runtime: GovernanceRuntime) -> list[dict]:
    scenarios = [
        ("allowed inventory", "inventory_resources", {}),
        ("allowed synthetic estimate", "estimate_cost", {"resource_id": "vm-lab-01"}),
        ("forbidden resource group", "inventory_resources", {"resource_group": "rg-production"}),
        ("forbidden classification", "estimate_cost", {"resource_id": "db-restricted-01"}),
        ("deployment awaits approval", "request_deployment", {"resource_group": "rg-agt-lab", "template": "approved-web-service"}),
        ("destructive tool denied", "delete_resource", {"resource_id": "vm-lab-01"}),
        ("read-only governance report", "create_governance_report", {}),
        ("cumulative budget exhausted", "inventory_resources", {}),
        ("unknown tool denied", "run_shell", {}),
        ("caller cannot override trust", "inventory_resources", {"actor": "admin", "cost_usd": 0, "budget_usd": 999}),
    ]
    results = []
    for label, tool, arguments in scenarios:
        result = runtime.call(tool, arguments)
        results.append({"scenario": label, "tool": tool, **result})
    return results


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Original AGT-inspired offline governance lab; all costs and Azure resources are synthetic.")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("demo", "call"):
        command = commands.add_parser(name)
        command.add_argument("--policy", help="Path to an original lab-schema YAML policy")
        command.add_argument("--output", default="artifacts/lab", help="Parent directory for a new unique session")
        if name == "call":
            command.add_argument("tool")
            command.add_argument("--arguments", default="{}", help="JSON object of tool arguments")
    args = parser.parse_args(argv)
    try:
        arguments = json.loads(args.arguments) if args.command == "call" else None
        runtime = GovernanceRuntime(args.policy, args.output)
        result = demo(runtime) if args.command == "demo" else runtime.call(args.tool, arguments)
        paths = runtime.write_summary()
        print(json.dumps({"results": result, "summary": runtime.summary(), "artifacts": paths}, indent=2))
        # A completed demo includes expected denials. Single calls return a
        # nonzero status when denied, pending approval, or execution failed.
        if args.command == "call" and (result["decision"] != "allow" or result["execution"]["status"] != "succeeded"):
            return 2
        return 0
    except (PolicyError, AuditError, json.JSONDecodeError) as exc:
        print(f"Lab refused to proceed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
