# Evaluation: codegraph

**Repo:** [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph)
**Stars:** 51,024 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Pre-indexed code knowledge graph that runs as an MCP server and auto-syncs on file changes. Agents query it for function definitions, call graphs, cross-module dependencies, and structural context. Runs 100% locally — no external API calls. Works with Claude Code, Codex, Gemini, Cursor, and other MCP-compatible agents.

## How we tested it

Installed the MCP server and let it index a TypeScript monorepo (~50k lines across 5 packages). Queried for function definitions, cross-package imports, and call chains during a feature implementation session.

```
claude mcp add codegraph
# Initial indexing: ~2 minutes for 50k lines
# Subsequent queries: <500ms each
```

## What worked

- Auto-sync is the killer feature — the graph stays current as you edit files, with no manual rebuild step
- Query latency is consistently under 500ms for most operations (function lookup, callers, callees)
- Benchmarked 16% cost savings and 58% fewer tool calls compared to sessions without it (author's benchmark on 7 real codebases)
- 100% local — no data leaves your machine, no API keys needed
- Initial indexing is fast enough to be a non-issue (~2 min for 50k lines)
- Agents automatically use it when available — no prompt engineering needed

## What didn't work or surprised us

- The initial index can be slow on very large monorepos (>200k lines reported to take 10+ minutes)
- Graph queries return raw structural data — the agent still needs to interpret relationships
- No visualization output (unlike graphify) — purely an agent-facing tool
- 51K stars but relatively new ecosystem — long-term stability is promising but unproven at multi-year scale

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Agents navigate code with structural awareness instead of grep-and-guess |
| Speed | + | 58% fewer tool calls means faster task completion |
| Maintainability | neutral | Helps agents understand structure but doesn't improve code itself |
| Safety | neutral | No security impact |
| Cost Efficiency | + | 16% token savings per session from reduced exploration |

## Verdict

**ADOPT**

The always-on, auto-syncing approach makes codegraph genuinely useful for daily development work. Unlike batch analysis tools (graphify, Understand-Anything), it stays current without manual intervention and integrates invisibly into agent sessions via MCP. The benchmarked cost and tool-call savings are meaningful over many sessions. The only reason not to install it is if you're working on very small projects where structural navigation isn't a bottleneck.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codegraph](https://github.com/colbymchenry/codegraph) | tool | Pre-indexed code knowledge graph that auto-syncs on changes | Agents lack structural awareness of the codebase | graphify, Understand-Anything |
