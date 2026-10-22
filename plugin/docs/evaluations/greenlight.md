# Evaluation: greenlight

**Repo:** [iadr-dev/greenlight](https://github.com/iadr-dev/greenlight)
**Stars:** 1 | **Last updated:** 2026-10-22 (pushed) | **License:** MIT
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

An AI × BDD spec-driven development plugin (MIT, pre-release) that turns a feature
request into human-approved, executable Gherkin specifications and then into working
code, under gates it cannot talk its way past.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Bands as a P2 challenger against `GSD` (ADOPT, pressure 1). GSD is a general
Discuss->Plan->Execute->Verify->Ship loop; greenlight's differentiator is a specifically
BDD/Gherkin-executable-spec gate, a narrower and distinct mechanism. Pre-release (★1,
created 2026-10-19) — too early for a confident SKIP or a hands-on eval. Left at
`discovery-log`.

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [greenlight](https://github.com/iadr-dev/greenlight) | plugin | AI × BDD spec-driven development (MIT, pre-release) turning a feature request into human-approved executable specs, then working code, under gates it cannot talk its way past | Agents implement before rules and examples are agreed, and "done" is asserted rather than checked against an approved contract | GSD, spec-kit, Foreman |
