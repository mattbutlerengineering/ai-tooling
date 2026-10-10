# Evaluation: strands-agents/box

**Repo:** [strands-agents/box](https://github.com/strands-agents/box)
**Stars:** 303 | **Last updated:** 2026-10-10 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-10
**Last triaged:** 2026-10-10  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A local sandbox engine (Apache-2.0, Rust) for running AI agents under OS-level
isolation: a default-deny policy engine shared across shell execution, Python,
network egress, and an MCP broker, plus credential injection so the agent process
never sees the secrets it's given access to. macOS/Apple-silicon preview today,
with Linux support planned.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only
(repo README plus metadata), consistent with an unattended discovery pass.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog — no overlap pressure (`Overlaps with`: daytona, agent-sandbox,
toolpermit; none is a STACK pick). A credential-injection + cross-tool default-deny
policy engine is differentiated enough from its catalogued peers (most cover shell
or filesystem isolation alone) to deserve a real hands-on eval rather than a
mechanical disposition. Left at `discovery-log`; stamped as examined.

_Triaged 2026-10-10 by the P3 backlog band._
