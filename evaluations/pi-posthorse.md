# Evaluation: pi-posthorse

**Repo:** [fitchmultz/pi-posthorse](https://github.com/fitchmultz/pi-posthorse)
**Stars:** 236 | **Last updated:** 2026-09-08 (pushed) | **License:** MIT
**Last verified:** 2026-09-08
**Last triaged:** 2026-09-08  <!-- triaged: bulk -->
**Dev loop stage:** Implement (context continuity across a session)
**Layer:** Process

---

## What it does

Native, no-summary context windows for the fitchmultz/pi fork of the Pi coding agent — rollover tools, durable notes, and history recovery so a fresh context window still carries the same task forward, instead of losing work through lossy summarization.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `claude-mem` despite the overlap citation. `claude-mem` is a Claude Code plugin providing searchable semantic memory and a knowledge graph across sessions; pi-posthorse is a native extension for a specific Pi-agent fork solving a different problem — avoiding lossy summarization on context rollover, not recall. Different target agent, different mechanism, not the same job duplicated.

_Triaged 2026-09-08 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pi-posthorse](https://github.com/fitchmultz/pi-posthorse) | tool | Native no-summary context windows (MIT) for the pi coding agent — rollover tools, durable notes, and history recovery instead of lossy summarization | Context resets lose work through lossy summarization; want a fresh context window that still carries the same task forward | staffetta, claude-mem, OMEGA |
