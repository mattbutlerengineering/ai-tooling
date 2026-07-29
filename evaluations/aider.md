# Evaluation: aider

**Repo:** [Aider-AI/aider](https://github.com/Aider-AI/aider)
**Stars:** 46,000 | **License:** Apache-2.0
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling (terminal harness)

---

## What it does

The original terminal AI pair-programmer — git-aware, repo-map-driven edits across many files
with automatic commits, works with most LLMs, voice + image input, and a built-in benchmark
harness. Picked up in the P2 challenger band of the daily discovery-and-triage pass.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (`opencode`, `gptme`, `plandex`, `goose`, `claude-squad`).
Only `claude-squad` is in STACK.md, and it's a session-multiplexer TUI, not a competing coding
harness — none of the five named overlaps is itself an adopted incumbent for "terminal AI
pair-programmer harness," so a mechanical SKIP isn't defensible from metadata alone.

## Triage note

Left at `discovery-log`: aider predates most of the catalog's coding-agent CLIs and remains one of
the most mature, widely-used options (46K stars, Apache-2.0). Too significant to dispose of as
"redundant" without a real hands-on comparison against Claude Code / opencode / goose.

_Triaged 2026-07-29 by the daily discovery scan's P2-band triage pass._
