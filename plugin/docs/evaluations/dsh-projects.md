# Evaluation: DSH-projects

**Repo:** [hovocope135-tech/DSH-projects](https://github.com/hovocope135-tech/DSH-projects)
**Stars:** 42 | **Last updated:** 2026-11-19 (pushed) | **License:** MIT
**Last verified:** 2026-11-20
**Last triaged:** 2026-11-20  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An open-source plugin for DeepSeek Harness that turns one goal sentence into
clarifying questions, parallel task runs, and a finished result brought back to
the user.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the repo's own description plus the CATALOG "Overlaps with" cell. That is
sufficient to place the lead against its closest catalog peers, not to support any
verdict, and none is offered here.

## Triage note

Newly catalogued from today's discovery pass. No structural signal (STACK
overlap, archived status, disqualifying license) bands this lead for a mechanical
disposition. Overlaps with `Parallax` (already catalogued, same DeepSeek Harness
ecosystem) and `open-multi-agent` (goal-first task decomposition), but neither is
a STACK pick, so this does not land in P2. Left at `discovery-log` for a
first-time hands-on eval.

_Triaged 2026-11-20 by the daily discovery-and-triage routine (bulk,
eliminate-only). Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [DSH-projects](https://github.com/hovocope135-tech/DSH-projects) | plugin | Open-source DeepSeek Harness plugin (MIT) turning one goal sentence into clarifying questions, parallel task runs, and a finished result | Stating a goal to an agent harness still means manually breaking it into tasks and running them one at a time; want it decomposed and parallelized automatically | Parallax, open-multi-agent, orca |
