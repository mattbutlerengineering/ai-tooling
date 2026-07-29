# Evaluation: orchestkit

**Repo:** [yonatangross/orchestkit](https://github.com/yonatangross/orchestkit)
**Stars:** 199 | **Last updated:** 2026-07-10 (pushed) | **License:** MIT
**Last verified:** 2026-07-27
**Last triaged:** 2026-07-27  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An AI development toolkit for Claude Code that installs 103 skills, 36 orchestration agents, and 172 hooks covering full-stack development patterns — the same job as an agentic-skills framework that structures how Claude Code operates (debugging, TDD, code review, verification), just with a much larger bundled surface.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `superpowers` (obra/superpowers, ADOPT and already installed in STACK). superpowers already provides the structured agentic-skills framework (debugging, TDD, code review, verification workflows) that orchestkit's 103-skill/36-agent/172-hook bundle targets. A second, much heavier skills-framework plugin for the same job earns nothing without a differentiated capability the incumbent lacks; nothing in the one-liner suggests one.

_Triaged 2026-07-27 by the P2 challenger band._
