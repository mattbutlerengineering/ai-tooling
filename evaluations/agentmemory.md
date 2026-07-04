# Evaluation: agentmemory

**Repo:** [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory)
**Stars:** 23,426 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

MCP-based persistent memory engine for AI coding agents with hybrid retrieval (BM25 + vector + knowledge graph via RRF fusion). Built on the "iii engine," it runs as a local server on `:3111` and auto-captures session context through 12 hooks — no manual `memory.add()` calls needed. Exposes 53 MCP tools, ships 15 native skills (8 invocable, 7 reference), and connects to 15+ agent platforms via `agentmemory connect <agent>`. Extends Karpathy's LLM Wiki pattern with confidence scoring, lifecycle management, and compression that claims 92% token savings.

## How we tested it

**Evidence:** REVIEW

Architecture review against README, published benchmarks, repo structure, and competitor comparison table. Compared claims against the existing memory-systems evaluation (`evaluations/memory-systems.md`) and catalog peers: claude-mem (ADOPT), engram (CONDITIONAL), mem0 (CONDITIONAL), cognee (CONDITIONAL).

```
gh api repos/rohitg00/agentmemory --jq '.description, .stargazers_count, .updated_at, .license.spdx_id'
gh api repos/rohitg00/agentmemory/readme --jq '.content' | base64 -d
gh api repos/rohitg00/agentmemory/git/trees/main --jq '.tree[].path'
```

Not hands-on tested (user already runs claude-mem + OMEGA). Evaluation is architecture-review-based.

## What worked

- **Published benchmarks with reproducible methodology**: 95.2% R@5 on LongMemEval-S (ICLR 2025, 500 questions), with eval harness in `eval/` and scorecards in `docs/benchmarks/`. This is the only catalog entry besides mem0 with reproducible retrieval benchmarks.
- **12-hook auto-capture**: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop, SubagentStop, Notification, PreCompact, and more — zero-manual-effort memory accumulation. More hooks than any competitor (claude-mem has 6, engram has 5).
- **Triple-search hybrid**: BM25 + vector (all-MiniLM-L6-v2, local, free) + knowledge graph with Reciprocal Rank Fusion. Most memory tools offer single or dual search modes.
- **Zero external database dependencies**: SQLite + local embeddings. No Postgres, no Redis, no cloud API keys for basic operation. Compare with cognee (requires LLM API for graph construction) or mem0 (cloud API for full features).
- **15+ agent platform support**: Claude Code native plugin + hooks, Codex CLI, Copilot CLI, Cursor, Gemini CLI, OpenCode, Goose, Hermes, pi, OpenHuman, OpenClaw, Cline, Kilo Code, Aider, Claude Desktop. Broadest platform support in the memory category.
- **1,423+ passing tests**: Serious engineering discipline. CI on every commit.
- **Real-time viewer**: Browser-based memory inspection — unique among CLI memory tools.

## What didn't work or surprised us

- **53 MCP tools is excessive surface area**: Most sessions need 3-5 memory operations (store, recall, search, forget). 53 tools means significant token overhead for tool descriptions in context, even with progressive disclosure. Claude-mem exposes ~20 tools, engram exposes 20 — both are more context-efficient.
- **12 auto-hooks risk conflicts**: Other hook-based tools (superpowers, hol-guard, claude-reflect) also claim hook slots. The more hooks a single tool occupies, the more likely it collides with the user's existing setup. No documented hook-conflict resolution strategy.
- **iii engine dependency is opaque**: The core is built on "iii engine" which appears to be the author's own framework. Limited external documentation on the engine itself — you're trusting a single-author infrastructure layer.
- **Confidence scoring lacks transparency**: The README claims confidence-based filtering but doesn't explain the scoring algorithm or thresholds. Users can't tune what "low confidence" means for their use case.
- **Competitor comparison table in README compares against self-reported numbers**: The 95.2% R@5 is from agentmemory's own benchmark suite against its own corpus. The mem0 number (68.5%) is from a different benchmark (LoCoMo). Not apples-to-apples.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | 95.2% R@5 on LongMemEval-S with published methodology |
| Speed | + | 14ms p50 latency, auto-capture eliminates manual memory management |
| Maintainability | neutral | Good test coverage but iii engine is opaque infrastructure |
| Safety | neutral | Local-first (no cloud dependency for basic use), but 53 MCP tools increase attack surface |
| Cost Efficiency | + | Local embeddings (free), 92% claimed token savings via compression |

## Verdict

**CONDITIONAL**

Use when you need the broadest agent platform support (15+ agents), published retrieval benchmarks for compliance/evaluation contexts, or the most comprehensive auto-capture hook coverage. claude-mem (ADOPT) remains the better choice for Claude Code-only users — it's simpler (20 vs 53 MCP tools), more battle-tested (82K stars, v13.4), and has a proven plugin ecosystem. agentmemory wins on benchmarks and cross-platform reach; claude-mem wins on ecosystem integration and context efficiency.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentmemory](https://github.com/rohitg00/agentmemory) | tool | Persistent memory for AI coding agents based on real-world benchmarks | Need memory that's been validated against actual dev workflows | OMEGA, beads, claude-mem |
