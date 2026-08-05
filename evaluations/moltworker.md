# Evaluation: moltworker

**Repo:** [cloudflare/moltworker](https://github.com/cloudflare/moltworker)
**Stars:** 9,927 | **Last updated:** 2026-05-09 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Implement (agent hosting)
**Layer:** Infrastructure
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Runs OpenClaw (formerly Moltbot, formerly Clawdbot) on Cloudflare Workers — a
deployment target that hosts one specific agent harness serverlessly on Cloudflare's edge.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Enough to
place and band it; not enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`, with two observations that matter more than the row does.

**Its overlaps cell compares it to the wrong things.** The cell names `daytona`, `vercel-sandbox`,
`beta9` and `freestyle` — general sandbox and execution infrastructure. moltworker is not that: it is a
**deployment target for one specific harness** (OpenClaw) on one specific vendor's edge. You do not
choose between "moltworker or daytona"; you choose it because you already run OpenClaw and want it on
Workers. That mis-comparison is the same class of defect recorded on `softaworks/agent-toolkit` in an
earlier slice, where an overlaps cell pointing at the wrong peers kept a lead out of the band that
could have disposed it — except here it points at peers that make the row look *more* substitutable
than it is.

**It is downstream of a project that has been renamed twice.** "OpenClaw, formerly Moltbot, formerly
Clawdbot" is two renames in the lifetime of a single catalog row. Nothing here disposes it, but a
hosting shim for a thrice-named upstream is worth re-checking on a short cycle; the last push was
2026-05-09, ~3 months, which is old for this category though far from the 13-month dormancy that
decided `plandex`.

Not SKIPped. Apache-2.0, Cloudflare-maintained, and a narrow-but-real job that nothing else in the
catalog does. The correct action is to fix the overlaps cell so the next pass bands it against harness
hosting rather than against sandboxes — a catalog edit, not a triage disposition.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [moltworker](https://github.com/cloudflare/moltworker) | tool | Run OpenClaw (formerly Moltbot/Clawdbot) on Cloudflare Workers (Apache-2.0) | Want to host an agent harness serverless on the edge | daytona, vercel-sandbox, beta9, freestyle |
