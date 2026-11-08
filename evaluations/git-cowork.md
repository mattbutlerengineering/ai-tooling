# Evaluation: git-cowork

**Repo:** [michael-smao/git-cowork](https://github.com/michael-smao/git-cowork)
**Stars:** 32 | **Last updated:** 2026-11-07 (pushed) | **License:** MIT
**Last verified:** 2026-11-08
**Last triaged:** 2026-11-08  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A small, fast, native Mac git client with a task board and code reviews that live in the repo —
no sign-up, no server.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner and its "Overlaps with" cell (`code-review`, `pr-review-toolkit`, `prod-readiness`).
That is sufficient to check for a named STACK redundancy; it is not sufficient to support an
ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — cites `code-review` and `pr-review-toolkit` (both STACK
picks) as overlaps, but those are agent-driven automated review plugins, while git-cowork is a
human-facing native git client with a built-in task board and review UI — a different job
(client UI vs. agent plugin), not clearly dominated by either incumbent. Left rather than
mechanically SKIPped as redundant.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane.

_Triaged 2026-11-08 by the daily discovery-and-triage routine._
