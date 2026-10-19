# Evaluation: modelplan

**Repo:** [modelplan/modelplan](https://github.com/modelplan/modelplan)
**Stars:** 19 | **Last updated:** 2026-10-19 (pushed) | **License:** MIT (data: CC BY 4.0)
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Answers "which AI coding model, at which reasoning effort, and is one more step up worth it"
from live, checkable public data — recommended efforts, a leaderboard at those efforts, and
plan advice from modelplan.ai — surfaced inside Claude Code, Codex, and the terminal (plugins,
Skill, CLI).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the README,
the CATALOG one-liner, and GitHub repo metadata (stars, license, topics). No hands-on run was
performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

New lead, cataloged today. P3 backlog — zero overlap pressure. Closest peers (`deadeye-cc`,
`agent-router`, `claude-code-routing`) are themselves discovery-log leads, not STACK picks, so
not a P2 challenger. Left at `discovery-log`; stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [modelplan](https://github.com/modelplan/modelplan) | tool | Recommends which coding model to use, at which reasoning effort, from live checkable public data (MIT) — in Claude Code, Codex, and the terminal | Picking a model and reasoning effort per task is manual guesswork with no data-backed recommendation or leaderboard to check it against | deadeye-cc, agent-router, claude-code-routing |  |
