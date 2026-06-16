# ai-tooling

Inventory and evaluation of AI tools, skills, agents, frameworks, harnesses, and workflows for building an ideal AI-assisted development setup.

Uses the [ACMM (AI Codebase Maturity Model)](https://arxiv.org/abs/2604.09388) as a framework for evaluating which tools matter at each maturity level.

## Contents

- [CATALOG.md](CATALOG.md) — flat inventory of every tool with definitions, problem statements, and overlap markers
- [WORKFLOW.md](WORKFLOW.md) — recommended tool stack per ACMM level, with exclusions and rationale

## Skills

Installable skills for maintaining this workflow:

- [`/evaluate-tool`](skills/evaluate-tool/SKILL.md) — evaluate a new tool before adopting it (checks overlap, ACMM fit)
- [`/audit-workflow`](skills/audit-workflow/SKILL.md) — audit your current setup against the recommended workflow
- [`/update-catalog`](skills/update-catalog/SKILL.md) — sync the catalog with current GitHub stars and local installs
