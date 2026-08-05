# Evaluation: trace-file-lineage

**Repo:** [uczltw6/trace-file-lineage](https://github.com/uczltw6/trace-file-lineage)
**Stars:** 259  <!-- repo-metadata.json, fetched 2026-08-04 -->
**License:** MIT
**Last verified:** 2026-07-31
**Last triaged:** 2026-07-31  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

CLI that traces which script, notebook, command, or AI agent produced a file — locally, with
evidence and honest uncertainty.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (re_gent, h5i, weave). That is sufficient to place the
lead and note none of its named overlaps are STACK incumbents, not to support an ADOPT — this
eval offers none.

## Triage note

Left at `discovery-log`: re_gent and h5i track *git*-level, prompt-to-commit provenance;
trace-file-lineage is broader — any file/command/agent lineage, not limited to git commits
(covers notebooks, data files, arbitrary CLI output). Different scope, not clearly dominated.
Left for the P0/eval-runner lane.

_Triaged 2026-07-31 by today's discovery lead._
