# Evaluation: explain-diff-html

**Repo:** [malav2110/explain-diff-html](https://github.com/malav2110/explain-diff-html)
**Stars:** 7 | **Last updated:** 2026-09-18 (pushed) | **License:** MIT
**Last verified:** 2026-09-19
**Last triaged:** 2026-09-19  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Turns a pull request or code diff into a self-contained, interactive HTML page that explains the
change by following its logical flow rather than Git's file-by-file ordering — meant to make a
reviewer's mental reconstruction of "what actually changed and why" faster.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (spotpatch, pr-lens, code-review). That is sufficient to
place the lead against its incumbents, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: very early (7 stars, days old) but a distinct format from its named
overlaps — `spotpatch` traces React UI elements to source, `pr-lens` draws architecture/data-flow
diagrams, `code-review` runs multi-agent review. A standalone diff-to-narrated-HTML explainer is a
different artifact (output for a human reader, not a review agent), so not mechanically redundant
with any one incumbent.

_Triaged 2026-09-19 by the daily discovery routine (today's new lead)._
