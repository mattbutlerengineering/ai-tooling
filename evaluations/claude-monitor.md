# Evaluation: claude-monitor

**Repo:** [Maciek-roboblog/Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor)
**Stars:** 8407 | **Last updated:** 2026-07-05 | **License:** MIT
**Last verified:** 2026-07-08  <!-- source-grounded re-check; not a hands-on re-verification -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

A Python CLI (`claude-monitor`, aliases `cmonitor`/`ccmonitor`) that reads Claude Code's on-disk session transcripts and renders a live Rich terminal HUD of token/message/cost usage, burn-rate, and limit forecasts against plan windows. The v4.0 "Usage Ops" release adds a **trust layer**: `--statusline` captures Claude Code's *official* `rate_limits` payload and labels every number with a provenance tag (`official`, `local_estimate`, `experimental`, `unknown`), so a stale official capture degrades to a clearly-labeled local estimate rather than a silent guess. A machine-readable snapshot protocol (`--once`, `--compact`, `--write-state`, `--output json`) gives GUIs/trays/status bars one versioned contract, and an opt-in **persistent usage warehouse** survives Claude's 30-day cleanup with project/model/day dimensions and CSV/JSON reports.

## How we tested it

**Evidence:** REVIEW

**Source-grounded review — not run hands-on.** I did not install or execute `claude-monitor`; every claim below comes from the repository (GitHub metadata, README, the PyPI package `claude-monitor` v4.0.0, and the documented CLI surface), not from an observed run. No metrics below are mine — the burn-rate / forecast behavior is described as the tool's claimed mechanism, and any numbers are the vendor's or my reading of the docs, not measured. The install command was verified to resolve against PyPI, but no session was pointed at it and no live HUD was watched.

```bash
# documented install (verified to resolve on PyPI; not executed end-to-end)
uv tool install claude-monitor        # or: pip install claude-monitor
claude-monitor --statusline           # capture official rate_limits (not run)
claude-monitor --once --output json   # machine-readable snapshot (not run)
```

## Test design

> Not run — see honesty rule above. A Reflect-stage cost monitor's measurable questions are (a) does the official-limit capture match `ccusage`'s attribution on the same sessions, (b) burn-rate forecast accuracy vs the real reset boundary, and (c) overhead while running live. None were executed here; this is a review of the documented mechanism, not a measurement.

## What worked

- **Provenance labels are the real differentiator.** Tagging each value `official`/`local_estimate`/`experimental`/`unknown` — and downgrading a stale `--statusline` capture to a labeled estimate — directly addresses the credibility gap that makes raw token monitors misleading. This is something neither `ccusage` nor `abtop` surface as explicitly.
- **Consumes the official `rate_limits` payload.** Reading Claude Code's own statusline `rate_limits` (not just transcript-derived estimates) is the most accurate input available post-ratelimit-reset, and the design consciously separates official from inferred.
- **External-companion boundary is clean.** A single versioned snapshot contract (`--write-state`/`--once --output json`) plus automation exit codes means GUIs/trays/status bars consume one stable interface rather than screen-scraping the Rich UI — a thoughtful separation for a monitoring tool.
- **Persistent warehouse.** Surviving Claude's 30-day session cleanup with project/model/day dimensions is a genuinely useful historical feature the live-only peers lack by default.
- **Healthy maintenance and reach.** 8.4K stars, v4.0.0 on PyPI, codecov coverage, Awesome Claude Code mention, same-week commit activity.

## What didn't work or surprised us

- **Overlaps heavily with two already-installed tools.** `ccusage` is ADOPT/MEASURED (aggregation/reporting) and `abtop` is CONDITIONAL/MEASURED (live TUI). claude-monitor's live Rich HUD overlaps `abtop`'s core job and `ccusage`'s reporting job; the decision for an existing adopter is whether the provenance/trust layer alone justifies a third monitor.
- **Not run, so accuracy of attribution and forecasts is unverified here.** The forecast/pace and "official-only weekly percentages" behavior is the vendor's described mechanism; I did not compare its numbers to a known-good baseline.
- **Python dependency and multi-source path complexity.** `--data-paths`/`CLAUDE_CONFIG_DIR`/WSL discovery add configuration surface; a wrong path could merge unrelated accounts into one 5-hour window if misconfigured.
- **Cost figures remain transcript-derived unless `--statuslines` is on.** Like all monitors in this category, absolute cost is only as trustworthy as the per-call token attribution Claude writes to transcripts.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Provenance labels improve *honesty* of displayed numbers, not their underlying accuracy; attribution still derives from transcripts unless `--statusline` official limits are captured |
| Speed | + | Live burn-rate HUD lets you react to a runaway session before the window resets |
| Maintainability | neutral | No effect on the code under development |
| Safety | + | Local-only, privacy-first, opt-in warehouse; no telemetry described |
| Cost Efficiency | + | Forecast + limit-hit warnings prevent burning an entire window on one task |

## Verdict

**CONDITIONAL**

Adopt claude-monitor when you want a *live* (real-time Rich HUD) token/cost monitor with an explicit provenance/trust layer over Claude's official `rate_limits`, and either you don't already run `abtop` or you specifically want the `official`/`local_estimate` labeling + persistent usage warehouse that `abtop` and `ccusage` don't surface. If you already run `ccusage` (aggregated reports) and `abtop` (live TUI) and are satisfied, claude-monitor's provenance labels are a nice-to-have, not a reason to run a third monitor — the overlap with both is substantial. Review-only: the forecast accuracy and attribution parity I'd want before an ADOPT were not measured here; a hands-on run comparing its `--statusline` capture to `ccusage` on the same sessions is the natural graduation step.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) | tool | Real-time terminal monitor for Claude Code token usage with daily/monthly cost breakdowns and burn-rate predictions | Want live + historical token/cost tracking against Claude's session windows with limit warnings | ccusage, ccstatusline, claude-hud |