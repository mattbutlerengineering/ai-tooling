# Evaluation: CL4R1T4S

**Repo:** [elder-plinius/CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S)
**Stars:** 45,144 | **Last updated:** 2026-06-15 (pushed) | **License:** AGPL-3.0
**Dev loop stage:** Reference
**Layer:** Process
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A collection of leaked system prompts for Claude, ChatGPT, Gemini, Cursor, Replit, Lovable and
other assistants — the deployed instructions rather than the published documentation.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this — it is a document collection. Source-grounded only: GitHub
metadata (fetched 2026-08-04) plus the CATALOG one-liner and "Overlaps with" cell
(`system-prompts-and-models`, `claude-code-system-prompts`). Sufficient for a SKIP that turns on
*supersession by catalogued rows*; not sufficient for a positive verdict, and none is offered.

## Verdict

**SKIP** — superseded by the two prompt-leak rows it names in its own "Overlaps with" cell, both
of which beat it on the two axes that matter for this genre.

Recency: a leaked-prompt collection is worth exactly what it is worth *today*, because the prompts
change with every model release. `system-prompts-leaks` (★55K) is updated continuously and was
pushed 2026-07-09; CL4R1T4S was last pushed 2026-06-15. Breadth: `system-prompts-and-models` (★142K)
covers more tools.

Licensing decides the rest. CL4R1T4S is AGPL-3.0 while `system-prompts-leaks` is CC0-1.0 — for a
resource whose entire use is reading and quoting, a public-domain dedication is strictly better than
a strong copyleft. (AGPL does not disqualify a *reference* row on its own; P4's copyleft band is
scoped to vendored skills and plugins. It is a tiebreak here, not a disqualification.)

★45K says a lot of people found it. Three collections of the same leaked prompts is two too many for
a catalog whose Reference section is meant to answer "where do I look".

Re-open if it resumes a faster update cadence than `system-prompts-leaks`, which is the only axis on
which it could win.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S) | reference | Leaked system prompts (AGPL-3.0, ★44K) for Claude, ChatGPT, Gemini, Cursor, Replit, Lovable, and others | Understanding AI system constraints and behaviors requires visibility into the actual deployed system prompts | system-prompts-and-models, claude-code-system-prompts |
