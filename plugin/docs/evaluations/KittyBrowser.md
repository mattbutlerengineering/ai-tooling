# Evaluation: KittyBrowser

**Repo:** [graiz/KittyBrowser](https://github.com/graiz/KittyBrowser)
**Stars:** 30 | **Last updated:** 2026-11-13 (pushed) | **License:** MIT
**Last verified:** 2026-11-16
**Last triaged:** 2026-11-16  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A real web browser in a terminal pane: headless Chrome drawn with the kitty graphics
protocol, built to work beside coding agents.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a P3
leave-at-discovery-log call, not to judge the tool's actual behavior — it would not
support an ADOPT, and this eval offers none.

## Triage note

Distinct problem from `browser-use`/`nanobrowser` (both automate browser *actions* for
an agent) — this renders a real browser *inline in the terminal* so a human reviewing a
coding-agent session doesn't have to switch to a separate window. Differentiated enough
to deserve a real hands-on eval; left at `discovery-log`.

_Triaged 2026-11-16 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [KittyBrowser](https://github.com/graiz/KittyBrowser) | tool | Real web browser in a terminal pane (MIT) — headless Chrome drawn with the kitty graphics protocol, built to work beside coding agents | Verifying a web UI change means leaving the terminal for a separate browser window alongside the coding agent | browser-use, nanobrowser, agent-browser |
