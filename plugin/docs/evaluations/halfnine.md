# Evaluation: halfnine

**Repo:** [notinferred/halfnine](https://github.com/notinferred/halfnine)
**Stars:** 20 | **Last updated:** 2026-11-01 (pushed) | **License:** NOASSERTION (no LICENSE file detected)
**Last verified:** 2026-11-01
**Last triaged:** 2026-11-01  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

A light TablePlus-style desktop Postgres GUI client (macOS and Windows) that AI agents can also use, over MCP.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on a missing license, not on the tool's behavior. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — no declared license (GitHub reports NOASSERTION; no LICENSE file in the repo). Per this catalog's adoption bar, a missing license is a disqualifying condition on its own regardless of functionality — there is no permissive grant to adopt against.

_Triaged 2026-11-01 — no declared license, disqualified on the catalog's license bar before any band/overlap question applies._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [halfnine](https://github.com/notinferred/halfnine) | tool | Lightweight TablePlus-style Postgres client (⚠️ no declared license) usable by AI agents too, over MCP — macOS and Windows | Giving an agent safe, inspectable Postgres access alongside a human-usable GUI client means running two disconnected tools | prisma, supabase, mcp-toolbox |
