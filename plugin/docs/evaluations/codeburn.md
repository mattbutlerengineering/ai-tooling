# Evaluation: codeburn

**Repo:** [getagentseal/codeburn](https://github.com/getagentseal/codeburn)
**Stars:** 8,178 | **Last updated:** 2026-06-22 (pushed; created 2026-04-13) | **License:** MIT
**Last verified:** 2026-06-22
**Dev loop stage:** Outer loop / Reflect — a cost-and-usage observability tool that runs *after* sessions, reading the on-disk logs your AI tools already write to attribute spend and surface waste. It informs model choice and config hygiene for the next cycle; it does not participate in any single inner-loop turn.
**Layer:** Infrastructure (a local Node.js CLI — `npx codeburn` — plus a native macOS menubar app and a GNOME extension that shell out to it; reads session files locally, no proxy, no API keys, nothing leaves the machine)

---

## What it does

CodeBurn answers "where did my AI spend actually go?" by **parsing the session files your tools already write to disk** — JSONL, SQLite, protobuf — and breaking every token and dollar down by **task, model, tool, and project across ~30 AI tools** (Claude Code, Codex, Cursor, Copilot, Gemini CLI, OpenCode, Goose, Devin, Warp, and a long tail more). Pricing comes from [LiteLLM](https://github.com/BerriAI/litellm), refreshed daily. The default surface is an interactive Ink TUI dashboard (`npx codeburn report`, last 7 days), but a fleet of **non-interactive subcommands** (`overview`, `status`, `models`, `optimize`, `yield`, `export`) produce plain-text / JSON / CSV output you can drive headless, with `--provider`/`--project`/`--period` filters.

It goes well past a usage table with three analysis commands. **`codeburn optimize`** scans both your sessions and your `~/.claude/` setup for concrete waste patterns — files re-read across sessions, low Read:Edit ratio, uncapped bash output, unused MCP servers paying schema overhead every session, ghost agents/skills defined but never invoked, bloated `CLAUDE.md`, high-cost session outliers — and emits **ranked, copy-paste fixes** (a `CLAUDE.md` line, a `claude mcp remove`, an env var) plus an A–F "setup health" grade. **`codeburn compare`** scores models head-to-head on *your* work (one-shot rate, retry rate, cost per edit). **`codeburn yield`** correlates sessions with git commits by timestamp to bucket spend as productive / reverted / abandoned — i.e., did the money actually ship.

As run (see below), the repo is a real engineered product: a Commander.js CLI in `src/cli.ts` with a per-provider parser model, Ink/React `.tsx` views, a Swift/SwiftUI menubar app in `mac/`, a GNOME extension, per-provider docs, an `architecture.md`, and CI/security hygiene (semgrep rules, SECURITY.md).

## How we tested it

**Evidence:** MEASURED

Ran it **hands-on, end-to-end** on 2026-06-22 (macOS arm64) against this machine's real Claude Code session data (`~/.claude/projects/`, 220 project directories). codeburn **v0.9.14** was fetched fresh via `npx --yes codeburn@latest` — first-run download was **~7 s**. The package declares `engines.node >= 22.13.0`; on the host's default Node v20.19.5 it **hard-exits** with `codeburn requires Node.js >= 22.13.0 (current: v20.19.5)`, so every run below used Node **v24.9.0** (via nvm). Every figure quoted is an **aggregate** read off codeburn's own output; no raw session transcripts or file contents were inspected, and project identifiers are generalized.

We drove the **non-interactive** surfaces and captured real output. The interactive Ink TUI dashboards (`report`, `today`, `month`, `web`, `menubar`) and **`compare`** were **not** exercised — `compare` explicitly refuses to run headless (`Model comparison requires an interactive terminal.`), and the dashboards need a TTY. The measured result is therefore the analysis/export layer, which is exactly the part that matters for a Reflect-loop cost audit.

**1 — version + flag surface (real CLI):**

```bash
export PATH="$HOME/.nvm/versions/node/v24.9.0/bin:$PATH"   # >=22.13.0 required
npx --yes codeburn@latest --version   # 0.9.14
npx --yes codeburn@latest --help      # report/overview/status/models/optimize/compare/yield/export/web/menubar/mcp...
```

**2 — compact status as JSON (~17 s):**

```bash
npx --yes codeburn@latest status --format json --period 30days
# {"currency":"USD","today":{"cost":279.1,"savings":0,"calls":2489},
#  "month":{"cost":6493.81,"savings":0,"calls":73300}}
```

**3 — plain-text overview, last 30 days (~3 s)** — real attribution, totals and breakdowns:

```text
CodeBurn  Last 30 Days
  Cost   $7,655.73    Tokens 9,814,450,396   Calls 87,625   sessions 4,315   Cache hit 99.8%

By tool      claude $7,653.86 (100%)   gemini $1.87 (0%)
Top models   Opus 4.8 $3,566.13 / 20,287 calls · Sonnet 4.6 $1,839.75 / 42,673 ·
             Opus 4.6 $1,598.21 · Fable 5 $435.63 · Opus 4.7 $148.64 · Haiku 4.5 $65.51 ·
             Gemini 3 Flash $1.87
```

The token breakdown is **96 % cache-read** (9.41B of 9.81B) — codeburn separates input / output / cache-in / cache-out, which is the whole game for pricing Claude spend correctly. It also emits a per-day table, highest-value days, and a top-projects table (project names redacted here for privacy).

**4 — `models` table, markdown, last 30 days (~113 s, the heaviest run)** — adds per-model task mix and efficiency columns:

```markdown
| Provider | Model      | Top Task          | Total   | Cost      |
| Claude   | Opus 4.8   | Coding (30%)      | 3915.4M | $3566.32  |
| Claude   | Sonnet 4.6 | Exploration (30%) | 2863.2M | $1839.75  |
| Claude   | Opus 4.6   | Refactoring (23%) | 2372.6M | $1598.21  |
| ...      | Total      |                   | 9814.8M | $7655.93  |
```

The CSV form of this table (`export`) carries `One-shot Rate (%)`, `Retries/Edit`, and `Cost/Edit (USD)` per model — the raw inputs to `compare`'s scoring.

**5 — `optimize` (text + JSON, ~12 s)** — the headline analysis. Setup-health grade and structured findings:

```text
CodeBurn config health  Last 30 Days
  4315 sessions   87,626 calls   $7655.76   Health: F (20/100, 13 issues)
  Potential savings: ~4421.6M tokens (~$2424.97, ~32% of spend)
```

`optimize --format json` returns `{period, summary, findings}` with `summary.healthScore=20`, `healthGrade="F"`, `findingCount=13`, `potentialSavingsPercent=31.7`. The **13 findings (12 `high`, 1 `medium`)** span concrete, paste-ready categories: Read:Edit ratio (1.6:1 vs healthy 4+), 6 MCP servers never called, 9 MCP servers with low tool coverage (each ~2 K tokens of schema per session), 3 MCP servers that should be project-scoped, a retry-correlated skill, 239 low-worth expensive sessions, 1008 context-heavy sessions, 165 high-cost outliers, re-read files, reads of build/dependency folders, an over-long `CLAUDE.md`, 36 unused skills, and a too-large bash output limit. Each finding ships a literal fix (`claude mcp remove <name>`, a `CLAUDE.md` line, an env var) ranked by token/dollar impact — the single largest being the 9 low-coverage MCP servers at ~462.3M tokens (~$253.52).

**6 — `yield`, last 30 days (~6 s)** — spend-vs-shipped via session↔commit correlation:

```text
Productive:  $5638.78 (74%) - 2558 sessions shipped to main
Reverted:       $4.17 (0%)  - 4 sessions were reverted
Abandoned:   $2012.96 (26%) - 1753 sessions never committed
Total:       $7655.90       - 4315 sessions
```

**7 — `export --format csv` (~3 s)** — writes a *directory* of CSVs (not a single file; the `-o` path becomes a folder with a `.codeburn-export` marker), one per view: `summary.csv`, `models.csv`, `tools.csv`, `projects.csv` (237 rows), `sessions.csv` (2807 rows), `mcp.csv`, `daily.csv`, `activity.csv`, `shell-commands.csv`, plus a `README.txt`. The aggregate `tools.csv` for a one-week window ranked tool calls `Bash 68.4% · Read 12.9% · Edit 9.3% · Write 3.2% · ...` across 28 tool types — a genuine cross-tool attribution surface, not a token table.

**Internal consistency:** every command's total agreed to within rounding across the same window — `overview` $7,655.73, `optimize` $7,655.76, `models` $7,655.93, `yield` $7,655.90 — and the figures track the host's session volume (220 project dirs, 4,315 sessions). We did **not** reconcile against an actual Anthropic invoice, so the dollar figures remain LiteLLM-priced *estimates*; the cross-command agreement validates codeburn's internal arithmetic, not the upstream prices.

```bash
# full reproducible run (Node >= 22.13)
npx --yes codeburn@latest status   --format json --period 30days
npx --yes codeburn@latest overview --period 30days --no-color
npx --yes codeburn@latest models   --period 30days --format markdown
npx --yes codeburn@latest optimize --format json
npx --yes codeburn@latest yield    --period 30days
npx --yes codeburn@latest export   --format csv --output ./cb_export --from 2026-06-15 --to 2026-06-22
```

## What worked

- **It genuinely parses real session data and produces coherent, cross-checking attribution.** Five commands independently reported the same ~$7,655 30-day total to the rounding digit, broken down by tool (claude/gemini), 7 models, 235 projects, and per-day — all from local logs, zero config, zero keys. This is a working data pipeline, not a mock.
- **Correct token taxonomy.** It splits input / output / cache-write / cache-read (96 % of these tokens were cache-read) — the distinction that makes Claude cost numbers meaningful. A naive total-token counter would misprice this by an order of magnitude.
- **`optimize` is uncommonly actionable — and the findings are specific.** A grade (F, 20/100), a quantified savings ceiling (~$2,425, ~32 %), and 13 ranked findings each with a literal paste-able command (`claude mcp remove computer-use`, a Read-before-Edit `CLAUDE.md` rule). It named exact unused/low-coverage MCP servers with session counts — config hygiene a human would never audit by hand.
- **`yield` ran headless and answered the question token counters can't:** 74 % of spend shipped to main, 26 % abandoned, <1 % reverted. Directional, but it ties dollars to outcomes.
- **JSON/CSV export is real and structured** — `optimize --format json` gives a clean `{summary, findings[]}` with severities; `export` drops a 9-file CSV bundle (sessions, projects, models, tools, MCP, shell commands). Easy to pipe into other analysis.
- **Local-only, fast.** Most commands finished in 3–17 s over 4,315 sessions; nothing left the machine.

## What didn't work or surprised us

- **Hard Node 22.13+ gate.** On the host default Node v20.19.5 it refuses to run (`codeburn requires Node.js >= 22.13.0`). Stock-LTS users will hit this immediately; we had to switch to Node v24.9.0.
- **The headline surfaces (`report`, `today`, `month`, `web`, `menubar`) and `compare` are interactive-only.** `compare` flatly errors `Model comparison requires an interactive terminal.` headless — so the per-model one-shot/retry scoring is TUI-gated (though its raw inputs *are* in the `models` CSV). Not exercised here.
- **`export -o foo.csv` produces a *directory* named `foo`, not a CSV file.** The `--output` path is treated as a folder; a script expecting a single CSV at that path will find nothing. Minor but a real footgun.
- **`models` was slow (~113 s)** versus 3–17 s for the others — the per-task explosion over thousands of sessions is the expensive path.
- **`optimize`'s setup heuristics can over-flag.** "Unused" MCP servers and "ghost" skills are inferred from observed invocations in the window; it even labels the skill-retry finding "a correlation report, not proof of causation." A rarely-but-legitimately-used server gets flagged as waste, so its `mv`/`remove` fixes need human judgment.
- **Dollars are LiteLLM-priced estimates, not invoices.** Cross-command agreement proves internal consistency, not upstream price accuracy; we did not reconcile against actual billing.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Cost Efficiency | + + | Measured: per-tool/model/project/day attribution across the whole local AI bill, plus `optimize` quantifying a ~$2,425 (~32 %) savings ceiling with 13 paste-ready fixes and an F grade, plus `yield` showing 26 % of spend abandoned. Directly drives spend down — *if* you act on it and treat dollars as estimates. |
| Speed | neutral | Runs out-of-loop; doesn't speed or slow any session. Most commands 3–17 s; `models` ~113 s. `optimize`'s retry/re-read fixes can indirectly reduce future-session waste. |
| Correctness | + / − | `models`/CSV expose one-shot/retry/cost-per-edit per model to inform selection; but the tool's own figures are log-derived LiteLLM estimates, not verified billing (unreconciled here). |
| Maintainability | + | `optimize` flagged an over-long `CLAUDE.md`, 36 unused skills, and 15 unused/low-coverage/mis-scoped MCP servers — concrete config-hygiene wins that keep an AI setup lean. |
| Safety | + | Local-only, no proxy/keys/network egress observed; reads local logs only. Lowest-risk class of tool. |

## Verdict

**ADOPT (with a caveat) — confirmed hands-on as the most actionable AI-spend tool in this catalog, provided you treat its dollar figures as estimates.** Run end-to-end (v0.9.14) against this machine's real 4,315-session Claude history, codeburn produced coherent, cross-checking attribution (five commands agreed on a ~$7,655 30-day total), a correct cache-aware token taxonomy, and — the real differentiator — an `optimize` pass that graded the setup F (20/100), named a ~$2,425 / 32 % savings ceiling, and emitted 13 ranked paste-ready fixes, plus a `yield` pass showing 26 % of spend never shipped. All of this ran headless with JSON/CSV export. Two caveats keep it from unqualified adoption: it requires Node ≥ 22.13 (refuses to run on the v20 LTS default), and every dollar is a LiteLLM-priced estimate, not an invoice — so reconcile against actual billing before acting on a big number. The headline TUI dashboards and `compare` are interactive-only and were not driven, but the analysis/export layer alone carries the value for a Reflect-loop cost audit.

Compared to neighbors: **tokencost** is a *library* for estimating token cost programmatically — a building block, where CodeBurn is the finished, multi-tool product. **abtop** is a live `top`-style monitor for a running agent (real-time, single-session focus); CodeBurn is retrospective, cross-tool, and analysis-oriented. **rtk** is a usage/rate-limit-leaning toolkit; CodeBurn's `optimize`/`yield` analysis layer and ~30-tool breadth are broader. CodeBurn wins on actionability (paste-ready fixes), breadth, and local-first trust; it's weaker than a billing API for ground-truth dollar accuracy.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codeburn](https://github.com/getagentseal/codeburn) | tool | Local-first TUI/menubar that parses on-disk session logs to attribute AI spend by task/model/tool/project across ~30 tools, with waste-finding fixes and spend-vs-shipped analysis | Your AI bill shows a total but never says where it went, which model wasted budget, or whether the spend actually shipped — CodeBurn breaks it down locally and emits ranked fixes | tokencost (cost-estimation library, a building block); abtop (live single-session monitor vs retrospective); rtk (usage/rate-limit toolkit) |

**Target category:** Observability (cost/usage analytics; outer-loop / Reflect, Cost signal)
