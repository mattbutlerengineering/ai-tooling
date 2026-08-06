# Evaluation: mcp-vision-bridge

**Repo:** [KuaaMU/mcp-vision-bridge](https://github.com/KuaaMU/mcp-vision-bridge)
**Stars:** 8 | **Last updated:** 2026-08-06 (pushed) | **License:** MIT
**Last verified:** 2026-08-06
**Last triaged:** 2026-08-06  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

MCP server giving text-only LLM coding agents vision — analyzes images via any multimodal model (Claude, Gemini, OpenAI-compatible). Works with Claude Code, Codex, Kimi, opencode, PI.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (README, topics, license) via the GitHub API, plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`: closely overlaps `agent-vision-toolkit` (added the same day),
but that lead is itself unevaluated, not a settled ADOPT/KEEP incumbent — SKIPping one
newcomer as "redundant" with another newcomer isn't a defensible call for a bulk pass.
The distinction (MCP server vs. skill+CLI toolkit) may matter to whoever runs the real
eval; leave both for that pass to compare.

_Triaged 2026-08-06 by the daily discovery routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mcp-vision-bridge](https://github.com/KuaaMU/mcp-vision-bridge) | MCP server | Gives text-only LLM coding agents vision (MIT) — analyze images via any multimodal model (Claude, Gemini, OpenAI-compatible); Claude Code, Codex, Kimi, opencode, PI | Text-only coding agents can't see screenshots or images; want an MCP-server route to a multimodal model instead of a per-agent skill | agent-vision-toolkit, UI-TARS-desktop, MinerU |
