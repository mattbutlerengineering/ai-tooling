# Evaluation: cli-faq-shortcuts

**Repo:** [kishormorol/cli-faq-shortcuts](https://github.com/kishormorol/cli-faq-shortcuts)
**Stars:** 64 | **Last updated:** 2026-09-19 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-20
**Last triaged:** 2026-09-20  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

An Agent Skill that mines your own Claude Code and Codex history for the asks you keep
re-typing, then turns the repeated ones into short, reusable commands.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (requirement-ledger, claude-reflect,
know-before-act). That is sufficient to place the lead and note its named overlaps are
not STACK incumbents, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: challenges `claude-reflect` (a STACK pick) in the P2 challenger
band, but the two work differently — claude-reflect captures corrections/preferences and
syncs them into CLAUDE.md as standing instructions, while cli-faq-shortcuts mines
*repeated verbatim asks* and turns each into its own slash-command shortcut. Different
mechanism, different artifact produced; not a mechanical SKIP. Left for the
P0/eval-runner lane.

_Triaged 2026-09-20 by today's discovery lead._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cli-faq-shortcuts](https://github.com/kishormorol/cli-faq-shortcuts) | skill | Agent Skill mining your own Claude Code/Codex history into short reusable commands | You keep re-typing the same requests to your coding agent with nothing turning them into a reusable shortcut | requirement-ledger, claude-reflect, know-before-act |
