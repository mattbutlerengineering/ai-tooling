# Evaluation: Continuous-Claude-v3

**Repo:** [parcadei/Continuous-Claude-v3](https://github.com/parcadei/Continuous-Claude-v3)
**Stars:** 3,818 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Implement / Observability
**Layer:** Infrastructure

---

## What it does

A persistent, learning, multi-agent development environment built on Claude Code. Ships 108 skills, 32 agents, 44 hooks, and a Python backend (MCP server + TLDR code analysis CLI + PostgreSQL-backed memory). The core thesis is "compound, don't compact" — extract learnings into YAML handoffs before context fills up, then start fresh sessions that inherit accumulated knowledge.

Three distinctive subsystems:

1. **TLDR Code Analysis** — a 5-layer static analysis stack (AST → Call Graph → CFG → DFG → PDG) exposed as a `tldr` CLI tool. Claims 95% token savings vs reading raw files by providing structural summaries (~1,200 tokens for what would cost ~23K in raw reads).

2. **Hook-based skill activation** — a `UserPromptSubmit` hook reads `skill-rules.json`, matches the user's prompt against trigger patterns, and injects skill suggestions into context. This is a custom skill router built on Claude Code's hooks API.

3. **YAML handoffs** — ~400-token YAML documents that capture session state (goal, current status, test command, decisions, files touched) and are resumed by future sessions. More token-efficient than markdown handoffs.

## How we tested it

**Evidence:** REVIEW

Architecture review based on repo structure (1,176 files), README, hooks configuration, and key skill files (tldr-code, create_handoff, skill-activation). No hands-on installation — the setup requires Docker, PostgreSQL, Python 3.12+, and a 12-step wizard, making it unsuitable for quick evaluation.

```bash
gh api repos/parcadei/Continuous-Claude-v3 --jq '.stargazers_count'
# 3818

gh api "repos/parcadei/Continuous-Claude-v3/git/trees/main?recursive=1" --jq '[.tree[].path] | length'
# 1176

# Examined: settings.json (hook config), hooks/README.md, 
# skills/tldr-code/SKILL.md, skills/create_handoff/SKILL.md,
# opc/pyproject.toml (Python dependencies)
```

## What worked

- **TLDR code analysis concept is strong** — the 5-layer stack (AST, Call Graph, CFG, DFG, PDG) with graduated token costs per layer is a genuinely novel approach to context efficiency. If the implementation is solid, 95% savings on code exploration would be significant.
- **YAML handoffs are more token-efficient than markdown** — ~400 tokens vs ~2,000 for equivalent information. The structured format also makes them machine-parseable for future sessions.
- **Hook architecture is pre-bundled** — all hooks ship as pre-built JS bundles in `dist/`, so users don't need to `npm install` or build anything. Just clone and hooks work.
- **Scale of coverage** — 108 skills covering code analysis, debugging, building, agent orchestration, memory extraction, braintrust tracing, and more. 32 specialized agents with JSON configs.
- **Actively maintained** — last updated June 17, 2026; 3.8K stars indicates real community adoption.

## What didn't work or surprised us

- **Heavy infrastructure requirements** — Docker, PostgreSQL, Python 3.12+, uv package manager, and a 12-step setup wizard. This is not a "clone and go" experience despite the README's claim. Compare with superpowers (`claude install-plugin obra/superpowers`) or caveman (single skill install).
- **Massive dependency surface** — pyproject.toml includes scipy, matplotlib, plotly, shapely, tiktoken, openai SDK, fastapi, uvicorn, and more. The MCP server alone pulls in a significant dependency tree that most dev workflows won't need.
- **108 skills is likely too many** — at scale, skill selection becomes noisy. The skill router hook tries to solve this but adds yet another layer of indirection. Compare with superpowers (focused set of ~15 well-integrated skills) or mattpocock/skills (~10 curated skills).
- **"Agentica" subsystem ties to external proprietary infrastructure** — several skills reference `symbolica-agentica` SDK (a dependency in pyproject.toml), suggesting tight coupling with an external platform.
- **Replaces rather than extends Claude Code** — this is a full environment replacement, not a composable plugin. Installing it means adopting its entire workflow philosophy, memory system, hook architecture, and agent roster. Hard to cherry-pick individual features.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | TLDR's structural analysis provides more accurate code understanding than raw reads |
| Speed | +/- | YAML handoffs save resume time, but 12-step setup and Docker overhead slow adoption |
| Maintainability | - | 1,176 files with tight internal coupling; maintaining a fork diverging from upstream would be difficult |
| Safety | neutral | No specific security innovations; hook system runs arbitrary scripts |
| Cost Efficiency | + | TLDR's 95% token reduction and YAML handoffs (~400 tokens) are genuine savings if they work as claimed |

## Verdict

**CONDITIONAL**

Use when you want a fully integrated, opinionated development environment and are willing to commit to its workflow philosophy, Docker-based infrastructure, and Python stack. The TLDR code analysis concept and YAML handoff format are genuinely innovative, but the all-or-nothing architecture makes it impractical for teams that want to compose tools incrementally. For most users, superpowers (ADOPT) + caveman (ADOPT) + claude-mem (ADOPT) provides similar benefits — structured workflows, token efficiency, and cross-session memory — with far lower adoption cost.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Continuous-Claude-v3](https://github.com/parcadei/Continuous-Claude-v3) | harness | Persistent learning dev environment: 108 skills, TLDR code analysis, YAML handoffs | Context loss on compaction, token waste from reading full files, no cross-session continuity | superpowers, ralph-claude-code, claude-mem |
