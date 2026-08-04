# Evaluation: skill-recorder

**Repo:** [microsoft/skill-recorder](https://github.com/microsoft/skill-recorder)
**Stars:** 1655 | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling (Electron desktop app)

---

## What it does

A desktop app, by Microsoft, that records an on-screen work session and uses the GitHub
Copilot CLI to reconstruct it as an intent plus ordered steps, then builds a reusable Skill
or Automation for Microsoft Scout, Microsoft Copilot Cowork, or Copilot Studio.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (skill-creator, Skill_Seekers,
agent-skill-creator). That is sufficient to place the lead, not to support an ADOPT — this
eval offers none.

## Triage note

Left at `discovery-log` rather than SKIPped as redundant with `skill-creator` (ADOPT/KEEP in
STACK): skill-creator is a manual meta-skill for authoring `SKILL.md`, while skill-recorder
generates a skill from a recorded screen session via Copilot CLI — a materially different
input method, and it targets the Microsoft Scout/Cowork/Studio surfaces rather than
`SKILL.md` directly. Worth a hands-on eval to see whether the recorded-session approach
transfers to our SKILL.md workflow.

_Triaged 2026-08-04 by the daily discovery routine (today's new lead)._
