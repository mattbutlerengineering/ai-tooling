# Evaluation: deckhand

**Repo:** [gethrbr/deckhand](https://github.com/gethrbr/deckhand)
**Stars:** 3 | **Last updated:** 2026-11-13 (pushed) | **License:** MIT
**Last verified:** 2026-11-14
**Last triaged:** 2026-11-14  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Free skills for coding agents that audit CLAUDE.md and AGENTS.md against the real code, check a diff against them, and turn repeated PR review comments into a rule.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — catalogued today; no hands-on run yet.

## Triage note

Left at `discovery-log`, not SKIPped. Zero overlap pressure (brand new). `claude-md-doctor`/`agents-contract`/`r-doc` audit or maintain instruction files, but none of them claims deckhand's specific "turn repeated PR review comments into a rule" loop — a differentiated enough angle to deserve a first-time read.

_Triaged 2026-11-14 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [deckhand](https://github.com/gethrbr/deckhand) | skill | Free skills (MIT) auditing CLAUDE.md/AGENTS.md against the real code, checking diffs against them, and turning repeated PR comments into rules | Instruction files drift from the code they describe, and repeated PR review comments never get turned into a rule that prevents the next one | claude-md-doctor, agents-contract, r-doc |
