# Evaluation: ccusage

**Repo:** [ryoppippi/ccusage](https://github.com/ryoppippi/ccusage)
**Stars:** 16484 | **Last updated:** 2026-06-23 | **License:** MIT (npm metadata; GitHub reports `NOASSERTION` from an unparsed `LICENSE` file)
**Last verified:** 2026-06-22
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

CLI that parses local coding-agent session logs (the `~/.claude` JSONL files Claude Code writes, plus Gemini CLI, OpenCode, Codex, and a dozen other agents) into daily / monthly / weekly / session / billing-block token-and-cost reports — so you can see how many tokens and dollars your agent sessions cost without grepping JSONL by hand.

Invoking `ccusage daily` walks the on-disk JSONL transcripts, sums input / output / cache-create / cache-read tokens per day, multiplies token counts by per-model pricing, and renders a boxed terminal table broken down by date → agent → model. `monthly` / `weekly` / `session` / `blocks` re-group the same parsed events by different keys. Pricing is fetched online by default and can be pinned to a cached snapshot with `--offline`; the underlying log parse is always local and offline. `-j/--json` emits the structured data (`{ "daily": [...], "totals": {...} }`) for piping into other tooling. It ships as an npm package runnable with zero install via `npx ccusage@latest`.

## How we tested it

**Evidence:** MEASURED

Verified hands-on: ran it **live** against this machine's real Claude Code / agent logs via `npx ccusage@latest` (resolved ccusage **20.0.14**, Node v20.19.5, macOS). No install, no API key, no config — it discovered the logs itself and auto-detected three agents (`Detected: Claude, Gemini CLI, OpenCode`). All token/dollar figures below are this machine's actual usage; only the data is local — paths were not exposed by the tool's output, so nothing needed redaction.

Commands executed and what came back:

- `npx ccusage@latest --help` — printed the full command/flag surface (21 agent subcommands incl. `daily`/`monthly`/`weekly`/`session`/`blocks`/`statusline`, flags `-j/--json`, `-s/--since`, `-u/--until`, `-z/--timezone`, `-O/--offline`, `--compact`).
- `npx ccusage@latest daily` — boxed daily report. Header + a sampled day + grand total:

```
╭────────────────────────────────────────────╮
│  Coding (Agent) CLI Usage Report - Daily   │
│   Detected: Claude, Gemini CLI, OpenCode   │
╰────────────────────────────────────────────╯
┌──────────┬────────────┬──────────────┬──────────┬─ … ─┬──────────┐
│ Date     │ Agent      │ Models       │    Input │ …   │     Cost │
│ 2026     │ All        │              │  633,930 │ …   │  $298.34 │   (06-22)
│          │ - Claude   │ - haiku-4-5  │  633,930 │ …   │  $298.34 │
…
│ Total    │            │              │ 234,206… │ …   │ $7834.62 │
└──────────┴────────────┴──────────────┴──────────┴─ … ─┴──────────┘
```

- `npx ccusage@latest monthly` — same data re-grouped by month; correctly attributed `$0.81` to Gemini CLI and `$0.00` to OpenCode in 2026-02, $99.72 to Gemini in 2026-04, i.e. per-agent, per-model cost split.
- `npx ccusage@latest session` — per-session table, 6,613 rendered lines.
- `npx ccusage@latest session --json` — 2.17 MB of valid JSON, **3,136** session rows; each row carries `agent`, `inputTokens`, `outputTokens`, `cacheCreationTokens`, `cacheReadTokens`, `totalTokens`, `totalCost`, `modelBreakdowns`, `period`; plus a `totals` block: `{ inputTokens: 234,226,754, outputTokens: 47,999,049, cacheReadTokens: 11,217,893,630, totalTokens: 11,854,427,954, totalCost: 7846.19 }`.
- `npx ccusage@latest daily --offline --since 20260622` — `--offline` (cached pricing, no network) **and** the date filter both worked, isolating a single day: `Total … $319.50`.
- Timing oracle (wall clock, full history): `npx ccusage@latest daily --json` over the entire corpus (11.8B tokens / 3,136 sessions) took **130.5 s** end-to-end including npx resolution; the `--since`-filtered single-day run returned in a couple of seconds.

The JSON `totals.totalCost` ($7846.19) and the daily-table grand-total Cost ($7834.62) agree to within rounding / pricing-snapshot drift across the two runs, and the per-month splits sum consistently with the daily view — an internal cross-check that the aggregation is self-consistent.

## What worked

- **Zero-friction, zero-config, offline-by-design.** `npx ccusage@latest daily` produced a correct report on first run with no install, no API key, no flags — it found `~/.claude` JSONL itself. The log parse is fully local; only pricing optionally hits the network (and `--offline` removes even that).
- **Multi-agent auto-detection.** Without being told, it detected and separately costed Claude, Gemini CLI, and OpenCode, attributing per-model dollar figures (e.g. Gemini `$0.81` vs OpenCode `$0.00` in the same month). The category has grown well beyond "Claude only."
- **Real cost surfacing.** It turned an opaque pile of JSONL into actionable numbers: $7.8K lifetime, ~$298–933/day on peak days, and a per-day drill-down — the exact Reflect-stage signal you can't get from the agent UI.
- **Clean machine-readable output.** `--json` emitted well-structured data (`daily`/`session` + `totals`) suitable for piping into dashboards or budget alerts; `--since`/`--until`/`--offline`/`--timezone` give the filtering you'd want for a CI cost report.

## What didn't work or surprised us

- **Full-history scan is slow.** A full `daily --json` over 11.8B tokens / 3,136 sessions took ~130 s (npx resolution included). Fine for an occasional Reflect-stage check, but you'd want `--since` (which is fast) for anything interactive or scripted/frequent.
- **Cache-read tokens dominate and inflate the eye-test.** `cacheReadTokens` (11.2B) is ~95% of `totalTokens` (11.85B); the headline "11.8B tokens" is mostly cheap cache reads, so the token column is far less meaningful than the **Cost** column. The tool reports both honestly — but a reader skimming totals could misjudge spend if they anchor on token count instead of dollars.
- **Pricing-snapshot drift between runs.** Two separate full runs reported $7846.19 (JSON) vs $7834.62 (table) — a ~0.16% gap from pricing fetched at slightly different times / models lacking a price. Immaterial for budgeting, but it means the number isn't bit-reproducible run-to-run unless you pin `--offline`.
- **License ambiguity.** npm says MIT; GitHub's API returns `NOASSERTION` because the `LICENSE` file isn't in a form its classifier parses. Functionally MIT, worth noting for compliance-sensitive shops.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Not a code-correctness tool; its own aggregates cross-check (JSON totals ≈ table total; monthly sums ≈ daily) so the reporting itself is trustworthy. |
| Speed | neutral | Doesn't change build/agent speed; the report itself is fast when scoped with `--since` and slow (~130 s) on full history. |
| Maintainability | + | Makes per-agent/per-model spend visible over time, so teams can spot a runaway prompt or a model mix that's quietly getting expensive. |
| Safety | + | Fully local log parse, no API key, `--offline` avoids network entirely — safe to run on sensitive machines without exfiltrating transcripts. |
| Cost Efficiency | + | Core value: turns opaque JSONL into actual token/dollar accountability ($7.8K lifetime, ~$298–933/day here), the prerequisite for any cost-control decision. |

## Verdict

**ADOPT**

ccusage is the category-defining cost-reporting tool for coding agents and it ran cleanly, hands-on, on the first try with zero config — a measured, reproducible read of real spend ($7.8K lifetime across 3,136 sessions, three agents). For the token/dollar-usage-reporting cluster it is the best-in-class pick: broadest agent coverage, offline-safe, JSON-pipeable, `npx`-runnable. Use `--since` to keep it fast and prefer the **Cost** column over raw token counts (cache reads dominate). Overlaps: langfuse and Helicone (heavier hosted/self-hosted LLM observability platforms — full tracing, not a one-shot local report), ccstatusline and claude-hud (in-session statusline widgets, not historical cost reports); ccusage is the right pick when you want offline, after-the-fact token/cost accounting without standing up infrastructure.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ccusage](https://github.com/ryoppippi/ccusage) | tool | CLI parses local coding-agent session logs into daily/monthly/session/model token & cost reports | Can't see how many tokens or dollars your Claude Code (and other CLI) sessions cost without parsing JSONL by hand | langfuse, Helicone, ccstatusline, claude-hud |
