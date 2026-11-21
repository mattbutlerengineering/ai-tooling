# Evaluation: toki

**Repo:** [BuildBias/toki](https://github.com/BuildBias/toki)
**Stars:** 23 | **Last updated:** 2026-11-17 (pushed) | **License:** MIT
**Last verified:** 2026-11-21
**Last triaged:** 2026-11-21  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A Claude Code plugin billed as being for "token-efficient coding." The repo's own
description is a single line with no further detail on the mechanism (prompt
compaction, code-style guidance, context pruning, or something else).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the CATALOG one-liner plus repo metadata, which is too thin to characterize what
the plugin actually does, let alone judge it against an incumbent.

## Triage note

Banded P2 (challenges `ccusage` via the CATALOG "Overlaps with" cell), but `ccusage`
is a cost-*reporting* CLI while toki's one-liner describes something about *writing*
more token-efficient code — a different job if the one-liner is accurate. The
description is too thin to confirm either way, so a redundancy SKIP isn't
defensible yet. Left at discovery-log pending a closer look at what the plugin
actually changes.

_Triaged 2026-11-21 by the P2 challenger band._
