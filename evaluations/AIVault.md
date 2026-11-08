# Evaluation: AIVault

**Repo:** [Mohammed-051/AIVault](https://github.com/Mohammed-051/AIVault)
**Stars:** 7 | **Last updated:** 2026-11-05 (pushed) | **License:** MIT
**Last verified:** 2026-11-08
**Last triaged:** 2026-11-08  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A lockfile and permission gate for agent skills: pins the version/permissions you approved for each installed skill, and holds back an update that silently adds network, secret, or publish access until you re-approve it. Zero dependencies.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner, the repo's own description, and its "Overlaps with" cell (`skill-safety-checker`,
`mcp-warden`, `agent-scan`). That is sufficient to place it in the catalog and check for a named
STACK redundancy; it is not sufficient to support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — a newly-discovered, 7-star lockfile/permission gate for
agent-skill updates. None of its cited peers (`skill-safety-checker`, `mcp-warden`, `agent-scan`)
is a STACK pick, so there is no named incumbent to call this redundant with, and the job it does —
pinning approved skill permissions across updates, rather than scanning code for vulnerabilities —
is distinct enough from the Security & Safety scanners already catalogued to deserve a real
hands-on eval rather than a mechanical SKIP.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane. Worth re-checking star growth before
investing eval time, given the very small current signal.

_Triaged 2026-11-08 by the daily discovery-and-triage routine._
