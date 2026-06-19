# Evaluation: hive

**Repo:** [aden-hive/hive](https://github.com/aden-hive/hive)
**Stars:** 10,565 | **Last updated:** 2026-05-29 | **License:** Apache-2.0
**Dev loop stage:** Implement (a platform you build agent *products* with — not a stage of your own coding dev loop)
**Layer:** Infrastructure

---

## What it does

Catalog one-liner: "Multi-agent harness for production AI." Hive (the product is branded "OpenHive," by Y Combinator company Aden) is a self-hosted, model-agnostic Python platform for *building and operating multi-agent systems that automate business workflows*. You describe an outcome in natural language; a "queen" coding agent compiles a graph-based execution DAG of specialized worker agents, then a runtime executes them in parallel with persistent role-based memory, crash recovery, observability, budget/cost enforcement, and human-in-the-loop controls. On failure it can "evolve the graph" and redeploy.

The mechanism: it is a `uv` workspace (Python 3.11+), **not** a `pip install` library. `./quickstart.sh` provisions two virtualenvs — `framework` (core agent runtime + graph executor) and `aden_tools` (an MCP tool layer, badged "102 tools") — plus an encrypted credential store at `~/.hive/credentials`, an interactive LLM provider config (LiteLLM-compatible: Anthropic, OpenAI, Gemini, OpenRouter, Hive LLM, local models), and a **browser dashboard**. You then build agents through that web UI ("type the agent you want in the home input box"), run templates, or talk to the queen. The product surface is a runtime + control plane + dashboard, oriented at moving agents "from prototype to production" for business processes (CRM, support, data, internal APIs via MCP), explicitly contrasting itself with "single agents like Openclaw and Cowork" that "finish personal jobs."

## How we tested it

Repo/README/structure review via the GitHub API: metadata, full README, recursive file tree, the `.claude/` directory, `CLAUDE.md`/`AGENTS.md`, release/tag history, contributor count, and the open-issue stream. **Did not install or run it.** Running it meaningfully requires cloning the repo, running `quickstart.sh` to build the `uv` workspace and two venvs, configuring an LLM provider and credential store, and then driving an interactive browser dashboard to author and execute agent graphs — a stateful, long-running platform setup, not a scriptable one-shot. No throughput, "self-healing," or "evolves the graph" claims are verified here; those are the project's.

```bash
gh api repos/aden-hive/hive --jq '{stars,license,description,pushed_at,created_at,language,topics}'
gh api repos/aden-hive/hive/readme --jq '.content' | base64 -d
gh api "repos/aden-hive/hive/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # inspected .claude/, core/, tools/, docs/
gh api repos/aden-hive/hive/contributors --jq 'length'                          # 30
gh api repos/aden-hive/hive/releases --jq '.[0:5] | .[] | {tag: .tag_name, date: .published_at}'  # v0.11.0 .. v0.10.2
gh api "repos/aden-hive/hive/issues?state=open&per_page=5" --jq '.[].title'
gh api "repos/aden-hive/hive/contents/.claude/skills" --jq '.[].name'           # browser-edge-cases, test-reporting, triage-issue
# Catalog overlaps:
grep -inE "superpowers|agent-orchestrator|hive" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Genuinely mature and active.** 10.5K stars, 30 contributors, steady semver releases (v0.11.0, May 2026), Apache-2.0, YC-backed, created Jan 2026. Open issues are real-subsystem bug reports (checkpoint-store integrity validation, silent exception swallowing in `NodeWorker`, orchestrator payload spillover) — the signature of a system in actual use, not a demo.
- **The production-harness story is coherent and ambitious.** State persistence + crash recovery, a control plane with cost/budget enforcement and audit trails, session isolation, shared buffers, and failure-driven graph evolution are the right concerns for running long-lived agents in production. This is a real "harness around the model," not a thin wrapper.
- **Model- and system-agnostic.** LiteLLM-backed (100+ providers per the FAQ, including local/Ollama), and a large MCP tool layer for connecting to business systems. Swapping the underlying LLM is a config change.
- **Outcome-driven authoring.** "Describe the outcome, the queen builds the graph" is a genuinely different UX from hand-wiring agent chains, and the template gallery lowers the on-ramp.

## What didn't work or surprised us

- **It is a platform to build agent *products*, not a tool that improves your coding dev loop.** The entire framing is "move AI agents from prototype to production" to "execute real business processes" — automating *jobs* (the HoneyComb "stock market for jobs" tie-in makes the thesis explicit). You would use Hive to build something like a support-automation or data-pipeline agent, the same way you'd use aisuite or LangGraph — not to plan/implement/verify/review/ship your own code faster. This is the aisuite/LangGraph category, not the gastown/claude-squad category.
- **No Claude-Code-facing integration.** The `.claude/` directory and `CLAUDE.md`/`AGENTS.md` in the repo are for Hive's *own contributors* (skills are `browser-edge-cases`, `test-reporting`, `triage-issue` — Hive's internal test/QA tooling). There is no installable Claude Code plugin, user-facing skill, MCP server, or hook that you'd add to *your* repo to enhance Claude Code. The "harness" in the catalog title means an agent-runtime harness for products, not an agentic-coding harness.
- **Heavy, opinionated install with a non-standard layout.** Not `pip`-installable; you must clone and run `quickstart.sh` to build a `uv` workspace with two venvs, a credential store, and a browser dashboard. The interaction model is a web UI + a "queen" agent, not a CLI you script into a dev workflow.
- **Pre-1.0 and centered on a hosted ecosystem.** v0.x releases, docs and the dashboard point at adenhq.com / Hive LLM / HoneyComb. Self-hosting is supported, but the gravity is toward the vendor's platform.
- **Not validated hands-on here.** Self-healing, graph evolution, and crash recovery are claimed by the project, not observed.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | A runtime for building agent products; it doesn't make *your* code more correct. Its own checkpoint/exception-handling correctness is the subject of current open bugs. |
| Speed | neutral | Doesn't speed up your coding dev loop; it speeds up building/operating separate agent products. |
| Maintainability | neutral | No integration with your repo's dev workflow; lives outside the dev loop. |
| Safety | neutral | HITL controls, budget enforcement, and audit trails are well-aimed — but they govern the agent products you build with Hive, not your Claude Code sessions. |
| Cost Efficiency | neutral | Cost/budget enforcement applies to the workloads you run on Hive, not to your agent-assisted development spend. |

## Verdict

**SKIP**

Hive is a serious, actively developed, YC-backed platform for **building and operating production multi-agent systems that automate business processes** — and on those merits it is well-engineered (state persistence, crash recovery, observability, HITL, cost controls, model-agnostic via LiteLLM/MCP). But in this catalog's framework — tools that move quality signals inside *your* coding dev loop (Plan, Implement, Verify, Review, Ship, Reflect) — it has no surface area. It is not a Claude Code plugin/skill/MCP, it doesn't write/review/ship your code, and its purpose is to produce agent *products*, not to make agent-assisted development better. This is the same SKIP rationale as **aisuite**: an excellent building block for AI applications, but a building block, not a dev-loop tool.

**Distinguishing it from the gastown / claude-squad / dmux cluster (which it superficially resembles via "multi-agent harness"):**
- **gastown / claude-squad / dmux** orchestrate *coding agents* (Claude Code, Codex, etc.) against *your git repos* to help *you ship code* — worktree isolation, merge queues, agent cockpits. They are dev-loop tools (gastown is CONDITIONAL; dmux CONDITIONAL).
- **hive** orchestrates *worker agents* against *business systems* to *automate jobs/workflows*. The agents it coordinates are the product's runtime workers, not coding assistants working on your codebase. Different category entirely — it belongs with aisuite/LangGraph (agent-product frameworks), not the parallel-coding-agent cluster.

The catalog's listed overlaps (superpowers, agent-orchestrator) are misleading: those are coding-dev-loop tools, whereas Hive is an agent-product platform. The closest real catalog analog is **aisuite** (SKIP, same reason).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [hive](https://github.com/aden-hive/hive) | harness | Multi-agent harness for production AI | Need production-grade multi-agent orchestration | superpowers, agent-orchestrator |
