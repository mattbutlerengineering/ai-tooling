# Evaluation: codegraph

**Repo:** [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph)
**Stars:** 51,024 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Pre-indexed code knowledge graph that runs as an MCP server and auto-syncs on file changes. Agents query it for function definitions, call graphs, cross-module dependencies, and structural context. Runs 100% locally — no external API calls. Works with Claude Code, Codex, Gemini, Cursor, and other MCP-compatible agents.

## How we tested it

**README/mechanism review — not run hands-on.** Note the install first: an earlier draft showed a bare `claude mcp add codegraph`, which is incomplete. The CLI publishes on npm as **`@colbymchenry/codegraph`**; you install it (`npm install -g @colbymchenry/codegraph`, or `npx @colbymchenry/codegraph`) and it then auto-wires the MCP server into Claude Code/Cursor/Codex. The behavior below is from the repo/README and the author's published benchmark, not an observed indexing run — no latency or indexing-time figures are claimed here as measured.

```bash
npm install -g @colbymchenry/codegraph    # then it configures the MCP server for your agent
```

## What worked (from the design + author's benchmark)

- **Auto-sync is the headline** — the graph is meant to stay current as you edit, with no manual rebuild step, and agents use it automatically over MCP (no prompt engineering).
- **100% local** — no external API calls, no keys; nothing leaves the machine (verifiable from the architecture/README).
- **Author-reported benchmark:** ~16% cost savings and ~58% fewer tool calls vs sessions without it, across 7 codebases. This is the project's own measurement, not reproduced here.

## What didn't work or surprised us

- **Not independently run.** The compelling claims (sub-500ms queries, ~2-min indexing of a 50k-line repo) are the project's, not observed in this evaluation — treat them as vendor figures pending a hands-on pass.
- Graph queries return raw structural data — the agent still has to interpret relationships.
- No visualization output (unlike graphify) — purely an agent-facing tool.
- Large star count (51K) but a young ecosystem — long-term stability is promising but unproven at multi-year scale.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Agents navigate code with structural awareness instead of grep-and-guess (by design). |
| Speed | + (author-reported) | ~58% fewer tool calls per the project's benchmark; not reproduced here. |
| Maintainability | neutral | Helps agents understand structure but doesn't improve code itself. |
| Safety | neutral | Local-only; no security impact. |
| Cost Efficiency | + (author-reported) | ~16% token savings per the project's benchmark; not reproduced here. |

## Verdict

**ADOPT** (review-based)

The always-on, auto-syncing knowledge-graph-over-MCP approach is a sound design for daily development: unlike batch analysis tools (graphify, Understand-Anything) it's meant to stay current without manual rebuilds and integrate invisibly into agent sessions. The 51K-star adoption and the author's cost/tool-call benchmark support an ADOPT lean — but this verdict rests on design + vendor numbers, not an independent run, so confirm the indexing/latency claims on your own repo before relying on them. Install via `npm install -g @colbymchenry/codegraph` (not the bare `claude mcp add codegraph`).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codegraph](https://github.com/colbymchenry/codegraph) | tool | Pre-indexed code knowledge graph that auto-syncs on changes | Agents lack structural awareness of the codebase | graphify, Understand-Anything |
