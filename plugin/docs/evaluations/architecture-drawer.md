# Evaluation: architecture-drawer

**Repo:** [Andy1314Chen/architecture-drawer](https://github.com/Andy1314Chen/architecture-drawer)
**Stars:** 18 | **License:** MIT
**Last verified:** 2026-08-05
**Last triaged:** 2026-08-05  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Process (skill)

---

## What it does

A skill for Claude Code & Codex that turns a text description of a system architecture into
an editable PowerPoint diagram — native shapes, not a flat rendered image.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (excalidraw-diagram-skill, graphify,
powerpoint). That is sufficient to place the lead, not to support an ADOPT — this eval
offers none.

## Triage note

Left at `discovery-log`: excalidraw-diagram-skill outputs Excalidraw diagrams, not editable
PPTX; the generic `powerpoint` skill handles layout/templates but not architecture-specific
diagramming. Native-shape PPTX output from a text architecture description is a real, narrow
gap worth a hands-on look rather than a redundancy SKIP.

_Triaged 2026-08-05 by the daily discovery routine (today's new lead)._
