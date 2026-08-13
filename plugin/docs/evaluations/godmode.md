# Evaluation: godmode

**Repo:** [thiientv/godmode](https://github.com/thiientv/godmode)
**Stars:** 63 | **Last updated:** 2026-08-13 (pushed) | **License:** MIT
**Last verified:** 2026-08-13
**Last triaged:** 2026-08-13  <!-- triaged: bulk -->
**Dev loop stage:** All stages (planning, TDD, debugging, review, UI/UX, releases, incidents, evals)
**Layer:** Process

---

## What it does

A composable pack of "production-grade" Agent Skills for AI coding agents, spanning planning,
TDD, debugging, review, UI/UX, releases, incidents, and evals — a coordinated skill set across
the dev lifecycle rather than one-off skills.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell.

## Triage note

Overlap-pressure keys this lead to `GSD`, the incumbent among its cited peers that happens to
be in STACK — but godmode is a skill *collection* (like `superpowers`, `ECC`,
`compound-engineering`, and `Aegis`, none of which were SKIPped as GSD-redundant), not an
orchestration framework. It's brand new (created today) with no track record, but the scope
(spanning the whole SDLC in one pack) is differentiated enough from a mechanical-scope-overlap
call to deserve a real look rather than a source-only SKIP. Left for the P0/eval-runner lane.

_Triaged 2026-08-13 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [godmode](https://github.com/thiientv/godmode) | skill | Composable Agent Skills pack (MIT) spanning planning, TDD, debugging, review, UI/UX, releases, incidents, and evals | Need a coordinated skill set across the whole dev lifecycle instead of assembling one-off skills | superpowers, ECC, compound-engineering, Aegis |
