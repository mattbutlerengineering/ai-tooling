# Evaluation: juror

**Repo:** [Juror-AI/juror](https://github.com/Juror-AI/juror)
**Stars:** 67 | **Last updated:** 2026-08-09 (pushed) | **License:** MIT
**Last verified:** 2026-08-10
**Last triaged:** 2026-08-10  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A self-hosted AI PR reviewer that runs on your own GitHub Actions, pitched as a
cheaper alternative to hosted services like Greptile.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Verdict

**SKIP** — redundant with `code-review` (the catalog's STACK-recommended AI PR
reviewer) and, more directly, with the already-catalogued self-hosted alternatives
`PR-Agent`, `open-code-review`, and `kodus-ai`, all of which already cover
self-hosted/CI-driven AI PR review with more traction and maturity. Juror is four
days old at 67 stars with no differentiation stated beyond "cheaper than Greptile" —
a second tool for this job earns nothing yet.

_Triaged 2026-08-10 by the P2 challenger band._
