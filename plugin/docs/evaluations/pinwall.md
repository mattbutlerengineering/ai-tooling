# Evaluation: pinwall

**Repo:** [dungnguyenv/pinwall](https://github.com/dungnguyenv/pinwall)
**Stars:** 7 | **Last updated:** 2026-11-14 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-15
**Last triaged:** 2026-11-15  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

A self-hosted artifact server: Claude Code, Cursor, and Codex publish HTML
pages over MCP, a human reviews them with pinned comments, versions, and
share links, and the agent reads that feedback back and fixes the page.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a
P3 leave/stamp disposition, not for an ADOPT/KEEP claim about the tool's
behavior.

## Triage note

No structural disqualifier. Very early (7 stars) but fills a specific gap —
a persistent, versioned, agent-readable review loop for agent-produced HTML —
that nothing else in the catalog covers directly. Left at `discovery-log` for
a full hands-on eval rather than a mechanical SKIP.

_Triaged 2026-11-15 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pinwall](https://github.com/dungnguyenv/pinwall) | MCP server | Self-hosted artifact server (Apache-2.0) where agents publish HTML pages over MCP for pinned-comment review, versions, and share links | Reviewing an agent-produced HTML page means screenshots and prose with no persistent, versioned review loop the agent can read back and fix from | gap-trap, code-quality, safe-ai-coding |
