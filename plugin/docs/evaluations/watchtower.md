# Evaluation: watchtower

**Repo:** [olucurious/watchtower](https://github.com/olucurious/watchtower)
**Stars:** 15 | **Last updated:** 2026-10-05 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-06
**Last triaged:** 2026-10-06  <!-- triaged: bulk -->
**Dev loop stage:** Verify / Reflect
**Layer:** Infrastructure

---

## What it does

Self-hosted error tracking — a drop-in for Sentry and AppSignal SDKs, one Go binary plus
Postgres, with Slack/Linear/email alerting and an MCP server for coding agents, per the repo
description and topics.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the GitHub
repository description, topics, and metadata. That is sufficient to place the lead, not to judge
its SDK-compatibility claims or MCP tool surface hands-on.

## Triage note

Left at `discovery-log`. No `Overlaps with` cell names a STACK pick, so this is plain P3 backlog.
It overlaps the catalogued `sentry` MCP server on the error-tracking job but differs on a real
axis — self-hosted vs. hosted, and an explicit Sentry/AppSignal SDK compatibility claim — which is
worth a hands-on check rather than a mechanical SKIP against a hosted-service incumbent.

_Triaged 2026-10-06 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [watchtower](https://github.com/olucurious/watchtower) | MCP server | Self-hosted error tracking (Apache-2.0) — a drop-in for Sentry/AppSignal SDKs (one Go binary + Postgres) with Slack/Linear/email alerts and an MCP server for coding agents | Agents need production error data for debugging but a hosted tracker means sending data off-box with no MCP access; want a self-hosted drop-in exposing errors over MCP | sentry, Infracost |
