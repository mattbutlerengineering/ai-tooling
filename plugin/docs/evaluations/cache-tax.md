# Evaluation: cache-tax

**Repo:** [karanb192/cache-tax](https://github.com/karanb192/cache-tax)
**Stars:** 28 | **Last updated:** 2026-09-20 (pushed) | **License:** MIT
**Last verified:** 2026-09-20
**Last triaged:** 2026-09-20  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code plugin that keeps the prompt cache warm during breaks and shows the
estimated cost before a cold send.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (cachebeat, opencode-cache-stats,
ccusage). That is sufficient to place the lead and note `ccusage` is the one named STACK
incumbent, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: challenges `ccusage` (a STACK pick, MEASURED) in the P2
challenger band, but ccusage parses session logs into cost *reports* after the fact —
cache-tax instead pings idle sessions to keep the cache warm and estimates cost *before*
a cold send, the same job as the still-undisposed `cachebeat` lead rather than ccusage's
job. Not redundant with the actual incumbent. Left for the P0/eval-runner lane.

_Triaged 2026-09-20 by today's discovery lead._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cache-tax](https://github.com/karanb192/cache-tax) | plugin | Claude Code plugin keeping the prompt cache warm during breaks and showing the estimated cost before a cold send | Idle gaps let the prompt cache expire, so the next message silently pays full price with no cost warning first | cachebeat, opencode-cache-stats, ccusage |
