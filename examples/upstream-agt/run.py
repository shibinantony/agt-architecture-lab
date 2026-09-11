"""Exercise the actual released AGT wrapper with an in-memory synthetic tool."""

from importlib.metadata import version
from pathlib import Path

from agentmesh.governance import GovernanceDenied, govern


EXPECTED_PACKAGE_VERSION = "4.1.0"


def main() -> None:
    installed = version("agent-governance-toolkit-core")
    if installed != EXPECTED_PACKAGE_VERSION:
        raise RuntimeError(
            f"This example requires agent-governance-toolkit-core=="
            f"{EXPECTED_PACKAGE_VERSION}; installed version is {installed}."
        )

    executed_actions: list[str] = []

    def synthetic_catalog(*, action: str) -> dict[str, object]:
        # A local stand-in: no shell, network, provider API or Azure access.
        executed_actions.append(action)
        return {"items": [{"id": "synthetic-001", "name": "Demo service"}]}

    guarded = govern(
        synthetic_catalog,
        policy=str(Path(__file__).with_name("policy.yaml")),
        agent_id="synthetic-catalog-agent",
    )

    result = guarded(action="read_catalog")
    if len(result["items"]) != 1 or executed_actions != ["read_catalog"]:
        raise AssertionError("The permitted request did not execute exactly once.")
    print("ALLOW read_catalog: handler executed once; synthetic items=1")

    for action in ("delete_catalog", "shell_exec", "unknown_action"):
        before = list(executed_actions)
        try:
            guarded(action=action)
        except GovernanceDenied as denial:
            if executed_actions != before:
                raise AssertionError(f"Denied action {action} reached the handler.")
            rule = denial.decision.matched_rule or "default-deny"
            print(f"DENY {action}: handler not executed; rule={rule}")
        else:
            raise AssertionError(f"Expected AGT to deny {action}.")

    if executed_actions != ["read_catalog"]:
        raise AssertionError("The synthetic handler executed an unexpected action.")
    print(f"PASS: actual AGT {installed}; 1 allow, 3 denials, 1 handler execution")


if __name__ == "__main__":
    main()
