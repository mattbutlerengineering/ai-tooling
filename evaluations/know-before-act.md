# Evaluation: know-before-act

**Repo:** [yj972/know-before-act](https://github.com/yj972/know-before-act)
**Stars:** 10 | **Last updated:** 2026-07-26 (pushed) | **License:** MIT
**Last verified:** 2026-07-30
**Last triaged:** 2026-07-30  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process (skill)

---

## What it does

A lightweight agent protocol for reducing uncertainty before execution. The repo is a minimal
(~4KB) skill definition, distributed via skills.sh.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (GSD, vibe-coding-prompt-template, planning-with-files).
That is sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the
tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and
this eval offers none.

## Verdict

**SKIP** — redundant with `GSD` (STACK, KEEP), whose Discuss phase already exists specifically to
reduce uncertainty before Plan/Execute begin. know-before-act is a ~4KB, single-file skill
describing the same "resolve uncertainty before acting" discipline with no additional tooling or
mechanism beyond what GSD's Discuss->Plan->Execute->Verify->Ship loop already covers in STACK.

_Triaged 2026-07-30 as part of a new discovery-log intake, not a P1/P2/P3 bulk-band pass._
