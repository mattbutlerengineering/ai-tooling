# ai-tooling

An operating manual for AI-assisted development that produces high-quality code — and keeps getting better.

Evaluates tools against five quality signals (Correctness, Speed, Maintainability, Safety, Cost Efficiency) across the dev loop stages where they intervene.

## Install

Add as a Claude Code marketplace:

```bash
claude plugins:add-marketplace https://github.com/mattbutlerengineering/ai-tooling.git
claude plugins:install ai-tooling
```

This gives you five skills:

- `/setup-workflow` — bootstrap the recommended AI workflow in any repo
- `/evaluate-tool` — evaluate a new tool before adopting it (checks stage fit, quality signals, overlap)
- `/audit-workflow` — audit your current setup against the recommended workflow
- `/update-catalog` — sync the catalog with current GitHub stars and local installs
- `/sync-stars` — find starred repos not in CATALOG.md and generate ready-to-paste entries

## Contents

- [WORKFLOW.md](WORKFLOW.md) — the dev loop (inner + outer), tools per stage, quality signals, adoption guide
- [CATALOG.md](CATALOG.md) — flat inventory of 412 tools with definitions, problem statements, and overlap markers
- [COMPARISON.md](COMPARISON.md) — all tools at a glance with evaluation status by dev loop stage
- [STACK.md](STACK.md) — the ~25 tools worth installing, distilled from 406 evaluations
- [evaluations/](evaluations/) — 406 evidence-based evaluations with verdicts (ADOPT/CONDITIONAL/SKIP)

## Quick Start

After installing, run `/setup-workflow` in any repo to bootstrap the recommended workflow. It creates a CLAUDE.md with quality-producing rules, checks your global tool installation, and identifies gaps.

## The Workflow

Two loops, three layers, five signals.

**Inner loop** (single task): Plan → Implement → Verify → Review → Ship, with Reflect as the feedback arc.

**Outer loop** (epic/project): Discover → Architect → Decompose → [inner loop per task] → Integrate → Retrospect.

**Three layers** per stage: Process (what you do), Tooling (what automates it), Infrastructure (what measures it) — connected by feedback arcs that close the loop.

**Five quality signals**: Correctness, Speed, Maintainability, Safety, Cost Efficiency. Every tool is justified by which signals it moves.

**Adopt in layers**: Start with process (skills, conventions, TDD). Add infrastructure when you want data. Add orchestration when you want autonomy.

See [WORKFLOW.md](WORKFLOW.md) for the full operating manual.
