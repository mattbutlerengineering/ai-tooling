# Evaluation: Engram

**Repo:** [Gentleman-Programming/engram](https://github.com/Gentleman-Programming/engram)
**Stars:** 4,493 | **Last updated:** 2026-06-18 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

Persistent memory for AI coding agents. A single Go binary with SQLite + FTS5 full-text search, exposed via 20 MCP tools, an HTTP API, a CLI, and a TUI. Works with any MCP-capable agent — Claude Code, OpenCode, Gemini CLI, Codex, VS Code, Cursor, Windsurf. The agent decides what's worth remembering (decisions, bugfixes, patterns) and calls `mem_save` with structured What/Why/Where/Learned content. Next session, the previous session context is auto-injected via hooks.

Ships as a proper Claude Code plugin with hooks for session lifecycle (start, stop, compaction recovery, subagent stop, user prompt submit) and an MCP server config. Also has first-class plugins for Pi, OpenCode, and Obsidian.

## How we tested it

**Evidence:** REVIEW

Architecture review based on repo structure, README, ARCHITECTURE.md, hooks config, MCP tool surface, and plugin layout. Did not install and run (Go build dependency), so this is an architecture-level assessment, not a hands-on test.

```bash
gh api repos/Gentleman-Programming/engram --jq '.description, .stargazers_count'
# Read: README.md, docs/ARCHITECTURE.md, plugin/claude-code/hooks/hooks.json,
#        plugin/claude-code/.mcp.json, plugin/claude-code/skills/
```

## What worked

- **20 MCP tools with progressive disclosure**: search returns compact results (~100 tokens each), then `mem_timeline` for context, then `mem_get_observation` for full content. Token-efficient by design.
- **Topic-key upserts**: saves with the same `topic_key` update existing memories instead of creating duplicates. Evolving decisions stay in one memory with `revision_count` — solves the "100 versions of the same decision" problem.
- **Agent-agnostic**: `engram setup <agent>` one-liner for 7+ agents. Genuine cross-editor portability — memories travel between Claude Code, Codex, Gemini CLI, etc.
- **Conflict surfacing**: `mem_judge` and `mem_compare` detect contradictory memories and surface them for resolution. Beta feature but architecturally sound — no other memory tool in the catalog does this.
- **Zero dependencies**: single Go binary, SQLite file in `~/.engram/`. No Node, no Python, no Docker for local use. `brew install` and done.
- **Git sync**: compressed chunks export/import via git — share memories across machines without merge conflicts. Cloud sync is opt-in replication, local stays authoritative.
- **Memory lifecycle**: `review_after` and `mem_review` let memories age and get reviewed rather than accumulating indefinitely. Includes dedup via hash + project + scope + type + title.
- **Full Claude Code plugin**: hooks for SessionStart, Stop, SubagentStop, UserPromptSubmit, and compaction recovery — properly integrated, not just an MCP server bolted on.

## What didn't work or surprised us

- **Not hands-on tested**: Go build dependency and `brew install` workflow means we couldn't install in this evaluation session. Assessment is architecture-review only.
- **Cloud complexity**: the cloud sync docs reveal a 4-step upgrade flow, repair scripts, and multiple failure modes (transport_failed, canonicalization failures). The local-only path is clean; cloud adds significant operational surface.
- **Large repo**: 1,176 files suggests scope creep beyond "simple memory tool" into a full agentic platform (Pi integration, Obsidian plugin, cloud infrastructure, beta features).
- **Competes with established tools**: claude-mem (ADOPT) has a simpler mental model and proven production track record. Engram's advantages (agent-agnostic, conflict surfacing, topic upserts) are real but may not justify the switching cost for Claude Code-only users.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Conflict surfacing catches contradictory memories; topic upserts prevent stale duplicates |
| Speed | + | Progressive disclosure prevents context flooding; auto-injection on session start |
| Maintainability | + | Memory lifecycle with review_after prevents unbounded growth |
| Safety | neutral | Local-first architecture; no external dependencies for core use |
| Cost Efficiency | + | Progressive disclosure is token-efficient by design (~100 tokens per search result) |

## Verdict

**CONDITIONAL**

Use when you work across multiple AI coding agents (Claude Code + Codex + Gemini CLI) and need shared memory, or when conflict surfacing for evolving architectural decisions matters. For Claude Code-only users, claude-mem (ADOPT) remains simpler and production-proven. Engram's unique strengths — agent-agnostic portability, topic-key upserts, and conflict surfacing — justify adoption when those capabilities are needed.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [engram](https://github.com/Gentleman-Programming/engram) | tool | Agent-agnostic persistent memory — Go binary with SQLite, FTS5, MCP, CLI, and TUI | Need a single portable binary for memory that works with any AI coding agent | OMEGA, claude-mem, SimpleMem, agentmemory |
