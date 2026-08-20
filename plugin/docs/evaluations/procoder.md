# Evaluation: procoder

**Repo:** [azrtydxb/procoder](https://github.com/azrtydxb/procoder)
**Stars:** 12 | **Last updated:** 2026-08-20 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-20
**Last triaged:** 2026-08-20  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Go binary (Apache-2.0, zero deps) enforcing senior-developer
discipline on coding agents — a commit gate treating unchecked work as failing, plus a
lessons loop closing each escaped bug's class." A single Go binary that gates commits
on unchecked items, refuses to let quality controllers call unfinished work done, and
records each escaped bug's class in a lessons loop so agents don't repeat it; claims
compatibility with 20+ agents.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata, README, and the CATALOG "Overlaps with" cell.

## Triage note

P3 backlog — no STACK pick cited in "Overlaps with" (vet, tdd-guard, and brooks-lint
are catalogued but not STACK picks). Left at `discovery-log`; stamped only.

_Triaged 2026-08-20 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [procoder](https://github.com/azrtydxb/procoder) | tool | Go binary (Apache-2.0, zero deps) enforcing senior-developer discipline on coding agents — a commit gate treating unchecked work as failing, plus a lessons loop closing each escaped bug's class | Agents call unfinished work done and repeat the same bug class; want a zero-dependency gate and a cross-session lessons ledger, works with 20+ agents | vet, tdd-guard, brooks-lint |
