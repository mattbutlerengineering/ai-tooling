# ai-tooling Plugin

## Install

```bash
claude plugin marketplace add mattbutlerengineering/ai-tooling
claude plugin install ai-tooling@ai-tooling
```

Or from inside a session: `/plugin marketplace add mattbutlerengineering/ai-tooling`
then `/plugin install ai-tooling@ai-tooling`.

AI workflow toolkit organized around inner/outer dev loop stages and six quality signals (Correctness, Speed, Maintainability, Safety, Cost Efficiency, Verifiability).

## Skills

- `/setup-workflow` — bootstrap the recommended AI workflow in any repo (creates CLAUDE.md, checks global tools, identifies gaps)
- `/evaluate-tool` — evaluate a new AI tool before adopting it (checks catalog overlap, quality signal fit, dev loop stage)
- `/audit-workflow` — audit current setup against the recommended dev loop tool stack
- `/update-catalog` — sync the AI tooling catalog with current GitHub stars and local installs
- `/sync-stars` — find starred repos not in CATALOG.md and generate ready-to-paste entries

## Reference Documents

The plugin includes reference documents under `docs/`:
- `CATALOG.md` — flat inventory of 797 tools across 13 categories with overlap markers
- `WORKFLOW.md` — inner/outer dev loop stages, tools per stage, quality signals, adoption guide
- `evaluations/` — 813 evaluation and comparison files

Skills reference these docs via `${CLAUDE_PLUGIN_ROOT}/docs/` paths.

## Hooks

A SessionStart hook and a PostToolUse hook run automatically:

**SessionStart:**
- Checks if any evaluation file is >30 days old → prompts to run `/update-catalog`
- Checks for new GitHub stars not in the catalog → prompts to run `/update-catalog`
- Outputs nothing if everything is current (suppressed)

**PostToolUse (on Edit/Write):**
- Runs the repo's own canonical gates — `reconcile-counts.py --check` (catalog total,
  eval count and composition) and `sync-plugin-docs.sh --check` (`plugin/docs/` and
  `skills/` against root) — and surfaces whatever they report
- Alerts on drift so counts stay consistent across commits
- Silent no-op in a repo that doesn't carry those scripts
