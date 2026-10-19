# Evaluation: Engram

**Repo:** [Gentleman-Programming/engram](https://github.com/Gentleman-Programming/engram)
**Stars:** 5,850 | **Last updated:** 2026-07-30 | **License:** MIT
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

Persistent memory for AI coding agents. A single Go binary with SQLite + FTS5 full-text search, exposed via 20 MCP tools, an HTTP API, a CLI, and a TUI. Works with any MCP-capable agent — Claude Code, OpenCode, Gemini CLI, Codex, VS Code, Cursor, Windsurf. The agent decides what's worth remembering (decisions, bugfixes, patterns) and calls `mem_save` with structured What/Why/Where/Learned content. Next session, the previous session context is auto-injected via hooks.

Ships as a proper Claude Code plugin with hooks for session lifecycle (start, stop, compaction recovery, subagent stop, user prompt submit) and an MCP server config. Also has first-class plugins for Pi, OpenCode, and Obsidian.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured.** Installed it (v1.20.0) with `go install github.com/Gentleman-Programming/engram/cmd/engram@latest` (Go 1.24.7, no brew), then ran the CLI and the stdio MCP server against a planted fixture in a throwaway `$HOME`.

```text
$ engram save "<title>" "<body>" --type decision --project evalproj --scope project   # x20
save 20: 6.37s
$ engram search "<query>" --project evalproj --limit 5                                  # x25, raw questions
level K (keyword):     n=10 engram@1=10 @3=10 any=10 | scan@1=10 @3=10 any=10
level P (paraphrase):  n=10 engram@1=0  @3=0  any=0  | scan@1=5  @3=7  any=7
level S (synonym):     n=5  engram@1=0  @3=0  any=0  | scan@1=1  @3=1  any=1
total:                 n=25 engram@1=10 @3=10 any=10 | scan@1=16 @3=18 any=18
$ same 25 queries, stopwords stripped (content words only)
K 10/10 hit@1 | P 1/10 (only "builds flaky") | S 0/5
$ engram search "why were builds flaky"  -> No memories found
$ engram search "flaky"                  -> #6 CI cache bug
$ MCP stdio, mem_save x3 with topic_key=arch/session-strategy (project evalproj)
-> all three return id 21; mem_search "session" -> 1 memory, latest body ("use server-side sessions in Redis")
$ MCP mem_save of two contradictory decisions, no topic_key
-> search shows "conflict: contested by #obs-... (pending)" on the new memory; mem_save returns judgment candidates
$ engram mcp --tools=agent -> tools/list returns 18 tools
```

## Test design

- **Task / corpus:** 20 planted engineering decisions (one title + one sentence each: auth tokens, retry policy, pagination, money-as-cents, deploy freeze, and so on) saved into one project; 25 recall queries with one known correct memory each, in three disclosed levels: 10 keyword (words copied from the body), 10 paraphrase (natural question, 0-2 shared words) and 5 synonym-only (no shared content word).
- **Baseline:** the same 20 facts in a flat `notes.md`, ranked by a keyword-count scan (lines scored by how many non-stopword query words they contain, OR semantics, ties by line order) — what an agent gets by grepping a notes file with no memory tool.
- **Metric:** hit@1 and hit@3 of the known memory, mechanically scored by title match in the output order; plus the topic_key upsert id count and conflict flags read from MCP JSON.
- **Reproduce:** `go install` as above, set a fresh `HOME`, save the 20 facts with `engram save`, run each query through `engram search` and through a keyword-count scan of the same text, count where the expected memory ranks. The fixture and scorer were scratch scripts under `/tmp/eval-engram/` and are not committed.

## What worked

- **Keyword recall is exact:** 10/10 hit@1 on keyword queries, same as the baseline, and it returned exactly one result each where the OR-scan returned 1-3 (e.g. `correlation id logs` -> engram `[5]`, scan `[5, 1, 16]`). Precision beats the scan on specific terms.
- **Topic-key upsert works as documented:** three saves with one `topic_key` produced a single observation (id 21) holding the latest content, not three near-duplicates.
- **Conflict surfacing works at save time:** saving contradictory decisions returned judgment candidates and `mem_search` flagged the new memory `contested by ... (pending)` — a feature neither the scan baseline nor, per the catalog, claude-mem offers.
- **Installs from source in one command** to a single binary; CLI, TUI, HTTP and an 18-tool MCP agent profile come from the same artifact.

## What didn't work or surprised us

- **FTS search is AND over exact tokens with no stemming or synonyms.** A natural-language question (`why were builds flaky`) returned nothing because `why` and `were` are not in the memory; stripping stopwords helped one query of ten. The paraphrase and synonym tiers scored 0/15 hit@1 against 6/15 for the OR-scan. Recall depends on the calling agent phrasing queries as bare keywords; the README's progressive-disclosure design assumes that.
- **Aggregate recall lost to the baseline:** 10/25 hit@1 vs 16/25 for a keyword-count scan of a notes file on this fixture. The fixture is small (20 facts) and hand-written; it measures query-matching behaviour, not long-session value, and the baseline is a scan we wrote, not a competing memory tool. No claude-mem head-to-head was run.
- **Speed figure is spawn-dominated:** ~0.3s per CLI call (25 searches in 7.87s) against ~0.001s for the in-process scan; each CLI call also tries an update check against the GitHub API and prints a warning on failure. Not a like-for-like comparison.
- **MCP save refuses an unknown project** (`unknown_project` with an `available_projects` hint) until the project exists in the store; the first attempt on a fresh store failed for that reason.
- The cloud-sync path, the TUI, the Claude Code plugin hooks and `conflicts scan --semantic` (which needs an LLM) were out of scope for this run.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | mixed | 10/10 on keyword queries with single-result precision; 0/15 on paraphrase and synonym queries (AND, no stemming) |
| Speed | neutral | ~0.3s per CLI call, dominated by process start and an update check; no latency win measurable here |
| Maintainability | + | topic_key upsert kept one observation across three revisions |
| Safety | neutral | local SQLite under `~/.engram`; no network needed for save or search (only the update check) |
| Cost Efficiency | neutral | Single-result keyword hits are compact, but no token measurement was taken |
| Verifiability | + | every recalled item is a stored row with id, type and timestamp; conflicts show as pending relations a human can list with `engram conflicts list` |

## Verdict

**discovery-log — tentative read** — Installed and run: exact-keyword recall and topic_key upserts work, but on a 25-query fixture the FTS search matched 10/25 at hit@1 against 16/25 for a keyword-count scan of a flat notes file, because multi-word natural questions return nothing. No head-to-head against claude-mem (STACK) was run, so there is no ground for SKIP as redundant and none for promotion; a real read needs that bake-off with agent-written queries.

## Triage note

Left at `discovery-log`, not SKIPped. Its recorded strengths — agent-agnostic
portability across Claude Code + Codex + Gemini CLI, topic-key upserts, and **conflict surfacing**
when architectural decisions evolve — are things [`claude-mem`](https://github.com/thedotmack/claude-mem)
(STACK) does not do. The eval is explicit that claude-mem stays simpler for Claude-Code-only work,
which is a fit statement, not a redundancy finding.

Re-examined 2026-09-16 (5-oldest-untriaged pass): reasoning still holds, not newly dominated
by a STACK incumbent.

Re-examined 2026-09-21 (5-oldest-untriaged pass): reasoning still holds, not newly dominated
by a STACK incumbent.

Re-examined 2026-09-25 (5-oldest-untriaged pass): reasoning still holds, not newly dominated
by a STACK incumbent.

Re-examined 2026-10-02 (5-oldest-untriaged pass): reasoning still holds, not newly dominated
by a STACK incumbent.

Re-examined 2026-10-14 (5-oldest-untriaged pass): reasoning still holds, not newly dominated
by a STACK incumbent.

Measured 2026-10-19 by the eval-runner lane (see How we tested it): left at `discovery-log` — no head-to-head against claude-mem, so neither SKIP nor promotion is supported.

_Triaged 2026-08-04 by the P2 challenger band ([#264](https://github.com/mattbutlerengineering/ai-tooling/issues/264)); re-stamped 2026-09-16, 2026-09-21, 2026-09-25, 2026-10-02, 2026-10-14._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [engram](https://github.com/Gentleman-Programming/engram) | tool | Agent-agnostic persistent memory — Go binary with SQLite, FTS5, MCP, CLI, and TUI | Need a single portable binary for memory that works with any AI coding agent | OMEGA, claude-mem, SimpleMem, agentmemory |
