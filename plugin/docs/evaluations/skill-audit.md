# Evaluation: skill-audit

**Repo:** [cth9191/skill-audit](https://github.com/cth9191/skill-audit)
**Stars:** 33 | **Last updated:** 2026-09-16 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-17
**Last triaged:** 2026-09-17  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling

---

## What it does

Audits installed AI agent skills — reviews usage evidence and compares a skill's original,
simplified, and baseline-agent-without-the-skill workflows, to decide whether to keep, repair, or
retire it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (waza (Microsoft), skillfid, SkillOpt). That is sufficient to
place the lead, not to judge the tool's behaviour hands-on.

## Triage note

Left at `discovery-log`. Directly relevant to this catalog's own concern with skill test-design
(with-skill-vs-baseline evidence, `TEMPLATE.md`'s "Test design — skills" section) — worth a real
look rather than a mechanical disposition. Small (★33) and brand new; not enough adoption signal
yet to call ADOPT-worthy, and no named incumbent it is clearly dominated by (`waza (Microsoft)`
benchmarks skill quality generally, `skillfid` checks documentation-vs-execution fidelity — neither
does this tool's keep/repair/retire comparison).

_Triaged 2026-09-17 by the P3 backlog band._
