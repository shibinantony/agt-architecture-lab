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
| Original upstream check | Released core 4.1.0 passed 1 allow, 3 denials and 1 handler execution on Windows; superseded because the dependency audit found vulnerable cryptography |
| Current upstream source | Ubuntu CI with Python 3.11 built the pinned development snapshot 5.0.0 with cryptography 50.0.1; 1 allow, 3 denials, exactly 1 handler execution; dependency check and advisory scan passed. Windows source installation failed at native ACS build metadata |
| Source provenance | 5 dependency-independent tests check required package/cryptography versions, archive/VCS origin and wrong/missing source metadata |
| CLI setup commands | Codex and Gemini MCP registration syntax checked against official documentation and installed help |

The MCP tests required normal permission to create Windows subprocess pipes. That is a local test-runner permission, not an agent authorization control.

## CI

The [validation workflow](../.github/workflows/repository-validation.yml) runs 30 runtime/MCP/schema/provenance tests and the demo on Windows and Ubuntu, checks repository links/JSON/encoding, and uploads synthetic demo evidence for seven days. A separate Ubuntu job builds the pinned upstream development source, exercises its AgentMesh wrapper and audits installed dependencies. Workflow results are available under [GitHub Actions](https://github.com/shibinantony/agt-architecture-lab/actions).

CI configuration is executable; use the run result for the commit being reviewed as evidence. Do not interpret a workflow file alone as a passed cross-platform test.

Observed publication gate: [run 34596282308](https://github.com/shibinantony/agt-architecture-lab/actions/runs/34596282308) passed all three jobs for commit `07ca7935d3e257aabc50386f54ec298cea73957d` on 2026-09-11. Windows and Ubuntu each passed all 30 tests and the demo. The separate Ubuntu job successfully built the pinned AGT source, checked its provenance, ran the four synthetic requests, passed `pip check`, and reported no known vulnerabilities with the strict isolated scanner. This validates the supplied AgentMesh wrapper cases, not native ACS execution or a provider-backed session.

## Publication review

The canonical repository is [shibinantony/agt-architecture-lab](https://github.com/shibinantony/agt-architecture-lab). The rename is reflected in repository links, clone instructions, the local Git remote and the decision schema identifier. Original code and documentation use the [MIT License](../LICENSE.md), with direct dependency attribution in [third-party notices](../THIRD-PARTY-NOTICES.md).

The publication pass repeats the runtime/MCP/schema tests, actual AGT example, dependency compatibility checks and documentation checks. `tests/check_links.py` checks local paths, heading fragments and contract references; `--external` separately checks HTTP reachability. A reachable link does not validate the linked claim.

Prepublication review includes all reachable Git commits, current tracked files and GitHub Actions logs/artifacts. Local environments, generated evidence, credentials/configuration and private conversation directories remain excluded from Git. Secret-pattern and dependency-advisory scans have bounded coverage and do not prove the absence of every possible vulnerability.

The local lab audit on 2026-09-11 checked 33 installed packages with pip-audit 2.10.1: zero skipped packages and no known vulnerabilities after updating pip and setuptools. The current upstream environment also passed its strict CI advisory scan, and GitHub reported zero open dependency alerts at this review. An installed-package scan checks package names/versions, not the source commit's code. The released upstream installation exposed cryptography advisories; it is no longer the documented installation path. The pinned-source choice and its native build requirement are explained in the [upstream example](../examples/upstream-agt/README.md).

## What has not been established

- An authenticated Codex or Gemini model session invoking the server end to end.
- Azure tenant inventory, deployment, enforcement, invoices or measured financial benefit.
- Native ACS execution or complete AGT component coverage.
- Enterprise identity, protected distributed budgets, signed audit storage, verified human approvals or production isolation.
- General resistance to every prompt-injection or alternate tool path.

The [architecture](architecture.md) and [roadmap](../ROADMAP.md) describe those additional gates. The lab YAML, released AgentMesh policy YAML and ACS manifests are distinct formats.

## Reproduce

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-bootstrap.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m lab demo
.\.venv\Scripts\python.exe tests/check_links.py
./tests/Test-Repository.ps1
```

Use `.venv/bin/python` on macOS/Linux. Follow the separate [upstream example](../examples/upstream-agt/README.md) for AGT, and the [client guide](cli-integration.md) for optional live acceptance tests.

### Dependency advisory scan

Run the scanner in a separate tools environment so its dependencies do not change the environments under test. From the repository root on Windows:

```powershell
py -3 -m venv artifacts/qa-venv
.\artifacts\qa-venv\Scripts\python.exe -m pip install -r requirements-bootstrap.txt
.\artifacts\qa-venv\Scripts\python.exe -m pip install -r requirements-audit.txt
.\artifacts\qa-venv\Scripts\python.exe -m pip_audit --path .venv/Lib/site-packages --strict
.\artifacts\qa-venv\Scripts\python.exe -m pip_audit --path .venv-agt/Lib/site-packages --strict
```

On Linux/macOS, use `python3` to create the environment and `artifacts/qa-venv/bin/python` to run the scanner. Get each target's installed-package directory with that environment's interpreter: `python -c "import sysconfig; print(sysconfig.get_path('purelib'))"`, then pass it to `--path`. The second scan requires the optional upstream environment to have been installed first. Scans require network access and send package names/versions to the advisory service. Do not silently suppress failures or skipped packages. Results are a dated inventory/advisory check, not a source-code security assessment or guarantee of future safety.
