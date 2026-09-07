# Evaluation: agit

**Repo:** [thegoodengineers/agit](https://github.com/thegoodengineers/agit)
**Stars:** 2 | **Last updated:** 2026-09-07 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-07
**Last triaged:** 2026-09-07  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A git-like CLI for AI coding-agent sessions — inspect, replay, share, and fork a session the way you would a git branch.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. Tiny (2★, days old) but the git-metaphor (fork/share a session, not just replay it) is a different angle from OrcaReplay's record-and-replay or csift's forensic search. Too early to call it redundant with either.

_Triaged 2026-09-07 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agit](https://github.com/thegoodengineers/agit) | tool | Git-like CLI (Apache-2.0) to inspect, replay, share, and fork AI coding-agent sessions | A misbehaving or interesting agent run can't be replayed, forked, or shared — only the transcript survives | OrcaReplay, roundtable, csift |
