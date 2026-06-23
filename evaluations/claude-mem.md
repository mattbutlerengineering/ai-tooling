# Evaluation: claude-mem

**Repo:** [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)
**Stars:** 83,792 | **Last updated:** 2026-06-22 | **License:** Apache-2.0
**Last verified:** 2026-06-22
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

Persistent memory with semantic search, timeline views, and knowledge graph management. Solves the problem of needing searchable, structured memory with temporal awareness across sessions.

claude-mem is a Claude Code plugin that captures everything an agent does during a session, compresses it into structured "observations" with an AI worker, and injects relevant context back into future sessions. The mechanism is concrete: a set of Claude Code hooks (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`) feed a background worker that writes structured records to a local SQLite database (`~/.claude-mem/claude-mem.db`). Observations are indexed two ways — an FTS5 full-text index for keyword search and a Chroma vector store for semantic search — and surfaced through a bundled MCP server (`scripts/mcp-server.cjs`) exposing 20 tools (`search`, `timeline`, `get_observations`, `observation_*`, `memory_*`, `smart_search/unfold/outline`, and a `*_corpus` family). A `mem-search` skill teaches the agent a 3-layer "search → filter → fetch" workflow to keep token usage low.

## How we tested it

**Evidence:** MEASURED

We verified the installed plugin source on disk and then ran discriminating read-only queries against the live persisted memory store this machine has been accumulating. The plugin is installed at `~/.claude/plugins/cache/thedotmack/claude-mem/13.6.1/` (`plugin.json` declares `name: claude-mem`, `version: 13.6.1`, `license: Apache-2.0`, repo `thedotmack/claude-mem`). The MCP entrypoint `scripts/mcp-server.cjs` is a 330,928-byte bundle; grepping its registered tool definitions returns exactly **20 unique tool names** — confirming the `search`/`timeline`/`get_observations`/`observation_*`/`memory_*`/`smart_*`/`*_corpus` surface the catalog one-liner implies, not marketing copy. The `.mcp.json` shim spawns that `.cjs` as a stdio MCP server.

The discriminating check was the data store itself. The live DB is a **176 MB** SQLite file with an active WAL, and querying it read-only (`file:...?mode=ro`) showed it is genuinely populated, not a stub:

- `observations`: **20,772** rows | `session_summaries`: **2,869** | `user_prompts`: **4,050** | `sdk_sessions`: **403**
- The companion Chroma vector store (`~/.claude-mem/chroma/chroma.sqlite3`, 334 MB) holds **103,011** embeddings — the semantic half of the dual index.
- The `observations` table schema carries exactly the structured fields the design implies (`project`, `type`, `title`, `subtitle`, `facts`, `narrative`, `concepts`, `files_read`, `files_modified`, `created_at_epoch`, …) with FTS5 triggers (`observations_ai`/`_ad`/`_au`) keeping `observations_fts` in sync on every insert/delete.

We then exercised the same operations the `search` and `timeline` MCP tools wrap, via the SQLite FTS5 index they query:

```bash
DB=~/.claude-mem/claude-mem.db; RO="file:$DB?mode=ro"

# tool surface: 20 MCP tools registered
grep -oE 'name:\s*"[a-z_]+"' \
  ~/.claude/plugins/cache/thedotmack/claude-mem/13.6.1/scripts/mcp-server.cjs \
  | sort -u | wc -l        # -> 20

# what the `search` tool wraps (FTS5 over the observation corpus)
sqlite3 "$RO" "SELECT o.created_at, substr(o.title,1,70)
  FROM observations_fts f JOIN observations o ON o.id=f.rowid
  WHERE observations_fts MATCH 'catalog audit'
  ORDER BY o.created_at_epoch DESC LIMIT 5;"
# -> dated, project-scoped hits, e.g.
#    2026-06-21T15:14:16Z | PR #2558 Dockerfile fix pushed successfully ...
#    2026-06-21T05:39:36Z | Omega Memory Briefing: Project Context and Prior Session State

# what the `timeline` tool wraps (most-recent observations, per project)
sqlite3 "$RO" "SELECT date(created_at), substr(title,1,60)
  FROM observations ORDER BY created_at_epoch DESC LIMIT 6;"
# -> 2026-06-21 | CI Test Job Confirmed: Coverage to Codecov Only ...
#    2026-06-21 | docs/ Directory Full Inventory ...
```

The FTS `MATCH` query returned real, dated, project-scoped observation titles (including memory of prior PRs and CI work), and the timeline query returned the most-recent observations ordered by `created_at_epoch` — exactly the keyword-search and temporal-recall behaviours the catalog describes, confirmed against live data rather than the README. Repo metadata (stars 83,792, Apache-2.0, `archived: false`, pushed 2026-06-22) was fetched via `gh api repos/thedotmack/claude-mem`.

## What worked

- **The persistence claim is real and substantial.** 20,772 structured observations across 403 sessions in a 176 MB SQLite store — this is a memory system that has actually been retaining cross-session context, not an empty scaffold.
- **Dual retrieval is genuinely present.** FTS5 keyword index (in the main DB) *and* a 103,011-embedding Chroma vector store back the search tools — keyword and semantic recall, matching the "semantic search" one-liner.
- **Structured, queryable schema.** Observations are typed and decomposed (`title`/`facts`/`narrative`/`concepts`/`files_read`/`files_modified`/`project`), indexed by project, type, and time, so `timeline` and project-scoped `search` are cheap index lookups.
- **Token-aware retrieval workflow.** The `mem-search` skill enforces a search→filter→fetch pattern ("NEVER fetch full details without filtering first. 10x token savings"), aligning the tool surface with low-context recall.
- **Multi-stage hook capture** (`SessionStart`/`UserPromptSubmit`/`Pre`+`PostToolUse`/`Stop`) means capture is automatic and ambient, not a manual `remember` command.

## What didn't work or surprised us

- **Capture has been fragile in practice.** A `~/.claude-mem/CAPTURE_BROKEN` marker on this machine records an empty-stdin worker failure (`[bun-runner] empty stdin payload received — issue #2188`, v13.4.0). The background-worker + bun-runner architecture has real failure modes that silently stop capture until noticed.
- **Heavy footprint.** Between the 176 MB main DB (+ a 66 MB `.bak`) and the 334 MB Chroma store, the on-disk cost is ~575 MB and growing — non-trivial for an "infrastructure" plugin, and there's no built-in pruning visible in the data layout.
- **Operational surface is large.** A supervisor process manages a `worker` and a `chroma-mcp` subprocess (`supervisor.json` shows live PIDs); that's more moving parts than a single MCP server, so more to go wrong than the lighter alternatives (e.g. `engram`, a single Go binary).
- **20 MCP tools** is a wide surface to expose to the agent; the `mem-search` skill exists precisely to keep the model from over-fetching, which implies naive use is easy to get wrong.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Cross-session recall of prior decisions/PRs (FTS `MATCH` returned real dated observations) reduces repeated work and contradicting earlier choices. |
| Speed | + | Index-backed `search`/`timeline` (FTS5 + Chroma) avoid re-deriving context; skill enforces filter-before-fetch for low-token recall. |
| Maintainability | neutral | Structured, project-scoped, time-indexed observations are inspectable SQLite, but ~575 MB store and no visible pruning add upkeep. |
| Safety | neutral | Fully local store (`~/.claude-mem`), no external API for storage; offset by automatic ambient capture of session content (privacy of what's retained). |
| Cost Efficiency | + | The search→filter→fetch workflow targets ~10x token savings vs dumping full history into context; recall avoids re-running prior analysis. |

## Verdict

**ADOPT**

claude-mem is the preferred persistent-memory plugin for Claude Code over OMEGA in this stack: the install verified cleanly, the 20-tool MCP surface is real, and the live store proves the core claim with 20,772 structured observations plus a 103k-embedding dual (FTS5 + vector) index that returns dated, project-scoped recall on demand. The capture pipeline has shown fragility (a `CAPTURE_BROKEN` marker and ~575 MB footprint), so operators should watch worker health and disk growth — but those are operational caveats, not reasons to reject a memory layer that demonstrably retains and surfaces cross-session context.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-mem](https://github.com/thedotmack/claude-mem) | plugin | Persistent memory with semantic search, timeline views, and knowledge graph management | Need searchable, structured memory with temporal awareness | OMEGA, agentmemory, beads |
