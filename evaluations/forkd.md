# Evaluation: forkd

**Repo:** [deeplethe/forkd](https://github.com/deeplethe/forkd)
**Stars:** 2,650 | **Last updated:** 2026-06-14 | **License:** Apache-2.0
**Dev loop stage:** Implement / Verify (parallel-agent and code-interpreter sandbox infrastructure)
**Layer:** Infrastructure

---

## What it does

forkd is a microVM sandbox runtime for AI-agent fan-out — its own one-liner is "Fork() for AI agent microVMs. Spawn 100 children in ~100ms from a warm parent; BRANCH a live VM in ~150ms. KVM-isolated, snapshot CoW." It is a Rust daemon (`forkd-controller`) built on a vendored fork of Firecracker. A parent VM boots once, imports your runtime (Python + deps, a JIT-warmed JVM, a loaded ML model) and is paused to disk; each child is a separate Firecracker process that `mmap`s the parent's memory image `MAP_PRIVATE`, so the kernel gives copy-on-write at the page level. The result is per-child KVM isolation with a spawn cost the project claims is closer to `fork(2)` than to a cold-boot VM.

The mechanism has two headline operations. (1) **fork** — fan out N children from a warmed snapshot; the warmed parent collapses the per-request `import numpy`/`import torch` cost across the whole cohort. (2) **BRANCH** — pause a *running* sandbox, snapshot its in-flight state, and resume, so an agent can fork "mid-thought" and N children inherit the source's exact reasoning + filesystem state then diverge under CoW. v0.4 adds a "live" BRANCH with a fire-and-forget mode; v0.5 adds stacked diff-snapshot chains (layer `pip install numpy`, `pandas`, `sklearn` as content-hashed edges). It surfaces through a REST API, a CLI (`forkd fork`, `forkd snapshot`), Python and TypeScript SDKs (the Python SDK is pitched as a drop-in for `from e2b import Sandbox`), and an MCP server (`forkd-mcp`). Operability is real for infra: daemon owns state, Prometheus `/metrics`, append-only JSON audit log, systemd unit. Requires Linux ≥ 5.7, `vm.unprivileged_userfaultfd=1`, and the vendored Firecracker fork.

## How we tested it

Inspected the GitHub repo via the API on 2026-06-19: README (full), repo tree, release history, the recipes directory, and crucially the `sdk/mcp/` MCP-server README and tool table. Did NOT install or run forkd — it requires a Linux host with KVM, an unprivileged-userfaultfd sysctl, and a custom-built Firecracker fork, none of which is available on the macOS evaluation machine. This is an architecture/surface-area review to decide catalog placement, using the same lens applied to the aisuite (SKIP) and fast-agent (CONDITIONAL) calibration evals. No metrics below are measured by us; every timing/benchmark figure is reported as the project's own claim.

```bash
gh api repos/deeplethe/forkd --jq '{stars,license,description,pushed_at,language,topics}'
gh api repos/deeplethe/forkd/readme --jq '.content' | base64 -d           # full README
gh api repos/deeplethe/forkd/contents --jq '.[].name'                     # tree
gh api repos/deeplethe/forkd/releases --jq '.[0:3][] | {tag,date}'        # v0.5.2 (2026-06-08)
gh api repos/deeplethe/forkd/contents/sdk --jq '.[].name'                 # mcp, python, typescript
gh api repos/deeplethe/forkd/contents/recipes --jq '.[].name'            # 18 framework recipes
gh api repos/deeplethe/forkd/contents/sdk/mcp/README.md --jq '.content' | base64 -d  # MCP tool table
```

Reviewed: the fork/BRANCH mechanism and CoW design, the benchmark table (forkd 101 ms vs Firecracker cold-boot 759 ms vs Docker 335 s for N=100, per project), the recipes for LangGraph/AutoGen/CrewAI/OpenAI-Swarm/E2B/Playwright/Jupyter/Postgres, and the `forkd-mcp` server which exposes ~12 tools (`spawn_sandboxes`, `branch_sandbox`, `exec_command`, `eval_code`, `kill_sandbox`, etc.) with documented `claude mcp add forkd ...` registration.

## What worked

- **It ships a real MCP server with first-class Claude Code registration.** `sdk/mcp/` documents `claude mcp add forkd ... -- forkd-mcp` and exposes ~12 tools (`spawn_sandboxes`, `branch_sandbox`, `exec_command`, `eval_code`, etc.). This is the dimension aisuite lacked entirely — forkd has an actual surface inside Claude Code, so an agent can spin up isolated microVMs as tools, not just a library you build a product against.
- **BRANCH (fork mid-execution) is a genuinely differentiated capability.** Pausing a running sandbox and fanning out N children that inherit exact reasoning + filesystem state — the README's coding-agent recipe travels a 50 MiB binary blob byte-identically across 4 sandboxes through one BRANCH. The project frames this as the open-source equivalent of Modal's proprietary feature; it maps cleanly onto speculative/parallel agent exploration ("try three fixes from the same warm state").
- **Strong, transparent benchmarking discipline.** The repo publishes raw RESULTS files per version, names a slow-path regression it fixed (#146, 150 ms → 2.7 s → flat), and documents a fair-comparison correction to a competitor's numbers (CubeSandbox #235). This is unusually honest for a perf-claim-heavy project and raises confidence the headline figures are real claims, not marketing.
- **Real Linux per child with hardware isolation.** Each child is its own Firecracker/KVM microVM with multi-vCPU, full TCP networking, and `apt install` — stronger isolation than worktree- or container-based agent sandboxes (dmux/worktrunk use git worktrees; nanoclaw/sandcastle are lighter). Escape requires a hypervisor/kernel vuln, not a `runc` regression.
- **Drop-in compatibility and broad recipe coverage.** Python SDK aims to be a drop-in for E2B's `Sandbox`; 18 recipes cover the major agent frameworks. Low switching cost for teams already on E2B-style sandboxes.

## What didn't work or surprised us

- **It is infrastructure for building agent platforms, not a tool that runs in your dev loop.** Like aisuite, forkd's center of gravity is "give your agent platform fast isolated sandboxes." The MCP server is a real Claude Code surface, but the value lands only if your workflow actually fans out many short-lived sandboxes (code-interpreter, eval rollouts, parallel-fix exploration). For ordinary Plan/Implement/Verify/Review/Ship coding it does nothing.
- **Hard Linux/KVM-only prerequisites.** Requires Linux ≥ 5.7, `vm.unprivileged_userfaultfd=1` (or `CAP_SYS_PTRACE`), root/`sudo -E` for the CLI fork path, and a *vendored Firecracker fork* you must build. It cannot run on macOS at all, and the MCP server needs the daemon reachable locally. This is a server-side deployment, not a `brew install`.
- **Young and pre-1.0 with composition gaps the README itself flags.** Latest release v0.5.2 (repo created 2026-05-11 — about five weeks old at review). The README openly notes "the two paths don't compose yet — daemon-side spawn from the CLI is the next gap (#209)" and queues optimizations for v0.6. APIs are still churning.
- **The chain-spawn perf story is more nuanced than the headline.** The 101 ms figure is fork-from-warm; v0.5 diff-chain spawn is reported at 751 ms (1 layer) to 1668 ms (3 layers) because of per-link SHA-256 verification (~460 ms/512 MiB). Fast for what it is, but not the "100 ms" number for the chained-dependency use case.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't write or check code; isolation prevents cross-run contamination in fan-out evals but doesn't move correctness of your own code |
| Speed | + | Only if you fan out: claimed 101 ms for 100 warm children vs 759 ms (Firecracker cold) / 335 s (Docker) at N=100 — collapses warm-up cost across a cohort |
| Maintainability | neutral | An infra dependency (daemon + custom Firecracker fork); affects platform ops, not codebase maintainability |
| Safety | + | Per-child KVM/hardware isolation, per-child netns + cgroup v2 limits, append-only audit log — stronger sandbox safety than worktree/container approaches |
| Cost Efficiency | + | Claimed 0.12 MiB host memory delta per sandbox via CoW page sharing vs 5–84 MiB for cold-boot alternatives — meaningfully cheaper at fan-out scale |

## Verdict

**CONDITIONAL**

forkd clears the bar aisuite did not: it ships a real MCP server with documented `claude mcp add forkd` registration, so it has an actual surface inside the dev loop rather than being a pure build-a-product library. Its BRANCH-mid-execution capability is genuinely differentiated for parallel/speculative agent exploration and code-interpreter fan-out, and its benchmarking discipline (published RESULTS files, self-reported regressions, fair-comparison corrections) is unusually credible. But it remains low-level infrastructure with a narrow trigger and hard prerequisites — Linux/KVM-only, a vendored Firecracker fork to build, root for the daemon, and zero value unless your workflow actually fans out many short-lived isolated sandboxes.

**Adopt it when** you are building or operating an agent platform that needs fast, hardware-isolated, warm-state-inheriting sandboxes at scale — code-interpreter tools, evaluation rollouts, or BRANCH-based "try N fixes from one warm state" parallelism on a Linux host. **Skip it for** ordinary single-agent Claude Code coding on macOS or any workflow that doesn't fan out — the setup cost dwarfs the benefit. It is the heavier, hardware-isolated end of the same space as dmux/worktrunk (worktree isolation), nanoclaw, and sandcastle (lighter sandbox orchestration).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [forkd](https://github.com/deeplethe/forkd) | tool | Fork() for AI agent microVMs — spawn 100 children in ~100ms from a warm parent with KVM isolation | Need fast, isolated agent sandboxes for parallel work without container overhead | nanoclaw, sandcastle, sandboxd; dmux/worktrunk (lighter worktree isolation) |
