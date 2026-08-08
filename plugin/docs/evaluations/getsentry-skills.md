# Evaluation: getsentry/skills

**Repo:** [getsentry/skills](https://github.com/getsentry/skills)
**Stars:** 903 | **License:** Apache-2.0
**Last verified:** 2026-08-08
**Last triaged:** 2026-08-08  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Process

---

## What it does

The agent skills Sentry's own engineering team develops with — a vendor's working set,
published rather than marketed.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (mattpocock/skills, agent-skills,
vercel-labs/agent-skills).

## Triage note

Left at `discovery-log` (P2 challenger band): same shape as `vercel-labs/agent-skills` — a
platform vendor's own working skill set, not a generic aggregation. That class of skill pack
(vendor-authored, dogfooded internally) is a genuinely different trust profile than the
community collections it's compared against, worth a real look rather than a mechanical
redundancy SKIP.

_Triaged 2026-08-08 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [getsentry/skills](https://github.com/getsentry/skills) | skill | The agent skills Sentry's own engineering team develops with (Apache-2.0) — a vendor's working set, published rather than marketed | Most skill packs are aspirational; want the set a production engineering org actually runs | mattpocock/skills, agent-skills, vercel-labs/agent-skills |
