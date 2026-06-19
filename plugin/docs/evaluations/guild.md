# Evaluation: guild

**Repo:** [mathomhaus/guild](https://github.com/mathomhaus/guild)
**Stars:** 312 | **Last updated:** 2026-06-15 | **License:** Apache-2.0
**Dev loop stage:** Reflect (memory/recall) + Plan/Ship (task coordination across sessions)
**Layer:** Infrastructure

---

## What it does

Shared context, memory, and task coordination across AI coding agents — a single Go binary backed by local SQLite, exposed as a first-class MCP server, with hybrid keyword + semantic search.

The mechanism: `guild` compiles to one Go binary that *is* an MCP server with embedded SQLite (state lives under `~/.guild/`, strictly local — no account, no API key, nothing leaves the host). Any MCP client (Claude Code, Codex, Cursor) becomes a "Gate" into a shared substrate. The data model is three write surfaces with three lifetimes: **quest_journal** (per-quest scratchpad, dies when the quest clears), **lore_inscribe** (durable cross-quest library entries — patterns, decisions, research), and **quest_brief** (a handoff note loaded by the next session). The intended loop is autonomous and agent-operated: on session start a single `guild_session_start(project)` call recovers the project "oath" (principles), the last brief (handoff), and the top-priority quest plus parallel-safe candidates; the agent then claims a quest with an atomic lock (`quest_accept` / `quest accept`), consults the archive before researching (`lore appraise`, run as BM25 + vector reciprocal-rank fusion), records observations and reasoning, and on parting writes a brief and fulfills the quest — which **cascades**, automatically unblocking any quest that was only waiting on it. The atomic claim is the coordination primitive that lets parallel agents across different editors share one task board without colliding. `guild init` is a guided per-project setup that registers the project, writes an `AGENTS.md` block, and offers to register guild with each detected MCP client. The whole thing is wrapped in a heavy fantasy-guild metaphor (Gates, oaths, quests, lore, briefs, wanderers).

## How we tested it

Repo + README + GitHub API metadata review. Read the full README (install paths, the three-act session flow, the three write surfaces, the hybrid-search design, the platform matrix) and the repo metadata via `gh api`. **Did not install or run it.** Method is honest: no hands-on session, no timing, no recall benchmarks were produced. Rationale matches every prior Memory & Context eval in this catalog (claude-mem ADOPT; agentic-stack, memsearch, agentmemory, SimpleMem all CONDITIONAL): the user already runs claude-mem + OMEGA as the live memory stack, so the relevant question is fit/displacement, answerable from architecture without installing a competing MCP memory server into the working setup.

```bash
gh api repos/mathomhaus/guild --jq '{full_name, description, stargazers_count, forks_count, open_issues_count, language, license: .license.spdx_id, created_at, updated_at, pushed_at, topics, archived}'
gh api repos/mathomhaus/guild/readme --jq '.content' | base64 -d
```

Metadata: 312 stars, 47 forks, 26 open issues, Go, Apache-2.0, created 2026-04-20, pushed 2026-06-15, not archived. Topics include `agent-coordination`, `agent-memory`, `local-first`, `mcp`, `mcp-server`, `sqlite`, `claude`, `claude-code`, `codex`, `cursor`.

## What worked

- **It targets coordination, not just memory — the genuine differentiator.** Most catalog memory tools (claude-mem, agentic-stack, memsearch, agentmemory) optimize *recall*: capture → summarize → surface past context. guild adds a **shared task board with atomic claims** so multiple agents across different MCP clients can work in parallel without stepping on each other, with dependency cascades that auto-unblock downstream quests. That is closer to beads (issue/dependency graph for agents) than to claude-mem, and it's why the prompt's "beads complementary" framing is right.
- **Three explicit write lifetimes is a clean, well-reasoned model.** journal (this quest) / lore (other quests) / brief (next session), with the crisp "who else needs this?" decision test, is a more disciplined memory taxonomy than undifferentiated auto-summary. It maps memory granularity to scope deliberately.
- **Strong local-first, zero-cost-to-run story.** Single Go binary, embedded SQLite, no account, no API key, nothing leaves the host. Semantic retrieval ships in-binary via ONNX (`-tags=withembed`) on macOS/Linux — no external vector DB and no embedding API. Same no-DB-lock-in, local-first philosophy that earned claude-mem and agentic-stack praise, and the hybrid BM25+vector RRF search is more sophisticated than keyword-only peers by default.
- **Genuinely multi-harness and MCP-native.** Because it *is* an MCP server, any MCP client is a Gate; the README shows Claude (left) and Codex (right) reading the same state. The shared substrate is real cross-editor, not a per-harness adapter shim like agentic-stack.
- **Reasonable engineering signals for its age.** CI badge, Go 1.25, SHA256-verified installers, Homebrew tap, Windows installer, guided `init` that auto-detects and registers MCP clients. The "search before you research" (`lore appraise`) discipline to prevent duplicate knowledge is a thoughtful touch.

## What didn't work or surprised us

- **Very young and small.** Created Apr 2026, 312 stars, 47 forks, 26 open issues, two months old. Far less proven than claude-mem (ADOPT) and even younger/smaller than agentic-stack. No published recall or coordination benchmarks — search quality and the autonomy loop can't be verified from sources, only the design.
- **The autonomy premise is aspirational.** "Designed to be operated autonomously by the agents, for the agents" with an autonomous claim→act→record→cascade loop is a strong claim that depends entirely on the agent reliably calling the right tools at the right moments. Whether agents actually maintain the board cleanly over many sessions is unproven here — and this is the hardest part of any agent-memory system.
- **Heavy fantasy metaphor adds cognitive overhead.** Oath/quest/lore/brief/Gate/wanderer/Guildmaster maps onto principles/task/knowledge/handoff/client/session/human — readable, but the renaming taxes both human operators and the agent's prompt budget, and obscures what are otherwise plain CRUD-on-SQLite operations.
- **Overlaps the user's existing stack on the memory axis without beating it there.** For recall alone, claude-mem (already ADOPT) plus OMEGA cover capture/recall in the Claude Code ecosystem and are more battle-tested. guild's unique value (multi-agent atomic task coordination) only pays off if you actually run parallel agents across editors sharing one board.
- **Windows is keyword-only.** Semantic retrieval is disabled on Windows (no ONNX `Dlopen` surface), so the headline hybrid search degrades to BM25 there. Not relevant to this user (macOS) but a real platform asymmetry.
- **Installing it means running a second MCP memory server alongside claude-mem + OMEGA.** Two systems both wanting to be "the agent's memory" risks split-brain context and operator confusion, the same collision concern flagged in the agentic-stack eval.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Hybrid BM25+vector recall surfaces prior decisions/observations into new sessions; "appraise before research" reduces duplicate/contradictory knowledge — but no published recall benchmark and the autonomy loop is unverified |
| Speed | + | Atomic quest claims let parallel agents work without collisions, and cascading unblock removes manual re-triage; one `session_start` call rehydrates context with no back-and-forth |
| Maintainability | + | Local SQLite single binary, three explicit memory lifetimes, no external DB/API lock-in; offset by a two-month-old pre-1.0 codebase and a metaphor that obscures the underlying model |
| Safety | + | Strictly local-first (no account, no key, nothing leaves host), SHA256-verified installers; atomic locks prevent parallel agents clobbering shared task state |
| Cost Efficiency | + | Zero API key, zero external vector DB, in-binary ONNX embeddings — no per-turn token cost for the memory layer itself; running N parallel agents still multiplies underlying agent spend |

## Verdict

**CONDITIONAL**

guild is a well-designed, local-first MCP server that is genuinely *not* another claude-mem clone: its distinctive value is **multi-agent task coordination** — a shared quest board with atomic claims and dependency cascades that lets parallel agents across different MCP clients (Claude Code, Codex, Cursor) share one substrate — layered on top of a clean three-lifetime memory model (journal / lore / brief) and hybrid BM25+vector recall, all in a single Go binary with embedded SQLite, no account, and no API key. Adopt it **when you actually run multiple coding agents in parallel and want them coordinating over one shared, local task-and-memory board across editors** — that is its real differentiator and where it earns its keep. For this user's case (single-harness Claude Code, already on claude-mem ADOPT + OMEGA), it does **not** displace the existing memory stack: claude-mem is more battle-tested for single-agent recall, guild is two months old with no published benchmarks and an unproven autonomy loop, and running a second "agent memory" MCP server alongside claude-mem/OMEGA risks split-brain context. Like agentic-stack, memsearch, agentmemory, and SimpleMem (all CONDITIONAL), it wins on a specific axis — here, parallel multi-agent coordination — but loses to claude-mem on single-agent ecosystem fit and proven track record.

**vs. claude-mem (ADOPT), beads, dmux:** guild overlaps *complementarily*, not competitively. **claude-mem** owns single-agent auto-capture → recall in Claude Code (passive, battle-tested); guild's memory is more manual/agent-driven but adds coordination claude-mem lacks. **beads** is the closest cousin — an issue/dependency graph for agents — and guild's quest board with cascading unblock covers similar ground but bundles memory (lore/brief) and ships as a local MCP server; they are complementary (beads as the richer issue tracker, guild as the lighter in-substrate task+memory layer). **dmux** (CONDITIONAL) solves parallel-agent *filesystem* isolation via tmux + git worktrees but adds no shared memory or task board; guild + dmux would be genuinely complementary — dmux isolates the worktrees, guild shares the context and coordinates the quests across them.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [guild](https://github.com/mathomhaus/guild) | tool | Single Go binary + local SQLite MCP server: shared context, memory, and atomic task coordination across AI coding agents, with hybrid keyword+semantic search | Parallel agents across different editors have no shared memory or task board and collide on work; need a local-first substrate that survives session compaction | engram, beads, claude-mem, dmux, agentic-stack, OMEGA |
