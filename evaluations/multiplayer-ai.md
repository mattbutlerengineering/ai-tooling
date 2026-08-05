# Evaluation: multiplayer-ai

**Repo:** [godfaddaai/multiplayer-ai](https://github.com/godfaddaai/multiplayer-ai)
**Stars:** 11 | **License:** MIT
**Last verified:** 2026-08-05
**Last triaged:** 2026-08-05  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling (CLI)

---

## What it does

Makes Codex and Claude Code terminal sessions multiplayer — a remote collaborator joins a
running session over Tailscale from another machine.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (diri, agmsg, orca). That is sufficient to
place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: diri and orca orchestrate *multiple agents* in parallel; agmsg lets
*agents* message each other. None gives a *human collaborator* real-time multiplayer access
to one running agent session the way this tool claims to — a different, narrower
collaboration problem worth a hands-on look rather than a redundancy SKIP.

_Triaged 2026-08-05 by the daily discovery routine (today's new lead)._
