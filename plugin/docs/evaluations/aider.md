# Evaluation: aider

**Repo:** [Aider-AI/aider](https://github.com/Aider-AI/aider)
**Stars:** ~47,229 | **Last updated:** 2026-05-22 | **License:** Apache-2.0
**Last verified:** 2026-07-28
**Last triaged:** 2026-07-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

The original terminal AI pair-programmer — git-aware, repo-map-driven edits across many files with automatic commits, works with most LLMs (Claude/GPT/local), voice + image input, and a built-in benchmark harness.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: `repo-metadata.json` (47.2K stars, Apache-2.0, pushed 2026-05-22) plus the CATALOG "Overlaps with" cell against opencode/gptme/plandex/goose/claude-squad.

## Triage note

P2 challenger band (overlaps claude-squad, a STACK pick), but aider is not redundant with it: claude-squad is a session multiplexer for running several agents, while aider is itself a full alternative coding-agent harness (46K+ stars, one of the most mature and widely used in the category). A tool this significant and differentiated is not a candidate for a mechanical SKIP — it deserves a real hands-on eval. Left at discovery-log.
