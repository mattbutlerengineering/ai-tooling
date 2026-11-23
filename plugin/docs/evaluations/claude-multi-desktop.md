# Evaluation: claude-multi-desktop

**Repo:** [jackson-cmd/claude-multi-desktop](https://github.com/jackson-cmd/claude-multi-desktop)
**Stars:** 347 | **Last updated:** 2026-11-17 (pushed) | **License:** MIT
**Last verified:** 2026-11-23
**Last triaged:** 2026-11-23  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Runs multiple Claude Desktop accounts simultaneously on Mac, each with its own
sign-in and icon, sharing one Claude Code setup, with sessions across accounts
able to message each other.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`, nothing structural bands it — new lead, first pass.

_Triaged 2026-11-23 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-multi-desktop](https://github.com/jackson-cmd/claude-multi-desktop) | tool | Runs multiple Claude Desktop accounts simultaneously on Mac (MIT) with separate sign-ins and cross-account session messaging | Juggling several Claude accounts on one Mac means separate logins with no way for their sessions to run concurrently or coordinate | claude-account, claude-rotate, t3code |
