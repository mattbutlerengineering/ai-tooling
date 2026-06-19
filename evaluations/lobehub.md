# Evaluation: LobeHub

**Repo:** [lobehub/lobehub](https://github.com/lobehub/lobehub)
**Stars:** 78,828 | **Last updated:** 2026-06-19 | **License:** LobeHub Community License (Apache-2.0 base with commercial restrictions)
**Dev loop stage:** Implement (Agent Orchestration)
**Layer:** Infrastructure

---

## What it does

LobeHub is a self-hosted agent operations platform — a "Chief Agent Operator" that hires, schedules, and reports on teams of AI agents. It provides a web UI for creating agents with multi-model support, connecting 10,000+ skills/MCP plugins, scheduling agent runs, organizing work by project, and enabling agent collaboration through "Agent Groups" with shared context. Agents can be deployed to messaging channels (Slack, Discord, Telegram) and run on schedules without human presence.

The v2 architecture (current) adds an Operator mode where agents are treated as units of work with scheduling, reporting, and IM gateway integration. Self-hosting options include Vercel, Docker, and Alibaba Cloud.

## How we tested it

Architecture review of the repository, README, feature documentation, release history, and ecosystem. Not installed locally — LobeHub is a full-stack web application (Next.js + PostgreSQL) that replaces rather than augments Claude Code.

```
gh api repos/lobehub/lobehub --jq '.description, .stargazers_count, .license.spdx_id'
gh api repos/lobehub/lobehub/contents/LICENSE --jq '.content' | base64 -d | head -20
gh api repos/lobehub/lobehub/releases --jq '.[0:3] | .[] | "\(.tag_name) — \(.published_at)"'
```

## What worked

- Massive ecosystem: 78.8K stars, 15.4K forks, 282 runtime dependencies, multiple daily canary releases — heavily invested
- Agent Groups with shared context, scheduled runs, and project organization is a genuinely novel collaboration model
- 10,000+ skills/MCP support means near-universal tool connectivity
- Multi-model: supports Claude, GPT, Gemini, DeepSeek, and many more simultaneously
- Agent Builder with auto-configuration reduces setup friction
- Personal Memory system with white-box (editable) memory and continual learning

## What didn't work or surprised us

- **Not a coding agent** — LobeHub is an agent operations platform, not a CLI coding tool. It doesn't write code, run tests, edit files, or integrate with git/CI. Same fundamental gap as cherry-studio (SKIP).
- Custom license with commercial restrictions — not truly open source despite the star count
- Heavyweight infrastructure: full Next.js app + PostgreSQL + S3-compatible storage
- The "Operator" framing (hiring, scheduling, reporting) targets enterprise agent fleet management, not individual developer workflow
- 450 open issues suggest scaling complexity

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't participate in the code-writing loop |
| Speed | neutral | Agent scheduling could save time on repetitive tasks, but not in a dev workflow context |
| Maintainability | neutral | No impact on codebase quality |
| Safety | neutral | Doesn't review or scan code |
| Cost Efficiency | - | Additional infrastructure costs (hosting, database, storage) with no dev-loop token savings |

## Verdict

**SKIP**

LobeHub is an impressive agent operations platform (78.8K stars, active daily development), but it operates outside the development loop. Like cherry-studio (also SKIP), it's a multi-model AI workspace — not a coding agent. It doesn't write code, run tests, edit files, or integrate with CI. The scheduling and team collaboration features target enterprise agent fleet management, not the Plan→Implement→Verify→Review→Ship cycle this catalog evaluates. Developers using Claude Code gain nothing from adding LobeHub to their workflow.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [lobehub](https://github.com/lobehub/lobehub) | platform | Agent operations platform — hire, schedule, and report on 7x24 AI agent teams | Want always-on agent fleet management with scheduling and reporting | claude-squad, OpenHands |
