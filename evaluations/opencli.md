# Evaluation: opencli

**Repo:** [jackwener/OpenCLI](https://github.com/jackwener/opencli)
**Stars:** 26,389 | **Last updated:** 2026-07-04 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Verify (browser automation)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Turns any website into a CLI an AI agent can drive, working through your already-logged-in
browser session.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04)
plus the CATALOG one-liner and "Overlaps with" cell (`agent-browser`, `browser-use`, `page-agent`).
Enough to place it in a crowded cluster; not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Apache-2.0, ★26.4K, pushed 2026-07-04 — a large, active entry in the
Verify browser cluster, and the one with a genuinely distinct premise.

The distinction is the authenticated session. `browser-use` and `agent-browser` drive a browser the
agent controls; opencli drives *yours*, reusing the login you already have. That reaches sites an
agent otherwise cannot touch, and it is also the reason to be careful with it — an agent operating
a session authenticated as you is a blast-radius question, not a capability question. Nothing in a
one-liner settles how that is scoped.

It is the reason `browser-act/skills` was SKIPped in this pass rather than this row: when a cluster
has four members, the one to dispose is the one whose differentiator is off-scope, not the one whose
differentiator is a real capability with an unexamined safety story.

Deciding it needs the safety model read and a with/without run against a site that requires login —
P0 work, and this lane may not conclude it.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [opencli](https://github.com/jackwener/opencli) | tool | Turn any website into a CLI driven by an AI agent via your logged-in browser (Apache-2.0) | Agents can't operate sites that need an authenticated browser session | agent-browser, browser-use, page-agent |
