# Evaluation: claude-terse

**Repo:** [lowenbjer/claude-terse](https://github.com/lowenbjer/claude-terse)
**Stars:** 49 | **Last updated:** 2026-10-08 (pushed) | **License:** MIT
**Last verified:** 2026-10-11
**Last triaged:** 2026-10-11  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code plugin that cuts reply length roughly in half and strips mannered prose
(slogans, metaphors, recaps) from replies, docs, commits, and subagents; ships a
status-line context meter. The README reports 46-54% fewer words on its own benchmark
prompts (self-reported, unverified).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Catalog entry

| [claude-terse](https://github.com/lowenbjer/claude-terse) | plugin | Claude Code plugin (MIT) cutting reply length ~half and stripping mannered prose (slogans, metaphors, recaps) from replies, docs, commits and subagents; ships a status-line context meter | Claude Code answers simple questions with essays full of filler that cost output tokens and reading time | caveman, tldr, humanizer |  |

## Verdict

**SKIP** — redundant with `caveman`, STACK's already-adopted, measured tool for the same
job (cutting verbose/mannered Claude Code output down to natural, token-efficient
register). claude-terse's self-reported 46-54% word reduction is not run-backed here
and the problem it targets is the one caveman was already adopted to solve.

_Triaged 2026-10-11 by the P2 challenger band._
