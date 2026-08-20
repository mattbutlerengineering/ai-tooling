# Evaluation: anti-slop (oxlint)

**Repo:** [dmmulroy/anti-slop](https://github.com/dmmulroy/anti-slop)
**Stars:** 2,964 | **Last updated:** 2026-08-18 (pushed) | **License:** MIT
**Last verified:** 2026-08-20
**Last triaged:** 2026-08-20  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Opinionated Oxlint rule set (MIT) rejecting low-evidence
TypeScript/JavaScript patterns as an agent skill." An Oxlint rule pack that flags the
guessed types and unchecked assumptions standard linters don't catch but that show up
disproportionately in AI-generated code, applied as an agent skill while the agent writes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata, README, and the CATALOG "Overlaps with" cell.

## Triage note

P3 backlog — no STACK pick cited in "Overlaps with." A different repo from the
already-catalogued `AgriciDaniel/anti-slop` (same display name, disambiguated here as
"anti-slop (oxlint)"): that one does structural-test slop detection across
prose/code/docs; this one is a specific Oxlint rule pack for TS/JS. Left at
`discovery-log`; stamped only.

_Triaged 2026-08-20 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [anti-slop (oxlint)](https://github.com/dmmulroy/anti-slop) | tool | Opinionated Oxlint rule set (MIT) rejecting low-evidence TypeScript/JavaScript patterns as an agent skill | Standard linters don't flag AI-generated code's guessed types and unchecked assumptions; want a fast rule set purpose-built for that | anti-slop, sloptrim, brooks-lint |
