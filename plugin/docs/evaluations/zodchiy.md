# Evaluation: zodchiy

**Repo:** [Socialpranker/zodchiy](https://github.com/Socialpranker/zodchiy)
**Stars:** 23 | **Last updated:** 2026-09-01 (pushed) | **License:** MIT
**Last verified:** 2026-09-02
**Last triaged:** 2026-09-02  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An architectural audit CLI (stdlib-only) that admits a finding only once its cost is
measured from git history, plus a doctrine for coding agents to follow when doing
architecture review.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata from the daily discovery scan.

## Triage note

No STACK-pick overlap detected (P3 backlog). Conceptually adjacent to `ratchet` (gone,
404) and `skylos` (CONDITIONAL/RUN), but zodchiy's angle — grounding a finding's *cost* in
measured git history rather than static heuristics — is distinct enough not to call it
redundant. Very early (23★, 1 day old); left at `discovery-log`.

_Triaged 2026-09-02 by the P3 backlog band (daily discovery-and-triage routine, bulk,
eliminate-only)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [zodchiy](https://github.com/Socialpranker/zodchiy) | tool | Architectural audit CLI (MIT, stdlib-only) admitting a finding only once its cost is measured from git history, plus a doctrine for coding agents | Architecture audits assert cost/severity without measuring it against how the code actually evolved; want findings grounded in git history, not opinion | ratchet, skylos, brooks-lint |
