# Memory Systems

**Evidence:** SOURCE-ONLY

Evaluation of persistent memory tools for AI coding agents. All aim to solve the same core problem: agents are stateless and forget everything between sessions.

## Evaluation Criteria

- **Recall quality** — does it surface relevant context without flooding the prompt?
- **Storage model** — local-first vs. cloud, structured vs. unstructured
- **Cross-agent support** — works with Claude Code only, or also Cursor, Codex, Gemini?
- **Installation complexity** — how much setup before it works?
- **Context cost** — how many tokens does it consume per session?
- **Active maintenance** — is it still being developed?

## Tool Comparisons

### beads (gastownhall/beads)

**Stars:** 24,545 | **Last updated:** 2026-06-15 | **License:** MIT

**What it actually does:** A distributed graph issue tracker powered by Dolt (version-controlled SQL database). Despite being categorized as "memory," beads is primarily a task/issue tracker with memory features bolted on. It replaces markdown TODO lists with a dependency-aware graph. The `bd remember "insight"` command stores project memories, and `bd prime` injects them into agent context. Key features: hash-based IDs prevent merge collisions in multi-agent workflows, semantic "memory decay" summarizes old tasks to save context, Dolt-based versioning with cell-level merge.

**Strengths:**
- Solves work coordination AND memory in one tool
- Dolt backend gives real version control (branch, merge, diff) on the memory database
- Agent-optimized JSON output, dependency tracking, auto-ready task detection
- Multi-agent safe: hash-based IDs prevent collisions across branches
- Stealth mode for personal use on shared projects
- Strong adoption (24.5k stars) with active development

**Weaknesses:**
- Memory is secondary to issue tracking — `bd remember` is a convenience, not the core product
- Requires Dolt installation (non-trivial dependency)
- Memory retrieval is keyword-based via `bd prime`, not semantic search
- Overkill if you just want cross-session memory without task tracking

---

### agentmemory (rohitg00/agentmemory)

**Stars:** 22,973 | **Last updated:** 2026-06-15 | **License:** Apache-2.0

**What it actually does:** MCP-based persistent memory with confidence scoring, lifecycle management, knowledge graphs, and hybrid search. Built on the "iii engine." Claims 95.2% retrieval R@5, 92% fewer tokens via compression, 53 MCP tools, 12 auto-hooks, zero external databases. Extends Karpathy's LLM Wiki pattern. Includes a real-time viewer for browsing stored memories.

**Strengths:**
- Purpose-built for memory (not a side feature like beads)
- Benchmark-validated: 95.2% retrieval recall with published methodology
- Hybrid search (semantic + keyword + knowledge graph)
- Confidence scoring prevents low-quality memories from polluting context
- Zero external database dependencies — self-contained
- Works with every major agent (Claude Code, Copilot, Cursor, Gemini CLI, Codex, etc.)
- 1,423+ tests passing — serious engineering
- Real-time viewer for inspecting what's stored

**Weaknesses:**
- 53 MCP tools is a lot of surface area — potential for context bloat
- 12 auto-hooks may conflict with other hook-based tools
- Relatively new (Feb 2025) — less battle-tested than some alternatives
- Large feature set may overlap with other tools (knowledge graph competes with graphify)

---

### claude-mem (thedotmack/claude-mem)

**Stars:** 82,562 | **Last updated:** 2026-06-15 | **License:** Apache-2.0

**What it actually does:** Claude Code plugin providing persistent memory via observation compression. Captures tool usage during sessions, compresses observations using the Claude Agent SDK, and injects relevant context into future sessions. Stores in SQLite + Chroma (vector DB). Includes 18 skills: semantic search, timeline views, knowledge graphs, weekly digests, codebase learning, smart exploration via tree-sitter AST parsing. Version 13.4.0 — very actively maintained.

**Strengths:**
- Most popular by far (82.5k stars) — massive community, well-tested
- Extremely feature-rich: memory + search + timeline + knowledge graphs + smart explore + wowerpoint slides
- Observation-based: captures what you DO, not just what you SAY — lower friction than manual storage
- Tree-sitter AST parsing for token-efficient code exploration
- Chroma vector DB for semantic search — high-quality retrieval
- `/learn-codebase` primes the entire repo into memory
- Mintlify docs site — professional documentation
- 13 major versions — battle-hardened through iteration

**Weaknesses:**
- Claude Code specific — doesn't work with Cursor, Codex, Gemini
- Requires Bun + uv + Node.js — non-trivial dependency chain
- 18 skills is a lot — some may conflict with other plugins
- Observation compression adds latency to every tool use via hooks
- Chroma adds ~600MB RAM overhead for vector search
- v13 suggests rapid iteration — possible breaking changes between versions

---

### OMEGA (omega-memory/omega-memory)

**Stars:** 162 | **Last updated:** 2026-06-15 | **License:** Apache-2.0

**What it actually does:** Cross-model memory with local-first storage. Works as both an MCP server and a Python library. Provides memory storage, semantic search, coordination between agents, user profiles, and decision tracking. Runs entirely on your machine — no cloud, no API keys. 1,123 tests passing. Installs as pip package with MCP server or hooks-only mode.

**Strengths:**
- True cross-model: works with Claude, GPT, Gemini, Cursor, Codex, and any MCP client
- Local-first with no cloud dependency — privacy-preserving
- Coordination features: handoff protocols, multi-agent memory sharing
- Lightweight hooks-only mode saves ~600MB RAM vs. full MCP server
- Clean Python API for programmatic access from scripts/CI
- Protocol-based: `omega_protocol()` returns operating instructions, making it self-documenting

**Weaknesses:**
- Very low adoption (162 stars) — small community, less battle-tested
- Python-only — adds a Python dependency even in Node.js projects
- Feature set is narrower than claude-mem or agentmemory
- No published benchmarks for retrieval quality
- Less transparent about what it stores and when — relies on hooks for auto-capture
- Documentation is sparse compared to alternatives

---

### claude-reflect (BayramAnnakov/claude-reflect)

**Stars:** 1,062 | **Last updated:** 2026-03-16 | **License:** MIT

**What it actually does:** NOT a memory system — it's a self-learning system. Captures corrections during sessions via hooks, queues them, and on `/reflect` syncs learnings to CLAUDE.md with human review. v2 added skill discovery: analyzes past sessions to find repeating patterns and generates reusable commands. 160 tests passing.

**Strengths:**
- Solves a different problem than the others: learning from mistakes, not storing context
- Human-in-the-loop: corrections are reviewed before becoming permanent
- Skill discovery (v2) is unique — mines patterns from session history
- Lightweight: no database, no vector store, just CLAUDE.md updates
- Complements any memory system rather than competing with it

**Weaknesses:**
- Not actually a memory system — doesn't provide cross-session context recall
- Last updated March 2026 — 3 months stale
- Modest adoption (1,062 stars)
- Claude Code only
- `/reflect` is manual — you have to remember to run it

## Verdict

**Recommended: claude-mem**

**Why:** Highest adoption (82.5k stars), most mature (v13), richest feature set (memory + search + timeline + AST exploration + knowledge graphs), and observation-based capture means it works without you having to explicitly store things. The automatic observation compression is the key differentiator — it captures what you DO, not just what you TELL it to remember. The trade-off is it's Claude Code specific and resource-heavy.

**Runner-up: agentmemory** — choose this if you need cross-agent support (Cursor, Codex, Gemini, etc.) or want benchmark-validated retrieval quality. It's purpose-built for memory with cleaner architecture than claude-mem's kitchen-sink approach. The 53 MCP tools are concerning but the 95.2% recall speaks for itself.

**Complementary: claude-reflect** — this is not a competitor to the above. It solves a different problem (learning from corrections) and should be used alongside whichever memory system you pick. WORKFLOW.md correctly recommends it as a separate tool.

**Reassess: OMEGA** — currently recommended in WORKFLOW.md as a memory option, but with only 162 stars and no published benchmarks, it's hard to justify over claude-mem (82.5k stars) or agentmemory (23k stars). The cross-model support is a legitimate advantage, but agentmemory offers the same with far more validation. **OMEGA should be downgraded in the workflow recommendation.**

**Specialized: beads** — not really a memory system; it's a work coordination tool. The WORKFLOW.md correctly places it at L6 for multi-agent work ledger, not as a memory system. It shouldn't be compared against the others in this category.
