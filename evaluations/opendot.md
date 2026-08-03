# Evaluation: opendot

**Repo:** [vedaant00/opendot](https://github.com/vedaant00/opendot)
**Stars:** 18 | **Last updated:** 2026-08-03 (pushed) | **License:** MIT
**Last verified:** 2026-08-03
**Last triaged:** 2026-08-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Terminal AI agent you can fully undo — every file and shell action is snapshotted and reversible,
model-agnostic, connects to 1000+ app tools and MCP servers.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (gptme, aider, pi, command-code). That is sufficient to place
the lead and note none of its named overlaps is a STACK incumbent, not to support an ADOPT — this
eval offers none.

## Triage note

Left at `discovery-log`: gptme/aider/pi/command-code are all terminal coding-agent harnesses, but
none of them advertise full snapshot-based undo of every file/shell action as opendot does; that
reversibility guarantee is a real differentiator worth a first-time look, not a mechanical SKIP.
Left for the P0/eval-runner lane.

_Triaged 2026-08-03 by today's discovery lead._
