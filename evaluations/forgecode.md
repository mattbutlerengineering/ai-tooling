# Evaluation: Forge (forgecode)

**Repo:** [tailcallhq/forgecode](https://github.com/tailcallhq/forgecode)
**Stars:** 7,423 | **Last updated:** 2026-06-19 (pushed) | **License:** Apache-2.0 | **Language:** Rust (by Tailcall)
**Dev loop stage:** Agent Harnesses / Implement — terminal AI pair programmer
**Layer:** Tooling (CLI coding agent)

---

## What it does

Forge (forgecode) is **an AI-enabled terminal pair programmer that is model-agnostic** across Claude, GPT, the O-series, Grok, DeepSeek, and more. It runs in the shell as a coding agent for refactoring, debugging, and feature work, with **MCP support**, custom workflows/agents, and shell-native operation. The pitch is one interactive multi-model pair-programming CLI rather than a vendor-locked agent, BYO provider keys.

## How we tested it

**Source-grounded inspection — not installed, not run.** No pairing session run.

```bash
gh api repos/tailcallhq/forgecode --jq '{stars,license:.license.spdx_id,archived,pushed:.pushed_at}'   # 7423, Apache-2.0, archived=false, pushed 2026-06-19
gh api repos/tailcallhq/forgecode --jq '.description'                                                  # AI pair programmer for Claude/GPT/O-series/Grok/DeepSeek
```

## What worked

- **Model-agnostic pairing.** One CLI that works across Claude/GPT/O-series/Grok/DeepSeek lets you pick the best model per task without switching tools — the core value.
- **MCP + custom workflows.** MCP support and custom agents/workflows mean it plugs into the wider tool ecosystem and is configurable, not a fixed surface.
- **Rust, active, Apache-2.0.** Fast/low-footprint implementation, daily pushes, permissive license, backed by Tailcall (a known dev-tools company).
- **Shell-native.** Operates in the terminal where developers already work; good for refactor/debug/feature loops.

## What didn't work or surprised us

- **Very crowded category.** Model-agnostic terminal coding agents are abundant (opencode, goose, grok-cli, qwen-code, oh-my-* , aider). Forge's wedge is "multi-model pair programmer with MCP/custom workflows," not a new capability — differentiation is incremental.
- **README detail was thin in inspection.** Verdict rests on description + metadata + the multi-model/MCP claims; depth of workflow/agent features not exercised here.
- **BYO keys + per-task cost.** Multi-model is great but you supply/pay for each provider.
- **Switching cost.** Teams already on Claude Code/Codex/opencode need a reason to add another agent; "more models in one CLI" may or may not be enough.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Picking the best model per task can improve output; quality is model-bound. |
| Speed | + | Shell-native, fast Rust agent for refactor/debug/feature loops. |
| Maintainability | neutral | MCP + custom workflows keep it configurable; another agent in the stack. |
| Safety | neutral | Standard coding-agent trust surface (runs in your shell, your keys). |
| Cost Efficiency | neutral | Apache-2.0/free tool; multi-provider inference cost is yours, choice helps optimize. |

## Verdict

**CONDITIONAL** — Forge (forgecode) is an active, Apache-2.0, Rust **model-agnostic terminal pair programmer** spanning Claude/GPT/O-series/Grok/DeepSeek with MCP and custom workflows. Adopt it if you specifically want **one interactive CLI that pairs across many models** (and you value Rust speed + MCP extensibility) rather than a single-vendor agent. It's CONDITIONAL primarily because the category is saturated — its edge over opencode/goose/grok-cli is multi-model + configurability, not a distinct capability — so the decision is whether that consolidation is worth adding another agent to your stack. Solid, well-maintained option; not obviously better than the incumbents for any one model.

Compared to neighbors: **opencode**/**goose** are model-agnostic open agents; **grok-cli** is Grok-native; **oh-my-openagent** is a token-efficient harness. Forge's distinguishing pitch is **a Rust, MCP-enabled, multi-model pair-programming CLI from Tailcall.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [forgecode](https://github.com/tailcallhq/forgecode) | harness | Terminal AI pair programmer (Apache-2.0) across Claude/GPT/O-series/Grok/DeepSeek and more — model-agnostic, MCP support, custom workflows/agents, and shell-native operation for refactors, debugging, and feature work | Want a single multi-model pair-programming CLI rather than a vendor-locked agent | opencode, goose, grok-cli, oh-my-openagent |
