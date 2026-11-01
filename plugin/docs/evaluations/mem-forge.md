# Evaluation: mem-forge

**Repo:** [dodo-labs-ai/mem-forge](https://github.com/dodo-labs-ai/mem-forge)
**Stars:** 24 | **Last updated:** 2026-11-01 (pushed) | **License:** NOASSERTION (no LICENSE file detected)
**Last verified:** 2026-11-01
**Last triaged:** 2026-11-01  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Infrastructure

---

## What it does

A memory layer for AI agents (marketed as "give every agent your team's brain on day one") — cited, continuously updated shared team knowledge.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on a missing license, not on the tool's behavior. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — no declared license (GitHub reports NOASSERTION; no LICENSE file in the repo). Per this catalog's adoption bar, a missing license is a disqualifying condition on its own regardless of functionality — there is no permissive grant to adopt against. Separately, it also overlaps `claude-mem` (ADOPT, MEASURED, in STACK) on the same "shared, persistent agent memory" job, which would be a second reason even with a clean license.

_Triaged 2026-11-01 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mem-forge](https://github.com/dodo-labs-ai/mem-forge) | MCP server | Team memory layer for AI agents (⚠️ no declared license) — cited, continuously updated shared knowledge | Each agent starts a project with none of the team's accumulated knowledge, re-learning what was already written down | claude-mem, OMEGA, mem0 |
