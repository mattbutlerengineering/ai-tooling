# Evaluation: wikiskill

**Repo:** [ashutoshsinghpr7/wikiskill](https://github.com/ashutoshsinghpr7/wikiskill)
**Stars:** 30 | **Last updated:** 2026-08-30 (pushed) | **License:** MIT
**Last verified:** 2026-08-31
**Last triaged:** 2026-08-31  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

An arXiv-backed (2608.27454) implementation of self-evolving agent skills via a persistent knowledge wiki, for Hermes Agent — skills accumulate and refine from real runs rather than staying flat, with isolated skill gating and a documented live run log.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a leave decision that turns on differentiation from existing entries, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. wikiskill implements a specific published algorithm (WikiSkill, arXiv:2608.27454) for skills that evolve via a shared wiki rather than staying static — a different mechanism from `Recuris`'s recursive working-memory evolution and from `obsidian-second-brain`'s self-rewriting vault, both cited as overlaps. It targets Hermes Agent rather than Claude Code, so portability to this catalog's primary harness is itself an open question a mechanical SKIP can't answer. Worth a real look at whether the self-evolution claim holds up outside the paper's own benchmark.

_Triaged 2026-08-31 by the P3 backlog band._
