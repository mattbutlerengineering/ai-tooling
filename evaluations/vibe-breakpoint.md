# Evaluation: vibe-breakpoint

**Repo:** [globalmpc/vibe-breakpoint](https://github.com/globalmpc/vibe-breakpoint)
**Stars:** 55 | **Last updated:** 2026-11-20 (pushed) | **License:** MIT
**Last verified:** 2026-11-24
**Last triaged:** 2026-11-24  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A Claude Code skill that load-tests an isolated copy of a vibe-coded app to find its user ceiling and its slowest database queries, without touching the live project.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — complementary to the pre-flight security/readiness checklist from the same author, not a substitute for it.

## Triage note

Left at `discovery-log`, stamped. It cites `vibe-preflight` (same author, globalmpc) in Overlaps, but vibe-preflight is a pre-launch security/readiness checklist while vibe-breakpoint is a load-test for capacity/slow queries — different checks, not a redundant pair, and neither cited peer is a STACK pick. Left for a real eval.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vibe-breakpoint](https://github.com/globalmpc/vibe-breakpoint) | skill | Claude Code skill (MIT) that load-tests an isolated copy of a vibe-coded app to find its user ceiling and its slowest database queries | Vibe-coded apps ship with no idea how many users they can handle or which queries slow down first, and testing against the live app risks breaking it | vibe-preflight, gap-trap, pixelpact |
