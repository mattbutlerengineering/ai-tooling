# Evaluation: omnigent

**Repo:** [omnigent-ai/omnigent](https://github.com/omnigent-ai/omnigent)
**Stars:** 3,985 | **Last updated:** 2026-06-19 (v0.2.0, status: alpha) | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan + Implement + Verify + Review + Ship (a meta-harness orchestration layer)
**Layer:** Infrastructure (the orchestration server/runtime + sandbox + policy engine) + Tooling (the `omnigent`/`omni` CLI and the agents you run)

---

## What it does

Catalog one-liner: "Meta-harness: orchestrate Claude Code, Codex, Cursor [and other agents]." Ground truth: Omnigent is an Apache-2.0 Python (3.12+) **meta-harness** — a common orchestration layer that sits *above* individual coding harnesses (Claude Code, Codex, Cursor, Pi, OpenAI Agents SDK, Antigravity, Databricks) so you can swap or combine them without rewriting your agent. The core mechanism: you `omnigent run path/to/agent.yaml`, where the YAML declares a prompt, an `executor.harness` (e.g. `claude-sdk`, `claude-native`, `codex`, `cursor`, `pi`, `openai-agents`, `antigravity`), tools (local Python functions and/or sub-agents), and optional governance policies. Omnigent spawns the chosen harness in a sandboxed terminal, exposes a shared session over a local server + web UI (`http://localhost:6767`), and lets that session be observed, co-driven, forked, or continued from any device including a phone.

It is explicitly framed around *your* dev loop, not around building an AI product for end users. The flagship example is **Polly**, a multi-agent coding orchestrator whose `claude-sdk` "brain" writes no code itself: it plans, delegates implement/explore/review tasks to `claude_code` / `codex` / `pi` sub-agents each in its own git worktree, routes each diff to a **different-vendor** reviewer, and each implementer opens its own PR for the human to merge (it never merges). A second example, **Debby**, fans every prompt to a Claude head and a GPT head side by side with a `/debate` mode. Beyond the CLI, Omnigent ships: per-session OS sandboxing (macOS seatbelt, Linux bubblewrap, plus cloud sandboxes via Modal/Daytona/Islo), a layered **policy** engine (server/agent/session-scoped) for spend caps, tool-call limits, and ask-before-risky-action gates, multi-user accounts with OIDC + invite links, real-time session sharing/co-drive/fork, and a Docker/Render/Fly/Railway deploy path so a server can host sessions and provision cloud sandboxes per session (*managed hosts*).

## How we tested it

**Evidence:** REVIEW

**Method: inspected the GitHub repo, full README, file tree, harness adapter modules, and the Polly orchestrator config + skills via the GitHub API and PyPI stats. Did NOT install or run it.** This is a deliberate non-install architecture/surface-area review to decide catalog placement, applying the same lens used for sandcastle (CONDITIONAL) and oh-my-openagent (SKIP). Installing would mean adding a Python server runtime, Node 22, tmux, and (on Linux) bubblewrap, plus standing up the web UI — out of scope for a placement call. No metrics below are measured by us; star/download/contributor counts are live API calls, and any performance claims would be the project's own (the README makes none of substance).

```bash
gh api repos/omnigent-ai/omnigent --jq '{stars,license,description,pushed_at,created_at,topics}'
# 3,985 stars; Apache-2.0; created 2026-06-11; pushed 2026-06-19; topics include claude-code, multi-agent, sandbox, agent-governance
gh api repos/omnigent-ai/omnigent/readme --jq '.content' | base64 -d            # full README
gh api "repos/omnigent-ai/omnigent/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # omnigent/inner/*_harness.py, examples/, deploy/, ap-web/
gh api repos/omnigent-ai/omnigent/contributors --paginate --jq '.[].login' | wc -l # 50
gh api repos/omnigent-ai/omnigent/languages                                       # ~25MB Python, ~5MB TypeScript (web UI)
curl -s https://pypistats.org/api/packages/omnigent/recent                        # ~15.7k downloads/month
gh api repos/omnigent-ai/omnigent/contents/omnigent/inner/claude_sdk_harness.py   # Claude Agent SDK wrap
gh api repos/omnigent-ai/omnigent/contents/examples/polly/config.yaml             # Polly orchestrator spec + policies
```

Reviewed: the harness adapter set (`claude_sdk`, `claude_native`, `codex`, `codex_native`, `cursor`, `cursor_native`, `pi`, `pi_native`, `openai_agents_sdk`, `antigravity`, `databricks` executors/harnesses under `omnigent/inner/`); the per-harness e2e test suite (`tests/e2e/omnigent/test_per_harness_*.py` with recorded snapshots for claude_sdk/codex/pi); the Agent YAML spec, POLICIES doc, and deploy guide; the Polly config (cross-vendor review, blast-radius / spawn-bounds / purpose-guard policies, per-turn dispatch caps) and its `investigate`/`fanout`/`cross-review` skills; the Debby `/debate` example.

## What worked

- **It is a dev-loop tool you run *against your repo*, not a library you import to build an app.** Polly produces git worktrees, diffs, cross-reviewed PRs you merge — squarely Plan/Implement/Verify/Review/Ship. This clears the bar that earned aisuite a SKIP, the same way sandcastle did.
- **Genuinely a meta-harness, and the Claude Code integration is first-class twice over.** There are *two* Claude paths: `claude-native` (wraps the real `claude` CLI in a tmux + OS-sandbox terminal a human can open and take over) and `claude-sdk` (drives the Claude Agent SDK programmatically, with model/gateway/permission-mode/cwd env config). Polly's orchestrator brain runs on `claude-sdk` and defaults to `claude-opus-4-8`. Per-harness e2e snapshot tests exist for claude_sdk specifically — this is real, tested CC support, not aspirational.
- **Cross-vendor review as a built-in pattern.** Polly enforces that a `claude_code` PR is reviewed by `codex` or `pi` and vice versa, handing the reviewer only the diff + acceptance contract (never the worktree, so stray reviewer edits can't reach the deliverable). This encodes the "don't trust the builder's green" discipline at the orchestration layer.
- **Governance is a real subsystem, not a checkbox.** Layered policies (server/agent/session) with builtins for spend caps (`max_cost_usd` + soft warning thresholds), per-session tool-call limits, and ask-on-OS-tools gates; Polly adds a `blast_radius` policy with a catastrophic DENY set (force-push, `rm -rf /`, hard-reset) and `spawn_bounds` capping fan-out per turn. Stricter session rules are checked first.
- **Per-session OS sandboxing built in.** macOS seatbelt, Linux bubblewrap (mandatory there), and disposable cloud sandboxes (Modal/Daytona/Islo) — the right shape for autonomous agents, comparable to sandcastle's Docker/Podman/Vercel isolation but provided by the runtime rather than hand-wired.
- **Provider-agnostic and anti-lock-in.** API key, Claude/ChatGPT subscription, any OpenAI/Anthropic-compatible gateway (OpenRouter, LiteLLM, Ollama, vLLM, Azure), or Databricks — all first-class; `/model` swaps mid-session. Aligns with Cost Efficiency for users not on a single subscription.

## What didn't work or surprised us

- **It is a *parallel* orchestration runtime, not a Claude Code extension.** There is no Omnigent plugin/skill/MCP/hook you add to an existing Claude Code session. Adopting it means running a separate server + web UI that *invokes* Claude Code as one of several harnesses — the same caveat sandcastle and fast-agent carry. (Its `.claude/skills/` are for the project's own dev, not artifacts you install into your CC.)
- **Status: alpha, v0.2.0, ~8 days old at review.** Created 2026-06-11, single release. ~50 contributors and ~15.7k PyPI downloads/month is a credible start, but this is far less battle-tested than sandcastle (v0.10, ADR-backed) — expect API/config churn. The `claude_sdk_harness` docstring already flags a documented "V1 config-flow limitation" (env-var config, single-config-per-process).
- **Heavy install + infra footprint.** Python 3.12+, `uv`, Node 22 LTS, tmux, and (Linux) bubblewrap just for the native wrappers; a full deployment adds a server, DB, web UI, optional OIDC, and cloud-sandbox providers. This is a platform you operate, not a one-line CLI tool — markedly heavier than claude-squad/dmux.
- **You own the agent YAML and orchestration logic.** Power comes from authoring agent specs (prompts, sub-agent rosters, policies). Polly's prompt alone is a multi-page, carefully-tuned orchestration contract — real authoring/maintenance work, like sandcastle's bespoke TypeScript `main.ts`.
- **Broad surface = more to learn and trust.** Servers, hosts, managed hosts, sessions, sub-agents, terminals, policies, sandboxes, multi-user/OIDC, collaboration — a large concept count for the marginal benefit over running a single CC session.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Cross-vendor review (different-vendor reviewer on every PR) + delegated independent verification target "ship unmergeable green"; per-harness e2e tests back the integration |
| Speed | + | Parallel sub-agents in separate git worktrees with inbox-driven (non-polling) supervision; fan-out skill runs independent tasks concurrently |
| Maintainability | neutral | Agents edit your repo like any agent and each opens a normal PR you merge; offset by owning tuned agent YAML/policies and operating a server runtime |
| Safety | + | Per-session OS sandboxing (seatbelt/bwrap/cloud), layered spend/tool/blast-radius policies with ask-before-risky-action and a catastrophic DENY set, spawn caps |
| Cost Efficiency | + | Provider-agnostic credentials let you route cheap models to explores/fan-outs and strong models to hard work; builtin cost-budget policy with hard cap + soft thresholds |

## Verdict

**CONDITIONAL**

Omnigent clears the bar aisuite/oh-my-openagent did not: it is a harness you run *against your own repo* to orchestrate sandboxed coding agents that produce cross-reviewed PRs you merge — landing across Plan, Implement, Verify, Review, and Ship. Its meta-harness claim is real (ten+ executor adapters under `omnigent/inner/`, per-harness e2e tests), and its Claude Code integration is first-class on two paths (`claude-native` CLI wrap + `claude-sdk`, the default Polly brain on `claude-opus-4-8`). The governance subsystem (layered spend/tool/blast-radius policies) and per-session OS sandboxing are genuine differentiators, and it is Apache-2.0 — properly open source, unlike oh-my-openagent's SUL-1.0.

It is CONDITIONAL rather than ADOPT because (a) it is a *parallel* orchestration runtime, not an enhancement to your interactive Claude Code setup — there is no plugin/skill to install; (b) adopting it well means authoring and maintaining tuned agent YAML + policies and **operating a server/UI/sandbox platform** (Python, Node, tmux, bubblewrap, optional cloud sandboxes); and (c) it is **alpha, v0.2.0, ~8 days old** — promising but unproven, with documented V1 limitations and likely churn. **Adopt it when** you want a governed, sandboxed, multi-vendor orchestrator with cross-vendor PR review and phone/web/team collaboration, and you can run the server and tolerate alpha churn.

**Differentiation:** vs **sandcastle** (CONDITIONAL) — both run sandboxed coding agents against your repo with git output, but sandcastle is a programmatic *TypeScript library* you script (`run()`/`createSandbox()`), while Omnigent is a *Python platform + server + web UI* with a YAML agent spec, a policy/governance engine, and multi-user real-time collaboration; sandcastle is leaner and more mature, Omnigent is broader and governance/collaboration-first. vs **claude-squad / dmux** (terminal multi-session managers) — those are lightweight TUIs that juggle several local CC/agent sessions; Omnigent is a far heavier platform that adds cross-vendor orchestration, sandboxing, policies, cloud hosts, and remote/phone access. vs **gastown** (multi-agent workspace manager) — similar parallel-worktree shape, but Omnigent's distinctive pieces are the meta-harness abstraction (swap harnesses via one YAML field) and the governance/policy + managed-cloud-host layer. vs **oh-my-openagent** (SKIP — alternative harness on OpenCode/Codex, not CC) — Omnigent is the inverse: it *consumes* Claude Code (and others) as harnesses rather than replacing the front-end, so it extends rather than supplants the CC dev loop.

Re-evaluate toward ADOPT if it reaches a stable (1.0-ish) release with the V1 config-flow limitations resolved and a track record of reliability, or if a team specifically needs the governed multi-vendor + remote-collaboration story.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [omnigent](https://github.com/omnigent-ai/omnigent) | framework | Meta-harness: orchestrate Claude Code, Codex, Cursor, Pi, and custom agents under one governed, sandboxed layer | Want to swap/combine coding harnesses without rewriting, with policies, sandboxing, and team/remote collaboration | sandcastle, claude-squad, gastown |
