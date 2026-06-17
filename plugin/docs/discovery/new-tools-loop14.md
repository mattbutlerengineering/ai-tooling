# Loop 14 — Tool Evaluations (2026-06-17)

Discovery channels: GitHub starred repos gap analysis, GitHub search (flaky test, agent sandbox, agent eval, CI/CD AI), skills.sh (feature flags, monitoring, documentation, migration), web search (AI dev workflow best practices 2026).

## New Entries Added (3 total + 1 overlap fix)

### Skills & Plugins (2 entries)
| Tool | Stars | Verdict | Rationale |
|------|-------|---------|-----------|
| agent-browser | 36K | ADD | Vercel's browser automation CLI for AI agents; backs our installed skill |
| azure-skills | 1.2K | ADD | Microsoft's official Azure plugin with 258K skills.sh installs; complements microsoft/skills |

### MCP Servers (1 entry + 1 fix)
| Tool | Stars | Verdict | Rationale |
|------|-------|---------|-----------|
| github-mcp-server | 31K | ADD | GitHub's official MCP server; replaces community server-github as first-party |
| server-github overlap fix | — | FIX | Updated server-github's overlap column to reference github-mcp-server |

## Evaluated but Skipped

| Tool | Stars | Reason |
|------|-------|--------|
| onyx-dot-app/onyx | 30K | General AI chat platform, not dev workflow-specific |
| himself65/finance-skills | 2.8K | Domain-specific finance skills; too niche for catalog |
| ruvnet/RuView | 74K | WiFi spatial intelligence — not AI dev tooling |
| ctrf-io/github-test-reporter | 356 | Flaky test detection in GH Actions; too low stars |
| box/flaky | 397 | pytest flaky test retry plugin; too niche/low stars |

## Skills.sh Landscape Scan

| Skill | Installs | Assessment |
|-------|----------|------------|
| microsoft/azure-skills@azure-upgrade | 258K | Massive adoption; azure-skills repo added to catalog |
| launchdarkly/agent-skills@onboarding | 2.4K | Best feature flag skills; LD not added (vendor-specific) |
| ruvnet/ruflo@observe-metrics | 445 | Ruflo already in catalog; observe-metrics is one of its skills |
| ahmedasmar/devops-claude-skills@monitoring-observability | 413 | DevOps monitoring skill; not standalone enough for catalog |
| sickn33/antigravity-awesome-skills@react-nextjs-development | 867 | Antigravity already in catalog; react-nextjs is one skill |

## Workflow Optimization Insights (from web research)

Key 2026 best practices aligned with our WORKFLOW.md:
1. **Agent-driven test loops** — already in our inner loop as TDD cycle
2. **Plan before generating** — already in our outer loop Design stage
3. **Small diffs with verification** — already in inner loop Verify stage
4. **Stop rules for bounding agents** — partially covered by our Safety signal; could expand
5. **AI code attribution tracking** — covered by our AI code churn rate metric in Ship stage
6. **70% of devs use 2-4 AI tools** — validates our multi-tool catalog approach

No WORKFLOW.md changes needed this loop — our structure already captures the 2026 consensus.

## Niche Areas Explored (Thin Results)

- **Flaky test detection**: No open-source tool with >500 stars; dominated by SaaS (TestDino, Katalon)
- **Prompt management**: Nearly empty category on GitHub; prompts are co-located with code in 2026
- **Agent sandbox/container**: Only NerdBaba/Octopus (2 stars); agents use git worktrees instead
- **AI code benchmarks**: No results; benchmarking is SaaS-dominated (SWE-bench, Aider leaderboard)

## Catalog count: 203 -> 206 entries (3 added)
