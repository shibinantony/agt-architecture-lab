"""Behavior and trust-boundary tests; entirely offline and credential-free."""

import concurrent.futures
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import yaml

from lab.__main__ import demo
from lab.runtime import AuditError, DEFAULT_POLICY_PATH, GovernanceRuntime, PolicyError, load_policy


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output = Path(self.temporary.name)
        self.policy = yaml.safe_load(DEFAULT_POLICY_PATH.read_text(encoding="utf-8"))

    def runtime(self, change=None):
        if change is None:
            return GovernanceRuntime(output_dir=self.output)
        policy = copy.deepcopy(self.policy)
        change(policy)
        path = self.output / "custom-policy.yaml"
        path.write_text(yaml.safe_dump(policy), encoding="utf-8")
        return GovernanceRuntime(path, self.output)

    def test_demo_exercises_real_results_and_all_decision_paths(self):
        runtime = self.runtime()
        results = demo(runtime)
        self.assertEqual(runtime.summary()["decision_counts"], {"allow": 3, "deny": 6, "require_approval": 1})
        self.assertEqual(runtime.summary()["synthetic_cost_usd"], 0.05)
        self.assertEqual(results[0]["result"]["count"], 2)
        self.assertEqual(results[1]["result"]["monthly_estimate"], 48.0)
        report = results[6]["result"]
        self.assertEqual(report["monthly_estimate_usd"], 53.0)
        self.assertEqual({finding["control"] for finding in report["findings"]}, {"tagging", "network_exposure"})
        self.assertTrue(report["read_only"])
        paths = runtime.write_summary()
        self.assertEqual(set(paths), {"evidence", "json", "markdown"})
        for path in paths.values():
            self.assertTrue(Path(path).is_file())
        evidence = [json.loads(line) for line in runtime.evidence_path.read_text().splitlines()]
        self.assertEqual(len(evidence), 13)
        self.assertTrue(all(event["policy_sha256"] == runtime.policy_digest for event in evidence))
        self.assertTrue(all(event["timestamp"].endswith("+00:00") for event in evidence))

    def test_denied_and_approval_requests_never_enter_handlers(self):
        runtime = self.runtime()
        spies = {name: Mock(side_effect=AssertionError("Must not dispatch")) for name in (
            "inventory_resources", "estimate_cost", "delete_resource", "request_deployment", "run_shell"
        )}
        runtime._handlers.update(spies)
        requests = [
            ("inventory_resources", {"resource_group": "rg-production"}),
            ("estimate_cost", {"resource_id": "db-restricted-01"}),
            ("delete_resource", {"resource_id": "vm-lab-01"}),
            ("run_shell", {}),
            ("request_deployment", {"resource_group": "rg-agt-lab", "template": "approved-web-service"}),
        ]
        for tool, arguments in requests:
            result = runtime.call(tool, arguments)
            self.assertNotEqual(result["decision"], "allow")
            self.assertIsNone(result["result"])
            self.assertEqual(result["execution"]["cost_usd"], 0)
        self.assertEqual(result["decision"], "require_approval")
        self.assertEqual(result["execution"]["status"], "pending_approval")
        self.assertEqual(runtime.summary()["synthetic_cost_usd"], 0)
        for spy in spies.values():
            spy.assert_not_called()

    def test_trusted_role_and_environment_enforced(self):
        for field, key, value, rule in (("actor", "role", "visitor", "actor_role"), ("environment", "name", "production", "environment")):
            with self.subTest(rule=rule):
                runtime = self.runtime(lambda policy: policy[field].update({key: value}))
                handler = Mock()
                runtime._handlers["inventory_resources"] = handler
                self.assertEqual(runtime.call("inventory_resources")["rule"], rule)
                handler.assert_not_called()

    def test_removed_catalog_tool_and_unknown_tool_default_deny(self):
        runtime = self.runtime(lambda policy: policy["tools"].pop("inventory_resources"))
        for tool in ("inventory_resources", "unknown_tool"):
            self.assertEqual(runtime.call(tool)["rule"], "default_deny")

    def test_classification_and_scope_apply_to_inventory_and_direct_lookup(self):
        runtime = self.runtime()
        inventory = runtime.call("inventory_resources")["result"]["resources"]
        self.assertEqual({resource["id"] for resource in inventory}, {"vm-lab-01", "storage-lab-01"})
        for resource_id, rule in (("db-restricted-01", "data_classification"), ("vm-prod-01", "resource_scope"), ("unknown-id", "resource_scope")):
            self.assertEqual(runtime.call("estimate_cost", {"resource_id": resource_id})["rule"], rule)

    def test_caller_fields_cannot_forge_identity_cost_scope_or_reset_budget(self):
        runtime = self.runtime()
        for override in ({"actor": "admin"}, {"role": "architect"}, {"cost_usd": 0}, {"remaining_budget_usd": 100}, {"classification": "public"}, {"environment": "sandbox"}, {"reset_budget": True}):
            self.assertEqual(runtime.call("inventory_resources", override)["rule"], "argument_schema")
        for _ in range(5):
            self.assertEqual(runtime.call("inventory_resources")["decision"], "allow")
        self.assertEqual(runtime.call("inventory_resources")["rule"], "session_budget")
        self.assertEqual(runtime.call("inventory_resources", {"cost_usd": 0})["rule"], "argument_schema")
        self.assertEqual(runtime.call("inventory_resources")["rule"], "session_budget")
        self.assertEqual(runtime.summary()["synthetic_cost_usd"], 0.05)

    def test_threads_cannot_overdraw_session_budget(self):
        runtime = self.runtime()
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda _: runtime.call("inventory_resources"), range(24)))
        self.assertEqual(sum(result["decision"] == "allow" for result in results), 5)
        self.assertEqual(sum(result["rule"] == "session_budget" for result in results), 19)
        self.assertEqual(runtime.summary()["synthetic_cost_usd"], 0.05)
        events = [json.loads(line) for line in runtime.evidence_path.read_text().splitlines()]
        self.assertEqual(len(events), 29)

    def test_secrets_and_unrecognized_argument_names_are_not_in_evidence(self):
        runtime = self.runtime()
        secret = "sk-secret-must-never-be-persisted"
        runtime.call("inventory_resources", {"prompt": secret, secret: "value"})
        runtime.call("estimate_cost", {"resource_id": secret})
        runtime.call(secret, {})
        evidence = runtime.evidence_path.read_text()
        self.assertNotIn(secret, evidence)
        self.assertNotIn("prompt", evidence)
        self.assertIn("<redacted>", evidence)

    def test_invalid_argument_types_fail_closed(self):
        runtime = self.runtime()
        for arguments in ([], "string", 12, {"resource_id": []}, {"resource_id": True}, {"resource_id": ""}, {"resource_id": "x" * 129}, {1: "value"}, {}):
            with self.subTest(arguments=arguments):
                result = runtime.call("estimate_cost", arguments)
                self.assertEqual(result["decision"], "deny")
                self.assertEqual(result["rule"], "argument_schema")

    def test_audit_failure_blocks_execution_and_closes_session(self):
        runtime = self.runtime()
        handler = Mock()
        runtime._handlers["inventory_resources"] = handler
        with patch.object(Path, "open", side_effect=OSError("unwritable evidence")):
            with self.assertRaises(AuditError):
                runtime.call("inventory_resources")
        handler.assert_not_called()
        with self.assertRaises(AuditError):
            runtime.call("inventory_resources")
        self.assertFalse(runtime.summary()["audit_healthy"])
        self.assertEqual(runtime.summary()["synthetic_cost_usd"], 0)

    def test_audit_is_durable_before_handler_dispatch(self):
        runtime = self.runtime()

        def handler(arguments):
            events = [json.loads(line) for line in runtime.evidence_path.read_text().splitlines()]
            self.assertEqual(events[-1]["phase"], "decision")
            self.assertEqual(events[-1]["execution"]["status"], "authorized")
            return {"checked": True}

        runtime._handlers["inventory_resources"] = handler
        self.assertEqual(runtime.call("inventory_resources")["result"], {"checked": True})

    def test_completion_audit_failure_does_not_claim_unexecuted_or_success(self):
        runtime = self.runtime()
        original_append = runtime._append
        handler = Mock(return_value={"local_only": True})
        runtime._handlers["inventory_resources"] = handler

        def fail_completion(event):
            if event["phase"] == "execution":
                with patch.object(Path, "open", side_effect=OSError("disk full")):
                    original_append(event)
            else:
                original_append(event)

        with patch.object(runtime, "_append", side_effect=fail_completion):
            with self.assertRaisesRegex(AuditError, "after a local handler ran"):
                runtime.call("inventory_resources")
        handler.assert_called_once()
        self.assertEqual(runtime.summary()["synthetic_cost_usd"], 0.01)
        with self.assertRaises(AuditError):
            runtime.call("inventory_resources")

    def test_handler_failure_is_recorded_and_dispatch_cost_remains_charged(self):
        runtime = self.runtime()
        runtime._handlers["inventory_resources"] = Mock(side_effect=RuntimeError("secret exception"))
        result = runtime.call("inventory_resources")
        self.assertEqual(result["execution"], {"status": "failed", "cost_usd": 0.01})
        self.assertEqual(runtime.summary()["execution_counts"]["failed"], 1)
        self.assertNotIn("secret exception", runtime.evidence_path.read_text())

    def test_budget_is_explicitly_per_runtime_and_sessions_have_distinct_evidence(self):
        first, second = self.runtime(), self.runtime()
        first.call("inventory_resources")
        self.assertEqual(first.summary()["synthetic_cost_usd"], 0.01)
        self.assertEqual(second.summary()["synthetic_cost_usd"], 0)
        self.assertNotEqual(first.evidence_path, second.evidence_path)


class PolicyValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "policy.yaml"
        self.original = DEFAULT_POLICY_PATH.read_text(encoding="utf-8")
        self.policy = yaml.safe_load(self.original)

    def reject(self, policy):
        self.path.write_text(yaml.safe_dump(policy), encoding="utf-8")
        with self.assertRaises(PolicyError):
            GovernanceRuntime(self.path, Path(self.temporary.name) / "out")
        self.assertFalse((Path(self.temporary.name) / "out").exists())

    def test_default_policy_loads_and_has_stable_digest(self):
        policy, digest = load_policy(DEFAULT_POLICY_PATH)
        self.assertEqual(policy["controls"]["max_session_cost_usd"], 0.05)
        self.assertEqual(len(digest), 64)
        self.assertEqual(digest, load_policy(DEFAULT_POLICY_PATH)[1])

    def test_unknown_keys_and_missing_required_controls_are_rejected(self):
        variations = []
        policy = copy.deepcopy(self.policy)
        policy["rules"] = {"allow_everything": True}
        variations.append(policy)
        policy = copy.deepcopy(self.policy)
        policy["controls"]["allow_prompt_override"] = True
        variations.append(policy)
        policy = copy.deepcopy(self.policy)
        del policy["controls"]["allowed_roles"]
        variations.append(policy)
        policy = copy.deepcopy(self.policy)
        policy["tools"]["shell"] = {"decision": "allow", "cost_usd": 0}
        variations.append(policy)
        policy = copy.deepcopy(self.policy)
        policy["tools"]["estimate_cost"]["budget_bypass"] = True
        variations.append(policy)
        for policy in variations:
            with self.subTest(policy=policy):
                self.reject(policy)

    def test_malformed_yaml_duplicate_keys_and_aliases_are_rejected(self):
        for text in ("[invalid", "", "null", self.original + "actor: {id: attacker, role: admin}\n", self.original.replace("id: learner-001", "id: learner-001\n  id: duplicate"), self.original.replace("name: Sandbox engineering review", "name: &label Sandbox engineering review").replace("id: learner-001", "id: *label")):
            with self.subTest(text=text[:40]):
                self.path.write_text(text, encoding="utf-8")
                with self.assertRaises(PolicyError):
                    load_policy(self.path)

    def test_invalid_money_cannot_allow_budget_bypass(self):
        for amount in (-0.1, float("nan"), float("inf"), -float("inf"), "0.01", True, [], 0.0000001, 1000001):
            for location in ("tool", "budget"):
                with self.subTest(amount=amount, location=location):
                    policy = copy.deepcopy(self.policy)
                    if location == "tool":
                        policy["tools"]["inventory_resources"]["cost_usd"] = amount
                    else:
                        policy["controls"]["max_session_cost_usd"] = amount
                    self.reject(policy)

    def test_unknown_decisions_and_destructive_allow_rules_are_rejected(self):
        for tool, decision in (("inventory_resources", "permit"), ("inventory_resources", True), ("inventory_resources", []), ("delete_resource", "allow"), ("delete_resource", "require_approval"), ("request_deployment", "allow")):
            with self.subTest(tool=tool, decision=decision):
                policy = copy.deepcopy(self.policy)
                policy["tools"][tool]["decision"] = decision
                self.reject(policy)
        policy = copy.deepcopy(self.policy)
        policy["controls"]["default_decision"] = "allow"
        self.reject(policy)

    def test_invalid_control_types_and_unknown_classifications_are_rejected(self):
        for key, value in (("allowed_roles", "engineer"), ("allowed_roles", []), ("allowed_roles", ["engineer", "engineer"]), ("allowed_roles", [True]), ("allowed_classifications", ["magic-safe"])):
            policy = copy.deepcopy(self.policy)
            policy["controls"][key] = value
            with self.subTest(key=key, value=value):
                self.reject(policy)


if __name__ == "__main__":
    unittest.main()
