# Evaluation: claude-sdlc-skills

**Repo:** [TsCarpe/claude-sdlc-skills](https://github.com/TsCarpe/claude-sdlc-skills)
**Stars:** 62 | **Last updated:** 2026-09-20 (pushed) | **License:** MIT
**Last verified:** 2026-09-23
**Last triaged:** 2026-09-23  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

An AI-native SDLC skill pack (Python, MIT) for Claude Code — five discrete skills covering
requirement intake & audit, an adversarial review gate, AI test orchestration, a decision re-check
step, and release config audit.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and
the README's description of the five skills. That is sufficient to catalog it and place it relative
to existing peers, not to support an ADOPT.

## Verdict

**discovery-log — tentative read**

## Triage note

P2 challenger by citation — `Overlaps with` names `GSD`, a STACK pick covering a full
Discuss->Plan->Execute->Verify->Ship loop. Not a clean redundancy: `claude-sdlc-skills` is five
narrower, independently-invocable skills (requirement audit, adversarial review gate, test
orchestration, decision re-check, release audit) rather than one cohesive framework, so it could
complement GSD's phases instead of duplicating the whole loop. Left at `discovery-log` rather than
SKIPped; whether the individual skills add anything GSD's own subagents don't already cover needs a
hands-on read, not a mechanical call.

_Triaged 2026-09-23 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [claude-sdlc-skills](https://github.com/TsCarpe/claude-sdlc-skills) | skill | AI-native SDLC skill pack (MIT) for Claude Code — requirement intake & audit, adversarial review gate, AI test orchestration, decision re-check, release config audit | Ad hoc AI-assisted development skips requirement audits, adversarial review, and release-config checks with nothing enforcing SDLC discipline | requirement-ledger, GSD, 8090 Software Factory |  |
