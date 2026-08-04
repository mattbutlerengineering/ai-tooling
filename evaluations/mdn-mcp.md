# Evaluation: mdn/mcp

**Repo:** [mdn/mcp](https://github.com/mdn/mcp)
**Stars:** 162 | **Last updated:** 2026-07-06 (pushed) | **License:** MPL-2.0
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

First-party MDN Web Docs lookup over MCP: current browser-compatibility data and web-platform
documentation, served to an agent instead of recalled from training data.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this server. This evaluation is source-grounded only: repo metadata
plus the CATALOG one-liner and "Overlaps with" cell (`context7`). That is enough to place the lead
against the STACK incumbent it names — the question this band asks — and nothing more. It would
not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped, and deliberately *not* treated the same as
`ref-tools-mcp`, which this band SKIPped the day before as redundant with
[`context7`](https://github.com/upstash/context7). The difference is the content, not the
mechanism. Ref is a general documentation-retrieval MCP competing for the exact slot context7
holds. mdn/mcp serves one corpus context7 does not index: **browser compatibility data** — the
BCD support tables — which is a different fact type from library documentation, and the thing an
agent is most reliably stale about. That distinction was already recorded in `ref-tools-mcp.md`
as neighbor placement ("mdn/mcp covers browser-platform docs"), and it holds here.

It is also first-party MDN and MPL-2.0, so provenance is not in question. The open question is
narrow and measurable — does context7 already answer web-platform compatibility questions well
enough to make a second server unnecessary? — which is a P0 measurement, not a triage call.

_Triaged 2026-08-04 by the P2 challenger band ([#265](https://github.com/mattbutlerengineering/ai-tooling/issues/265))._
