# Evaluation: video-to-skill

**Repo:** [Lum1104/video-to-skill](https://github.com/Lum1104/video-to-skill)
**License:** MIT
**Last verified:** 2026-07-31
**Last triaged:** 2026-07-31  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling

---

## What it does

Turns videos and courses into evidence-grounded Agent Skills for Claude Code and Codex.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (Skill_Seekers, skill-creator, book-to-skill). That is
sufficient for a SKIP that turns on redundancy with a catalogued incumbent, not on the tool's
behavior — a question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Verdict

**SKIP** — redundant with `Skill_Seekers` (source-to-skill compiler that already scrapes docs
sites, GitHub repos, PDFs, **and videos**, packaging one knowledge asset for Claude, Gemini,
OpenAI, LangChain, and vector DBs). video-to-skill's video/course input is a subset of what
Skill_Seekers already ingests; it doesn't earn a second catalogued entry for the same job.

_Triaged 2026-07-31 by today's discovery lead._
