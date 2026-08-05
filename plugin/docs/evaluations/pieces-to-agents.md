# Evaluation: pieces-to-agents

**Repo:** [tiagolauer/pieces-to-agents](https://github.com/tiagolauer/pieces-to-agents)
**Stars:** 11 | **License:** MIT
**Last verified:** 2026-08-05
**Last triaged:** 2026-08-05  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling (CLI)

---

## What it does

Converts Pieces Long-Term Memory into an AGENTS.md file coding agents can read — local-only
and redaction-first.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (memory-os, microsoft/skills, claude-mem).
That is sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: memory-os and claude-mem are self-contained memory stores, not
bridges from a third-party memory product (Pieces); microsoft/skills' AGENTS.md usage is
Microsoft-SDK-specific. A dedicated, redaction-first Pieces→AGENTS.md exporter is a narrow
niche with no catalogued incumbent, worth a hands-on look rather than a redundancy SKIP.

_Triaged 2026-08-05 by the daily discovery routine (today's new lead)._
