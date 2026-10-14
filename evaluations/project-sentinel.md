# Evaluation: project-sentinel

**Repo:** [Arjun0014/project-sentinel](https://github.com/Arjun0014/project-sentinel)
**Stars:** 49 | **Last updated:** 2026-10-14 (pushed) | **License:** MIT
**Last verified:** 2026-10-14
**Last triaged:** 2026-10-14  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

Mission control for long Claude Code runs: context and run progress at a glance,
Autopilot handoffs to a fresh context before the window fills, guardrails, and a
calm activity view — in the terminal and Claude Desktop.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read**

## Triage note

Triage bands this P2 challenger against `headroom`, but `headroom`'s job is
compressing tool output before it reaches the model, which is not what
project-sentinel does. Its actual closest peer is `ctx-handoff-mod` (automatic
handoff on context fill) and `claude-rein` (session handover before exhaustion) —
both cited in the "Overlaps with" cell. Not plainly dominated by either (different
UI: Autopilot handoffs plus a guardrails/activity view, not just a handoff
trigger); left at `discovery-log` for a real hands-on eval rather than a mechanical
SKIP.

_Triaged 2026-10-14 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [project-sentinel](https://github.com/Arjun0014/project-sentinel) | plugin | Mission control (MIT) for long Claude Code runs — context/progress at a glance, autopilot handoffs before context exhausts, guardrails, and a calm activity view | Long Claude Code runs give no at-a-glance context/progress view or automatic handoff before the window fills | ctx-handoff-mod, claude-rein, headroom |
