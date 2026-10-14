# Evaluation: claude-flightdeck

**Repo:** [scasella/claude-flightdeck](https://github.com/scasella/claude-flightdeck)
**Stars:** 84 | **Last updated:** 2026-10-14 (pushed) | **License:** MIT
**Last verified:** 2026-10-14
**Last triaged:** 2026-10-14  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A Claude Code mod that puts a live agent dashboard in the terminal: context and cost,
an advisor timeline, every permission check, and subagent cards/swimlanes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for triage,
not for a verdict, and this eval offers none.

## Verdict

**discovery-log — tentative read**

## Triage note

Banded P2 challenger against `abtop` (both are local session-observability tools),
but `abtop`'s real-time multi-project TUI and claude-flightdeck's single-session
terminal dashboard (permission-check log, subagent cards/swimlanes, cost/context
advisor) are different presentations of different scopes — closer in spirit to
`claude-devtools`. Too new (84 stars, 12 days old) to call redundant; left at
`discovery-log` for a real hands-on eval rather than a mechanical SKIP.

_Triaged 2026-10-14 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-flightdeck](https://github.com/scasella/claude-flightdeck) | plugin | Live Claude Code dashboard (MIT) in the terminal — context and cost, an advisor timeline, every permission check, and subagent cards/swimlanes | Claude Code with subagents gives no live terminal view of context, cost, permission checks, or what each subagent is doing | claude-devtools, claude-hud, abtop |
