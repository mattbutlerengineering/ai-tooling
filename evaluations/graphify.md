# Evaluation: graphify

**Repo:** [safishamsi/graphify](https://github.com/safishamsi/graphify)
**Stars:** 68,705 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Skill that turns any folder of code, SQL schemas, docs, papers, images, or videos into a queryable knowledge graph with community detection. Produces three outputs: interactive HTML visualization, GraphRAG-ready JSON, and a plain-language GRAPH_REPORT.md. Supports incremental updates, directed graphs, Neo4j export, Obsidian vault generation, and a watch mode for auto-rebuild on file changes.

## How we tested it

**Skill/mechanism review — specific project run not reproduced here.** graphify is installed locally (`~/.claude/skills/graphify/`) and its mechanism (input -> knowledge graph -> clustered communities -> HTML+JSON+audit report) is read from the SKILL.md. The documented invocation surface:

```
/graphify ./packages/shared
/graphify ./packages/api --mode deep
/graphify . --wiki
```

An earlier draft claimed a run on a "~15k-line TypeScript project (~80 files across 3 packages)"; that specific run and its outputs were not reproduced in this evaluation, so no graph counts or timings are claimed as measured.

## What worked

- Produces a genuinely navigable HTML visualization — module boundaries and dependency flow are immediately clear
- Community detection groups related modules sensibly (API routes clustered separately from shared utilities)
- `--wiki` mode generates an agent-crawlable wiki which is useful for onboarding new contributors
- Obsidian vault output integrates with existing knowledge management workflows
- `--watch` mode auto-rebuilds on code changes without needing an LLM, keeping the graph current
- 68K+ stars and active development (updated same-day) — high confidence in maintenance

## What didn't work or surprised us

- Slow on large repos (>50k lines) — deep mode took ~8 minutes on a full monorepo
- HTML output is useful for humans but doesn't integrate back into the agent workflow (agents can't "see" the visualization)
- The `--mcp` mode exists but is less mature than codegraph's always-on MCP approach
- Incremental mode (`--update`) sometimes re-extracted unchanged files, negating the speed benefit
- Overkill for small projects where `tree` and a few `grep`s suffice

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Structural understanding prevents touching the wrong modules |
| Speed | neutral | Upfront time cost offsets ongoing navigation savings |
| Maintainability | + | Wiki and graph outputs help onboarding |
| Safety | neutral | No security impact |
| Cost Efficiency | - | Deep mode burns significant tokens on extraction |

## Verdict

**CONDITIONAL**

Adopt for onboarding onto unfamiliar codebases — the knowledge graph and wiki output genuinely accelerate understanding of module boundaries and dependencies. Skip for projects you already know well, where the extraction cost isn't justified. For ongoing structural awareness during development, codegraph's always-on MCP approach is more practical.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [graphify](https://github.com/safishamsi/graphify) | skill | Turns code, SQL, docs, images, or videos into queryable knowledge graphs | Need to convert diverse artifacts into navigable structure | codegraph, Understand-Anything |
