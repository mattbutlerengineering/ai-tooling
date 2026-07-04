# Evaluation: longhand

**Repo:** [Wynelson94/longhand](https://github.com/Wynelson94/longhand)
**Stars:** 10 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

A 100%-local, lossless memory layer for Claude Code, distributed as a `pip` package + Claude Code plugin + MCP server (19 tools). Where most memory tools store *AI-generated summaries* of what mattered, longhand stores the **verbatim** raw record — every tool call, file edit (full before/after diffs), and `thinking` block — by ingesting the JSONL transcripts Claude Code already writes to `~/.claude/projects/`, before Claude Code rotates and deletes them.

The mechanism: `longhand setup` backfills existing history into a SQLite store (source of truth, raw JSON preserved as a blob) plus a ChromaDB vector index (semantic-search shadow, rebuildable), then installs two hooks — a `Stop` hook (`ingest-live`) that tails the active transcript between turns so in-flight sessions are queryable immediately, and a `SessionEnd` hook (`ingest-session`) that runs the full analysis pass (project inference, problem→fix episode extraction, conversation segments, embeddings). Crucially, **the entire analysis pipeline is deterministic and rules-based — no LLM, zero API calls**: regex error detection, hash-based project IDs, forward-walking episode extraction. Recall (`longhand recall "that stripe webhook bug last week"` or the `recall` MCP tool) parses the time phrase, matches the project, finds the problem→fix episode, and returns the actual diff. An optional `UserPromptSubmit` hook auto-injects relevant past context, and an optional launchd reconciler self-heals the index in the background.

## How we tested it

**Evidence:** REVIEW

Architecture / source-code review — **not a hands-on install.** Inspected the repo metadata, the full README, `CHANGELOG.md`, `SECURITY.md`, the plugin manifest (`.claude-plugin/plugin.json`, v0.11.1), the hooks layer (`hooks/hooks.json`), and the key source modules: `longhand/mcp_server.py` (output caps), `longhand/redaction.py` (secret masking), and the documented `storage/` (SQLite + ChromaDB), `analysis/`, and `recall/` packages. Verified specific load-bearing claims directly in source rather than trusting the README.

I deliberately **did not run `pip install longhand`**: it is an obscure 10-star, single-author package whose `setup` command writes hooks into the live `~/.claude/settings.json` and ingests the real `~/.claude/projects/` history into `~/.longhand/`. Installing it would risk hook collisions with the user's existing live setup (claude-mem, OMEGA, superpowers, claude-reflect) and execute unvetted code against real session data — the same security posture taken in `memsearch.md`. The auto-mode classifier independently blocked the install for the same reason, which I respected rather than working around. Honest method statement: claims below are grounded in source inspection and the project's own published benchmarks, not in metrics I produced.

```bash
gh api repos/Wynelson94/longhand --jq '{stars,license,description,pushed_at,created_at,open_issues}'
gh api repos/Wynelson94/longhand/readme --jq '.content' | base64 -d         # full README
gh api repos/Wynelson94/longhand/contents/hooks/hooks.json --jq '.content' | base64 -d
gh api repos/Wynelson94/longhand/contents/.claude-plugin/plugin.json --jq '.content' | base64 -d  # v0.11.1
gh api repos/Wynelson94/longhand/contents/longhand/mcp_server.py --jq '.content' | base64 -d | grep -nE "MAX_OUTPUT_CHARS|_truncate_output"
gh api repos/Wynelson94/longhand/contents/longhand/redaction.py --jq '.content' | base64 -d | head -90
gh api repos/Wynelson94/longhand/contents/SECURITY.md --jq '.content' | base64 -d
gh api "repos/Wynelson94/longhand/git/trees/HEAD?recursive=1" --jq '[.tree[].path|select(startswith("tests/") and endswith(".py"))]|length'  # 35 test files
gh api repos/Wynelson94/longhand/releases --jq '.[].tag_name'   # v0.9.0 latest tag; README/plugin say v0.11.1
```

Verified in source: `MAX_OUTPUT_CHARS = 200000` and a `_truncate_output(text, max_chars, hint)` helper enforcing per-tool caps; redaction patterns for AWS/GitHub/Slack/Anthropic/OpenAI/Stripe tokens, JWTs, DB-URL passwords, SSNs, and Luhn-checked credit cards (opt-in via `redact.enabled=true`); `SECURITY.md` documenting no-shell/no-`eval`, parameterized SQL with LIKE-wildcard escaping, read-only access to `~/.claude/projects/`, `0700` perms on `~/.longhand/`, and fail-open hooks. 35 test files (README claims "316 tests passing"). 0 open issues at time of review.

## What worked

- **The lossless / zero-summary thesis is genuinely distinct.** Storing verbatim events (including `thinking` blocks and full diffs) means recall can return the *exact* fix, not a paraphrase, and supports deterministic file-state replay (`replay_file` reconstructs any file at any point by re-applying diffs). This is a real capability claude-mem and OMEGA structurally cannot offer because they store LLM-distilled observations.
- **Zero API calls, fully deterministic core.** The entire analysis + recall pipeline is rules-based (regex, hashing, forward-walking) with local ONNX/ChromaDB embeddings. No per-turn summarizer cost (unlike claude-mem and memsearch, which call an LLM at capture time). This is the strongest cost-efficiency story among the memory tools evaluated.
- **Solves a concrete, time-sensitive problem: transcript rotation.** Claude Code deletes session JSONL after a few weeks. longhand captures it into SQLite first, so it becomes the *only* surviving copy — a defensible reason to install early that the summary-based tools don't address.
- **Hard output caps are real and enforced in code** (`MAX_OUTPUT_CHARS`, per-tool `max_chars`, `summary_only`), directly addressing the usual MCP-memory failure mode of dumping 96k-token blobs into context. Published budget: ~3–4K tokens for a full `recall`.
- **Serious security hygiene for a 10-star project.** No shell/`eval`, parameterized SQL, read-only source access, `0700` store perms, opt-in secret redaction with a credible pattern set + Luhn validation, fail-open hooks, third-party SafeSkill 93/100. `SECURITY.md` reads like the author actually threat-modeled it.
- **Lean Claude Code footprint** — `Stop` + `SessionEnd` (+ optional `UserPromptSubmit`), all non-blocking and fail-open, lower collision risk than heavy multi-hook installs (e.g. agentmemory's 12 hooks).
- **Coexists with claude-mem by design.** Both read the same JSONL without interfering — so this is additive, not mutually exclusive, with the user's ADOPTED tool.

## What didn't work or surprised us

- **10 stars, single author, no external contributors.** Created April 2026, sole committer (Nate Nelson, self-described "no CS degree"). Bus-factor of one and no community vetting — a real adoption risk for infrastructure that ingests your entire dev history.
- **Version signals are inconsistent.** Latest *git tag* is `v0.9.0`, but `plugin.json` and the README status line say `v0.11.1`, and the README still carries "Upgrading to 0.9.0" / "0.8.1" notes. The product is moving fast and the published surface isn't fully reconciled — pre-1.0, expect churn (the v0.11.1 changelog itself fixes a 13%-of-sessions project-misattribution bug found on a real corpus).
- **Benchmarks are self-reported on the author's own single corpus** (246 sessions / 125k events / ~56ms search / ~1.4s recall). No independent or reproducible retrieval evaluation (same gap as memsearch — no R@5-style numbers).
- **Test-count claim doesn't match the tree.** README advertises "316 tests passing" but the repo has 35 test files. Plausible (many tests per file), but unverified without running them, and a minor credibility ding.
- **ChromaDB dependency + Python 3.14 caveat.** Pulls in ChromaDB (segfaults on 3.14, pinned `<1.0` as a workaround per issue #4) and an ~80MB embedding-model download. Heavier dependency surface than SQLite-only peers; multi-GB histories take 10–30 min to backfill.
- **Storage cost is non-trivial at scale** — ~8 MB/session, ~2 GB for a heavy power user. That is the literal price of losslessness; acceptable, but it is a duplicate of (eventually-rotated) data, not free.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Verbatim diffs + deterministic problem→fix episode extraction return the exact past fix, not a lossy summary; deterministic replay reconstructs file state |
| Speed | + | Local vector search ~56ms / full recall ~1.4s (self-reported); rules-based analysis at ingest keeps queries fast; non-blocking hooks |
| Maintainability | + | SQLite source-of-truth with raw JSON preserved, ChromaDB rebuildable; but single-author, pre-1.0, version-signal drift add maintenance risk |
| Safety | + | Local-only, no network/telemetry, parameterized SQL, no shell/eval, 0700 perms, opt-in secret redaction, fail-open hooks; SafeSkill 93/100 |
| Cost Efficiency | + | Zero API calls in capture and recall (deterministic, no summarizer); flat per-call token cap; cost is disk (~8 MB/session), not tokens |

## Verdict

**CONDITIONAL**

longhand is a credible, well-secured tool with a genuinely differentiated thesis — lossless, verbatim, zero-API session memory with deterministic problem→fix recall and file-state replay — that the summary-based tools (claude-mem, OMEGA, mem0, memsearch) structurally cannot replicate. It is **additive rather than duplicative**: it reads the same JSONL claude-mem does, without interfering, and offers forensic "give me the exact diff" recall that complements claude-mem's semantic-observation timeline and OMEGA's cross-session decision graph. That is its real, unique value.

It falls short of ADOPT on maturity and trust, not concept: 10 stars, a single author, pre-1.0 with inconsistent version signals and only self-reported benchmarks, ingesting the user's entire dev history. Adopt it when you specifically need **forensic, lossless recall of past Claude Code work** (exact diffs, verbatim thinking blocks, deterministic replay) and you are protecting against Claude Code's transcript rotation — and run it alongside, not instead of, claude-mem (ADOPT). For users content with semantic summaries, claude-mem + OMEGA already cover the recall need without ChromaDB or the bus-factor risk. KEEP the catalog entry; re-evaluate toward ADOPT if it gains contributors, a stable 1.0, and independent retrieval benchmarks.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [longhand](https://github.com/Wynelson94/longhand) | MCP server | Lossless local Claude Code memory — verbatim tool calls, edits, and thinking blocks indexed for deterministic cross-session recall, zero API calls | Claude Code rotates session transcripts away and summary-based memory drops the detail (thinking blocks, exact diffs) you later need | claude-mem, OMEGA, memsearch, mem0, agentmemory |
