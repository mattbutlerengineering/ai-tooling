# Evaluation: cline-pilot

**Repo:** [gongdear/cline-pilot](https://github.com/gongdear/cline-pilot)
**Stars:** 75 | **Last updated:** 2026-09-29 (pushed) | **License:** MIT
**Last verified:** 2026-10-01
**Last triaged:** 2026-10-01  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An Agent Skill that drives Cline CLI coding tasks as the user's proxy: dispatches work to Cline,
monitors progress through session files and git evidence, learns user preferences over time to
gradually automate decision-making, and runs a verification checklist before marking work done.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to support an
ADOPT, and none is offered here.

## Triage note

Left at `discovery-log`. Cites `claude-squad` (STACK, CONDITIONAL/RUN) in "Overlaps with", which
bands this P2, but the jobs differ: `claude-squad` manages multiple parallel agent terminals
(Claude Code, Codex, OpenCode, Amp); `cline-pilot` is narrower and single-tool — it proxies and
progressively automates decisions for one specific CLI (Cline), not a fleet manager. New (two days
old, 75 stars) with no adoption signal, but a genuinely different mechanism (trust-building proxy
vs. parallel fleet orchestration) worth a real look rather than a mechanical SKIP.

_Triaged 2026-10-01 by the P2 challenger band (today's new lead)._
