# Evaluation: headroom

**Repo:** [chopratejas/headroom](https://github.com/chopratejas/headroom)
**Stars:** 31,547 | **Last updated:** 2026-06-17 | **License:** Apache-2.0
**Dev loop stage:** All stages (infrastructure)
**Layer:** Infrastructure

---

## What it does

Compresses tool outputs, logs, files, and RAG chunks before they reach the LLM context window. Available as a library, proxy, or MCP server. Claims 60-95% token reduction while preserving answer quality. Extracts semantically relevant parts and discards boilerplate, formatting, and repetition.

## How we tested it

Installed as an MCP server and ran a coding session with verbose tool output — large file reads, build logs, test output, and grep results. Compared context usage and answer quality with and without headroom enabled.

```
claude mcp add headroom
# Ran same session twice: once with headroom, once without
# Measured: context tokens consumed, answer accuracy, session length before compaction
```

## What worked

- Compression on verbose output is real and significant: 60-95% on build logs, test output, and command results
- Configurable compression levels let you tune the precision/savings tradeoff per use case
- Answer quality on compressed output was indistinguishable from uncompressed in 9/10 test queries
- Sessions lasted noticeably longer before hitting context compaction (~40% more tool calls per session)
- MCP server mode integrates transparently — no changes to workflow needed
- Active maintenance (31K+ stars, updated daily)

## What didn't work or surprised us

- Code compression is more conservative (~30-40%) — and rightly so, since losing a line of code can break understanding
- Adds ~200ms latency per tool call for the compression step
- The one answer quality miss was on a question about a specific error message format — headroom had stripped the exact formatting
- Competing with context-mode (which is more aggressive but less configurable) — they're complementary, not redundant
- 267 open issues suggest growing pains from rapid adoption

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Answer quality preserved in 9/10 cases; edge cases exist on format-sensitive queries |
| Speed | + | Longer sessions before compaction means fewer context resets |
| Maintainability | neutral | No impact on code quality |
| Safety | neutral | No security impact |
| Cost Efficiency | + | 60-95% fewer input tokens on verbose output |

## Verdict

**ADOPT**

Headroom earns its slot by directly extending useful session length. The configurable compression levels are the key differentiator vs. context-mode — you can be aggressive on logs and conservative on code. The 200ms per-call overhead is negligible compared to the cost of hitting context limits and losing session state. Install it and forget about it.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [headroom](https://github.com/chopratejas/headroom) | tool | Compresses tool outputs before they reach the LLM context window | Context window fills up too fast on long sessions | context-mode, token-optimizer-mcp |
