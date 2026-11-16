# Evaluation: learn-from-lessons

**Repo:** [assassin808/learn-from-lessons](https://github.com/assassin808/learn-from-lessons)
**Stars:** 46 | **Last updated:** 2026-11-09 (pushed) | **License:** MIT
**Last verified:** 2026-11-16
**Last triaged:** 2026-11-16  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

A skill/tool that lets a coding agent learn from your corrections — a correction you make
once is captured and reapplied automatically in a later session. Works across Claude Code,
Codex, opencode, and MCP-based agents.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `claude-reflect` (STACK pick,
KEEP/MEASURED). claude-reflect is a persistent-memory-with-semantic-search plugin;
learn-from-lessons' own description is narrower and more mechanical — capture a correction,
replay it next time — closer in shape to `requirement-ledger` (reads back corrections and
turns them into a Skill) and `PeerHarness` (one correction becomes a team-voted rule) than
to a general memory layer. Multiple catalogued tools already work this niche from different
angles; worth a real comparison before concluding which (if any) is redundant, not a
mechanical SKIP on a shared "corrections" keyword.

_Triaged 2026-11-16 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [learn-from-lessons](https://github.com/assassin808/learn-from-lessons) | skill | Turns your corrections to a coding agent into reusable lessons it applies next time (MIT) | Correcting an agent's mistake once doesn't stop it repeating the same mistake in a later session | requirement-ledger, claude-reflect, PeerHarness |
