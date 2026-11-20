# Evaluation: claude-antigravity

**Repo:** [RedFer855/claude-antigravity](https://github.com/RedFer855/claude-antigravity)
**Stars:** 5 | **Last updated:** 2026-11-20 (pushed) | **License:** MIT
**Last verified:** 2026-11-20
**Last triaged:** 2026-11-20  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code plugin where Claude plans and reviews while the Antigravity CLI
(`agy`) executes — quota-aware, git-checkpointed, secret-fenced, with every run
measured.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the repo's own description plus the CATALOG "Overlaps with" cell. That is
sufficient to place the lead against its closest catalog peers, not to support any
verdict, and none is offered here.

## Triage note

Newly catalogued from today's discovery pass. No structural signal (STACK
overlap, archived status, disqualifying license) bands this lead for a mechanical
disposition. Overlaps with `claudes-workbench` (added in the same pass, a
different plan/execute pairing) and `pi-subagents`/`babysitter`
(delegation/obedience framing), but none of those subsumes the specific
quota-aware, git-checkpointed execution contract this tool claims. Left at
`discovery-log` for a first-time hands-on eval.

_Triaged 2026-11-20 by the daily discovery-and-triage routine (bulk,
eliminate-only). Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-antigravity](https://github.com/RedFer855/claude-antigravity) | plugin | Claude Code plugin (MIT) where Claude plans and reviews while the Antigravity CLI executes, quota-aware and git-checkpointed | Letting one agent plan and execute burns the planning model's quota on execution and leaves no checkpoint to roll back a bad run | claudes-workbench, pi-subagents, babysitter |
