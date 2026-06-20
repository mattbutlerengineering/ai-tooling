# ai-tooling Plugin

AI workflow toolkit organized around inner/outer dev loop stages and five quality signals (Correctness, Speed, Maintainability, Safety, Cost Efficiency).

## Skills

- `/setup-workflow` — bootstrap the recommended AI workflow in any repo (creates CLAUDE.md, checks global tools, identifies gaps)
- `/evaluate-tool` — evaluate a new AI tool before adopting it (checks catalog overlap, quality signal fit, dev loop stage)
- `/audit-workflow` — audit current setup against the recommended dev loop tool stack
- `/update-catalog` — sync the AI tooling catalog with current GitHub stars and local installs
- `/sync-stars` — find starred repos not in CATALOG.md and generate ready-to-paste entries

## Reference Documents

The plugin includes reference documents under `docs/`:
- `CATALOG.md` — flat inventory of 476 tools across 13 categories with overlap markers
- `WORKFLOW.md` — inner/outer dev loop stages, tools per stage, quality signals, adoption guide
- `evaluations/` — 469 evidence-based evaluation and comparison files

Skills reference these docs via `${CLAUDE_PLUGIN_ROOT}/docs/` paths.

## Hooks

A SessionStart hook and a PostToolUse hook run automatically:

**SessionStart:**
- Checks if any evaluation file is >30 days old → prompts to run `/update-catalog`
- Checks for new GitHub stars not in the catalog → prompts to run `/update-catalog`
- Outputs nothing if everything is current (suppressed)

**PostToolUse (on Edit/Write):**
- Validates catalog entry count in CLAUDE.md matches actual CATALOG.md rows
- Validates evaluation file count in README.md and CLAUDE.md matches actual files
- Alerts on drift so counts stay consistent across commits
