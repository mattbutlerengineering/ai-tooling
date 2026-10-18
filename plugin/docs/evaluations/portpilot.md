# Evaluation: PortPilot

**Repo:** [m4cd4r4/PortPilot](https://github.com/m4cd4r4/PortPilot)
**Stars:** 16 | **Last updated:** 2026-10-18 (pushed) | **License:** MIT
**Last verified:** 2026-10-18
**Last triaged:** 2026-10-18  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A localhost dev-port manager shipping an Electron app, a VS Code extension, a web portal, and an
MCP server to start, stop, and monitor local dev servers — giving a shared view of what's running
across agent sessions instead of ad hoc port collisions.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner and GitHub repo metadata (stars, license, activity). No hands-on run was performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

P3 backlog, oldest-untriaged (no prior eval file). Not a P2 challenger: its cited peers
(`portly`, `simfleet`) are themselves `discovery-log` leads, not a STACK pick — and PortPilot's
multi-surface shape (Electron app + VS Code extension + MCP server) is differentiated enough
from either to deserve its own look rather than a mechanical SKIP. Left at `discovery-log`;
stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [PortPilot](https://github.com/m4cd4r4/PortPilot) | tool | Localhost dev-port manager (MIT) — Electron app, VS Code extension, web portal, and MCP server to start/stop/monitor local dev servers | Running multiple local dev servers across agent sessions causes port collisions with no shared view of what's running | portly, simfleet |  |
