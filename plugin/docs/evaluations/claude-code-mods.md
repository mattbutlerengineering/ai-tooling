# Evaluation: claude-code-mods

**Repo:** [karanb192/claude-code-mods](https://github.com/karanb192/claude-code-mods)
**Stars:** 31 | **Last updated:** 2026-09-18 (pushed) | **License:** MIT
**Last verified:** 2026-09-20
**Last triaged:** 2026-09-20  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (authoring/improving the tools the loop itself uses)
**Layer:** Tooling

---

## What it does

A builder skill for authoring "Claude Mods" — hook-based Claude Code behavior tweaks —
plus a library of already-published mods.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (skill-creator, plugin-dev, cache-tax).
That is sufficient to place the lead and note its named overlaps' STACK member
(skill-creator) targets a different artifact, not to support an ADOPT — this eval offers
none.

## Triage note

Left at `discovery-log`: challenges `skill-creator` (a STACK pick, ADOPT/MEASURED) in the
P2 challenger band, but skill-creator authors SKILL.md skills through a draft/eval/
benchmark pipeline, while claude-code-mods builds hook-based behavior tweaks ("mods") —
a different artifact with a different authoring loop. Not redundant on the stated job.
Left for the P0/eval-runner lane.

_Triaged 2026-09-20 by today's discovery lead._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-mods](https://github.com/karanb192/claude-code-mods) | skill | Builder skill for authoring "Claude Mods" — hook-based Claude Code behavior tweaks — plus a library of published mods | Writing a Claude Code hook/behavior tweak from scratch each time has no shared authoring workflow or mod library | skill-creator, plugin-dev, cache-tax |
