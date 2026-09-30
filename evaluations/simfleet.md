# Evaluation: simfleet

**Repo:** [entropyconquers/simfleet](https://github.com/entropyconquers/simfleet)
**Stars:** 99 | **Last updated:** 2026-09-30 (pushed) | **License:** MIT
**Last verified:** 2026-09-30
**Last triaged:** 2026-09-30  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A control plane for parallel React Native work on macOS — slimmed iOS simulators and Android
emulators, a live dashboard, shared native build cache, and per-agent device attribution for Claude
Code and Codex.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to support an
ADOPT, and none is offered here.

## Triage note

Left at `discovery-log`. `dsh-ios`, `mobilecode`, and `oh-my-android` are all `discovery-log`
themselves, not STACK picks, so this isn't a P2 redundancy call. Narrower in scope than any of them
(React Native on macOS only), but its specific problem — port/build-cache collisions when several
coding agents drive simulators/emulators in parallel — isn't addressed by any of the three. Worth a
real look for anyone doing mobile dev with parallel agents rather than a mechanical dismissal.

_Triaged 2026-09-30 by the P3 backlog band (today's new lead)._
