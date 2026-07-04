# Evaluation: skill-seekers

**Repo:** [yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)
**Stars:** 14,197 | **Last updated:** 2026-06-16 (pushed; created 2025-10-17) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Outer-loop **Reflect / setup** — a one-time ingestion step that converts external knowledge (docs sites, repos, PDFs, videos) into a reusable skill/RAG asset *before* the inner loop runs. Not invoked per task; you run it to provision a skill, then the inner loop consumes it.
**Layer:** Tooling (a Python CLI + MCP server with a scraping/chunking/packaging pipeline; produces artifacts, does not run inside your dev session)

---

## What it does

Skill Seekers is a **source-to-skill compiler**: point it at a documentation site, a GitHub repo (`facebook/react`), a local project, a PDF, a Jupyter notebook, a wiki, or a YouTube/local video, and it scrapes, chunks, and synthesizes the content into a structured "knowledge asset" — then *packages* that one asset for many downstream targets. The headline workflow is three commands: `skill-seekers create <source>` builds the asset, `skill-seekers package output/<name> --target claude` emits a Claude AI Skill (SKILL.md + YAML, zipped), and the same asset re-exports to Gemini, OpenAI/Custom GPT, LangChain Documents, LlamaIndex TextNodes, Haystack, Pinecone/Chroma/FAISS/Qdrant markdown, IBM Bob, and Cursor `.cursorrules` — the README claims 18 source types in and 21 export targets out, "one prep, every target."

It positions itself as "the data layer for AI systems," i.e. the preprocessing stage shared by skill authoring *and* RAG ingestion. The README advertises 500+ line SKILL.md outputs with examples/patterns/guides, "smart chunking" that preserves code blocks, and a `scan` command where an AI agent reads a project's manifests/README/Dockerfile/CI and emits one config per detected framework (pinning detected versions so re-runs report bumps). Enhancement during `create` is delegated to a configurable agent (`--agent claude|kimi|codex` or a custom command). It ships as a multi-repo ecosystem (core CLI/MCP here, plus website, community config registry, GitHub Action, Claude Code plugin, Homebrew tap), is on PyPI as `skill-seekers`, and exposes 40 MCP tools.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** Nothing was `pip install`ed; no `create`/`package`/`scan` was executed; no generated SKILL.md was inspected for quality on a real doc set. Every claim below comes from GitHub metadata, the README, the file tree, and release listing — not from observed pipeline output. The "99% faster," "500+ line," "battle-tested," and "3,700+ tests passing" figures are the author's README/badge framing, not anything I measured or ran.

```bash
gh api repos/yusufkaraaslan/Skill_Seekers --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id,lang:.language,issues:.open_issues_count}'
# {stars:14197, forks:1455, pushed:2026-06-16, created:2025-10-17, MIT, Python, issues:103}
gh api repos/yusufkaraaslan/Skill_Seekers/readme --jq '.content' | base64 -d | head -130
gh api "repos/yusufkaraaslan/Skill_Seekers/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # api/ configs/ src/ skills/ tests/ helm/ distribution/ + 12 README translations, Dockerfile.mcp
gh api repos/yusufkaraaslan/Skill_Seekers/releases --jq '.[0:3][] | {tag:.tag_name,date:.published_at[0:10]}'  # v3.8.0 (2026-06-15), v3.7.0, v3.6.0
gh api repos/yusufkaraaslan/Skill_Seekers/commits --jq 'length'   # 30 (page-1 cap; very active)
```

## What worked

- **Genuine breadth, and the "compile once, export everywhere" framing is the real value.** Most skill generators target one platform; Skill Seekers decouples *ingestion* from *packaging*, so the expensive scrape/chunk step is amortized across Claude, Gemini, OpenAI, and four+ vector DBs. That is a legitimately useful architectural choice for teams who feed the same docs into both a skill and a RAG index.
- **Strong release and engineering discipline.** 30+ tagged releases, semver (v3.8.0), CHANGELOG, multi-arch Docker (`Dockerfile.mcp`), Helm chart, GitHub Actions for tests/quality-metrics/scheduled-updates/vector-db-export, PyPI distribution, and 12 translated READMEs. This is a maintained product, not a weekend dump — rare for this category.
- **MCP server + 40 tools + Claude Code plugin** mean it can run in-session if you want, not only as an offline CLI.
- **`scan` is the standout feature.** Detecting frameworks from a project's manifests and emitting per-framework configs (version-pinned, re-runnable for drift) turns skill provisioning into something repeatable and CI-able — closer to dependency management than one-shot generation.

## What didn't work or surprised us

- **Output quality is entirely unverified and is the whole ballgame.** A "500+ line SKILL.md" scraped from a docs site is exactly the failure mode Anthropic's skill-creator and SkillOpt push *against*: long, unfocused skill text dilutes triggering and burns context. Scrape-and-synthesize optimizes for volume; nothing in the repo demonstrates the *brevity and precision* that actually make a skill fire correctly. We did not run it, so we cannot confirm the output is good — and the architecture biases toward bloat.
- **Quality depends on a second agent you supply.** `create --agent claude` means the synthesis quality is bounded by whatever model you wire in and its prompt — the tool is a pipeline, not a guarantee. Cost and correctness are pushed onto the enhancement step.
- **Scraping has the usual liabilities** — brittleness vs. JS-heavy/auth-gated docs, licensing/ToS questions when ingesting third-party sites and YouTube, and silent staleness once the source changes (mitigated only partly by `scan` version-pinning).
- **Heavy marketing surface.** "The data layer for AI systems," Trendshift badge, website, Twitter, 21-target matrix — the framing oversells; the core is a competent scraper-packager, valuable but not a paradigm.
- **103 open issues** against very high velocity suggests breadth is outrunning polish across the 18 sources × 21 targets matrix; expect rough edges on the long-tail combinations.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / − | A well-scoped doc-derived skill can ground an agent in a library's real API; but unverified 500+ line synthesized output risks diluting triggering and injecting scraped errors. Quality hinges on the enhancement agent, untested here. |
| Speed | + | Genuine setup-time win: provisioning a skill/RAG asset from docs in minutes vs. hand-authoring; `--target` reuse avoids re-scraping per platform. |
| Maintainability | + | `scan` version-pins detected frameworks and re-runs to report drift; GitHub Action enables CI regeneration — better-than-typical answer to skill staleness. |
| Safety | − / neutral | Scrapes arbitrary external sites/videos (ToS/licensing exposure) and feeds them to an agent; generated skill text should be reviewed before trusting. No code from sources is executed, but injected instructions are a vector. |
| Cost Efficiency | − / neutral | The `create` enhancement step spends real agent tokens per source; long synthesized skills cost context on every later invocation. Amortized export across targets is the offsetting saving. |

## Verdict

**CONDITIONAL — adopt as a one-time provisioning tool for library/framework skills, with mandatory output review and trimming.** Skill Seekers is the most mature tool in its niche: a maintained, semver-released, multi-target source-to-skill *compiler* that legitimately separates ingestion from packaging. The catch is that it generates *volume* and leaves *precision* to a downstream agent — exactly inverse to where skill quality actually lives. Use it to bootstrap a skill from a big docs set, then hand the output to skill-creator-style evals/trimming before shipping. Do not treat its 500+ line outputs as production skills.

Compared to neighbors: **skill-creator** (anthropics) authors *one* skill with a draft→eval→trigger-optimization loop — it optimizes quality, not breadth, and is the natural finisher for Skill Seekers' raw output. **SkillOpt** (Microsoft) *trains* a compact skill against held-out scores — the rigorous opposite of scrape-and-synthesize. **openskills**/**capa** install/wire skills but don't generate them; Skill Seekers fills the *authoring-from-sources* gap none of those cover. It wins on breadth and ingestion; it loses on the one thing that matters most (concise, verified skill text), so it's a front-end to the quality tools, not a replacement.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) | tool | Source-to-skill compiler: scrapes docs sites / GitHub repos / PDFs / videos and packages one knowledge asset for Claude, Gemini, OpenAI, LangChain, and 4+ vector DBs (14.2K stars) | Hand-authoring a skill or RAG index from a library's docs is slow; need to ingest once and export to every AI platform | skill-creator (authors/optimizes one skill — natural finisher), SkillOpt (trains compact skills), openskills/capa (install/wire, don't generate) |
