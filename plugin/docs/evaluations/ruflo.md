# Evaluation: ruflo (formerly claude-flow)

**Repo:** [ruvnet/ruflo](https://github.com/ruvnet/ruflo)
**Stars:** 60,327 | **Last updated:** 2026-06-19 (v3.12.4, released 2026-06-18) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan + Implement + Verify + Review + Reflect (an orchestration + memory + learning layer over Claude Code)
**Layer:** Infrastructure (MCP server, hooks daemon, WASM kernels, vector DB) + Tooling (45 CLI commands, 35 plugins, 98 agents)

---

## What it does

Catalog one-liner: "Agent meta-harness with multi-agent swarms, adaptive memory, self-improvement." Ground truth: **ruflo is the rebranded `claude-flow`** (the GitHub `claude-flow` repo redirects here; npm still ships both `ruflo` and `claude-flow` packages, and many docs/issue links still say claude-flow). It is an MIT-licensed TypeScript orchestration layer that bolts onto **Claude Code** (and Codex) to turn a single-context coding assistant into a coordinated, memory-backed, self-learning swarm. Unlike omnigent (a *parallel* runtime that *invokes* Claude Code as one of several harnesses), ruflo's primary surface is *inside* your Claude Code session: `npx ruflo init` writes a `CLAUDE.md` with routing rules, registers an **MCP server exposing 323 tools** (`memory_store`, `swarm_init`, `agent_spawn`, …), installs ~27 hooks, and seeds `.claude-flow/` with config + a vector memory store. After that you "just use Claude Code normally" and the hooks route tasks, retrieve memory, and coordinate background agents.

The mechanism stack: (1) **Swarm coordination** — queen-led hierarchical/mesh/adaptive topologies with consensus (Raft/Byzantine/Gossip); (2) **Vector memory** — AgentDB with HNSW indexing for sub-ms semantic retrieval across sessions; (3) **Self-learning** — "SONA" neural patterns + ReasoningBank + trajectory learning that feed successful patterns back into routing; (4) **Federation** — zero-trust cross-machine agent comms (mTLS + ed25519, PII-stripping pipeline, behavioral trust scoring); (5) **MetaHarness** — a *separate* dev-loop tool (`/harness-score`, `/harness-genome`, `/harness-mcp-scan`, `/harness-threat-model`, `/harness-mint`) that grades your agent setup (1-100 readiness), statically scans tool/MCP configs for security risks, and can `eject` a ruflo project into a standalone toolkit. There are two install paths: **Path A** Claude Code plugins (`/plugin marketplace add ruvnet/ruflo`, slash commands only, zero workspace files, no MCP) and **Path B** full CLI `init` (98 agents, 60+ commands, 30 skills, MCP server, hooks, daemon).

## How we tested it

**Evidence:** REVIEW

**Method: inspected the GitHub repo, full README, STATUS.md, the metaharness plugin README + ADR-150, and verified that the cited evidence artifacts actually exist, via the GitHub API and npm stats. Did NOT install or run it.** This is a deliberate non-install architecture/surface-area review, same lens as omnigent (CONDITIONAL) and oh-my-openagent (SKIP). ruvnet ships many high-claim repos, so the explicit goal here was *substance verification*: do the benchmark/audit docs the README links actually exist, and is the Claude Code integration real and installable? Installing the full Path B (MCP server + hooks daemon + WASM kernels + AgentDB + 323 tools writing to `CLAUDE.md`/`.claude-flow/`) is out of scope for a placement call and would heavily mutate the harness. No metrics below are measured by us; star/download/release counts are live API calls, and all performance/accuracy figures (HNSW speedups, "89% routing accuracy", SOTA-vs-LangGraph matrix) are the **project's own self-reported claims** — though, unusually for this author, the cited backing artifacts do exist (see below).

```bash
gh api repos/ruvnet/ruflo --jq '{stars,license,description,pushed_at,created_at}'
# 60,327 stars; MIT; created 2025-06-02; pushed 2026-06-19; "🌊 The leading agent meta-harness for Claude"
gh api repos/ruvnet/ruflo/readme --jq '.content' | base64 -d                      # full README (415 lines)
gh api repos/ruvnet/ruflo/contents/docs/STATUS.md --jq '.content' | base64 -d      # "what currently works" doc
gh api repos/ruvnet/ruflo/contents/plugins/ruflo-metaharness/README.md            # MetaHarness skills + ADR-150 contract
# Substance checks — do the README's cited evidence files actually exist?
gh api repos/ruvnet/ruflo/contents/docs/reviews/intelligence-system-audit-2026-05-29.md  # EXISTS, 15,821 bytes
gh api repos/ruvnet/ruflo/contents/scripts/benchmark-intelligence.mjs                     # EXISTS, 27,029 bytes
gh api repos/ruvnet/ruflo/contents/.claude-plugin/marketplace.json                        # EXISTS, 7,721 bytes
gh api repos/ruvnet/ruflo/contents/plugins --jq '[.[]|select(.type=="dir")]|length'       # 35 plugin dirs
gh api repos/ruvnet/ruflo/releases --paginate --jq '.[].tag_name' | wc -l                 # 1,539 releases (v3.12.4)
gh api "repos/ruvnet/ruflo/commits?since=2026-05-19" --paginate --jq '.[].sha' | wc -l    # 425 commits / 30d
curl -s https://api.npmjs.org/downloads/point/last-month/ruflo        # 277,726 /mo
curl -s https://api.npmjs.org/downloads/point/last-month/claude-flow  # 131,368 /mo
```

Reviewed: the README capability matrix and "With vs Without Ruflo" table; STATUS.md's test baseline (1999/1999 cli vitest green, 366/366 federation vitest green) and capability inventory; the two-path install model (#1744); the metaharness plugin's ADR-150 "removable augmentation / graceful degradation / CI gate" contract and its five skills; the existence (not the correctness) of the cited intelligence audit, benchmark script, and SOTA matrix.

## What worked

- **The cited evidence actually exists — this is not pure vapor.** The README's headline HNSW claim links to a 15.8KB audit doc *and* a 27KB reproducible benchmark script, both present in-repo. The metaharness plugin enforces a real ADR (ADR-150) with a CI gate (`no-metaharness-smoke.yml`) asserting ruflo still works with `--no-optional`. For a prolific high-claim author, this is meaningfully better substance-to-marketing than the typical ruvnet repo, and clears the skepticism bar the task flagged.
- **Exceptional maturity signals.** 60.3k stars, ~278k npm downloads/month on `ruflo` (+131k still on `claude-flow`), 1,539 releases, v3.12.4, 425 commits in the last 30 days, MIT-licensed (truly open source, unlike oh-my-openagent's SUL-1.0). STATUS.md reports 1999/1999 + 366/366 green test suites. This is among the highest-traffic projects in the inventory.
- **Claude Code integration is first-class and installable *into your session* — it extends rather than replaces.** Path A is a real Claude Code marketplace (`/plugin marketplace add ruvnet/ruflo`, 35 plugins, verified marketplace.json) and Path B registers an MCP server + hooks that augment the existing Claude Code loop. This is the inverse of oh-my-openagent (which replaces the front-end) and unlike omnigent (which runs a parallel server) — ruflo sits *inside* the CC loop.
- **MetaHarness is a genuine dev-loop-against-your-repo tool.** `/harness-score`, `/harness-mcp-scan`, and `/harness-threat-model` run against *your* project to grade agent-setup readiness and statically flag MCP/tool security risks — Reflect/Review-stage value that stands on its own even if you skip the swarm machinery.
- **Honest two-path documentation.** The README explicitly warns that Path A does NOT register the MCP server (so `memory_store`/`swarm_init` are unavailable) and that only Path B is "production use — everything works as documented." That candor about surface-area differences is a good sign.

## What didn't work or surprised us

- **Enormous, sprawling surface area — the dominant risk.** 323 MCP tools, 45 CLI commands, 98 agents, 35 plugins, 27 hooks, swarms, federation, SONA, ReasoningBank, AgentDB, WASM kernels, GOAP planner, web UI, neural-trader/IoT/market-data domain plugins. The README itself concedes "you don't need to learn 314 MCP tools," which is a tell: this is a platform, not a tool. Concept count and cognitive load dwarf focused entries like superpowers or claude-squad.
- **Heavy install + harness mutation (Path B).** Full init writes routing rules into your `CLAUDE.md`, seeds `.claude-flow/`, installs a hooks daemon, and registers a 323-tool MCP server. That is a large, opinionated takeover of the Claude Code config — far heavier than adding a plugin, and a lot to trust running in the background.
- **Self-reported, provider-shifting performance claims.** "89% routing accuracy", "1.3×–1953× vs LangGraph/AutoGen/CrewAI", the HNSW speedups — all the project's own numbers (the SOTA matrix even lives on an off-main `perf/` branch + a gist). The backing artifacts exist, but we did not reproduce any figure, and the self-improvement/"agents get smarter" framing remains unbenchmarked by us.
- **653 open issues** against 32 contributors and a 1,539-release / 425-commit-per-month cadence signals a very high churn, single-vision project. Expect breaking changes, half-migrated naming (ruflo vs claude-flow vs @claude-flow/* across npm, issue links, and badges), and feature surface that moves faster than it stabilizes.
- **Branding/identity sprawl.** Hosted UIs (flo.ruv.io, goal.ruv.io), Cognitum.One, RuVector, ruvLLM, neural-trader, agentic-flow, Flow Nexus — the ecosystem pulls toward a constellation of related properties, some hosted/commercial, which complicates "what am I actually adopting."

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | +/- | Cross-session vector memory + learned routing + dedicated reviewer/tester agents can raise quality; offset by unverified self-improvement claims and a huge surface that's hard to reason about |
| Speed | + | Parallel swarm agents + background workers + HNSW sub-ms retrieval (self-reported ~1.9×–4.7× over brute force above crossover); fan-out for parallelizable work |
| Maintainability | - | Path B mutates `CLAUDE.md`/`.claude-flow/`, installs a hooks daemon + 323-tool MCP, and adds a sprawling platform you must keep updated through fast churn and an in-flight rename |
| Safety | +/- | AIDefence (prompt-injection/PII), CVE remediation, federation zero-trust, `ruflo verify` signed-witness, and MetaHarness security scans are real positives; offset by a large autonomous background daemon with broad tool access |
| Cost Efficiency | + | Multi-provider routing (Claude/GPT/Gemini/Cohere/Ollama) with failover + a `ruflo-cost-tracker` plugin (budgets, alerts); cheap models can take cheap work |

## Verdict

**CONDITIONAL**

ruflo (formerly claude-flow) clears the bar that oh-my-openagent did not, and lands like omnigent: it is a Claude-Code-integrated orchestration layer you run *with* and *against* your own repo — installable as real CC plugins (Path A) or a full MCP/hooks loop (Path B) — spanning Plan, Implement, Verify, Review, and Reflect. Crucially for a prolific high-claim author, the substance checks out where it counts: the cited audit and benchmark artifacts exist, there's an ADR-governed plugin with a CI removability gate, green test suites, and genuinely first-class Claude Code integration. It is MIT-licensed and among the most-used projects in the catalog (60k stars, ~278k downloads/month).

It is CONDITIONAL rather than ADOPT because (a) the full install is a heavy, opinionated platform with an enormous surface (323 MCP tools, 98 agents, 35 plugins, a background hooks daemon) that takes over your `CLAUDE.md`/`.claude-flow/` — a large trust and maintenance commitment, not a focused tool; (b) the marquee performance and self-improvement claims are self-reported and not reproduced here; and (c) 653 open issues + a 1,539-release / 425-commit-per-month cadence + an in-flight ruflo↔claude-flow rename mean real churn. **Adopt it when** you specifically want persistent cross-session vector memory and multi-agent swarm/federation coordination layered onto Claude Code and can tolerate a heavy install and fast-moving platform — or adopt *just* Path A (e.g. `ruflo-metaharness` for setup grading + MCP security scans, or `ruflo-rag-memory`) to get targeted value without the full daemon.

**Differentiation:** vs **omnigent** (CONDITIONAL) — both are large multi-agent orchestration layers, but omnigent is a *parallel* Python server/UI that *invokes* Claude Code (and Codex/Cursor/Pi) as one of several swappable harnesses with a governance/policy engine, whereas ruflo installs *into* the Claude Code session itself (MCP + hooks + `CLAUDE.md` routing) and centers on persistent vector memory + self-learning + federation rather than harness-swapping. omnigent is alpha/days-old; ruflo is v3.x with years of releases. vs **oh-my-openagent** (SKIP) — OmO replaces the front-end (runs on OpenCode/Codex, SUL-licensed); ruflo augments Claude Code directly and is MIT. vs **superpowers / oh-my-claudecode** (focused CC skill/plugin collections) — those are lean, in-loop skill libraries; ruflo is a far heavier full platform (memory DB, daemon, federation, WASM) with overlapping swarm/agent functionality but an order of magnitude more surface. vs the **MetaHarness** component specifically — its setup-grading + MCP-security-scan role overlaps with this catalog's own evaluate-tool/audit-workflow skills, but as a runnable scorer rather than a manual rubric.

Re-evaluate toward ADOPT if the rename stabilizes to a single name, the open-issue count and churn settle, and an independent (non-author) benchmark confirms the swarm/memory/self-improvement wins — or down to a narrower recommendation if hands-on install reveals the background daemon to be fragile or noisy.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ruflo](https://github.com/ruvnet/ruflo) | harness | Claude Code orchestration layer (formerly claude-flow): multi-agent swarms, HNSW vector memory, self-learning, federation, MetaHarness scoring | Want persistent cross-session memory + coordinated multi-agent swarms + setup auditing layered onto Claude Code, not a single isolated session | omnigent, oh-my-claudecode, superpowers |
