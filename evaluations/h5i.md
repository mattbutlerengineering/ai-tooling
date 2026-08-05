# Evaluation: h5i

**Repo:** [h5i-dev/h5i](https://github.com/h5i-dev/h5i)
**Stars:** 502  <!-- repo-metadata.json, fetched 2026-08-04 -->
**License:** Apache-2.0
**Last verified:** 2026-07-30
**Last triaged:** 2026-07-30  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Auditable sandboxed workspaces for AI agents — isolated worktrees, prompt-aware commits (which
prompt wrote which change), and real-time multi-agent collaboration, with a claimed ~95% less
token waste.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (worktrunk, dmux, re_gent, orca). That is sufficient to
place the lead and note none of its named overlaps are STACK incumbents, not to support an
ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: none of worktrunk, dmux, re_gent, or orca are in STACK, and h5i's
combination of prompt-level provenance (which prompt wrote which commit) plus real-time
multi-agent collaboration is not a single job any current STACK pick performs. The claimed ~95%
token-waste reduction is exactly the kind of number this repo's measurement protocol exists to
verify hands-on, not to wave through or dismiss from source alone. Left for the P0/eval-runner
lane.

_Triaged 2026-07-30 by the P3 backlog band._
