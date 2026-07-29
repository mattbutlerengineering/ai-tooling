# Evaluation: reporails/cli

**Repo:** [reporails/cli](https://github.com/reporails/cli)
**Stars:** 63 | **Last updated:** 2026-06-27 (pushed) | **License:** NOASSERTION (⚠️ unclear/not confirmed permissive)
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling (CLI diagnostics)

---

## What it does

AI-instructions diagnostics for Claude, Codex, Copilot, Cursor, and Gemini agents — checks
whether `CLAUDE.md` / agent instruction files are well-formed or conflicting. Picked up from the
P3 backlog band of the daily discovery-and-triage pass.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. CATALOG itself marks this relationship *complementary*
("reporails = diagnostics, agnix = lint + LSP"), not competing, so there is no redundancy basis
for a SKIP. Its license resolves as `NOASSERTION` in `repo-metadata.json` — under this repo's
license bar that rules out ever reaching ADOPT for it, but `reporails/cli` is Type `tool` (run,
not vendored), so the P4 mechanical-skip band's copyleft/missing-license rule (scoped to
vendored `skill`/`plugin` Types) does not mechanically apply here — a license-based SKIP would
need a human call, not a bulk one.

## Triage note

Left at `discovery-log`: complementary rather than redundant with its named overlap, and the
license concern is real but outside this lane's mechanical SKIP authority for a `tool` Type.
Flagging the `NOASSERTION` license for whoever runs a full eval.

_Triaged 2026-07-29 by the daily discovery scan's P3-band triage pass._
