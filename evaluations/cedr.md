# Evaluation: cedr

**Repo:** [Sheernox/cedr](https://github.com/Sheernox/cedr)
**Stars:** 59 | **Last updated:** 2026-10-31 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-31
**Last triaged:** 2026-10-31  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A developer CLI (Apache-2.0, Rust) that routes work to the right AI coding agent, merges multi-vendor reviews into one gate, and pins the skills/MCP servers agents load.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (agent-dispatcher, duo, claude-codex-coop). That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead.

## Triage note

P3 backlog. Left at `discovery-log`; its overlaps (agent-dispatcher, duo, claude-codex-coop) are themselves discovery-log leads, not STACK picks, so it doesn't land in P2. Bundling task routing, cross-vendor review merging, and skill/MCP pinning into one CLI is a differentiated combination worth a hands-on look rather than a bulk disposition.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cedr](https://github.com/Sheernox/cedr) | tool | Developer CLI (Apache-2.0, Rust) routing work to the right AI coding agent, merging multi-vendor reviews into one gate, and pinning the skills/MCP servers agents load | Teams running several coding agents have no single router, cross-vendor review gate, or pinned skill/MCP config to keep them consistent | agent-dispatcher, duo, claude-codex-coop |
