# Evaluation: farol

**Repo:** [winnin/farol](https://github.com/winnin/farol)
**Stars:** 171 | **Last updated:** 2026-10-26 (pushed) | **License:** MIT
**Last verified:** 2026-11-02
**Last triaged:** 2026-11-02  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A CLI and GitHub Action that scores a pull request's merge risk after an AI review —
riskiest files, blast radius, diff coverage, and contract breaks — rather than a
pass/fail review verdict.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner, repo metadata, and the "Overlaps with" cell. That is sufficient for
a P2 band disposition that turns on redundancy with the named STACK incumbent, not on
the tool's own behavior — a question the overlap answers directly. It would not
support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. `triage.py` challenges it against
`pr-review-toolkit` (STACK, KEEP/MEASURED), but pr-review-toolkit does the review
itself (type analysis, silent-failure hunting, test coverage, comment analysis).
farol's own pitch is explicitly *after* a review pass — quantifying what a merge
actually reaches (blast radius, diff coverage, contract breaks) rather than reviewing
the diff's content. That is a different question than the incumbent answers, not a
thinner clone of it.

_Triaged 2026-11-02 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [farol](https://github.com/winnin/farol) | tool | CLI + GitHub Action (MIT) scoring a PR's merge risk — riskiest files, blast radius, diff coverage, contract breaks | An AI review pass says a PR looks fine but gives no measure of what the change actually reaches or how risky merging it is | pr-review-toolkit, pullfrog, code-quality |
