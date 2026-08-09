# Evaluation: staffetta

**Repo:** [RaffaeleSpezia/staffetta](https://github.com/RaffaeleSpezia/staffetta)
**Stars:** 3 | **Last updated:** 2026-08-09 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-09
**Last triaged:** 2026-08-09  <!-- triaged: bulk -->
**Dev loop stage:** Implement (context continuity across a long session)
**Layer:** Process

---

## What it does

A bash pattern for a self-handing-off agent: on closing a milestone, it writes a summary of what happened to disk, then resumes work with a clean context window instead of letting one session balloon.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on redundancy with a catalogued incumbent, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `claude-mem` (already-adopted persistent memory: semantic search, timeline, and knowledge-graph management already give a coding agent structured continuity across sessions). staffetta's self-handoff-on-milestone pattern is a thinner, single-purpose version of the same job at 3 stars with no track record; claude-mem already covers this job in STACK, and a second tool for it earns nothing.

_Triaged 2026-08-09 by the P2 challenger band._
