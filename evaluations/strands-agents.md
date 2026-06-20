# Evaluation: Strands Agents (harness-sdk)

**Repo:** [strands-agents/harness-sdk](https://github.com/strands-agents/harness-sdk)
**Stars:** 6,218 | **Last updated:** 2026-06-20 (pushed) | **License:** Apache-2.0 | **Language:** Python + TypeScript (PyPI: `strands-agents`; npm: `@strands-agents/sdk`)
**Dev loop stage:** Agent Harnesses (agent-building SDK) — Implement
**Layer:** Infrastructure (SDK/framework for building production agents)

---

## What it does

Strands Agents is **a model-driven SDK for building and running AI agents** — "build an agent harness, control it end-to-end." A monorepo with Python and TypeScript SDKs (agent loop, model providers, tools), WASM bindings (run Python tools from TS agents), a `strandly` developer CLI, and docs. Pitch: **any model, any cloud** — first-class Amazon Bedrock, Anthropic, OpenAI, Gemini (plus more/custom providers) — with **context management, execution limits, and observability built in before you write config**, and "swap backends when you scale; your code stays the same." Control features: the **agent loop traces every decision by default**; **hooks** intercept any step to log/validate/redirect; **guardrails** catch mistakes before they run; **steering handlers** let agents self-correct instead of failing silently. MCP, streaming, multi-agent patterns, and structured output are built in. Quick start: `pip install strands-agents strands-agents-tools` (defaults to Bedrock; other providers documented).

## How we tested it

**Source-grounded inspection — not installed, not run.** No agent built with the SDK, no provider configured.

```bash
gh api repos/strands-agents/harness-sdk --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 6218, Apache-2.0, pushed 2026-06-20
gh api repos/strands-agents/harness-sdk/readme --jq '.content' | base64 -d | head -75               # SDKs, model-driven, hooks/guardrails/steering
```

## What worked

- **"Harness you control," not a black-box framework.** Tracing every decision by default, plus hooks to intercept/validate/redirect any step, is exactly the controllability 12-factor-agents argues for — closer to "own your control flow" than crew/langchain-style magic.
- **Genuinely multi-language + multi-cloud.** Parallel Python and TS SDKs with a shared model-provider abstraction (Bedrock/Anthropic/OpenAI/Gemini/custom) is rare and valuable for polyglot teams.
- **Guardrails + steering as first-class.** Catching mistakes before execution and letting agents self-correct (vs. silent failure) are production concerns most SDKs leave to you.
- **Batteries included.** MCP, streaming, multi-agent, structured output, execution limits, observability built in — less stitching.
- **Credible backing + traction.** Apache-2.0, 6.2K stars, active (pushed same day), WASM cross-language interop signals real engineering investment.

## What didn't work or surprised us

- **It builds agents; it isn't a coding agent.** This is an SDK for *developers building agentic applications*, not a drop-in coding harness like Claude Code/letta-code — relevant to the catalog as infrastructure, not an install-and-code tool.
- **Bedrock-default, AWS-leaning.** Defaults to Amazon Bedrock (needs AWS creds + model access); other providers are supported but the gravity is AWS/Strands.
- **SDK = you write the software.** The payoff requires building and operating your agent; it's a foundation, not a finished workflow.
- **Crowded SDK space.** Competes with the Claude/OpenAI Agent SDKs, mcp-use, and framework incumbents; the wedge is end-to-end control + dual-language + built-in guardrails.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Guardrails catch mistakes pre-execution; steering enables self-correction; tracing aids debugging. |
| Speed | neutral | Faster to a controllable production agent than rolling your own loop; still real development. |
| Maintainability | + | Backend swaps without code changes, full decision tracing, hooks — testable, observable agents. |
| Safety | + | Guardrails, execution limits, and intercept hooks are built-in safety surfaces. |
| Cost Efficiency | neutral | Apache-2.0/free SDK; inference/cloud cost is yours; context management can reduce token waste. |

## Verdict

**CONDITIONAL** — Strands Agents is a serious, Apache-2.0 **model-driven SDK for building production agent harnesses** with the controllability (decision tracing, intercept hooks, guardrails, steering, execution limits) that reliable agentic software demands — dual Python/TS, any-model/any-cloud. Adopt it when you're *building an agentic application or a custom harness* and want end-to-end control plus built-in observability and guardrails, rather than a finished coding agent. It's infrastructure: the value is realized by writing and operating your agent, with AWS/Bedrock as the path of least resistance. For "I just want to code with an agent," a ready harness (Claude Code, letta-code, oh-my-pi) fits better; Strands is for when *you* are the one building the agent.

Compared to neighbors: **mcp-use**/**fastmcp** build MCP servers/clients; **ruflo** is a meta-harness; **phantom** is a standing agent on the Claude Agent SDK. Strands' distinguishing pitch is **a dual-language, any-cloud SDK to build an agent harness you trace and control end-to-end.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [strands-agents (harness-sdk)](https://github.com/strands-agents/harness-sdk) | framework | Model-driven agent SDK (Apache-2.0, Python + TS) — build and control an agent harness end-to-end: agent loop, any model/cloud (Bedrock/Anthropic/OpenAI/Gemini), built-in context management, execution limits, hooks/steering, guardrails, MCP, and multi-agent patterns | Building production agents means hand-stitching the loop, providers, observability, and guardrails; want a controllable SDK that scales local→prod without rewrites | fastmcp, mcp-use, ruflo, phantom |
