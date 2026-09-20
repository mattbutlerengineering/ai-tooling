# Evaluation: AXguard

**Repo:** [awarexone/AXguard](https://github.com/awarexone/AXguard)
**Stars:** 4 | **Last updated:** 2026-09-15 (pushed) | **License:** MIT
**Last verified:** 2026-09-16
**Last triaged:** 2026-09-16  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An open-source AI security scanner that finds and fixes vulnerabilities in vibe-coded apps
before you ship — SAST, secret scanning, pre-commit and CI/CD integration.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the disposition
below, not for an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. P3 backlog — nothing structural flags it for a mechanical
disposition; stamping records that it was examined.

_Triaged 2026-09-16 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [AXguard](https://github.com/awarexone/AXguard) | tool | Open-source AI security scanner (MIT) finding and fixing vulnerabilities in vibe-coded apps before you ship | Vibe-coded apps ship with unreviewed security flaws; want a scan-and-fix pass before deploy instead of a manual audit | skylos, cdmx-in/security-review, patchbot |
