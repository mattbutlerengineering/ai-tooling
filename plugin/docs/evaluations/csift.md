# Evaluation: csift

**Repo:** [wdhwg001/csift](https://github.com/wdhwg001/csift)
**Stars:** 7 | **Last updated:** 2026-08-29 (pushed) | **License:** MIT
**Last verified:** 2026-08-30
**Last triaged:** 2026-08-30  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A Rust CLI (published on crates.io) sifting Claude Code sessions — regex search across all JSONL record types, file recovery, image extraction, and subagent-topology inspection, plus matching plan files back to sessions.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`claude-devtools`, `roundtable`, `zoetrope`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` — a first-time lead with no overlap pressure yet. `claude-devtools` reads the same session transcripts for a visual debugger; csift is a lower-level regex/recovery CLI over the raw JSONL rather than a UI. Whether that CLI-first angle (recovery, image extraction, subagent-topology inspection) is differentiated enough to earn a seat needs a real look, at 7 stars and days old.

_Triaged 2026-08-30 by the P3 backlog band ([#567](https://github.com/mattbutlerengineering/ai-tooling/issues/567))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [csift](https://github.com/wdhwg001/csift) | tool | Rust CLI (MIT) sifting Claude Code sessions — regex search across record types, file recovery, image extraction, subagent topology inspection | Claude Code session JSONL is opaque to search, recovery, and topology inspection without ad-hoc parsing | claude-devtools, roundtable, zoetrope |
