"""Exercise an exact upstream AGT development snapshot with a synthetic tool."""

import json
from importlib.metadata import distribution, version
from pathlib import Path


EXPECTED_PACKAGE_VERSION = "5.0.0"
EXPECTED_SOURCE_COMMIT = "0533ceaf6c5b0975bfc71bff42f6ccd2d34c8adf"
EXPECTED_REPOSITORY_URL = "https://github.com/microsoft/agent-governance-toolkit"
EXPECTED_SOURCE_URL = f"{EXPECTED_REPOSITORY_URL}/archive/{EXPECTED_SOURCE_COMMIT}.zip"
EXPECTED_SUBDIRECTORY = "agent-governance-python/agent-governance-toolkit-core"
EXPECTED_CRYPTOGRAPHY_VERSION = "50.0.1"


def verify_installation() -> str:
    """Reject the PyPI wheel sharing version 5.0.0 and any other source revision.

    PEP 610 metadata records installation provenance. This check catches a wrong
    environment; editable local metadata is not a cryptographic attestation.
    It deliberately runs before importing or invoking the upstream toolkit.
    """
    installed = distribution("agent-governance-toolkit-core")
    if installed.version != EXPECTED_PACKAGE_VERSION:
        raise RuntimeError(
            f"This example requires agent-governance-toolkit-core=="
            f"{EXPECTED_PACKAGE_VERSION} from the pinned development snapshot; "
            f"installed version is {installed.version}."
        )
    try:
        provenance = json.loads(installed.read_text("direct_url.json") or "null")
    except (TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("The installed AGT package has invalid source provenance metadata.") from exc
    if not isinstance(provenance, dict):
        raise RuntimeError("The installed AGT package lacks pinned-source provenance; the PyPI wheel is not supported by this example.")
    archive_matches = provenance.get("url") == EXPECTED_SOURCE_URL
    vcs_info = provenance.get("vcs_info", {})
    vcs_matches = (
        isinstance(vcs_info, dict)
        and provenance.get("url") in {EXPECTED_REPOSITORY_URL, EXPECTED_REPOSITORY_URL + ".git"}
        and vcs_info.get("vcs") == "git"
        and vcs_info.get("commit_id") == EXPECTED_SOURCE_COMMIT
    )
    if provenance.get("subdirectory") != EXPECTED_SUBDIRECTORY or not (archive_matches or vcs_matches):
        raise RuntimeError("The installed AGT package does not match the reviewed upstream source commit and package directory.")
    if version("cryptography") != EXPECTED_CRYPTOGRAPHY_VERSION:
        raise RuntimeError(f"This example requires the reviewed cryptography=={EXPECTED_CRYPTOGRAPHY_VERSION} pin.")
    return installed.version


def main() -> None:
    installed = verify_installation()
    from agentmesh.governance import GovernanceDenied, govern

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
    print(
        f"PASS: actual AGT development snapshot {EXPECTED_SOURCE_COMMIT}; "
        f"package {installed}; 1 allow, 3 denials, 1 handler execution"
    )


if __name__ == "__main__":
    main()
