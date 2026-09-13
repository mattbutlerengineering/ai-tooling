# Evaluation: SkillAdam

**Repo:** [ruc-datalab/SkillAdam](https://github.com/ruc-datalab/SkillAdam)
**Stars:** 36 | **Last updated:** 2026-09-07 (pushed) | **License:** NOASSERTION (no detected LICENSE file)
**Last verified:** 2026-09-13
**Last triaged:** 2026-09-13  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

Claude Code/Codex/Cursor plugin that iteratively evolves and improves an existing
agent skill — "one-click evolve your skill."

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on the license bar and on redundancy with a catalogued/STACK incumbent,
not on the tool's behaviour — questions the repo metadata and the overlap answer
directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — no declared license (GitHub's licensee detector reports `NOASSERTION`;
no LICENSE file, no license text in the README or manifest at the pushed commit).
A vendored plugin is copied into the consuming repo, so text carrying no license
grant cannot be copied in — the same mechanical bar `P4` applies, reached here via
the license check rather than the metadata cache (this repo is too new to have a
`repo-metadata.json` record yet). Separately, it also challenges `skill-creator`
(STACK, ADOPT, MEASURED) — the first-party draft→eval→benchmark→optimize
skill-authoring meta-skill — which already covers "improve an existing skill";
a second, unlicensed tool for the same job earns nothing even setting the license
aside.

_Triaged 2026-09-13 by the P2 challenger band._
