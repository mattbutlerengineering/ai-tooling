# Evaluation: codeburn

**Repo:** [getagentseal/codeburn](https://github.com/getagentseal/codeburn)
**Stars:** 8,113 | **Last updated:** 2026-06-19 (pushed; created 2026-04-13) | **License:** MIT
**Dev loop stage:** Outer loop / Reflect — a cost-and-usage observability tool that runs *after* sessions, reading the on-disk logs your AI tools already write to attribute spend and surface waste. It informs model choice and config hygiene for the next cycle; it does not participate in any single inner-loop turn.
**Layer:** Infrastructure (a local Node.js CLI — `npx codeburn` — plus a native macOS menubar app and a GNOME extension that shell out to it; reads session files locally, no proxy, no API keys, nothing leaves the machine)

---

## What it does

CodeBurn answers "where did my AI spend actually go?" by **parsing the session files your tools already write to disk** — JSONL, SQLite, protobuf — and breaking every token and dollar down by **task, model, tool, and project across ~30 AI tools** (Claude Code, Codex, Cursor, Copilot, Gemini CLI, OpenCode, Goose, Devin, Warp, and a long tail more). Pricing comes from [LiteLLM](https://github.com/BerriAI/litellm), refreshed daily. The default surface is an interactive Ink TUI dashboard (`npx codeburn`, last 7 days), with a `--provider` filter, period flags, and CSV/JSON export.

It goes well past a usage table with three analysis commands. **`codeburn optimize`** scans both your sessions and your `~/.claude/` setup for concrete waste patterns — files re-read across sessions, low Read:Edit ratio, uncapped `BASH_MAX_OUTPUT_LENGTH`, unused MCP servers paying schema overhead every session, ghost agents/skills/commands defined but never invoked, bloated `CLAUDE.md` (with `@-import` expansion counted), cache-creation overhead — and emits **ranked, copy-paste fixes** (a `CLAUDE.md` line, an env var, an `mv`) plus an A–F "setup health" grade, with repeat runs classifying findings as new/improving/resolved. **`codeburn compare`** scores models head-to-head on *your* work (one-shot rate, retry rate, self-correction, cost per call/edit, cache hit rate). **`codeburn yield`** correlates sessions with git commits by timestamp to bucket spend as productive / reverted / abandoned — i.e., did the money actually ship.

As inspected, the repo is a real engineered product: ~81 files under `src/` (Commander.js CLI in `src/cli.ts`, Ink/React `.tsx` views, a per-provider parser model where "adding a provider is a single file"), a Swift/SwiftUI menubar app in `mac/`, a GNOME extension, per-provider docs under `docs/providers/`, an `architecture.md`, and CI/security hygiene (semgrep rules, SECURITY.md, a "block-claude-coauthor" workflow).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** `npx codeburn` was never executed, no dashboard was opened, no `optimize`/`compare`/`yield` was run, and no session files were parsed. Every claim comes from the repository (GitHub metadata, README, recursive file tree, `docs/architecture.md`, release/commit counts) — not from observed output. I did not verify the parsers against real session files or check the LiteLLM price accuracy.

```bash
gh api repos/getagentseal/codeburn --jq '{stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'  # 8113★, 637 forks, MIT
gh api repos/getagentseal/codeburn/readme --jq '.content' | base64 -d | head -260
gh api "repos/getagentseal/codeburn/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # src/*.ts(x), mac/ (Swift), gnome/, docs/providers/*.md, .semgrep/
gh api repos/getagentseal/codeburn/contents/docs/architecture.md --jq '.content' | base64 -d | head -40  # three surfaces: CLI + menubar + gnome
gh api "repos/getagentseal/codeburn/git/trees/HEAD?recursive=1" --jq '[.tree[]|select(.path|startswith("src/"))]|length'  # 81 src files
gh api repos/getagentseal/codeburn/commits --jq 'length'    # 30 (page-1 cap)
gh api repos/getagentseal/codeburn/releases --jq 'length'   # 30 (actively versioned, npm-published)
```

## What worked

- **Local-only by design, which is the right call for cost data.** No wrapper, no proxy, no API keys — it reads files already on disk, so nothing leaves the machine. That sidesteps the trust problem most spend trackers have and means zero-setup `npx codeburn`.
- **Cross-tool attribution is the real differentiator.** ~30 tools in one view, with `--provider`/`--project` filters, means it captures the *whole* AI bill across a fragmented toolchain — not just one vendor's dashboard. The single-file-per-provider parser model is a clean, extensible design.
- **`optimize` is uncommonly actionable.** Most cost tools stop at "here's your spend." CodeBurn names specific waste (re-read files, unused MCP schema overhead, ghost agents/skills, bloated `CLAUDE.md`) and hands you a paste-ready fix ranked by impact, with an A–F grade and progress tracking across runs. That turns observability into a Reflect-loop action.
- **`yield` ties spend to outcomes.** Correlating sessions to git commits (productive/reverted/abandoned) is the metric people actually want — "did the money ship?" — and is something raw token counters can't answer.
- **Engineered and maintained like a product.** 81 `src/` files, native menubar + GNOME clients sharing a documented JSON output contract, `architecture.md`, semgrep rules, SECURITY.md, and 30 npm-published releases in ~2 months. This is not a weekend script.

## What didn't work or surprised us

- **Accuracy is entirely contingent on session-file parsing and LiteLLM prices — and unverified here.** Per-provider log formats drift (the README itself asks users to file issues when paths change); a stale parser or stale price silently produces wrong dollar figures. The numbers look authoritative but are estimates derived from logs, not invoices.
- **`yield`'s git-by-timestamp correlation is heuristic.** Attributing commits to sessions by time proximity will misclassify interleaved work, squashed/rebased history, and long-running branches. Treat productive/abandoned buckets as directional, not exact.
- **Young and fast-moving.** Created 2026-04-13 — about two months old. 30 releases in that window signals momentum but also churn; provider coverage and metric definitions are still stabilizing.
- **`optimize`'s setup heuristics can over-flag.** "Ghost" agents/skills and "unused" MCP servers are inferred from observed invocations; rarely-but-legitimately-used items may be flagged as waste, so its fixes need human judgment before you `mv` things away.
- **Scope is measurement, not enforcement.** It tells you a cheap model would have one-shot the task; it can't route you there. The savings are advisory and depend on you acting on them.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Cost Efficiency | + + | The core purpose: per-task/model/tool/project attribution across ~30 tools, plus `optimize` waste-finding with ranked paste-ready fixes and an A–F grade, plus `yield` spend-vs-shipped. Directly drives spend down — *if* parsing and prices are accurate. |
| Speed | neutral | Runs out-of-loop; doesn't speed up or slow down any session. `optimize` can indirectly reduce retry/re-read waste, marginally helping future-session throughput. |
| Correctness | + / − | `compare`'s one-shot/retry/self-correction metrics help pick a better model for your work; but the tool's own figures are log-derived estimates, not verified billing. |
| Maintainability | + | `optimize` flags bloated `CLAUDE.md`, ghost skills/agents, and unused MCP servers — config-hygiene wins that keep an AI setup lean over time. |
| Safety | + | Local-only, no proxy/keys/network egress; semgrep rules and SECURITY.md in repo. Lowest-risk class of tool — it only reads local logs. |

## Verdict

**ADOPT (with a caveat) — the most actionable AI-spend tool in this catalog, provided you treat its dollar figures as estimates.** CodeBurn is a well-engineered, local-first, zero-setup (`npx codeburn`) cost dashboard whose real value is going past "here's your spend" into ranked, copy-paste *fixes* (`optimize`), model selection on your own work (`compare`), and spend-vs-shipped attribution (`yield`) — across ~30 tools in one view. The one caveat that keeps it from unqualified adoption: every number is derived from parsing session logs and daily LiteLLM prices, so it's an estimate, not an invoice, and a stale parser/price can mislead. For anyone with a meaningful multi-tool AI bill, the value-to-effort ratio is excellent; just reconcile against actual billing before acting on a big number.

Compared to neighbors: **tokencost** is a *library* for estimating token cost programmatically — a building block, where CodeBurn is the finished, multi-tool product. **abtop** is a live `top`-style monitor for a running agent (real-time, single-session focus); CodeBurn is retrospective, cross-tool, and analysis-oriented. **rtk** is a usage/rate-limit-leaning toolkit; CodeBurn's `optimize`/`yield`/`compare` analysis layer and ~30-tool breadth are broader. CodeBurn wins on actionability (paste-ready fixes), breadth (30 tools), and local-first trust; it's weaker than a billing API for ground-truth dollar accuracy.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codeburn](https://github.com/getagentseal/codeburn) | tool | Local-first TUI/menubar that parses on-disk session logs to attribute AI spend by task/model/tool/project across ~30 tools, with waste-finding fixes and spend-vs-shipped analysis | Your AI bill shows a total but never says where it went, which model wasted budget, or whether the spend actually shipped — CodeBurn breaks it down locally and emits ranked fixes | tokencost (cost-estimation library, a building block); abtop (live single-session monitor vs retrospective); rtk (usage/rate-limit toolkit) |

**Target category:** Observability (cost/usage analytics; outer-loop / Reflect, Cost signal)
