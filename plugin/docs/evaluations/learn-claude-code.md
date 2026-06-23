# Evaluation: learn-claude-code

**Repo:** [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)
**Stars:** 67,447 | **Last updated:** 2026-06-07 | **License:** MIT
**Dev loop stage:** Reference
**Layer:** Process

---

## What it does

A 12-stage progressive tutorial that teaches you to build a Claude Code-like agent harness from scratch in Python. Each stage (`s01` through `s12`) adds one capability — agent loop, tool use, todos, subagents, skill loading, context compaction, task system, background tasks, agent teams, team protocols, autonomous agents, worktree isolation — with a matching runnable Python script and English/Chinese/Japanese documentation. The full harness (`s_full.py`, 740 lines) combines all 12 stages into a working multi-agent system with team coordination, worktree isolation, and background tasks.

The README is an 462-line essay on "harness engineering" — a conceptual framework arguing that agency comes from model training, not code orchestration, and that the developer's job is building the vehicle (harness), not the driver (model). It traces the lineage from DQN Atari through AlphaStar to modern coding agents, framing Claude Code as the reference implementation of this pattern.

## How we tested it

**Evidence:** REVIEW

Architecture-review-based. Read the README, inspected the 12-stage progression, read `s01_agent_loop.py` (core loop), `s_full.py` (combined harness), and the task-system documentation. Verified repo structure: 557 files, 43 Python, 105 markdown, 3 languages.

```bash
gh api repos/shareAI-lab/learn-claude-code --jq '.stargazers_count, .updated_at, .license.spdx_id'
gh api repos/shareAI-lab/learn-claude-code/git/trees/main?recursive=1 --jq '.tree[].path'
# Read s01_agent_loop.py, s_full.py, docs/en/s07-task-system.md
```

## What worked

- **Progressive disclosure is exemplary.** Each stage adds exactly one concept with a runnable script. Stage 1 is 80 lines. Stage 12 has worktree isolation. You can stop at any stage and have a working agent.
- **The conceptual framework is the strongest in the catalog.** The "model is the driver, harness is the vehicle" framing with historical evidence (DQN → AlphaStar → LLM agents) gives readers the right mental model before they write any code.
- **Production patterns in the code.** `s01_agent_loop.py` includes readline UTF-8 fixes for macOS, `.env` override support, and clean Anthropic SDK usage — not toy code.
- **Real community engagement.** 10,962 forks, 74 open issues, merged PRs fixing real bugs (compaction pair handling, memory system prompt). Active maintenance.
- **Trilingual documentation.** English, Chinese, Japanese — broadest language coverage of any reference in the catalog.

## What didn't work or surprised us

- **Not a tool you install or run in your workflow.** This is a learning resource, not something that integrates with Claude Code or any agent. The value is knowledge transfer, not automation.
- **Chinese-primary authorship.** The README essay is excellent in English, but commit messages and issue discussions are predominantly Chinese, which may limit contribution from English-speaking developers.
- **740-line full agent is still minimal.** Compared to Claude Code's actual implementation, the full harness lacks permissions governance, hook systems, MCP routing, and prompt caching. It's a teaching scaffold, not a production harness.
- **No automated tests for the learning stages.** CI exists but test coverage is unclear — easy to break a stage without noticing.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Understanding how agent loops work prevents architectural mistakes in harness design |
| Speed | + | 12-stage progression gets readers to a working agent faster than reading source code |
| Maintainability | + | The "harness vs. model" mental model prevents overengineering orchestration code |
| Safety | neutral | Mentions permission boundaries conceptually but doesn't teach implementation depth |
| Cost Efficiency | neutral | No cost optimization content |

## Verdict

**CONDITIONAL**

Use as the first resource when learning how agent harnesses work or when onboarding engineers who will build custom agents. The progressive 12-stage structure is unmatched for building understanding from zero. Skip if you're already experienced with Claude Code internals — the conceptual framework is valuable but the code is deliberately simplified. The closest comparables in the catalog are `claude-code-system-prompts` (shows the real implementation) and `claude-code-best-practice` (practical tips) — learn-claude-code is the "how it works from first principles" resource between those two.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | reference | Build a Claude Code-like agent harness from scratch — 12-stage educational deep dive (67K stars) | Want to understand how agent harnesses work by building one | claude-howto, claude-code-system-prompts |
