# Evaluation: codedna

**Repo:** [crafteraadarsh/codedna](https://github.com/crafteraadarsh/codedna)
**Stars:** 1 | **Last updated:** 2026-10-17 (pushed) | **License:** MIT
**Last verified:** 2026-10-17
**Last triaged:** 2026-10-17  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Offline, read-only Rust CLI/MCP server/skill profiling a codebase's stack, architecture, dead
code, and supply-chain risk in milliseconds.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge the
tool's behaviour hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; picked up as one of the oldest
untriaged leads in the P2 challenger band this pass.

## Triage note

P2 challenger: cites `codegraph` (STACK ADOPT pick) in Overlaps, pressure 0. The jobs differ —
codegraph is a pre-indexed, auto-syncing code knowledge graph for live agent context, while
codedna is a one-shot offline profiler surfacing dead code and supply-chain risk, a different
output codegraph doesn't produce. Calling this "redundant with codegraph" would misstate what
either tool does. Left at `discovery-log`; a real eval would need to confirm the dead-code/risk
detection actually works, not just that the one-liner is differentiated.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [codedna](https://github.com/crafteraadarsh/codedna) | tool | Offline, read-only Rust CLI/MCP server/skill (MIT) profiling a codebase's stack, architecture, dead code, and supply-chain risk in milliseconds | Understanding an unfamiliar codebase's structure and risk surface means manual digging across many separate tools | codegraph, graphify, skylos |  |
