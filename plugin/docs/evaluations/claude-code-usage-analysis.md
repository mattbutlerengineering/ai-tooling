# Evaluation: claude-code-usage-analysis

**Repo:** [inevolin/claude-code-usage-analysis](https://github.com/inevolin/claude-code-usage-analysis)
**Stars:** 119 | **Last updated:** 2026-11-17 (pushed) | **License:** MIT
**Last verified:** 2026-11-19
**Last triaged:** 2026-11-19  <!-- triaged: bulk -->
**Dev loop stage:** Discover (outer loop)
**Layer:** Process

---

## What it does

A written empirical analysis of Claude Code token usage — auto-compaction sweet spots
measured across 8 developer workflows, and Claude Desktop vs. CLI overhead.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run anything here — there is nothing to install. This
evaluation is source-grounded only: the CATALOG one-liner, repo metadata, and the
"Overlaps with" cell. It would not support an ADOPT, and this eval offers none.

## Triage note

`triage.py` challenges this against `ccusage` (STACK, MEASURED) because both cite
token/cost vocabulary, but this repo is a **research write-up**, not an installable
competing tool — there is nothing here a reader would run instead of ccusage. "Redundant
with ccusage" doesn't apply to a document; it is reference material adjacent to
ccusage's domain, not a substitute for it. Left at `discovery-log`, not SKIPped.

_Triaged 2026-11-19 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-usage-analysis](https://github.com/inevolin/claude-code-usage-analysis) | reference | Empirical analysis (MIT) of Claude Code token usage — auto-compaction sweet spots across 8 developer workflows, Claude Desktop vs. CLI overhead | Claude Code's auto-compaction behavior and Desktop-vs-CLI overhead are undocumented, with no measured data to tune a workflow against | harness-profiler, agentpace, ccusage |
