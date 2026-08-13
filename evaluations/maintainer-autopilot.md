# Evaluation: maintainer-autopilot

**Repo:** [phungkaizen/maintainer-autopilot](https://github.com/phungkaizen/maintainer-autopilot)
**Stars:** 67 | **Last updated:** 2026-08-12 (pushed) | **License:** MIT
**Last verified:** 2026-08-13
**Last triaged:** 2026-08-13  <!-- triaged: bulk -->
**Dev loop stage:** Implement (autonomous maintenance pipeline)
**Layer:** Tooling

---

## What it does

Local-first, resumable AI maintenance pipelines (dependency bumps, repo hygiene, and similar
recurring chores) with single-writer safety and deterministic verification, wired for GitHub
Actions.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell.

## Triage note

Overlap-pressure keys this to `GSD`, but maintainer-autopilot's actual job — autonomous,
resumable *maintenance* loops with crash-safe single-writer state and a deterministic finish
gate — is a different niche from GSD's feature-development loop. It sits closer to
`proof-of-done-loop` and `ralph-claude-code` (both cited in its own Overlaps cell), which is a
real overlap worth a hands-on comparison rather than a source-only SKIP against the wrong
incumbent. Left for the P0/eval-runner lane.

_Triaged 2026-08-13 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [maintainer-autopilot](https://github.com/phungkaizen/maintainer-autopilot) | tool | Local-first, resumable AI maintenance pipelines (MIT) with single-writer safety and deterministic verification | Autonomous maintenance loops need crash-safe resumability and a provable finish gate, not just a cron job | proof-of-done-loop, ralph-claude-code, GSD |
