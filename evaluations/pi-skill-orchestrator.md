# Evaluation: pi-skill-orchestrator

**Repo:** [badgids/pi-skill-orchestrator](https://github.com/badgids/pi-skill-orchestrator)
**Stars:** 17 | **Last updated:** 2026-09-18 (pushed) | **License:** MIT
**Last verified:** 2026-09-24
**Last triaged:** 2026-09-24  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling

---

## What it does

A Pi extension that keeps Pi's normal skill autocomplete working while stopping the full installed
skill catalog from being loaded into the LLM system prompt on every turn.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus
the CATALOG "Overlaps with" cell (context-engineering-kit, skillranker). That is sufficient to place
the lead against its incumbents, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`. Not a P2 challenger — its closest peers (context-engineering-kit, skillranker)
are themselves un-promoted leads, so there is no STACK incumbent to weigh redundancy against. Scoped
specifically to the Pi harness rather than Claude Code, which narrows its applicability to this
repo's own recommended stack; worth a look if Pi usage grows or the same technique is ported.

_Triaged 2026-09-24 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pi-skill-orchestrator](https://github.com/badgids/pi-skill-orchestrator) | tool | Pi extension (MIT) keeping skill autocomplete while stopping the full skill catalog from sitting in the system prompt every turn | A large installed skill catalog burns system-prompt tokens every turn even on turns that use none of it | context-engineering-kit, skillranker |
