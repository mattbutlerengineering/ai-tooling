# Evaluation: context-mode

**Repo:** [mksglu/context-mode](https://github.com/mksglu/context-mode)
**Stars:** 17,768 | **Last updated:** 2026-06-19 | **License:** Elastic License 2.0 (source-available)
**Last verified:** 2026-07-08  <!-- source-grounded re-check; not a hands-on re-verification -->
**Dev loop stage:** All stages (cross-cutting infrastructure)
**Layer:** Infrastructure

---

## What it does

An MCP server (distributed as a Claude Code plugin and as native plugins/configs for 15 agent platforms) that keeps verbose tool output out of the context window. Rather than compressing data after it lands in context, it routes data-producing tool calls through a sandboxed subprocess: only the script's `stdout` re-enters the conversation, the raw bytes never do. It exposes 11 MCP tools — six "sandbox" tools (`ctx_execute`, `ctx_execute_file`, `ctx_batch_execute`, `ctx_index`, `ctx_search`, `ctx_fetch_and_index`) and five meta-tools (`ctx_stats`, `ctx_doctor`, `ctx_upgrade`, `ctx_purge`, `ctx_insight`).

Three mechanisms do the work:

1. **Sandbox execution ("Think in Code").** The agent writes a script (12 runtimes: JS/TS, Python, Shell, Ruby, Go, Rust, PHP, Perl, R, Elixir, C#) that does the analysis and `console.log()`s only the answer. A 56 KB Playwright snapshot becomes a 299-byte summary because the snapshot is parsed in the subprocess and only the extracted fact returns. This is the source of the headline 98% number.
2. **FTS5 knowledge base.** `ctx_index` chunks markdown by heading (keeping code blocks intact) into a SQLite FTS5 table; `ctx_search` retrieves only matching chunks via BM25 + trigram with Reciprocal Rank Fusion, Porter stemming, proximity reranking, and Levenshtein typo correction. Outputs over 100 KB are auto-externalized to FTS5 and replaced with a searchable pointer — no truncation, no data loss. Crucially, search returns code blocks **verbatim**, not summarized.
3. **Session continuity.** Five hooks (PreToolUse, PostToolUse, UserPromptSubmit, PreCompact, SessionStart) capture ~23 event categories (files, tasks, decisions, errors, git ops, blockers) into per-project SQLite. On compaction or `--continue`, it rebuilds a priority-tiered "Session Guide" (≤2 KB) so the model resumes without re-prompting.

Notably, it explicitly does **not** enforce prose style — the README cites benchmark evidence that aggressive brevity prompts degrade reasoning, so it governs *where data goes*, not *how the model writes*.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README, `BENCHMARK.md` (21 published scenarios with fixtures from real tool outputs), the repo file tree, and the plugin/skill manifests. Not hands-on installed — the user already runs a context stack (claude-mem + OMEGA), and the prior version of this evaluation claimed a hands-on run with a non-existent `npx context-mode init` command, so this revision is grounded in verifiable repo evidence instead. Cross-referenced the savings claims against the methodology in BENCHMARK.md and differentiated against catalog peers headroom (ADOPT), caveman (ADOPT), and token-optimizer-mcp.

```bash
gh api repos/mksglu/context-mode --jq '{stars,license,description}'
gh api repos/mksglu/context-mode/readme --jq '.content' | base64 -d        # full install + mechanism docs
gh api repos/mksglu/context-mode/contents/BENCHMARK.md --jq '.content' | base64 -d   # 21-scenario benchmark table
gh api 'repos/mksglu/context-mode/git/trees/main?recursive=1' --jq '.tree[].path'    # plugin/skill/adapter layout
```

Verified: the real install path (`/plugin marketplace add mksglu/context-mode` then `/plugin install`, or `claude mcp add context-mode -- npx -y context-mode`); the 11 MCP tools; the FTS5 retrieval pipeline; the 5-hook session model; and the per-tool savings breakdown.

## What worked

- **The headline number is mechanistically sound, with caveats.** The 98% claim is the `ctx_execute_file` subtotal (315 KB → 5.5 KB across 14 summarization scenarios). The overall BENCHMARK.md headline is 96% across all 21 scenarios. It is *not* "compression" in the lossy sense — the agent computes the answer in a sandbox and only the answer returns, so for "count/aggregate/find X in this dump" tasks the reduction is real and the answer is exact.
- **It honestly separates summarization from retrieval.** BENCHMARK.md openly reports that `ctx_index + ctx_search` only achieves 50-93% savings *because it returns exact code chunks, not summaries* — and argues (correctly) that a 1-line summary of React docs is "useless for coding" while the indexed code block is "actually useful." This directly mitigates the correctness risk that plagues blind output compressors.
- **Genuine session-continuity layer.** The 5-hook capture → PreCompact snapshot → SessionStart restore loop is a real feature most output-compressors lack. It overlaps with claude-mem/OMEGA territory (working-state recovery across compaction), not just token reduction.
- **Broadest platform reach in this category.** 15 platforms (Claude Code, Qwen, Gemini CLI, VS Code/JetBrains Copilot, Cursor, OpenCode, KiloCode, OpenClaw, Codex, Antigravity, Kiro, Zed, Pi, OMP), with a per-platform capability matrix that is honest about partial support.
- **Strong traction and active maintenance.** 17.8K stars in under 4 months (created 2026-02-23), HN #1, same-day commit activity, published reproducible benchmark fixtures.
- **Thoughtful security posture.** Inherits Claude Code permission deny/allow rules into the sandbox; SSRF hardening on `ctx_fetch_and_index` (blocks cloud-metadata/link-local, scheme allowlist); credential redaction of MCP tool args before SQLite persistence; local-only, no telemetry.

## What didn't work or surprised us

- **"Skill" is the wrong type.** This is an MCP server + multi-platform plugin (with hooks and an optional bundled ops skill), not a skill. The catalog entry should classify it as a tool/MCP server.
- **The 98% headline overstates the typical case.** It applies only to the summarization path. For the documentation/code-retrieval path most coding work actually needs, savings are 50-93% and one scenario (Supabase docs) was only 44%. Real-world blended savings depend heavily on workload mix.
- **Routing depends on hook enforcement, which varies by platform.** With hooks: ~98% saved. Without (Zed, Antigravity, and the MCP-only install): only ~60% — because a single unrouted `curl` or Playwright snapshot can dump 56 KB and wipe a session's savings. The headline number assumes the model actually prefers the `ctx_*` tools, which is only reliably enforced on hook-capable platforms.
- **Hook surface area is large and collision-prone.** It claims PreToolUse, PostToolUse, UserPromptSubmit, PreCompact, and SessionStart. Users already running claude-mem, OMEGA, superpowers, or claude-reflect occupy the same hook slots — there's no documented conflict-resolution strategy, and overlapping SessionStart/PreCompact capture with an existing memory tool risks double-injection.
- **Elastic License 2.0, not MIT.** Source-available but restricts hosted/managed-service redistribution. Fine for internal dev use; a consideration for anyone wanting to repackage it.
- **"Think in code" adds a reasoning tax.** Forcing the model to write a script for routine reads trades context tokens for output tokens and an extra round-trip; for small outputs (the 0.4 KB network-requests scenario showed 13% savings) the overhead isn't worth it.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Sandbox returns exact computed answers and `ctx_search` preserves code verbatim (100% in benchmark); summarization path can still over-condense if the model picks `ctx_execute_file` for content it later needs as code |
| Speed | + | Sessions extend from ~30 min to ~3 hours before context exhaustion; FTS5 retrieval is 15-32ms |
| Maintainability | neutral | No effect on code output quality; large hook footprint adds setup/conflict complexity |
| Safety | + | Permission inheritance into sandbox, SSRF hardening, credential redaction, local-only/no-telemetry |
| Cost Efficiency | + | 96% blended context reduction in published benchmark; frees ~94% of the window for problem-solving |

## Verdict

**CONDITIONAL**

Adopt on hook-capable platforms (Claude Code, Codex, Gemini CLI, OpenCode) for research/analysis/scanning-heavy sessions where tool output is voluminous — repo research, log/CSV analysis, web scraping, large API responses. The "think in code" sandbox is a genuinely different (and more correctness-safe) approach than blind output compression: it returns computed answers, and its retrieval path preserves code exactly rather than summarizing it. Be deliberate about hook conflicts if you already run a memory/continuity tool (claude-mem, OMEGA) — context-mode's session-continuity layer overlaps with theirs, and you likely want one owner of PreCompact/SessionStart, not two. Skip the MCP-only install and non-hook platforms (Zed, Antigravity), where routing is unenforced and savings collapse to ~60%. It is complementary, not redundant, with caveman (output-side brevity — context-mode deliberately leaves prose untouched) and headroom (configurable post-hoc compression — context-mode intercepts upstream at the MCP layer).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [context-mode](https://github.com/mksglu/context-mode) | MCP server | Sandboxes tool output so only computed results enter context — 96% reduction across 15 platforms | Verbose tool output (snapshots, logs, API dumps) exhausts the context window | headroom, token-optimizer-mcp, caveman, claude-mem |
