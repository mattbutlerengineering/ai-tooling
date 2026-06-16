# ai-tooling

Inventory and evaluation of AI tools, skills, agents, frameworks, harnesses, and workflows for building an ideal AI-assisted development setup.

Uses the [ACMM (AI Codebase Maturity Model)](https://arxiv.org/abs/2604.09388) as a framework for evaluating which tools matter at each maturity level.

## Install

Add as a Claude Code marketplace:

```bash
claude plugins:add-marketplace https://github.com/mattbutlerengineering/ai-tooling.git
claude plugins:install ai-tooling
```

This gives you four skills:

- `/setup-workflow` — bootstrap the recommended AI workflow in any repo
- `/evaluate-tool` — evaluate a new tool before adopting it (checks overlap, ACMM fit)
- `/audit-workflow` — audit your current setup against the recommended workflow
- `/update-catalog` — sync the catalog with current GitHub stars and local installs

## Contents

- [CATALOG.md](CATALOG.md) — flat inventory of every tool with definitions, problem statements, and overlap markers
- [WORKFLOW.md](WORKFLOW.md) — recommended tool stack per ACMM level, with exclusions and rationale
- [evaluations/](evaluations/) — 11 evidence-based evaluations covering every recommended tool:
  - [Code Understanding](evaluations/code-understanding.md) — codegraph + graphify > Understand-Anything > repomix
  - [Agent Harnesses](evaluations/agent-harnesses.md) — superpowers > compound-engineering > gstack > ECC > ruflo
  - [Memory Systems](evaluations/memory-systems.md) — claude-mem > agentmemory > OMEGA
  - [Skills Collections](evaluations/skills-collections.md) — mattpocock/skills + agent-skills > everything-claude-code
  - [Recommended Tools](evaluations/recommended-tools.md) — individual evaluations for 15 tools with no direct competitor
  - [Composio](evaluations/composio.md) — CONDITIONAL: skip below L4
  - [mem0 vs claude-mem](evaluations/mem0-vs-claude-mem.md) — keep claude-mem unless multi-tool or scale needs emerge
  - [New Tools (Loop 1)](evaluations/new-tools-loop1.md) — caveman, trailofbits/skills, book-to-skill, humanizer
  - [New Tools (Loop 2)](evaluations/new-tools-loop2.md) — claude-code-action, shadcn/improve, design-council
  - [New Tools (Loop 3)](evaluations/new-tools-loop3.md) — CLI-Anything, chrome-devtools-mcp, claude-subconscious, tokencost
  - [New Tools (Loop 4)](evaluations/new-tools-loop4.md) — Fabric, claude-task-master, scorecard, SimpleMem

## Quick Start

After installing, run `/setup-workflow` in any repo to bootstrap the recommended workflow. It creates a CLAUDE.md with quality-producing rules, checks your global tool installation, and identifies gaps for your target ACMM level.
