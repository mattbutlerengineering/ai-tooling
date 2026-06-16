# New Tools Evaluation (Loop 9)

Newly cataloged starred repos assessed for WORKFLOW.md inclusion.

## context-mode
**Repo:** [mksglu/context-mode](https://github.com/mksglu/context-mode)
**Stars:** 17,525 | **Last updated:** 2026-06-15 | **Forks:** 1,247
**What it does:** MCP server that intercepts tool calls and sandboxes their output — stripping raw data from context before it lands. A 56 KB Playwright snapshot becomes 299 bytes. Tracks session state in SQLite so context compaction doesn't lose file-edit history, decisions, or task progress. Claims 98% context reduction, extending usable sessions from ~30 min to ~3 hours.
**Current workflow alternative:** caveman (L2, compresses agent output), headroom (L4, monitors context fill and triggers compaction), token-optimizer-mcp (reduces token cost of inputs).
**Key difference:** Operates upstream — sandboxes tool output before it enters the conversation, rather than compressing after the fact. Caveman is manual post-hoc compression; headroom triggers compaction reactively. context-mode is proactive interception at the MCP layer, plus session continuity across compaction events via SQLite state snapshots.

**Verdict:** ADD to L3
**Justification:** Architecturally distinct from caveman (manual compression) and headroom (compaction triggering) — solves the input pollution problem at the source. At 17.5K stars with active same-day maintenance, it has strong community validation. Fits naturally at L3 where agents start generating large tool outputs that exhaust context. Complementary to caveman (L2, output) and headroom (L4, reactive compaction).

---

## planning-with-files
**Repo:** [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files)
**Stars:** 23,397 | **Last updated:** 2026-06-14 | **Forks:** 2,056
**What it does:** Persistent file-based planning skill. Keeps `task_plan.md`, `findings.md`, and `progress.md` on disk so agents survive context loss, `/clear`, and crashes. Uses lifecycle hooks to re-inject the plan at each turn. Adds a completion gate that blocks the Stop hook until the plan is done. Supports parallel plan isolation via slugged directories.
**Current workflow alternative:** GSD (L4) handles persistent milestone/phase planning. feature-dev covers single-feature planning. TodoWrite handles lightweight in-context tracking.
**Key difference:** Operates one level lower than GSD — stateless-session recovery and per-task plan persistence without full roadmap/milestone scaffolding. Crash-proof hook-driven re-injection and completion gate are unique: even after `/clear`, the next turn automatically reloads the plan.

**Verdict:** CONDITIONAL at L2-L3
**Justification:** At L2-L3 (pre-GSD), fills a genuine gap — lightweight persistent planning with zero ceremony and crash recovery. At L4+ where GSD is active, the `.planning/` file conventions could conflict; teams should pick one. The 23K stars signal this is the community standard for this pattern. Best for teams not yet ready for GSD's full machinery.

---

## cognee
**Repo:** [topoteretes/cognee](https://github.com/topoteretes/cognee)
**Stars:** 17,843 | **Last updated:** 2026-06-15 | **Forks:** 1,893
**What it does:** Open-source AI memory platform that builds a self-hosted knowledge graph from ingested data. Combines graph storage, vector embeddings, and cognitive ontology. Core API: `remember`, `recall`, `forget`, `improve`. Ships Python SDK, CLI, and MCP plugin.
**Current workflow alternative:** claude-mem (L4), OMEGA, SimpleMem — all store memories as retrievable blobs with semantic search.
**Key difference:** Constructs an explicit knowledge graph — nodes are concepts, edges are typed relationships. Enables relational reasoning ("what projects depend on this decision?") rather than just similarity retrieval. Auto-ingests multi-format external data.

**Verdict:** CONDITIONAL at L5 for knowledge-intensive codebases
**Justification:** At L4, claude-mem covers the primary need and cognee's graph infrastructure is heavy overhead. At L5+ where agents operate across large corpora or domains with dense concept relationships, cognee's relational graph fills a gap vector-only memory can't. The 17K+ stars and MCP plugin signal production traction, but self-hosting the graph backend is real ops cost.

---

## ponytail
**Repo:** [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)
**Stars:** 17,403 | **Last updated:** 2026-06-16 | **Forks:** 735
**What it does:** Plugin that enforces a "lazy senior developer" decision hierarchy before writing code — checking stdlib, platform features, installed deps, then one-liners before custom implementation. Offers intensity levels and audit commands (`/ponytail-review`, `/ponytail-audit`, `/ponytail-debt`).
**Current workflow alternative:** implementation-discipline.md (user rules) covers YAGNI, simplicity-first, surgical changes. caveman (L2) handles token compression.
**Key difference:** An installable, invocable plugin with active enforcement commands and configurable intensity levels — operationalizes the principles rather than just stating them.

**Verdict:** SKIP
**Justification:** Core philosophy (YAGNI, minimal code) is already encoded in implementation-discipline.md and followed by default. The review and audit commands overlap with existing code-review and simplify skills. Adding ponytail creates redundant enforcement layers without meaningfully different outcomes.
