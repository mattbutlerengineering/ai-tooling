# Evaluation: PeerHarness

**Repo:** [aryehlev/PeerHarness](https://github.com/aryehlev/PeerHarness)
**Stars:** 29 | **Last updated:** 2026-11-12 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-12
**Last triaged:** 2026-11-12  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

A peer-voted governance skill: a team corrects Claude Code's behavior once, and
PeerHarness turns that correction into a one-sentence rule that a majority of the team
votes into every member's agent, peer-to-peer with no server, per the repo's own
description.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-12) plus the CATALOG one-liner and "Overlaps with" cell. That is
sufficient to decide whether this lead is clearly dominated by a cataloged incumbent, not
to judge the tool's actual behavior — it would not support an ADOPT, and this eval offers
none.

## Triage note

Left at `discovery-log`. It cites no STACK (ADOPT/KEEP) incumbent — `governed-agent-skills`
and `model-citizen` are themselves undisposed `discovery-log` leads — and its peer-voting
mechanism (a team majority ratifying one member's correction into everyone's agent rules)
is a differentiated enough shape to deserve a real hands-on eval rather than a mechanical
SKIP.
