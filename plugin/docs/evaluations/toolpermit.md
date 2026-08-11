# Evaluation: toolpermit

**Repo:** [sunhao123456sun-svg/toolpermit](https://github.com/sunhao123456sun-svg/toolpermit)
**Stars:** 30 | **Last updated:** 2026-08-11 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-11
**Last triaged:** 2026-08-11  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A local-first permission firewall and approval layer for AI agent tool calls (Python, Apache-2.0). Sits between an agent and its tool calls to gate/approve/audit-log risky calls before they execute.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (description, topics, license, stars) plus the CATALOG one-liner. That is sufficient to place the tool and note its nearest catalogued peers, not to judge its actual approval-gate behavior or false-positive rate.

## Verdict

**discovery-log — tentative read**

## Triage note

Newly discovered and catalogued today (daily discovery pass). Left at `discovery-log` — a first-day lead with zero overlap pressure and no adoption signal yet; too early to call redundant with anything already in STACK (`cc-safety-net` catches destructive commands after the fact, `agentlint`/`numbat` are broader guardrail/visibility tools — none is a direct permission-firewall equivalent). Worth a look once it has more track record.

_Triaged 2026-08-11 by the daily discovery-and-triage pass._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [toolpermit](https://github.com/sunhao123456sun-svg/toolpermit) | tool | Local-first permission firewall and approval layer (Apache-2.0) for AI agent tool calls | Agents call tools with no policy gate; want local approval/audit before a risky call executes | cc-safety-net, agentlint, numbat |
