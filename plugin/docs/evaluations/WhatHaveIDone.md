# Evaluation: WhatHaveIDone

**Repo:** [hasan-gundogdu/WhatHaveIDone](https://github.com/hasan-gundogdu/WhatHaveIDone)
**Stars:** 0 | **Last updated:** 2026-10-21 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-23
**Last triaged:** 2026-10-23  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process (skill)

---

## What it does

A vendor-neutral agent skill (PowerShell tooling) for understanding repository changes —
one portable skill meant to explain a diff regardless of which harness is running it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Pressure 0 — nothing in the catalog cites it yet. Its "Overlaps with" cell names `sem`,
`explain-for-dumb`, and `codebase-map`, none of which is a STACK pick, so this does not
band as a P2 challenger. No archived flag, no disqualifying license — Apache-2.0 is
permissive, and while this is a vendored `skill` Type (P4 is scoped to vendored Types
under a disqualifying license), Apache-2.0 is not one of the disqualifying licenses
(`NONE`/`AGPL`/`GPL`/`CC-BY-SA`/`EUPL`), so this does not band as P4 either. No
`Ships inside` container. Zero stars and genuinely new (created 2026-09-27); its own
pitch — vendor-neutrality across harnesses — is the differentiator over the more
code-structure-focused `sem`/`codebase-map` peers. Left at `discovery-log`.

_Triaged 2026-10-23 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [WhatHaveIDone](https://github.com/hasan-gundogdu/WhatHaveIDone) | skill | Vendor-neutral agent skill (Apache-2.0) for understanding repository changes | Reviewing what actually changed in a repo means reading raw diffs harness-by-harness; want one portable skill that explains changes | sem, explain-for-dumb, codebase-map |
