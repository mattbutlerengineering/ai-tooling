# Evaluation: jarvis-os

**Repo:** [ManceRayder42/jarvis-os](https://github.com/ManceRayder42/jarvis-os)
**Stars:** 4 | **Last updated:** 2026-08-27 (pushed) | **License:** MIT
**Last verified:** 2026-09-02
**Last triaged:** 2026-09-02  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

A memory hub and curated skill set for Claude Code — persistent memory that loads from
any directory, plus a guided local setup script.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata and the CATALOG "Overlaps with" cell. That is sufficient for the verdict below,
because the verdict turns on redundancy with a catalogued incumbent, not on the tool's
behavior — a question the overlap answers directly. It would not support an ADOPT, and
this eval offers none.

## Verdict

**SKIP** — redundant with `claude-mem` (already ADOPT/MEASURED and in STACK). Both are
persistent-memory tools for Claude Code; jarvis-os is a brand-new (4★, 6 days old), thinly
documented alternative with no differentiating capability over the incumbent's semantic
search, timeline views, and knowledge-graph management. `claude-mem` already covers this
job in STACK; a second tool for it earns nothing.

_Triaged 2026-09-02 by the P2 challenger band (daily discovery-and-triage routine, bulk,
eliminate-only)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [jarvis-os](https://github.com/ManceRayder42/jarvis-os) | tool | Memory hub and curated skill set for Claude Code (MIT) — persistent memory that loads from any directory, plus a guided local setup | Claude Code forgets project context across sessions and directories; want persistent memory bundled with a curated skill set instead of assembling one by hand | claude-mem, OMEGA, agentmemory |
