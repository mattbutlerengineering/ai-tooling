# Evaluation: requirement-ledger

**Repo:** [adand-91/requirement-ledger](https://github.com/adand-91/requirement-ledger)
**Stars:** 29 | **Last updated:** 2026-08-17 (pushed) | **License:** MIT
**Last verified:** 2026-08-23
**Last triaged:** 2026-08-23  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

Points at a project you already built with an AI agent, reads the conversation history back, and derives the requirement you actually meant from your own corrections — then turns repeated corrections into a reusable Skill file. Works with Claude Code and Codex, EN/中文.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a leave decision, not on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped, though it banded as a P2 challenger against `claude-reflect` (STACK ADOPT). The two occupy adjacent but distinct ground: claude-reflect captures corrections and preferences as they happen and syncs them to CLAUDE.md, while requirement-ledger works retroactively — reading back a finished (or drifted) project's history to reconstruct the *original* intent and mechanically count repeated corrections into a Skill. That "vibe-coding drift" framing is different enough from claude-reflect's live-capture model that a bulk pass shouldn't call it redundant on a metadata skim; brand new (created 2026-08-17) and unproven either way. Worth a real comparison before a redundancy call.

_Triaged 2026-08-23 by the P2 challenger band (daily discovery routine)._
