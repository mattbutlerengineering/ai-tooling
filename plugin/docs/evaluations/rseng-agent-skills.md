# Evaluation: rseng-agent-skills

**Repo:** [fdiblen/rseng-agent-skills](https://github.com/fdiblen/rseng-agent-skills)
**Stars:** 13 | **Last updated:** 2026-09-07 (pushed) | **License:** MIT
**Last verified:** 2026-09-09
**Last triaged:** 2026-09-09  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

Research Software Engineering skills for AI coding agents — reproducibility, citation
handling, and code-quality checks aimed at bringing FAIR/reproducible-research discipline to
code an agent writes for academic/research projects.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on
redundancy with a catalogued incumbent, not on the tool's behaviour — a question the overlap
answers directly. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`: no structural disposition applies — brooks-lint/mkanat-skills/
skylos are general-purpose code-quality tools, none of them scoped to research-software
conventions (citation, FAIR compliance, reproducibility) the way this skill pack is. Narrow
academic-research niche; worth a look if this catalog starts tracking research-software
tooling specifically, but not urgent backlog otherwise.

_Triaged 2026-09-09 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [rseng-agent-skills](https://github.com/fdiblen/rseng-agent-skills) | skill | Research Software Engineering skills (MIT) for AI coding agents — reproducibility, citation, and code-quality checks for research code | Research code AI agents produce rarely meets FAIR/reproducibility standards; want RSE discipline built into the agent's skill set | brooks-lint, mkanat/skills, skylos |
