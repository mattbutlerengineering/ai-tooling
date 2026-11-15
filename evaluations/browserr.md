# Evaluation: browserr

**Repo:** [Omodaka9375/browserr](https://github.com/Omodaka9375/browserr)
**Stars:** 57 | **Last updated:** 2026-11-15 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-15
**Last triaged:** 2026-11-15  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

A Servo-based headless browser engine for AI agents, positioned as an
auditable alternative to embedding Chromium under agent browser-automation
tooling.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide
whether this lead is redundant with a catalogued incumbent, not to judge the
tool's actual behavior — this eval offers no ADOPT/KEEP signal.

## Triage note

This lead cites `playwright` (a STACK ADOPT pick) in its "Overlaps with" cell,
which bands it P2 challenger, but the two sit at different layers: playwright
is a browser-automation API/MCP server, while this tool is an alternative
*engine* underneath such automation (a Chromium substitute), not a competing
automation surface. Not a clear redundancy, and at only 57 stars it's early —
not dominant enough to leave uncatalogued, not proven enough to claim it
competes directly with playwright. Left at `discovery-log` for a real hands-on
eval.

_Triaged 2026-11-15 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [browserr](https://github.com/Omodaka9375/browserr) | tool | Servo-based headless browser engine (Apache-2.0) — an auditable alternative to embedding Chromium for agent browser automation | Agent browser-automation tools embed Chromium with no open, auditable alternative engine underneath | playwright, browser-use, agent-browser |
