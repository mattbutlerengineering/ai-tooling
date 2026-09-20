# Evaluation: cachebeat

**Repo:** [ARahim3/cachebeat](https://github.com/ARahim3/cachebeat)
**Stars:** 16 | **Last updated:** 2026-09-15 (pushed) | **License:** none specified
**Last verified:** 2026-09-16
**Last triaged:** 2026-09-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A tiny Claude Code skill that pings idle sessions to keep the prompt cache warm, so the
next message reads from cache instead of paying full price.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the disposition
below, not for an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. Its catalogued overlap (`ccusage`) reports cost/token
spend after the fact; cachebeat does a different, narrower job — actively preventing cache
expiry during idle gaps — that no catalogued incumbent performs. No incumbent to call this
redundant with. Also carries no declared license, which the catalog's SKIP bar does not
reach on its own for a `skill` Type without a copyleft or missing-grant finding to state;
left for a human read rather than a mechanical P4 disposition.

_Triaged 2026-09-16 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cachebeat](https://github.com/ARahim3/cachebeat) | skill | Tiny Claude Code skill (⚠️ no license) pinging idle sessions to keep the prompt cache warm | Claude Code's prompt cache expires during idle gaps, so the next message pays full price instead of reading from cache | opencode-cache-stats, ccusage, deadeye-cc |
