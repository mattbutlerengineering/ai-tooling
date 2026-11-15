# Evaluation: community-claude-code

**Repo:** [theRizwan/community-claude-code](https://github.com/theRizwan/community-claude-code)
**Stars:** 48 | **Last updated:** 2026-11-13 (pushed) | **License:** NOASSERTION (⚠️ no LICENSE file detected)
**Last verified:** 2026-11-15
**Last triaged:** 2026-11-15  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A local proxy connecting Claude Code and other coding agents to any
OpenAI-compatible AI provider, with streaming, tool use, fallbacks, and rate
limiting.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a
P3 leave/stamp disposition, not for an ADOPT/KEEP claim about the tool's
behavior.

## Triage note

No structural disqualifier that applies to a `tool` Type (the missing LICENSE
file only mechanically SKIPs a vendored `skill`/`plugin`). Sits in the
already-crowded model-routing-proxy cluster (`litellm`, `CLIProxyAPI`,
`claude-code-router`) but at this evidence level there isn't a basis to call
it dominated rather than simply another entrant. Left at `discovery-log` for a
full hands-on eval rather than a mechanical SKIP.

_Triaged 2026-11-15 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [community-claude-code](https://github.com/theRizwan/community-claude-code) | tool | Local proxy (⚠️ license NOASSERTION) connecting Claude Code and other coding agents to any OpenAI-compatible provider | Claude Code is locked to Anthropic's API; want streaming, tool use, fallbacks, and rate limiting against any OpenAI-compatible backend instead | litellm, CLIProxyAPI, claude-code-router |
