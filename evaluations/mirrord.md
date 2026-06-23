# Evaluation: mirrord

**Repo:** [metalbear-co/mirrord](https://github.com/metalbear-co/mirrord)
**Stars:** 5,142 | **Last updated:** 2026-06-19 (pushed; created 2022-02-01) | **License:** MIT
**Dev loop stage:** Implement + Verify — gives the agent live cluster context while writing, then runs the change against real services to confirm it end-to-end
**Layer:** Infrastructure (Rust CLI + VS Code extension + IntelliJ plugin; bridges a local process into a Kubernetes pod)

---

## What it does

The catalog one-liner: "Runs your local process inside a live Kubernetes cluster — same for developers and for AI coding agents." mirrord intercepts a locally-running process and routes its **traffic, file reads, and environment variables through a target pod** in a live cluster. The code executes on your machine, but it sees the cluster's real env vars, real service responses, and real queue contents — so an agent both *writes* against what's actually deployed and *runs* the change against those same services without doing a deploy. It explicitly markets AI-coding-agent use (Claude Code, Cursor, Codex, Copilot, Windsurf) alongside human developers, and ships as a CLI, VS Code extension, and IntelliJ plugin.

The mechanism is a local layer (injected into the process) plus an agent pod in the cluster; mirrord uses your machine's default kubeconfig for cluster API access. "Steal" vs "mirror" modes control whether it diverts a pod's traffic or duplicates it, so it can run without disrupting the cluster for others.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No cluster, no kubeconfig, no process intercepted. Claims come from the repository (GitHub metadata, README, release count) and the project's documentation framing, not observed behavior. The adopter list (monday.com, SurveyMonkey, Cadence, …) is the project's self-reported `ADOPTERS.md`, not independently verified.

```bash
gh api repos/metalbear-co/mirrord --jq '{desc,stars:.stargazers_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id,lang:.language}'
gh api repos/metalbear-co/mirrord/readme --jq '.content' | base64 -d
gh api repos/metalbear-co/mirrord/releases --jq 'length'   # 30
```

## What worked

- **Solves a real grounding problem.** Agents normally write cloud-native code against mocks or stale assumptions; mirrord feeds them *live* env/services/data, which directly improves Correctness for Kubernetes-deployed services — a genuine dev-loop contribution, not just infra.
- **Covers both halves of the loop.** Live context while implementing + run-against-real-services to verify end-to-end, "feedback of a deploy in seconds without the deploy."
- **Genuinely mature.** Since 2022, MIT, 30 releases, active CI, multi-surface (CLI + VS Code + IntelliJ), and a real enterprise adopter list — far more established than most of this catalog.
- **Agent-aware by design.** First-class docs for driving it from coding agents, not a human-only tool retrofitted.
- **Non-disruptive modes.** Mirror-vs-steal lets it read cluster reality without hijacking a shared environment.

## What didn't work or surprised us

- **Kubernetes-only — narrow applicability.** If you don't develop against a live K8s cluster, mirrord is irrelevant. That bounds it to cloud-native teams.
- **Serious access/Safety surface.** It uses your default kubeconfig and routes a process's traffic/files/env through a real cluster pod. Handing that to an autonomous agent means the agent can read live secrets/data and (in steal mode) divert real traffic — a high-trust capability that needs scoped RBAC and care.
- **Open-core.** The OSS core is MIT, but the team (MetalBear) sells a paid "mirrord for Teams" (shared queues, policies, SSO); some collaboration/governance features sit behind that.
- **Not a coding agent.** It's an environment bridge the agent uses, not an agent itself — value depends entirely on the agent driving it correctly against live infra.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Grounding changes in real cluster env/services/data (not mocks) catches integration mismatches an agent would otherwise miss. |
| Speed | + | "Deploy-grade feedback in seconds without deploying" tightens the cloud-native iteration loop dramatically. |
| Maintainability | neutral | No effect on codebase structure; affects how changes are validated, not how they're organized. |
| Safety | − | Uses your kubeconfig and routes traffic/files/env through a live pod; giving an agent this reach exposes real secrets/data and can divert prod-like traffic — needs scoped RBAC. |
| Cost Efficiency | neutral | OSS core is free; team features are paid; avoids repeated deploy cycles. |

## Verdict

**CONDITIONAL** — adopt if you develop services that run on Kubernetes and want your agent (and you) to write and verify against live cluster reality instead of mocks; it's mature, multi-surface, and genuinely improves Correctness and Speed for that workflow. The blockers are scope (K8s-only) and a real Safety surface — an agent wielding your kubeconfig and live traffic needs scoped, read-mostly RBAC and human-gated steal mode. Out of scope for non-cloud-native projects.

Compared to neighbors: it's unlike the coding-agent harnesses (opencode/goose/jcode) — those *are* the agent; mirrord is the **live-environment bridge** they run inside, closest in spirit to the sandbox tools (sandboxd, vercel-sandbox) but inverted: instead of isolating agent code in a fresh sandbox, it connects local code into a *real* cluster. No current catalog entry covers live-cluster grounding, so it fills a distinct gap for the K8s niche.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mirrord](https://github.com/metalbear-co/mirrord) | tool | Runs a local process (or an AI agent's code) inside a live Kubernetes cluster — routes real traffic/files/env through a target pod for deploy-grade feedback without deploying; CLI + VS Code + IntelliJ | Agents write cloud-native code against mocks/stale assumptions; need live cluster context to implement and verify end-to-end | sandboxd, vercel-sandbox (sandbox isolation — mirrord is the inverse: connect to real infra); agent-browser (live-env verification) |
