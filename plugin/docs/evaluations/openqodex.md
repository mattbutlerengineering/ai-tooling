# Evaluation: openqodex

**Repo:** [openqodex/openqodex](https://github.com/openqodex/openqodex)
**Stars:** 371 | **Last updated:** 2026-10-06 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-08
**Last triaged:** 2026-10-08  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Open-source pre-push code review for Claude Code and Codex — runs SAST, secrets,
dependency, and lint scanners on changed lines, then a separate reviewer process
checks every scanner finding against the diff before you push, with no second API
key required.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Verdict

**SKIP** — redundant with `code-review`, `pr-review-toolkit` (both `anthropics/claude-plugins-official`, both MEASURED STACK picks already covering Claude-Code-generated-diff review) — a pre-push checkpoint and an independent scanner suite are a different trigger point for the same job, not a different job; a second tool for it earns nothing without a differentiated finding class STACK doesn't already catch.

_Triaged 2026-10-08 by the P2 challenger band._
