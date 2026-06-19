# Evaluation: fast-agent

**Repo:** [evalstate/fast-agent](https://github.com/evalstate/fast-agent)
**Stars:** 3,830 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Implement / Verify (CLI coding agent + agent/eval harness)
**Layer:** Tooling (the CLI agent) + Infrastructure (the Python framework)

---

## What it does

fast-agent is a CLI-first, MCP-native agent runtime that doubles as a Python framework for composing multi-agent workflows. Its own one-liner is telling: "a flexible way to interact with LLMs, excellent for use as a **Coding Agent**, **Development Toolkit**, **Evaluation** or **Workflow platform**." Unlike aisuite and LangGraph (pure libraries you import to build a product), fast-agent ships a runnable coding agent you drive from the terminal — `uvx fast-agent-mcp@latest -x` opens an interactive shell-enabled session, and `fast-agent --model opus -x --smart` runs it as a subagent-capable coding agent against Anthropic/OpenAI/Google/Ollama/dozens-of-others.

The mechanism has two faces. (1) **As a coding agent**: a prompt_toolkit TUI with shell mode (`!` or `! npm run build`), slash commands (`/skills`, `/connect`), SKILL.md (Agent Skills) support, MCP server connection over stdio/streamable-HTTP with OAuth (PKCE + OS keychain via `keyring`), and "card packs" (`--pack codex`, `--pack hf-dev`, `--pack analyst`) that preconfigure it for a coding task. It exposes an ACP server (`fast-agent-acp`) so it runs inside any ACP client (e.g. Toad), and any agent can itself be exposed as an MCP server (`--transport http`). (2) **As a framework**: a declarative decorator API (`@fast.agent`, `@fast.chain`, `@fast.parallel`, `@fast.router`, `@fast.orchestrator`, `@fast.evaluator_optimizer`, `@fast.maker`) for building the "Building Effective Agents" patterns with minimal boilerplate, claiming first-complete end-to-end MCP feature coverage including Sampling and Elicitations. The author (evalstate / llmindset) is a recognized contributor in the MCP ecosystem.

## How we tested it

Inspected the GitHub repo via the API: README (711 lines), repo tree, `AGENTS.md`, `examples/` directory (a2a, acp, function-tools, harness-api, tool-runner-hooks, workflows, workflows-md, etc.), `docs/`, and release history. Did NOT install or run it — this is an architecture/surface-area review to decide catalog placement, applying the same lens used for the aisuite and LangGraph SKIP evaluations. No metrics below are measured; all claims are sourced from the repo.

```bash
gh api repos/evalstate/fast-agent --jq '{stars,license,description,pushed_at,language,forks,open_issues,homepage}'
gh api repos/evalstate/fast-agent/readme --jq '.content' | base64 -d   # 711-line README
gh api repos/evalstate/fast-agent/contents --jq '.[].name'
gh api repos/evalstate/fast-agent/contents/examples --jq '.[].name'
gh api repos/evalstate/fast-agent/contents/AGENTS.md --jq '.content' | base64 -d
gh api repos/evalstate/fast-agent/releases --jq '.[0:3][] | {tag,date}'  # v0.7.17, 2026-06-10
```

Reviewed: the coding-agent invocation paths (`-x` shell mode, `--smart`, `--pack codex/hf-dev`, `/skills`, `/connect`), SKILL.md / Agent Skills support, the ACP server (`fast-agent-acp`, `src/fast_agent/acp/`), the MCP OAuth + ping config, and the full decorator-based workflow API. PyPI package is `fast-agent-mcp`; actively released (v0.7.x cadence, pushed same day as review).

## What worked

- **It is itself a usable coding agent**, not just a library — `fast-agent --model opus -x --smart` gives a terminal coding agent with shell access, skills, and MCP connectivity. This is the dimension aisuite/LangGraph lack, and it puts fast-agent squarely in the dev loop (Implement) as an alternative/complement to Claude Code, Codex, or Aider.
- **Best-in-class MCP coverage** — claims first complete end-to-end MCP feature support (Sampling, Elicitations, Roots, MCP-UI, OpenAI Apps SDK / Skybridge), plus the only tool that inspects Streamable HTTP transport usage. OAuth is real (PKCE, keyring, no tokens on disk by default).
- **Honors SKILL.md and ACP** — the same Agent Skills you author for Claude Code load here, and ACP support means it slots into editor/agent clients without bespoke glue. Strong interop story.
- **Provider-agnostic with first-class Anthropic support** — native Anthropic/OpenAI/Google, plus Azure/Ollama/Deepseek/dozens via TensorZero; model query overrides (`?reasoning=low`, `?context=1m`, `?web_search=on`) are convenient for testing model↔MCP behavior. Lets you run the same coding/eval task across models for cost/quality comparison.
- **Evaluation/workflow primitives are dev-loop-relevant** — `@fast.evaluator_optimizer` (generate→judge→refine loop) and MAKER (k-voting error reduction) are genuinely useful for Verify-stage harnesses and for building repeatable model evals, which is a stated catalog use case ("Evaluate agents").

## What didn't work or surprised us

- **Dual identity creates adoption ambiguity** — it is simultaneously a coding agent AND a framework for building agents. The framework half (decorators, workflows) is the same "build AI apps" category as aisuite/LangGraph and on its own would be SKIP for this catalog. Only the coding-agent/dev-toolkit half earns it a place.
- **No Claude Code plugin/skill/MCP-server integration of its own** — it consumes SKILL.md and speaks MCP/ACP, but there is no `fast-agent` plugin you add to Claude Code. It is a *parallel* agent runtime, not an enhancement to Claude Code. Adopting it means running a second agent, not extending your current one.
- **Smaller and younger than the libraries it competes with** — 3.8K stars vs aisuite 14.7K / LangGraph 35K. Fast-moving (v0.7.x, frequent releases) but pre-1.0; APIs and packs are still churning.
- **Python/uv-centric** — install and per-agent config live in `fast-agent.yaml` + `uv`; not a drop-in for non-Python shops, and the framework boilerplate (asyncio, decorators) is real even if minimal.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Evaluator-optimizer and MAKER (k-voting) reduce agent error rates; can build repeatable evals to catch regressions |
| Speed | + | CLI coding agent with shell mode lets you implement directly in-terminal; card packs preconfigure common coding setups |
| Maintainability | neutral | As a coding agent it edits your code like any agent; the framework half adds a dependency only if you build on it |
| Safety | + | MCP OAuth (PKCE, keyring, no on-disk tokens), per-server auth control, and transport diagnostics are stronger than most agent runtimes |
| Cost Efficiency | + | Provider-agnostic model strings let you run the same task on cheaper models and compare; local models via Ollama/llama.cpp |

## Verdict

**CONDITIONAL**

fast-agent clears the bar that aisuite and LangGraph did not: it is not merely a library for building AI products — it ships a runnable, MCP-native, SKILL.md/ACP-aware **coding agent and evaluation toolkit** you drive from the terminal (`fast-agent --model opus -x --smart`), which lands directly in the Implement and Verify stages of the dev loop. That is a real dev-loop surface, so it does not get the SKIP that the pure frameworks received.

It is CONDITIONAL rather than ADOPT because (a) it is a *parallel* agent runtime, not an enhancement to your existing Claude Code setup (no plugin/skill of its own), so adopting it means running a second agent; and (b) its other half is a general agent-building framework that, in isolation, is out of catalog scope. **Adopt it when** you want a provider-agnostic, MCP-first coding agent or a lightweight harness to build/run model-vs-model and evaluator-optimizer **evaluations** — especially if you live outside the Anthropic-only Claude Code path or need deep MCP transport/OAuth control. If your workflow is fully inside Claude Code and you only need MCP servers and skills, the marginal benefit is smaller.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [fast-agent](https://github.com/evalstate/fast-agent) | framework | MCP-native CLI coding agent and framework to build, run, and evaluate agents with broad model/skill/MCP/ACP support | Want a provider-agnostic coding agent and lightweight harness to compose and evaluate MCP-based agents | aisuite, LangGraph (agent-building frameworks); Claude Code / Codex / Aider (CLI coding agents) |
