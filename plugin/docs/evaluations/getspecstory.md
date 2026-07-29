# Evaluation: getspecstory

**Repo:** [specstoryai/getspecstory](https://github.com/specstoryai/getspecstory)
**Stars:** 1,274 | **Last updated:** 2026-07-09 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-07-27
**Last triaged:** 2026-07-27  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

Local-first AI-IDE extensions that mine conversation histories into reusable skills and sync them to the cloud — turning past chat sessions with an AI coding tool into durable, reusable context.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `claude-mem` (thedotmack/claude-mem, ADOPT and already installed in STACK for the Retrospect stage). claude-mem already gives persistent memory with semantic search, timeline views, and knowledge-graph recall across Claude Code sessions — the same "don't lose what happened in past sessions" job getspecstory targets by mining conversation history into reusable skills. Without a hands-on comparison showing getspecstory's skill-mining + cloud-sync angle beats the incumbent on a real workflow, a second memory/session-recall tool doesn't earn its own install.

_Triaged 2026-07-27 by the P2 challenger band._
