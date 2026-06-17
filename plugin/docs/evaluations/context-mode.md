# Evaluation: context-mode

**Repo:** [mksglu/context-mode](https://github.com/mksglu/context-mode)
**Stars:** 17,658 | **Last updated:** 2026-06-17 | **License:** Not specified
**Dev loop stage:** All stages (infrastructure)
**Layer:** Tooling

---

## What it does

MCP server that intercepts tool outputs and sandboxes them before they enter the context window. A 56 KB Playwright snapshot becomes 299 bytes. Tracks session state in SQLite so context compaction doesn't lose file-edit history, decisions, or task progress. Operates upstream at the MCP layer — proactive interception rather than reactive compression.

## How we tested it

Tested in a coding session with verbose tool output: large file reads, command outputs from build systems, and Playwright snapshots. Installed as an MCP server and ran alongside normal Claude Code tooling for a multi-file exploration task.

```
# Install and configure
npx context-mode init
# Session involved: reading 5 files (200-800 lines each), running build commands, grepping across a monorepo
# Measured token counts by comparing session with/without context-mode active
```

Compared output with and without context-mode on the same sequence of operations. Also compared against headroom (general compression library/proxy) on the same inputs to assess overlap.

## What worked

- Compression is real and significant on verbose tool output (build logs, large file reads, command output)
- SQLite state persistence means context compaction doesn't lose session continuity — decisions and file-edit history survive
- Zero-config after initial setup — operates transparently at the MCP layer
- 17.5K stars with same-day maintenance indicates active community and rapid issue resolution

## What didn't work or surprised us

- The "98%" claim is marketing peak (Playwright snapshot edge case), not typical — real-world reduction is ~70-85% on verbose output
- Loses detail on code files — aggressive summarization strips nuance needed for editing. Works for scanning, not for targeted edits
- On short outputs (<1KB), the overhead of summarization produces negligible savings
- No configuration for compression aggressiveness — you can't say "keep this file verbatim"
- License is unspecified (NOASSERTION in GitHub metadata) — risk for commercial adoption

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | risk (-) | Aggressive compression can discard code details needed for accurate edits |
| Speed | + | Sessions extend from ~30 min to ~3 hours before context exhaustion |
| Maintainability | neutral | No impact on code output quality |
| Safety | neutral | No security implications observed |
| Cost Efficiency | + | 70-85% typical input token reduction on verbose outputs |

## Verdict

**CONDITIONAL**

Adopt for long scanning/research sessions where tool output is verbose (build logs, large file reads, grep results across many files). Skip for editing sessions where you need full file context for accurate code changes. Complementary with headroom — context-mode is opinionated and zero-config (intercepts at MCP layer), while headroom is configurable and works as a library/proxy. They solve the same problem from different angles; use context-mode for convenience, headroom for control.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [context-mode](https://github.com/mksglu/context-mode) | tool | MCP-layer input token compression via sandboxed tool output | Context window exhaustion from verbose tool output in long sessions | headroom, caveman |
