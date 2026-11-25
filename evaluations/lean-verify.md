# Evaluation: lean-verify

**Repo:** [hirosassa/lean-verify](https://github.com/hirosassa/lean-verify)
**Stars:** 22 | **Last updated:** 2026-11-24 (pushed) | **License:** MIT
**Last verified:** 2026-11-25
**Last triaged:** 2026-11-25  <!-- triaged: bulk -->
**Dev loop stage:** Review (formal verification)
**Layer:** Tooling

---

## What it does

A Claude Code skill (MIT) that finds bugs and proves optimizations behave the same
as the code they replace, using the Lean 4 theorem prover.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on redundancy with a catalogued incumbent, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this
eval offers none.

## Triage note

Newly discovered and catalogued today via the daily discovery pass. No STACK pick
is cited in "Overlaps with" (pressure 0) — it names `fast-anything` (also proves
behavioral equivalence, but via tests rather than a theorem prover), `skylos`, and
`vet` as conceptual peers, none of which it clearly duplicates; formal proof via
Lean 4 is a meaningfully different (and much stronger) correctness claim than any
of them makes. Left at `discovery-log` for a real hands-on eval — low star count
(22) and very new, but the Lean 4 angle is differentiated enough to be worth a look
rather than a mechanical SKIP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [lean-verify](https://github.com/hirosassa/lean-verify) | skill | Claude Code skill (MIT) that finds bugs and proves optimizations behave the same using the Lean 4 theorem prover | Proving a refactor or optimization preserves behavior usually relies on tests and eyeballing rather than formal proof | fast-anything, skylos, vet |
