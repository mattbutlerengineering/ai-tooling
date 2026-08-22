# Evaluation: zoetrope

**Repo:** [furkankly/zoetrope](https://github.com/furkankly/zoetrope)
**Stars:** 152 | **Last updated:** 2026-08-22 (pushed) | **License:** MIT
**Last verified:** 2026-08-22
**Last triaged:** 2026-08-22  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop (Observability)
**Layer:** Tooling

---

## What it does

Watches a running Claude Code session and renders it as a live flow graph — in the terminal or a browser — instead of a scrolling transcript.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a leave decision that turns on differentiation from existing observability entries, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. The Observability category already carries several session-visualization tools (`claude-devtools`, `roundtable`, `claude-code-hooks-multi-agent-observability`), but zoetrope's specific angle — a live *flow graph* representation, in-terminal or browser, rather than a replay/dashboard/hook-log view — is different enough in presentation that a mechanical "redundant with X" call is not defensible from metadata alone. Leaves it for a real hands-on look at whether the flow-graph view is a genuine improvement over the incumbents' transcripts/timelines.

_Triaged 2026-08-22 by the P3 backlog band._
