# Evaluation: memorax-code

**Repo:** [memorax-ai/memorax-code](https://github.com/memorax-ai/memorax-code)
**Stars:** 32 | **Last updated:** 2026-08-03 (pushed) | **License:** MIT
**Last verified:** 2026-08-07
**Last triaged:** 2026-08-07  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

A memory plugin for AI coding that turns engineering experience, repository knowledge, and
personal working style into memory reusable across future coding tasks.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (mem0, claude-mem, agentmemory). That is
sufficient for a redundancy SKIP, which turns on overlap with a catalogued incumbent rather
than the tool's behavior.

## Verdict

**SKIP** — redundant with `claude-mem` (ADOPT, MEASURED). claude-mem already covers this
exact job — persistent, searchable memory of engineering experience and preferences for
Claude Code — and is a hands-on-validated, currently-adopted tool in this repo's stack.
memorax-code (32 stars, one week old) pitches the same job with no differentiating mechanism
disclosed in its description; a second unvalidated tool for a job claude-mem already fills
earns nothing without a specific reason to switch.

_Triaged 2026-08-07 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [memorax-code](https://github.com/memorax-ai/memorax-code) | plugin | Memory plugin (MIT) turning engineering experience, repo knowledge, and personal working style into memory reusable across future coding tasks | Agents don't retain how you like things done or what was learned on past tasks between sessions | mem0, claude-mem, agentmemory |
