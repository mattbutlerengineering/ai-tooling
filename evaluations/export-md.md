# Evaluation: export-md

**Repo:** [yussufs/export-md](https://github.com/yussufs/export-md)
**Stars:** 24 | **Last updated:** 2026-07-30 (pushed) | **License:** MIT
**Last verified:** 2026-08-01
**Last triaged:** 2026-08-01  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

A `/export-md` slash command for Claude Code that saves the current session as
clean, readable Markdown.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Verdict

**SKIP** — redundant with `handoff-skill` (already turns a conversation into a
complete, structured handoff document so any LLM can resume, a strict superset of
"save the session as Markdown"). export-md is a narrower single-command version of
a job `handoff-skill` already does; a second, thinner tool earns nothing.

_Triaged 2026-08-01 by the daily discovery routine (today's lead)._
