# Evaluation: claude-code-plugins-plus-skills

**Repo:** [jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills)
**Stars:** ~2.6K | **License:** MIT
**Last verified:** 2026-08-02
**Last triaged:** 2026-08-02  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling

---

## What it does

An open-source marketplace of 471 plugins, 3,069 skills, and 347 agents for Claude Code, paired with the `ccpi` CLI package manager — search, install, and update extensions from the terminal ("install the CLI, then install any plugin with a single command"), similar in spirit to an npm for Claude Code extensions.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the repo's README and metadata (stars, license) gathered via web fetch. That is sufficient to catalog it and record what differentiates it from existing directory-style entries, but not to assess whether `ccpi` reliably installs/updates extensions in practice.

## Triage note

Left at `discovery-log` rather than SKIPped: unlike existing directory/hub entries (`buildwithclaude`, `claude-plugins-official`), this one ships an actual CLI package manager (`ccpi`) for search/install/update rather than just a browsable list — a meaningfully different mechanism, not a duplicate. That differentiation is worth a real hands-on eval (does `ccpi` actually work, is the catalog curated or scraped) rather than a mechanical SKIP as "redundant with buildwithclaude."

_Triaged 2026-08-02 by the daily discovery routine (today's new lead)._
