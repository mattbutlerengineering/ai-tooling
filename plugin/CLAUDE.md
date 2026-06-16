# AI Tooling Plugin

ACMM-based AI workflow toolkit. Provides skills for adopting and maintaining an optimal AI-assisted development workflow.

## Skills

- `/setup-workflow` — bootstrap the recommended AI workflow in any repo (creates CLAUDE.md, checks global tools, identifies gaps)
- `/evaluate-tool` — evaluate a new AI tool before adopting it (checks catalog overlap, ACMM-level fit)
- `/audit-workflow` — audit current setup against the recommended ACMM-leveled tool stack
- `/update-catalog` — sync the AI tooling catalog with current GitHub stars and local installs

## Reference Documents

The plugin includes reference documents under `docs/`:
- `CATALOG.md` — flat inventory of 89+ AI tools with overlap markers
- `WORKFLOW.md` — recommended tool stack per ACMM level (L2-L6) with daily practice guide
- `evaluations/` — evidence-based comparisons for each tool overlap group

Skills reference these docs via `${CLAUDE_PLUGIN_ROOT}/docs/` paths.
