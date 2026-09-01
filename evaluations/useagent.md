# Evaluation: useagent

**Repo:** [useagenthq/useagent](https://github.com/useagenthq/useagent)
**Stars:** 265 | **Last updated:** 2026-08-31 (pushed) | **License:** AGPL-3.0
**Last verified:** 2026-09-01
**Last triaged:** 2026-09-01  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure (cloud sandbox running Claude Code/Codex/OpenCode on the user's own subscription)

---

## What it does

An open-source "AI coworker" that gives agents their own cloud computer with your tools and context, running Claude Code, Codex, or OpenCode on your own subscription and handing back finished work (websites, decks, spreadsheets, reports, PRs).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: GitHub repo
metadata (license, description, topics). That is sufficient for the verdict below, because the
verdict turns on the license bar, not on the tool's behaviour. It would not be sufficient to
support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — AGPL-3.0. This repo is infrastructure you would run as a service, not a vendored
skill/plugin, but the daily-discovery license bar for this pass treats any copyleft or missing
license as a mechanical SKIP rather than a judgement call. Re-evaluate if the project relicenses
to permissive terms, or if a human wants to assess AGPL's actual exposure for a
self-hosted-only deployment.

_Triaged 2026-09-01 by the daily discovery pass's license bar._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [useagent](https://github.com/useagenthq/useagent) | tool | Open-source cloud "AI coworker" (⚠️ AGPL-3.0) — runs Claude Code, Codex, or OpenCode on your own subscription inside a cloud computer with your tools/context, handing back finished PRs/decks/reports | Running long agent tasks needs a persistent cloud sandbox with real tool/context access, not just a terminal session on your laptop | claude-squad, agent-of-empires, vercel-sandbox |
