# Evaluation: pristine-skill

**Repo:** [newbanser/pristine-skill](https://github.com/newbanser/pristine-skill)
**Stars:** 13 | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process (skill)

---

## What it does

An agent skill enforcing the "First-Time Principle": write every change in its final
form — no patches, no what-comments, no leftovers, no local/deployed drift. Cross-platform
(Claude Code, Codex, OpenCode).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (ratchet, old-coder, brooks-lint). That is
sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: ratchet, old-coder, and brooks-lint are themselves `discovery-log`,
not STACK incumbents, and each targets a different failure mode (mid-session compliance
grading, evidence-first completion claims, and book-grounded design-decay review,
respectively) rather than this skill's specific "no patches/no drift/no leftovers" discipline.
Differentiated enough to deserve a real eval.

_Triaged 2026-08-04 by the daily discovery routine (today's new lead)._
