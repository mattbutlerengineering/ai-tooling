# Evaluation: awesome-mcp-servers

**Repo:** [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
**Stars:** 91,824 | **Last updated:** 2026-08-03 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Reference (discovery)
**Layer:** Process

---

## What it does

The community-curated directory of MCP servers — the de facto discovery index for the ecosystem, at
~92K stars and updated continuously.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this — it is a directory, not a tool. Source-grounded only: GitHub
metadata (fetched 2026-08-04) plus the CATALOG one-liner and "Overlaps with" cell
(`awesome-claude-code`, `buildwithclaude`, `claude-plugins-official`). Enough to place it against
the STACK incumbent; not enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`, not SKIPped — the banding is a category error.
[`claude-plugins-official`](https://github.com/anthropics/claude-plugins-official) (STACK) is
Anthropic's registry of installable *Claude Code plugins*; this indexes *MCP servers*, a different
artifact from a different ecosystem with its own protocol. Neither one lists what the other lists.

There is a general point here about `reference` rows that this band should apply consistently: a
directory's job is to be findable when you need it, and it costs nothing to keep. "Redundant with
another index" is only true when the two index the same things, which is not the case for any of
the three peers named in the row — `awesome-claude-code` covers Claude Code resources,
`buildwithclaude` covers Claude-specific builds, this covers MCP servers.

No further work is queued. It is not an install decision, it does not compete for a STACK slot, and
at ~92K stars with pushes this week it needs no maintenance watch. The row stands as the answer to
"where do I look for an MCP server".

_Triaged 2026-08-04 by the P2 challenger band ([#267](https://github.com/mattbutlerengineering/ai-tooling/issues/267))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | reference | Community-curated directory of MCP servers — the canonical discovery index for the MCP ecosystem (90K stars) | Hard to discover which MCP servers exist across a fast-growing ecosystem | awesome-claude-code, buildwithclaude, claude-plugins-official |
