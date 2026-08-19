# Evaluation: autoprompt-skill

**Repo:** [Spielewoy/autoprompt-skill](https://github.com/Spielewoy/autoprompt-skill)
**Stars:** 141 | **Last updated:** 2026-08-19 (pushed) | **License:** MIT
**Last verified:** 2026-08-19
**Last triaged:** 2026-08-19  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Coding-agent skill (MIT) that restructures a prompt before execution, across 6 agent providers, with a published Terminal-Bench 2.1 benchmark (self-reported)." Installed as a global npm CLI (`autoprompt-skill`), it wraps a task prompt through an agent-specific rewriting pass before the underlying coding agent (Claude Code, Codex, OpenCode, Kilo, VS Code, Prime) starts work. README claims a 45% reduction in agentic-task failures and +14.61 points on Terminal-Bench 2.1; these are self-reported and not independently reproduced here.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata, README, and the CATALOG "Overlaps with" cell. The benchmark claims in the README are not independently verified by this evaluation and are not treated as fact here.

## Triage note

Left at `discovery-log` rather than SKIPped. `triage.py` bands this P2 (cites `superpowers`/GSD via its `agent-orchestration`/`prompt-engineering` topics), but autoprompt-skill solves a narrower, different-mechanism problem — prompt preprocessing before a task starts — than GSD's full Discuss→Plan→Execute→Verify→Ship orchestration loop. That is not the redundancy P2 asks a bulk pass to act on; a real hands-on comparison against the benchmark claim would need to be run to say more. Left for the P0/eval-runner lane.

_Triaged 2026-08-19 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [autoprompt-skill](https://github.com/Spielewoy/autoprompt-skill) | skill | Coding-agent skill (MIT) that restructures a prompt before execution, across 6 agent providers, with a published Terminal-Bench 2.1 benchmark (self-reported) | Ambiguous or underspecified prompts cause agentic coding tasks to fail; want structured prompt preprocessing before the agent starts work | superpowers, ECC, SkillOpt |
