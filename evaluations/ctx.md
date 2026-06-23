# Evaluation: ctx

**Repo:** [stevesolun/ctx](https://github.com/stevesolun/ctx)
**Stars:** 518 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Plan (recommends the right tools for the task before/during work)
**Layer:** Tooling

---

## What it does

ctx (PyPI: `claude-ctx`) recommends a small, top-scored bundle of skills, agents, MCP servers, and harnesses for whatever you are currently building. It ships a pre-built "LLM-wiki" knowledge graph (README states 79,958 nodes / 2.6M edges in the shipped snapshot; repo description cites 102,928 nodes) indexing 68,494 skill entity pages (67,024 with hydrated installable `SKILL.md` bodies), 467 agents, 10,790 MCP servers, and 207 harnesses. Edges span semantic similarity, tags, slug tokens, source overlap, direct links, quality, usage, type affinity, and graph structure.

The mechanism: after `ctx-init --hooks`, ctx attaches to Claude Code's `PostToolUse` and `Stop` events to observe what you're working on. `ctx-scan-repo --repo . --recommend` scans the repo's stack signals and walks the graph to surface the right ~10-15 entities for the session — the stated goal being to avoid loading everything (context-budget waste) and to flag stale/unused skills (skill rot). It also offers entity management (`ctx-skill-add`, `ctx-agent-add`, `ctx-mcp-add`, `ctx-harness-add`) with benefits/risks update reviews, a four-signal skill quality scorer (`ctx-skill-quality`), structural health/drift detection (`ctx-skill-health`), capped/dry-run harness installation for non-Claude-Code custom LLMs (`ctx-harness-install --dry-run`), a council runner over diffs (`ctx-toolbox run`), and a local monitoring dashboard (`ctx-monitor serve`).

## How we tested it

**Evidence:** REVIEW

Method: inspected the GitHub repo metadata and README only. Did NOT install the PyPI package, build the graph, run `ctx-init`, or execute any recommendations. No hands-on metrics are reported below — claims are sourced from the README and repo description, which are noted as such.

```bash
gh api repos/stevesolun/ctx
gh api repos/stevesolun/ctx/readme --jq '.content' | base64 -d
```

Reviewed: repo description, topics, license, activity dates, and the full README (install flow, hook wiring, command surface, graph artifacts, CI preflight, monitoring dashboard).

## What worked

- **Directly targets a real gap this catalog also addresses**: with 91K+ skills, 460+ agents, and 10K+ MCP servers in the wild, knowing which to load is a genuine discovery + context-budget problem. ctx is a meta-tool that recommends tools — the same problem space as awesome-claude-code, awesome-agent-skills, and buildwithclaude, but graph-ranked and automated rather than a flat curated list.
- **Real Claude Code integration surface**: ships hooks (`PostToolUse`/`Stop`), a repo scanner, entity add/update flows with benefits/risks review, and a monitoring dashboard — it lives inside the dev loop rather than beside it.
- **Maturity signals are strong for a ~2-month-old repo**: published PyPI package (`claude-ctx`), MIT license, 4,091 collected tests per the README badge, a `ci_preflight.py` PR gate mirroring GitHub Actions, MkDocs Material docs site, active daily pushes (last push 2026-06-19).
- **Safety-conscious install model**: harness installs default to dry-run, entity updates print benefits/risks and skip replacement unless explicitly approved — good restraint for a tool that clones and runs third-party code.
- **Quality + health scoring** (four-signal skill quality, drift detection) goes beyond pure discovery into the Reflect stage (flagging skill rot).

## What didn't work or surprised us

- **Not installed or run** — all capability claims are README-sourced; recommendation quality, graph relevance, and false-positive rate are unverified.
- **Heavy footprint for a recommender**: requires downloading a large pre-built graph artifact (repo size ~723 MB; full `wiki-graph.tar.gz` expands 68K+ entity pages locally) and Python 3.11+. Semantic backend and harness runs are separate extras.
- **Self-reported figures are internally inconsistent**: repo description says 102,928 nodes / 91,464 skills; README badges/body say 79,958 nodes / 68,494 skills. Likely a snapshot-versioning lag, but it muddies the headline metrics.
- **Single-maintainer, young project** (created 2026-04-08, 518 stars, 4 subscribers) — adoption and longevity are unproven; the graph's freshness depends on one author's ingestion pipeline.
- **Recommendations are only as good as the indexed corpus** — a curated catalog (this repo) trades coverage for vetted, evaluated entries; ctx trades vetting for scale, so its ranking surfaces unvetted third-party skills/MCPs.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Surfacing the right task-specific skill/agent can improve output, but unverified without hands-on use |
| Speed | + | Automated discovery beats manually searching 91K skills; offset by graph download/setup cost |
| Maintainability | neutral | Recommends tools; doesn't change your codebase |
| Safety | + | Dry-run harness installs and benefits/risks update gates, though it surfaces unvetted third-party entities |
| Cost Efficiency | + | Core thesis is context-budget economy — load the right 10-15 entities instead of everything |

## Verdict

**CONDITIONAL**

ctx is a credible, actively-developed meta-tool that automates exactly the discovery + context-budget problem this catalog tackles by hand. The Claude Code hook integration, dry-run safety model, and CI maturity are real and distinguish it from flat curated lists (awesome-claude-code, awesome-agent-skills, buildwithclaude), which it overlaps with on purpose. Adopt it conditionally — when you regularly start work across unfamiliar stacks and want graph-ranked skill/agent/MCP suggestions, and you accept the heavy local graph footprint, a single-maintainer young project, and that its recommendations span unvetted third-party entities. Re-evaluate with hands-on installation to verify recommendation relevance and false-positive rate before promoting to ADOPT.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ctx](https://github.com/stevesolun/ctx) | tool | Graph-ranked skill, agent, MCP, and harness recommendations for the current task | Can't know which of 91K+ skills / 10K+ MCPs apply, and loading everything wastes context | awesome-claude-code, awesome-agent-skills, buildwithclaude |
