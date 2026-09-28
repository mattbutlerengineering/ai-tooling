# Evaluation: first-pass

**Repo:** [joetawil7/first-pass](https://github.com/joetawil7/first-pass)
**Stars:** 44 | **Last updated:** 2026-09-27 (pushed) | **License:** MIT
**Last verified:** 2026-09-28
**Last triaged:** 2026-09-28  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Claude Code plugin of rules and checks that widen a change's review beyond the lines an agent wrote itself: ten questions asked before code is written, an independent reviewer that didn't write the diff, proof-before-done gating, and bugs fixed as a class rather than as one-offs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a bulk-triage disposition, not for an ADOPT/KEEP call — this eval offers none.

## Triage note

No STACK pick in the row's Overlaps with cell (vet, prove-it, brooks-lint — none is a STACK pick), so this lands in P3 backlog rather than a redundancy band. Newly catalogued (added 2026-09-28); zero overlap pressure keeps it low-priority for now. Left at discovery-log for a future hands-on look rather than a mechanical SKIP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [first-pass](https://github.com/joetawil7/first-pass) | plugin | Claude Code plugin (MIT) with pre-change questions, an independent reviewer, and proof-before-done checks | Agents review only the lines they wrote, skip proof of done, and fix bugs as one-offs instead of as a class | vet, prove-it, brooks-lint |
