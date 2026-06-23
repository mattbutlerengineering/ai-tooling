# mem0 vs claude-mem

**Evidence:** SOURCE-ONLY

## mem0
**Repo:** [mem0ai/mem0](https://github.com/mem0ai/mem0)
**Stars:** 58,645 | **Forks:** 6,739 | **Open issues:** 361 | **Last updated:** 2026-06-15 | **License:** Apache-2.0 | **Created:** 2023-06-20 | **Backed by:** Y Combinator S24

**What it actually does:** AI memory layer with a research-backed algorithm. Stores User, Session, and Agent state with entity linking and temporal reasoning. Supports semantic search, BM25 keyword search, and entity matching scored in parallel. Available as a pip/npm library, self-hosted Docker server, or managed cloud platform.

**April 2026 algorithm update (benchmarked):**
- LoCoMo: 91.6 (+20 over previous)
- LongMemEval: 94.8 (+27 over previous)
- BEAM (1M tokens): 64.1
- Single-pass retrieval: ~1s p50 latency, ~7K tokens

**Key features:**
- Multi-level memory: User, Session, Agent state
- Entity linking across memories for retrieval boosting
- Temporal reasoning (time-aware retrieval for past/present/future)
- Agent self-signup (CLI: `mem0 init --agent --agent-caller claude-code`)
- Claude Code skills shipped in-repo (reference skills for SDK knowledge)
- MCP server available via community (pinkpixel-dev/mem0-mcp at 96 stars, plus self-hosted options)
- Multi-platform: Python SDK, Node SDK, REST API, browser extension

**Strengths:**
- Published, reproducible benchmarks (91.6 LoCoMo, 94.8 LongMemEval) — no other memory tool in the catalog has benchmarks
- Entity linking is a genuine differentiator — connects people, code, and concepts across memories
- Temporal reasoning handles "what was X last month?" vs "what is X now?" — critical for long-running projects
- YC-backed with a funded team — likely to keep improving
- Model-agnostic and platform-agnostic — works beyond Claude Code
- Agent self-signup flow means Claude Code can provision its own memory without human setup

**Weaknesses:**
- Not a native Claude Code plugin — requires MCP server setup (community-maintained, not official)
- Cloud platform has a cost beyond free tier (managed service pricing)
- 361 open issues suggests rapid growth outpacing support
- The richest features (dashboard, auth, advanced retrieval) require the cloud platform or self-hosted Docker
- No native observation-based capture — you call `mem0 add` explicitly, it doesn't auto-capture session learnings

## claude-mem (current recommendation)
**Repo:** [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)
**Stars:** 82,567 | **Forks:** 7,145 | **Open issues:** 138 | **Last updated:** 2026-06-15

**What it actually does:** Claude Code plugin providing persistent memory with semantic search, timeline views, observation-based capture, knowledge graph management, and session monitoring. Installed as a native plugin marketplace — no external services required.

**Key features:**
- Native Claude Code plugin (marketplace install, zero external dependencies)
- Observation-based auto-capture (SessionStart/PostToolUse hooks capture learnings passively)
- Semantic search across all observations
- Timeline views for temporal browsing
- Knowledge graph management
- Smart exploration and structural code search
- 18+ bundled skills (babysit, design-is, do, learn-codebase, make-plan, pathfinder, etc.)

**Strengths:**
- Native Claude Code plugin — install once, works everywhere with no config
- Observation-based capture is passive — you don't have to remember to call `mem0 add`
- 18+ skills that extend beyond memory (planning, execution, code exploration, weekly digests)
- 82.5K stars — larger community than mem0
- Zero external dependencies — no Docker, no cloud service, no API keys
- Timeline and knowledge graph views built-in
- Actively maintained (updated same day as evaluation)

**Weaknesses:**
- No published benchmarks for retrieval quality
- No entity linking or temporal reasoning algorithms
- No multi-platform support — Claude Code only
- The 18+ bundled skills may add context overhead if you only want memory
- No agent self-signup or multi-agent coordination primitives

## Head-to-Head

| Dimension | mem0 | claude-mem |
|-----------|------|-----------|
| Claude Code native | No (MCP via community) | **Yes (plugin)** |
| Semantic search | **Yes (multi-signal fusion)** | Yes |
| Timeline views | No (cloud dashboard only) | **Yes (built-in)** |
| Entity linking | **Yes (cross-memory)** | No |
| Temporal reasoning | **Yes (time-aware retrieval)** | No |
| Auto-capture | No (explicit `add` calls) | **Yes (observation hooks)** |
| Published benchmarks | **Yes (91.6 LoCoMo, 94.8 LongMemEval)** | No |
| Multi-platform | **Yes (Python, Node, REST, MCP)** | Claude Code only |
| Bundled skills | Reference skills only | **18+ skills** |
| Community size | 58.6K stars | **82.5K stars** |
| External dependencies | Docker or cloud service | **None** |
| Setup effort | MCP config + API key or Docker | **One-line plugin install** |

## Verdict

**Keep claude-mem as the primary recommendation. Add mem0 as a conditional alternative.**

**Why claude-mem stays on top for most users:**
1. Zero-friction install. A one-line marketplace install vs. Docker + MCP config or cloud signup. For someone who is just adding memory for the first time, friction kills adoption.
2. Observation-based auto-capture. You don't have to remember to save memories — the hooks do it. mem0 requires explicit `mem0 add` calls, which means the agent has to be instructed to save, and it will forget.
3. The 18+ bundled skills (make-plan, do, learn-codebase, pathfinder, weekly-digests) provide immediate workflow value beyond raw memory. mem0 is memory-only.

**When mem0 is the better choice:**
1. **Multi-tool workflows.** If you use Claude Code AND Codex AND Cursor, mem0 is the only option that shares memory across all of them. claude-mem is Claude Code only.
2. **Large-scale or team contexts.** mem0's entity linking and temporal reasoning become critical when memory grows past thousands of entries. claude-mem's retrieval is simpler and may degrade at scale.
3. **Benchmark-driven confidence.** If you need to justify memory quality to stakeholders, mem0's published 91.6 LoCoMo / 94.8 LongMemEval scores are the only hard numbers in the ecosystem.

**Recommendation for WORKFLOW.md:**
- L4 primary: claude-mem (zero friction, auto-capture, bundled skills)
- L4 conditional: mem0 (if multi-tool or multi-agent workflows, or at scale past ~5K memories)
- Do not run both simultaneously
