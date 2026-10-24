# Evaluation: whatsmyagentdoing

**Repo:** [Charonyuu/whatsmyagentdoing](https://github.com/Charonyuu/whatsmyagentdoing)
**Stars:** 80 | **Last updated:** 2026-10-24 (pushed) | **License:** MIT
**Last verified:** 2026-10-24
**Last triaged:** 2026-10-24  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop (session/agent observability)
**Layer:** Tooling

---

## What it does

A Claude Code/Codex/Gemini CLI skill: type `/myoffice` and see every agent running on
the machine live, rendered as a 3D office — agents at their desks when working, off
duty ones wandering around. Also ships 2D and list views.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Triage banded this as a P2 challenger against `abtop` (pressure 0 — the citation is
one-directional so far). `abtop`'s real-time TUI and `claude-super-sidebar`/
`agent-orchestration-standard`'s dashboard views already cover "what is every agent
doing right now," but the presentation here (a spatial, ambient 3D scene rather than
a terminal/dashboard) is a different interaction model, same shape as `roundtable`'s
pixel-art replay being kept distinct from `abtop` in an earlier pass. Too new (created
2026-10-23) and too differentiated in presentation to call redundant yet. Left at
`discovery-log` for a real hands-on eval rather than a mechanical SKIP.

_Triaged 2026-10-24 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [whatsmyagentdoing](https://github.com/Charonyuu/whatsmyagentdoing) | skill | Claude Code/Codex/Gemini CLI skill (MIT) rendering every agent on the machine live, in a 3D office view | Running several agent sessions across terminals gives no at-a-glance visual view of what each is doing | agent-orchestration-standard, claude-super-sidebar, roundtable, abtop |
