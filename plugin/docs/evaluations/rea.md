# Evaluation: rea

**Repo:** [morluto/rea](https://github.com/morluto/rea)
**Stars:** 343,600 | **Last updated:** 2026-10 (recently active; exact push date not independently verifiable this session — see below) | **License:** MIT
**Last verified:** 2026-10-20
**Last triaged:** 2026-10-20  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An MCP server that lets an AI agent reverse-engineer software it has no source
code for — native binaries, Electron/JS apps, .NET assemblies, and websites — by
running analysis locally and returning findings with supporting evidence rather
than a bare guess.

## How we tested it

**Evidence:** SOURCE-ONLY

**Source-grounded review — not run hands-on.** This session's GitHub access is
scoped to `mattbutlerengineering/ai-tooling` only; arbitrary-repo API lookups and
installs are not available without an explicit `add_repo` grant, which an
unattended discovery pass does not request. This read comes from the repo's public
GitHub page (About text, README) plus independent web coverage of its growth, not
from running the tool.

## What worked

- N/A — not run.

## What didn't work or surprised us

- N/A — not run.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Not exercised. |
| Speed | neutral | Not exercised. |
| Maintainability | neutral | Not exercised. |
| Safety | neutral | Not exercised; worth checking hands-on, since reverse-engineering tools that execute/patch binaries carry more inherent risk than most dev-loop skills. |
| Cost Efficiency | neutral | Not exercised. |
| Verifiability | neutral | Not exercised. |

## Triage note

Left at `discovery-log` — a P3 backlog lead, and deliberately not a mechanical SKIP.
This is one of the most prominent GitHub-trending AI dev tools of October 2026 (public
coverage puts it in the hundreds of thousands of stars, created April 2026), and it is
genuinely differentiated from the catalog's existing RE tools (`eleven`, `decomp.wtf`):
it targets agent-driven analysis of native binaries, Electron/JS apps, .NET assemblies,
*and* websites as one MCP server, rather than one narrower format. A tool at this scale
and visibility deserves a real hands-on eval, not a bulk SKIP.

One caution worth recording for whoever picks this up: multiple fact-check sources
report trojanized copies of this project circulating under similar names/forks,
distinct from the real upstream repo — worth verifying the install source carefully
(official repo / `rea.tools` / the `rea-agents` npm package per the project's own
README) before running anything, and worth specifically checking supply-chain safety
as part of that eval given the tool's own purpose is running analysis against
untrusted binaries.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [rea](https://github.com/morluto/rea) | tool | Agent-driven reverse engineering (MIT) — analyzes native binaries, Electron/JS apps, .NET assemblies, and websites locally, returning evidence-backed findings | Understanding unfamiliar compiled or obfuscated software is manual and tool-fragmented; want one agent-native workflow across binary formats | eleven, decomp.wtf, awesome-reverse-engineering |
