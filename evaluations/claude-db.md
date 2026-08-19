# Evaluation: claude-db

**Repo:** [Avijit07x/claude-db](https://github.com/Avijit07x/claude-db)
**Stars:** 116 | **Last updated:** 2026-08-19 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-19
**Last triaged:** 2026-08-19  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Bring-your-own-database persistent memory for Claude Code (Apache-2.0) — semantic recall injected into every prompt." An npm-installed CLI + skill (`claude-db search`, `claude-db capture`) that stores session decisions/corrections and injects relevant context automatically on future prompts, backed by a database the user supplies.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the README and the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on redundancy with a catalogued incumbent, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `claude-mem` (already ADOPT/MEASURED and covers persistent, semantic-search memory for Claude Code). claude-db's headline differentiator is bring-your-own-database backend flexibility, not a different job — claude-mem already solves the "Claude re-derives context every session" problem this row targets. A second tool for the same job earns nothing without evidence its backend choice changes the outcome.

_Triaged 2026-08-19 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-db](https://github.com/Avijit07x/claude-db) | tool | Bring-your-own-database persistent memory for Claude Code (Apache-2.0) — semantic recall injected into every prompt | Claude re-derives project decisions and abandoned approaches every session; want memory injected automatically, not queried by hand | claude-mem, claude-reflect, mem0 |
