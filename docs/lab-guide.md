# Guided lab: govern a cloud-operations assistant

You are an engineer reviewing a fictional Azure sandbox. The assistant should inspect permitted inventory, estimate cost and report issues. It should stop before deployment or deletion, stay within its resource/data scope, and use a bounded tool allowance.

This exercise mimics selected AGT concepts through an original emulator. For the actual Microsoft implementation and policy formats, use the [AGT reference](agt-reference.md).

## 1. Prepare Python

Install Python 3.11 or later if needed. Open a terminal in this repository. Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m lab demo
```

macOS/Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m lab demo
```

The remaining examples use `python`. Either substitute the full interpreter path above or activate the environment with `.\.venv\Scripts\Activate.ps1` in PowerShell / `source .venv/bin/activate` in bash. Full paths work even if PowerShell activation is disabled.

## 2. Predict the YAML policy

Open [policy.yaml](../lab/policy.yaml). This excerpt is part of the complete file; run the complete file:

```yaml
schema_version: agt-architecture-lab/v1
# Other required sections are in lab/policy.yaml.
controls:
  default_decision: deny
  allowed_environments: [sandbox]
  allowed_roles: [engineer, architect]
  allowed_resource_groups: [rg-agt-lab]
  allowed_classifications: [public, internal]
  max_session_cost_usd: 0.05
tools:
  inventory_resources:
    decision: allow
    cost_usd: 0.01
  request_deployment:
    decision: require_approval
    cost_usd: 0
  delete_resource:
    decision: deny
    cost_usd: 0
```

The policy belongs to the trusted host. The caller supplies tool arguments; it cannot supply its own identity or cheaper execution price. The actor is a synthetic fixture, not a signed enterprise identity.

## 3. Explain the ten scenarios

```shell
python -m lab demo --output artifacts/my-first-run
```

| Request, in order | Expected decision | Why |
|---|---|---|
| Inventory allowed resources | allow | Approved role, scope and tool; reserves $0.01 |
| Estimate `vm-lab-01` | allow | Permitted resource; reserves $0.02 |
| Inventory `rg-production` | deny | Outside allowed resource group |
| Estimate `db-restricted-01` | deny | Restricted classification |
| Request deployment | require_approval | Proposal stops; no deployment occurs |
| Delete a resource | deny | Prohibited operation; no delete handler |
| Create governance report | allow | Read-only fixture analysis; reserves $0.02 |
| Inventory again | deny | $0.05 allowance exhausted |
| Call `run_shell` | deny | Unknown tool |
| Supply actor/cost/budget overrides | deny | Unsupported arguments |

Expected totals: **3 allowed, 6 denied, 1 requiring approval, 3 executed, $0.05 synthetic cost**. No real resource is read, created, changed or deleted.

The report identifies issues in the visible synthetic resources, such as missing allocation metadata and public network access. Its findings are teaching examples, not a complete Azure security assessment.

## 4. Inspect the evidence

The command prints artifact paths under a unique session directory:

```text
artifacts/my-first-run/<session-id>/
  evidence.jsonl
  summary.json
  summary.md
```

Start with `summary.md`. In `evidence.jsonl`, correlate the decision and completion of one allowed call. Confirm that denied and pending requests have no completion from a handler. Ten decisions plus three completions produce thirteen records.

The evidence includes rule/reason, policy digest, session/event identifiers, status and synthetic cost. It minimizes raw arguments and does not save the full returned inventory/report. Those payloads appear in the caller's result. Files are local and editable: this is not a signed or immutable audit system.

## 5. Make and compare one policy change

Using your editor, copy `lab/policy.yaml` to `lab/policy.exercise.yaml`. Change `controls.max_session_cost_usd` to `0.02`, then run:

```shell
python -m lab demo --policy lab/policy.exercise.yaml --output artifacts/lower-budget
```

Predict the outcome first. In this modified run, the first $0.01 inventory succeeds, the $0.02 estimate and report are refused, and the later $0.01 inventory can consume the remaining allowance. Failed admission does not spend the reservation. Each process starts a new session; separate `call` invocations do not share a daily budget.

Next change `tools.inventory_resources.decision` to `deny`. Explain both the immediate denial and its effect on later available budget. Remove a tool entry to see default deny. Try an unknown policy key: startup must fail instead of silently ignoring the intended control.

Deployment cannot be made executable by editing its decision to `allow`; the policy loader refuses that configuration. The lab intentionally has no deployment executor.

## 6. Make a single request

```shell
python -m lab call inventory_resources
python -m lab call create_governance_report
```

Both use default permitted scope. For structured arguments on macOS/Linux:

```bash
python -m lab call estimate_cost --arguments '{"resource_id":"vm-lab-01"}'
```

Windows PowerShell 5.1 has different native JSON quoting behavior. Use the demo for the complete argument cases, or use this shell-independent Python entry point:

```shell
python -c "from lab import GovernanceRuntime; r = GovernanceRuntime(); print(r.call('estimate_cost', {'resource_id': 'vm-lab-01'})); print(r.write_summary())"
```

Exit codes: `0` means a completed demo or successful single call; `2` means a denied/pending/unsuccessful single call; `1` means invalid input/policy or evidence failure. The demo normally contains expected denials, so it exits successfully.

## 7. Connect a real client and challenge the design

Follow [Codex / Gemini MCP integration](cli-integration.md). The same server-side decision must apply regardless of what the model asks. Client authentication and model charges are separate from this offline setup.

Then complete your [role-based exercise](learning-path.md). Advanced learners should test malformed policy, evidence failure, concurrent calls and restart behavior, and compare with a version-pinned upstream AGT example.

## Troubleshooting

| Symptom | Check |
|---|---|
| `No module named yaml` | Install requirements with the same Python interpreter used to run the lab |
| `No module named lab` | Run module commands from the repository root |
| Invalid policy | Use the complete original schema, spaces for indentation, and known keys |
| Inventory denied unexpectedly | Read the rule/reason; check scope, identity fixture and remaining budget |
| Evidence cannot be written | Choose a writable output parent; the runtime stops before execution |
| Client cannot find tools | Use absolute paths, install MCP dependencies, inspect client/server stderr |
| Model claims it deleted something | Inspect server evidence; this lab has no delete implementation |

For the precise implementation contract and limitations, see [technical implementation](technical-implementation.md).
