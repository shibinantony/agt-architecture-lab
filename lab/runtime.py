"""Fail-closed, offline policy gateway for a small set of synthetic Azure tools.

The gateway controls only calls routed through this object. Its actor is a local
policy fixture, not an authenticated identity. The budget and lock are local to
one runtime object in one process. JSONL is local evidence, not a signed ledger.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import threading
import uuid
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml

PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_POLICY_PATH = PACKAGE_DIR / "policy.yaml"
SCHEMA_VERSION = "agt-architecture-lab/v1"


class PolicyError(ValueError):
    """A policy cannot be safely interpreted; no runtime should be started."""


class AuditError(RuntimeError):
    """Evidence storage failed; this runtime refuses further actions."""


def _schema(properties: dict[str, Any], required: list[str] | None = None) -> dict:
    schema = {"type": "object", "properties": properties, "additionalProperties": False}
    if required:
        schema["required"] = required
    return schema


_STRING = {"type": "string", "minLength": 1, "maxLength": 128}
TOOL_DEFINITIONS = [
    {
        "name": "inventory_resources",
        "description": "Read synthetic Azure inventory in a policy-allowed resource group.",
        "inputSchema": _schema({"resource_group": _STRING}),
    },
    {
        "name": "estimate_cost",
        "description": "Read a fixture's synthetic monthly USD estimate; no Azure pricing API.",
        "inputSchema": _schema({"resource_id": _STRING}, ["resource_id"]),
    },
    {
        "name": "create_governance_report",
        "description": "Compute read-only tagging, exposure and cost findings from fixtures.",
        "inputSchema": _schema({"resource_group": _STRING}),
    },
    {
        "name": "request_deployment",
        "description": "Record an approval-required proposal. Deployment is never executed.",
        "inputSchema": _schema(
            {"resource_group": _STRING, "template": _STRING},
            ["resource_group", "template"],
        ),
    },
    {
        "name": "delete_resource",
        "description": "Demonstrate a prohibited destructive request; no delete implementation.",
        "inputSchema": _schema({"resource_id": _STRING}, ["resource_id"]),
    },
]
_TOOL_SCHEMAS = {tool["name"]: copy.deepcopy(tool["inputSchema"]) for tool in TOOL_DEFINITIONS}
_EXECUTABLE_TOOLS = {"inventory_resources", "estimate_cost", "create_governance_report"}


class _StrictLoader(yaml.SafeLoader):
    def compose_node(self, parent, index):
        if self.check_event(yaml.AliasEvent):
            raise PolicyError("YAML aliases are not supported by the lab policy schema.")
        return super().compose_node(parent, index)

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, yaml.MappingNode):
            raise PolicyError("Policy mappings must contain explicit keys.")
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if type(key) is not str:
                raise PolicyError("Policy keys must be strings.")
            if key in mapping:
                raise PolicyError(f"Duplicate policy key: {key}.")
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def _keys(value: Any, required: set[str], location: str, optional: set[str] | None = None):
    if type(value) is not dict:
        raise PolicyError(f"{location} must be a mapping.")
    if set(value) - required - (optional or set()):
        raise PolicyError(f"{location} contains unknown keys.")
    if required - set(value):
        raise PolicyError(f"{location} is missing required keys.")


def _string(value: Any, location: str):
    if type(value) is not str or not value.strip() or len(value) > 128:
        raise PolicyError(f"{location} must be a nonempty string of at most 128 characters.")


def _strings(value: Any, location: str):
    if type(value) is not list or not value:
        raise PolicyError(f"{location} must be a nonempty list of strings.")
    for item in value:
        _string(item, location)
    if len(set(value)) != len(value):
        raise PolicyError(f"{location} must not contain duplicate entries.")


def _money(value: Any, location: str) -> Decimal:
    if type(value) not in (int, float) or (type(value) is float and not math.isfinite(value)):
        raise PolicyError(f"{location} must be a finite numeric USD amount, not a string or boolean.")
    amount = Decimal(str(value))
    if amount < 0 or amount > Decimal("1000000") or amount.as_tuple().exponent < -6:
        raise PolicyError(f"{location} must be 0..1000000 USD with at most six decimal places.")
    return amount


def load_policy(path: str | Path = DEFAULT_POLICY_PATH) -> tuple[dict, str]:
    """Read the original lab schema strictly; return validated policy and file digest."""
    try:
        raw = Path(path).read_bytes()
        if len(raw) > 131072:
            raise PolicyError("Policy files must be at most 128 KiB.")
        policy = yaml.load(raw.decode("utf-8"), Loader=_StrictLoader)
    except PolicyError:
        raise
    except (OSError, UnicodeError, yaml.YAMLError, RecursionError, ValueError) as exc:
        raise PolicyError("Policy could not be read as the lab's YAML schema.") from exc
    _keys(policy, {"schema_version", "metadata", "actor", "environment", "controls", "tools"}, "policy")
    if policy["schema_version"] != SCHEMA_VERSION:
        raise PolicyError(f"schema_version must be {SCHEMA_VERSION}.")
    _keys(policy["metadata"], {"name"}, "metadata")
    _string(policy["metadata"]["name"], "metadata.name")
    _keys(policy["actor"], {"id", "role"}, "actor")
    for key in ("id", "role"):
        _string(policy["actor"][key], f"actor.{key}")
    _keys(policy["environment"], {"name"}, "environment")
    _string(policy["environment"]["name"], "environment.name")
    controls = policy["controls"]
    list_controls = {
        "allowed_environments", "allowed_roles", "allowed_resource_groups", "allowed_classifications"
    }
    _keys(controls, list_controls | {"default_decision", "max_session_cost_usd"}, "controls")
    if controls["default_decision"] != "deny":
        raise PolicyError("controls.default_decision must be deny.")
    for key in list_controls:
        _strings(controls[key], f"controls.{key}")
    if set(controls["allowed_classifications"]) - {"public", "internal", "restricted"}:
        raise PolicyError("allowed_classifications contains an unknown classification.")
    _money(controls["max_session_cost_usd"], "controls.max_session_cost_usd")
    _keys(policy["tools"], set(), "tools", set(_TOOL_SCHEMAS))
    for name, tool in policy["tools"].items():
        _keys(tool, {"decision", "cost_usd"}, f"tools.{name}")
        decision = tool["decision"]
        if type(decision) is not str or decision not in {"allow", "deny", "require_approval"}:
            raise PolicyError(f"tools.{name}.decision is unknown.")
        cost = _money(tool["cost_usd"], f"tools.{name}.cost_usd")
        if name == "request_deployment" and decision == "allow":
            raise PolicyError("request_deployment may only require approval or be denied.")
        if name == "delete_resource" and decision != "deny":
            raise PolicyError("delete_resource must be denied; this lab has no delete executor.")
        if name not in _EXECUTABLE_TOOLS and cost != 0:
            raise PolicyError("Non-executing tools must have zero synthetic execution cost.")
    return policy, hashlib.sha256(raw).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


class GovernanceRuntime:
    """One session with a trusted startup policy, local budget and durable audit gate."""

    def __init__(self, policy_path: str | Path | None = None, output_dir: str | Path = "artifacts/lab"):
        policy, digest = load_policy(policy_path or DEFAULT_POLICY_PATH)
        self._policy = policy
        self.policy_digest = digest
        self.session_id = uuid.uuid4().hex
        self.output_dir = Path(output_dir) / self.session_id
        self.evidence_path = self.output_dir / "evidence.jsonl"
        self._lock = threading.RLock()
        self._spent = Decimal("0")
        self._budget = _money(policy["controls"]["max_session_cost_usd"], "budget")
        self._audit_failed = False
        self._events: list[dict] = []
        self._resources = json.loads((PACKAGE_DIR / "fixtures" / "resources.json").read_text(encoding="utf-8"))
        self._handlers = {
            "inventory_resources": self._inventory,
            "estimate_cost": self._estimate,
            "create_governance_report": self._report,
        }
        try:
            self.output_dir.mkdir(parents=True, exist_ok=False)
            # Fail before accepting calls when the evidence destination is unavailable.
            with self.evidence_path.open("x", encoding="utf-8") as handle:
                handle.flush()
                os.fsync(handle.fileno())
        except OSError as exc:
            raise AuditError("Cannot initialize evidence storage; no tool has executed.") from exc

    def _append(self, event: dict):
        try:
            with self.evidence_path.open("a", encoding="utf-8", newline="\n") as handle:
                handle.write(json.dumps(event, sort_keys=True, allow_nan=False) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
        except (OSError, ValueError, TypeError) as exc:
            self._audit_failed = True
            raise AuditError("Evidence append failed; this session is closed to further actions.") from exc
        self._events.append(copy.deepcopy(event))

    def _safe_arguments(self, arguments: Any) -> dict:
        """Persist known fixture labels only; unknown values and fields never enter JSONL."""
        if type(arguments) is not dict:
            return {"shape": "invalid"}
        known_fields = {"resource_id", "resource_group", "template"}
        safe = {"provided_fields": sorted(key for key in arguments if type(key) is str and key in known_fields)}
        safe["unknown_field_count"] = sum(type(key) is not str or key not in known_fields for key in arguments)
        fixture_values = {
            "resource_id": {resource["id"] for resource in self._resources},
            "resource_group": {resource["resource_group"] for resource in self._resources},
            "template": {"approved-web-service"},
        }
        for key in safe["provided_fields"]:
            value = arguments[key]
            safe[key] = value if type(value) is str and value in fixture_values[key] else "<redacted>"
        return safe

    def _evaluate(self, tool: Any, arguments: Any) -> tuple[str, str, str, dict, Decimal]:
        deny = lambda rule, reason: ("deny", rule, reason, {}, Decimal("0"))
        if type(tool) is not str or tool not in _TOOL_SCHEMAS or tool not in self._policy["tools"]:
            return deny("default_deny", "The tool is not in the trusted policy catalog.")
        schema = _TOOL_SCHEMAS[tool]
        if type(arguments) is not dict:
            return deny("argument_schema", "Arguments must be a JSON object.")
        if any(type(key) is not str for key in arguments) or set(arguments) - set(schema["properties"]):
            return deny("argument_schema", "Unknown argument fields are forbidden, including caller identity and cost overrides.")
        if set(schema.get("required", [])) - set(arguments):
            return deny("argument_schema", "A required argument is missing.")
        if any(type(value) is not str or not value.strip() or len(value) > 128 for value in arguments.values()):
            return deny("argument_schema", "Arguments must be nonempty strings of at most 128 characters.")
        controls = self._policy["controls"]
        if self._policy["actor"]["role"] not in controls["allowed_roles"]:
            return deny("actor_role", "The trusted actor role is not allowed.")
        if self._policy["environment"]["name"] not in controls["allowed_environments"]:
            return deny("environment", "The trusted environment is not allowed.")
        normalized = copy.deepcopy(arguments)
        if "resource_id" in arguments:
            resource = next((item for item in self._resources if item["id"] == arguments["resource_id"]), None)
            if resource is None:
                return deny("resource_scope", "The resource is absent from the trusted fixture inventory.")
            resource_group = resource["resource_group"]
            if resource["classification"] not in controls["allowed_classifications"]:
                return deny("data_classification", "The resource classification is not allowed.")
        else:
            resource_group = arguments.get("resource_group", controls["allowed_resource_groups"][0])
            normalized["resource_group"] = resource_group
        if resource_group not in controls["allowed_resource_groups"]:
            return deny("resource_scope", "The resource group is outside the policy's allowed scope.")
        if tool == "request_deployment" and arguments["template"] != "approved-web-service":
            return deny("deployment_template", "The proposed template is not in the lab's fixed catalog.")
        tool_policy = self._policy["tools"][tool]
        decision = tool_policy["decision"]
        if decision == "deny":
            return deny("tool_policy", "The trusted policy prohibits this tool.")
        if decision == "require_approval":
            return "require_approval", "human_approval", "Human approval is required; this lab records a proposal and has no approval executor.", normalized, Decimal("0")
        cost = _money(tool_policy["cost_usd"], "tool.cost_usd")
        if self._spent + cost > self._budget:
            return deny("session_budget", "The fixed synthetic tool cost would exceed the cumulative session budget.")
        return "allow", "policy_allow", "Role, environment, scope, classification, tool policy and session budget permit this call.", normalized, cost

    def call(self, tool_name: str, arguments: dict | None = None) -> dict:
        """Evaluate, durably record, and dispatch at most one fixed local handler.

        All steps share a lock. No caller-provided actor, classification, cost or
        budget can override the policy. Denial and approval never enter a handler.
        An evidence completion failure raises, even if a local handler has run.
        """
        with self._lock:
            if self._audit_failed:
                raise AuditError("This session is closed after an evidence failure; no further tool executed.")
            arguments = {} if arguments is None else arguments
            decision, rule, reason, normalized, cost = self._evaluate(tool_name, arguments)
            event_id = uuid.uuid4().hex
            event = {
                "schema_version": SCHEMA_VERSION,
                "session_id": self.session_id,
                "event_id": event_id,
                "timestamp": _now(),
                "phase": "decision",
                "policy_sha256": self.policy_digest,
                "actor": copy.deepcopy(self._policy["actor"]),
                "environment": self._policy["environment"]["name"],
                "tool": tool_name if type(tool_name) is str and tool_name in _TOOL_SCHEMAS else "<unknown>",
                "arguments": self._safe_arguments(arguments),
                "decision": decision,
                "rule": rule,
                "reason": reason,
                "synthetic_cost_usd": float(cost),
                "session_spent_usd": float(self._spent),
                "execution": {"status": "authorized" if decision == "allow" else ("pending_approval" if decision == "require_approval" else "blocked"), "cost_usd": 0},
            }
            # Audit success is a prerequisite for ALL execution.
            try:
                self._append(event)
            except AuditError:
                self._audit_failed = True
                raise
            result = None
            execution = copy.deepcopy(event["execution"])
            if decision == "allow":
                self._spent += cost
                try:
                    result = self._handlers[tool_name](normalized)
                    execution = {"status": "succeeded", "cost_usd": float(cost)}
                except Exception:
                    # No caller data or raw exceptions are included in evidence.
                    execution = {"status": "failed", "cost_usd": float(cost)}
                    reason = "The local synthetic handler failed; its fixed dispatch cost remains charged."
                completion = {
                    **event,
                    "timestamp": _now(),
                    "phase": "execution",
                    "session_spent_usd": float(self._spent),
                    "execution": execution,
                    "reason": reason,
                }
                try:
                    self._append(completion)
                except AuditError as exc:
                    self._audit_failed = True
                    raise AuditError("Completion evidence failed after a local handler ran. The session is closed; execution must not be assumed absent.") from exc
            return {
                "session_id": self.session_id,
                "event_id": event_id,
                "decision": decision,
                "rule": rule,
                "reason": reason,
                "execution": execution,
                "result": result,
                "session_spent_usd": float(self._spent),
                "remaining_budget_usd": float(self._budget - self._spent),
                "synthetic": True,
            }

    def _visible_resources(self, group: str) -> list[dict]:
        classifications = self._policy["controls"]["allowed_classifications"]
        return [resource for resource in self._resources if resource["resource_group"] == group and resource["classification"] in classifications]

    def _inventory(self, arguments: dict) -> dict:
        resources = copy.deepcopy(self._visible_resources(arguments["resource_group"]))
        return {"synthetic": True, "resource_group": arguments["resource_group"], "resources": resources, "count": len(resources)}

    def _estimate(self, arguments: dict) -> dict:
        resource = next(item for item in self._resources if item["id"] == arguments["resource_id"])
        return {"synthetic": True, "resource_id": resource["id"], "currency": "USD", "monthly_estimate": resource["monthly_cost_usd"], "source": "Bundled fixture; not an Azure quote or model usage charge"}

    def _report(self, arguments: dict) -> dict:
        resources = self._visible_resources(arguments["resource_group"])
        findings = []
        for resource in resources:
            for tag in ("owner", "cost_center", "environment"):
                if not resource["tags"].get(tag):
                    findings.append({"resource_id": resource["id"], "control": "tagging", "severity": "warning", "finding": f"Required tag '{tag}' is missing."})
            if resource["public_network_access"]:
                findings.append({"resource_id": resource["id"], "control": "network_exposure", "severity": "review", "finding": "Public network access is enabled in this fixture; review whether it is required."})
        return {
            "synthetic": True,
            "read_only": True,
            "resource_group": arguments["resource_group"],
            "resources_reviewed": len(resources),
            "monthly_estimate_usd": float(sum((Decimal(str(resource["monthly_cost_usd"])) for resource in resources), Decimal("0"))),
            "findings": findings,
            "limitation": "Reviews only policy-visible fixtures. Findings do not prove compliance or trigger remediation.",
        }

    def summary(self) -> dict:
        with self._lock:
            decisions = Counter(event["decision"] for event in self._events if event["phase"] == "decision")
            executions = Counter(event["execution"]["status"] for event in self._events if event["phase"] == "execution")
            return {
                "schema_version": SCHEMA_VERSION,
                "session_id": self.session_id,
                "policy_sha256": self.policy_digest,
                "generated_at": _now(),
                "decision_counts": {key: decisions[key] for key in ("allow", "deny", "require_approval")},
                "execution_counts": {key: executions[key] for key in ("succeeded", "failed")},
                "synthetic_cost_usd": float(self._spent),
                "budget_usd": float(self._budget),
                "remaining_budget_usd": float(self._budget - self._spent),
                "audit_healthy": not self._audit_failed,
                "evidence_path": str(self.evidence_path),
                "limitations": [
                    "Original lab policy schema; not AGT or ACS compatible.",
                    "Synthetic fixtures and costs; no Azure, model, shell or deployment execution.",
                    "Budget and actor belong to one local runtime session; restarting resets the budget.",
                    "Local evidence is unsigned and editable; this is not a production audit ledger.",
                    "Only calls through this gateway are governed; other client tools are outside its boundary.",
                ],
            }

    def write_summary(self) -> dict:
        with self._lock:
            summary = self.summary()
            json_path = self.output_dir / "summary.json"
            markdown_path = self.output_dir / "summary.md"
            counts = summary["decision_counts"]
            markdown = (
                "# AGT architecture lab: synthetic session evidence\n\n"
                f"Session: `{self.session_id}`\n\n"
                f"Policy SHA-256: `{self.policy_digest}`\n\n"
                f"Allowed: {counts['allow']} | Denied: {counts['deny']} | Awaiting approval: {counts['require_approval']}\n\n"
                f"Successful local executions: {summary['execution_counts']['succeeded']}\n\n"
                f"Synthetic execution cost: ${summary['synthetic_cost_usd']:.6f} / ${summary['budget_usd']:.6f} USD\n\n"
                f"Evidence storage healthy: {summary['audit_healthy']}\n\n"
                "## Interpretation limits\n\n"
                + "\n".join(f"- {item}" for item in summary["limitations"])
                + "\n"
            )
            try:
                for path, content in ((json_path, json.dumps(summary, indent=2) + "\n"), (markdown_path, markdown)):
                    temporary = path.with_suffix(path.suffix + ".tmp")
                    temporary.write_text(content, encoding="utf-8")
                    os.replace(temporary, path)
            except OSError as exc:
                self._audit_failed = True
                raise AuditError("Could not write session summaries; evidence remains in the JSONL file.") from exc
            return {"evidence": str(self.evidence_path), "json": str(json_path), "markdown": str(markdown_path)}
