# Evaluation: objection

**Repo:** [victorserpa/objection](https://github.com/victorserpa/objection)
**Stars:** 2 | **Last updated:** 2026-09-24 (pushed) | **License:** MIT
**Last verified:** 2026-09-24
**Last triaged:** 2026-09-24  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An adversarial-review plugin for Claude Code — accuser agents, a defender, and a judge debate the
PR, with a hook that blocks the PR from shipping until the verdict is APPROVED.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus
the CATALOG "Overlaps with" cell (claude-octopus, hubo, code-review). That is sufficient to place the
lead against its incumbents, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `code-review` (the STACK incumbent triage.py
matched on). code-review is a single-pass review skill; objection's multi-role adversarial-debate
mechanism plus a merge-blocking gate is the same pattern already carried, unresolved, by two other
catalogued leads (`claude-octopus` — multi-LLM consensus review; `hubo` — two-agent adversarial
sparring) that were themselves left rather than SKIPped against the same incumbent. A brand-new
entrant (2 stars, same-day repo) in an already-undecided niche isn't grounds to dispose of this one
while its closer peers remain open leads.

_Triaged 2026-09-24 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [objection](https://github.com/victorserpa/objection) | plugin | Adversarial PR review (MIT) for Claude Code — accusers, a defender, and a judge, with a hook blocking the PR until the verdict is approved | Single-pass agent review misses issues; want an adversarial multi-role review that gates the PR before it ships | claude-octopus, hubo, code-review |
