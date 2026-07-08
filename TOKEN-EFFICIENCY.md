# Token Efficiency — Curated Guide

A curated subset of [CATALOG.md](CATALOG.md) covering skills, agents, MCP servers, and tools that **measure**, **optimize** (reduce), or **improve** token efficiency. Organized by the four-jobs framework from [WORKFLOW.md](WORKFLOW.md#cross-cutting-token-tooling--four-jobs-four-picks). Verdicts and Evidence come from [COMPARISON.md](COMPARISON.md); a `discovery-log` verdict means catalogued but not yet hands-on exercised.

> **One tool per job is the rule** — stacking two tools in the same job is redundant; one per job composes. See the "I want to…" cheat sheet at the bottom.

---

## 1. Measure — token usage & cost

| Tool | Type | Verdict | Evidence | What it does |
|------|------|---------|----------|--------------|
| [abtop](https://github.com/graykode/abtop) | tool | CONDITIONAL | MEASURED | htop-style live TUI: per-session tokens, cost, context %, rate limits |
| [ccusage](https://github.com/ccusage/ccusage) | tool | ADOPT | MEASURED | Historical daily/monthly/session/model token & cost reports from local logs |
| [codeburn](https://github.com/getagentseal/codeburn) | tool | ADOPT | MEASURED | Cross-tool spend attribution by task/model/tool/project + ranked waste fixes |
| [tokencost](https://github.com/AgentOps-AI/tokencost) | tool | CONDITIONAL | RUN | Per-call cost estimation for 400+ models (Python lib) |
| [claude-monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) | tool | CONDITIONAL | REVIEW | Real-time terminal monitor + burn-rate predictions |
| [agentsview](https://github.com/kenn-io/agentsview) | tool | discovery-log | REVIEW | Cross-agent browse/search + cost tracking, local SQLite |
| [ccstatusline](https://github.com/sirmalloc/ccstatusline) | plugin | discovery-log | REVIEW | Inline token/spend status line in Claude Code |
| [claude-hud](https://github.com/pesto-studios/claude-hud) | plugin | discovery-log | REVIEW | HUD overlay for token/cost |
| [claude-devtools](https://github.com/matt1398/claude-devtools) | tool | CONDITIONAL | REVIEW | Visual debugger over session transcripts — tool calls, tokens, subagents |
| [langfuse](https://github.com/langfuse/langfuse) | platform | discovery-log | SOURCE-ONLY | Production LLM tracing, evals, cost tracking, latency |

---

## 2. Optimize — reduce tokens the model receives or emits

### 2a. Compress prose output (what the model writes back)

| Tool | Type | Verdict | Evidence | What it does |
|------|------|---------|----------|--------------|
| [caveman](https://github.com/JuliusBrussee/caveman) | skill | ADOPT | MEASURED | ~49–59% measured prose compression, no accuracy loss |

### 2b. Compress tool output (before it reaches the context window)

| Tool | Type | Verdict | Evidence | What it does |
|------|------|---------|----------|--------------|
| [headroom](https://github.com/headroomlabs-ai/headroom) | tool | CONDITIONAL | MEASURED | Compresses tool output/logs/files 60–95%, reversible via local cache |
| [context-mode](https://github.com/mksglu/context-mode) | MCP server | CONDITIONAL | REVIEW | Sandboxes tool output, 96% reduction across 15 platforms |
| [token-optimizer-mcp](https://github.com/ooples/token-optimizer-mcp) | MCP server | CONDITIONAL | REVIEW | 95%+ context reduction for tool outputs |
| [claw-compactor](https://github.com/open-compress/claw-compactor) | tool | CONDITIONAL | REVIEW | Deterministic reversible 14-stage compression, no LLM cost |
| [lean-ctx](https://github.com/yvgude/lean-ctx) | tool | CONDITIONAL | REVIEW | Rust binary: ~13-tok re-reads, persistent memory, signed savings ledger |
| [rtk](https://github.com/rtk-ai/rtk) | tool | CONDITIONAL | REVIEW | CLI proxy trimming dev-command output 60–90% |

> ⚠️ Every REVIEW-only compressor's headline % (60–96%) is **self-reported** — see `audit-evals.py --savings-claims`. Only `caveman` and `headroom` have measured savings in this repo.

### 2c. Structure tool output (so less is sent without loss)

| Tool | Type | Verdict | Evidence | What it does |
|------|------|---------|----------|--------------|
| [Pare](https://github.com/Dave-London/Pare) | MCP server | discovery-log | REVIEW | Token-efficient structured MCP servers (git, tests, npm, docker) |
| [mcp2cli](https://github.com/knowsuchagency/mcp2cli) | tool | discovery-log | REVIEW | Call tool schemas on-demand instead of loading all every turn |
| [ref-tools-mcp](https://github.com/ref-tools/ref-tools-mcp) | MCP server | discovery-log | REVIEW | Token-efficient doc search — returns only ~5k relevant tokens/session-aware |

---

## 3. Improve — read less code, route fewer tokens, pick the right model

### 3a. Read less code (code intelligence & retrieval)

| Tool | Type | Verdict | Evidence | What it does |
|------|------|---------|----------|--------------|
| [codegraph](https://github.com/merajmehrath/codegraph) | tool | ADOPT | MEASURED | Code intelligence graph for agentic search |
| [serena](https://github.com/oraios/serena) | MCP server | ADOPT | MEASURED | Semantic code tools, language-server-backed retrieval |
| [code-context-engine](https://github.com/elara-labs/code-context-engine) | MCP server | CONDITIONAL | REVIEW | Index once, search instead of reading — 94% savings (self-reported) |
| [SocratiCode](https://github.com/giancarloerra/SocratiCode) | tool | discovery-log | REVIEW | Semantic search + dependency graphs — 61% fewer tokens (self-reported) |
| [gortex](https://github.com/zzet/gortex) | MCP server | CONDITIONAL | REVIEW | 257 languages, 50× token reduction (self-reported) |
| [cocoindex-code](https://github.com/cocoindex-io/cocoindex-code) | tool | discovery-log | REVIEW | Zero-config AST semantic search — ~70% savings (self-reported) |
| [semble](https://github.com/MinishLab/semble) | tool | CONDITIONAL | REVIEW | ~98% fewer tokens than grep+read (self-reported), CPU-only |
| [claude-context](https://github.com/zilliztech/claude-context) | MCP server | CONDITIONAL | REVIEW | Milvus vector semantic search over whole codebase |
| [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | MCP server | discovery-log | REVIEW | Persistent code knowledge graph, 158 languages |

### 3b. Curate context before prompting (what files reach the model)

| Tool | Type | Verdict | Evidence | What it does |
|------|------|---------|----------|--------------|
| [markitdown](https://github.com/microsoft/markitdown) | tool | ADOPT | MEASURED | Binary docs → token-efficient Markdown |
| [repomix](https://github.com/yamadashy/repomix) | tool | CONDITIONAL | RUN | Pack repo/code into a single LLM-ready file |
| [gitingest](https://github.com/coderamp-labs/gitingest) | tool | CONDITIONAL | MEASURED | URL → repo digest with file tree + token counts |
| [repoprompt-ce](https://github.com/repoprompt/repoprompt-ce) | tool | discovery-log | SOURCE-ONLY | Hand-curate exactly which files reach the model |
| [opensrc](https://github.com/opensrc/opensrc) | tool | discovery-log | REVIEW | Context-engineering companion |
| [context7](https://github.com/upstash/context7) | MCP server | KEEP | RUN | On-target dependency/library docs — avoids 20k-token doc dumps |

### 3c. Route to the right model / split reasoning from execution

| Tool | Type | Verdict | Evidence | What it does |
|------|------|---------|----------|--------------|
| [litellm](https://github.com/BerriAI/litellm) | tool | CONDITIONAL | REVIEW | Multi-provider routing to pick cheapest capable model per call |
| [Portkey-gateway](https://github.com/Portkey-AI/gateway) | tool | CONDITIONAL | REVIEW | 1,600+ LLMs, retries/fallbacks/load balancing + caching |
| [bifrost](https://github.com/centralmind/bifrost) | tool | discovery-log | REVIEW | Fast AI gateway with multi-provider routing |
| [OmniRoute](https://github.com/diegosouzapw/OmniRoute) | tool | discovery-log | SOURCE-ONLY | 231+ providers with built-in RTK+Caveman compression |
| [claude-code-router](https://github.com/musistudio/claude-code-router) | tool | discovery-log | REVIEW | Route Claude Code requests across providers |
| [architect-loop](https://github.com/DanMcInerney/architect-loop) | skill | CONDITIONAL | REVIEW | Reasoning model as architect, cheaper coder model as builder |
| [shadcn/improve](https://github.com/shadcn/improve) | tool | discovery-log | REVIEW | Most capable model audits → cheaper models execute the plan |

### 3d. Remember instead of re-reading (long-horizon memory)

| Tool | Type | Verdict | Evidence | What it does |
|------|------|---------|----------|--------------|
| [claude-mem](https://github.com/crystallabs/claude-mem) | plugin | ADOPT | MEASURED | Persistent memory → no re-reading on next session |
| [beads](https://github.com/gastownhall/beads) | tool | KEEP | MEASURED | Work ledger, prevents duplicate effort across agent fleets |
| [OMEGA](https://github.com/Vertex-2/OMEGA) | MCP server | KEEP | REVIEW | Memory + retrieval |
| [MemOS](https://github.com/MemTensor/MemOS) | platform | discovery-log | REVIEW | Layered memory, 35%+ savings (self-reported) |
| [agentmemory](https://github.com/rohitg00/agentmemory) | tool | discovery-log | REVIEW | Persistent memory benchmarked on real dev workflows |

### 3e. Tune reasoning / effort (no dedicated tool — operator-applied)

There is **no tool** in the catalog that picks reasoning-effort level; that is a per-model knob the operator sets. Skills that shape *how hard* the model thinks (and therefore thinking-token spend):

| Tool | Type | Verdict | Evidence | What it does |
|------|------|---------|----------|--------------|
| [thinking-claude](https://github.com/richards199999/thinking-claude) | framework | discovery-log | SOURCE-ONLY | Structured deliberation before answering |
| [adhd](https://github.com/UditAkhourii/adhd) | skill | CONDITIONAL | REVIEW | Tree-of-thought with pruning — divergent ideas under a token budget |
| [agent-rules-books](https://github.com/ciembor/agent-rules-books) | skill | CONDITIONAL | REVIEW | Rule sets with tiered token budgets (DDD, Clean Arch, DDIA) |

---

## "I want to…" cheat sheet

| Goal | Pick |
|------|------|
| Watch a running session burn tokens live | **abtop** |
| See what last week/month cost | **ccusage** |
| Find *where* the money went, or what never shipped | **codeburn** |
| Price a prompt before sending it (Python pipeline) | **tokencost** |
| Make the model write fewer tokens back | **caveman** |
| Shrink tool output before it reaches context | **headroom** (STACK); context-mode / token-optimizer-mcp / claw-compactor / lean-ctx as alternatives |
| Stop reading whole files to find code | **codegraph** or **serena** (measured); code-context-engine / semble / SocratiCode / gortex (REVIEW) |
| Curate which files reach the model | **repoprompt-ce** / **gitingest** / **opensrc** |
| Docs without 20k-token dumps | **context7** / **ref-tools-mcp** |
| Pick cheapest capable model per call | **litellm** / **Portkey-gateway** |
| Reasoning model architects, cheap model builds | **architect-loop** / **shadcn/improve** |
| Stop re-reading on every new session | **claude-mem** / **beads** |
| Cap thinking-token spend | operator-set reasoning effort; **adhd** (pruned tree-of-thought); **agent-rules-books** (tiered budgets) |

---

## Honesty notes

- **Verdicts vs. evidence**: `MEASURED`/`RUN` = hands-on in this repo; `REVIEW`/`SOURCE-ONLY` = read from docs/source only — try at your own risk. Full field defs in [COMPARISON.md](COMPARISON.md).
- **Savings % are mostly self-reported**: `python3 audit-evals.py --savings-claims` lists every unverified savings headline across the catalog. Only `caveman` (49–59%) and `headroom` were measured here. Reproduce a claim via [evaluations/token-savings-protocol.md](evaluations/token-savings-protocol.md) to graduate it.
- **Source of truth**: this file is a *curated subset* of [CATALOG.md](CATALOG.md). Cross-check catalog entries before acting — it is not authoritative for counts or verdicts.