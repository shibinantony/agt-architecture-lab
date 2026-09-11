# Validation record

Review date: **2026-09-11**. Tests use synthetic inputs. Record observed execution separately from architectural proposals.

## Baseline reviewed before editing

The entire local tracked project and GitHub default branch were inspected before the rework: 31 files, 144,984 bytes, with matching blob IDs at commit `0003bbef775e96ddcef04f4fb73afab5f14bb470`. The GitHub tree was complete, not truncated. Local continuity records were also reviewed and remain ignored.

At review time GitHub contained a private repository, one initial commit and one successful documentation-validation run. It had no Pages site, hosted application, deployment, release, issue or pull request. “Deployed” referred to publishing the repository.

## Observed local execution

Environment: Windows, Python 3.11.9. Core dependency: PyYAML 6.0.3; MCP SDK: 1.30.0; JSON Schema validator: 4.26.0.

| Check | Observed result / scope |
|---|---|
| Offline demo | 10 decisions: 3 allow, 6 deny, 1 approval required; 3 handler executions; synthetic $0.05; 13 JSONL records |
| Runtime tests | 20 tests cover fixture results, denied/pending dispatch, scope/classification, caller overrides, malformed policy, concurrency and audit failure before/after execution |
| MCP protocol tests | 4 tests launch a real stdio server and use the SDK client; discovery, structured replies, denial, pending approval, malformed arguments, cumulative budget and startup failure |
| Decision contracts | Both original Azure and new agent examples validated against JSON Schema, including date formats |
| Actual Microsoft AGT | Separate environment with core 4.1.0; 1 allow, 3 denials, exactly 1 synthetic handler execution; dependency check passes |
| CLI setup commands | Codex and Gemini MCP registration syntax checked against official documentation and installed help |

The MCP tests required normal permission to create Windows subprocess pipes. That is a local test-runner permission, not an agent authorization control.

## CI

The [validation workflow](../.github/workflows/repository-validation.yml) runs runtime/MCP/schema tests and the demo on Windows and Ubuntu, checks repository links/JSON/encoding, and uploads synthetic demo evidence for seven days. A separate Ubuntu job installs and exercises actual AGT 4.1.0. Workflow results are available under [GitHub Actions](https://github.com/shibinantony/governance-evidence-lab/actions).

CI configuration is executable; use the run result for the commit being reviewed as evidence. Do not interpret a workflow file alone as a passed cross-platform test.

## What has not been established

- An authenticated Codex or Gemini model session invoking the server end to end.
- Azure tenant inventory, deployment, enforcement, invoices or measured financial benefit.
- Native ACS execution or complete AGT component coverage.
- Enterprise identity, protected distributed budgets, signed audit storage, verified human approvals or production isolation.
- General resistance to every prompt-injection or alternate tool path.

The [architecture](architecture.md) and [roadmap](../ROADMAP.md) describe those additional gates. The lab YAML, released AgentMesh policy YAML and ACS manifests are distinct formats.

## Reproduce

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m lab demo
./tests/Test-Repository.ps1
```

Use `.venv/bin/python` on macOS/Linux. Follow the separate [upstream example](../examples/upstream-agt/README.md) for AGT, and the [client guide](cli-integration.md) for optional live acceptance tests.
