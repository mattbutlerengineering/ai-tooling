# Evaluation: dsh-TUI

**Repo:** [ccch1mneyyy/dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI)
**Stars:** ~3,000 | **Last updated:** 2026-09-14 (pushed) | **License:** MIT
**Last verified:** 2026-09-14
**Last triaged:** 2026-09-14  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Claude-Code-style terminal UI plugin for DeepSeek Harness — status bar, streaming thoughts, context/TPS gauges, double-Esc rollback.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG one-liner and "Overlaps with" cell; no cached `repo-metadata.json` record existed for this repo, so the star count above is read directly from the GitHub repo page rather than the metadata cache.

## Verdict

**discovery-log — tentative read** — not previously examined; picked up as one of the oldest untriaged leads in the P3 backlog this pass.

## Triage note

P3 backlog (no STACK overlap flagged — `ccstatusline`/`claude-hud` are Claude-Code-specific, not DeepSeek-Harness). Fills a real gap (DSH has no first-party TUI polish) rather than duplicating a STACK pick. Left at discovery-log.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) | plugin | Claude-Code-style terminal UI plugin (MIT) for DeepSeek Harness — status bar, streaming thoughts, context/TPS gauges, double-Esc rollback | DeepSeek Harness ships no built-in TUI polish; want Claude-Code-grade session visibility | ccstatusline, claude-hud, deepseek-harness |  |
