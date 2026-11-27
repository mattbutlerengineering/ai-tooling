# Evaluation: ai-sdlc-factory

**Repo:** [ai-sdlc-factory/ai-sdlc-factory](https://github.com/ai-sdlc-factory/ai-sdlc-factory)
**Stars:** 26 | **Last updated:** 2026-11-26 (pushed) | **License:** MIT
**Last verified:** 2026-11-27
**Last triaged:** 2026-11-27  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

An "AI software factory": label a ticket on Forgejo or GitHub and get back a
reviewed pull request. Role agents run in disposable sandboxes and only advise —
deterministic code decides what actually ships.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the CATALOG one-liner plus repo metadata from GitHub's search API (this session's
GitHub access is scoped to this repo only, so a direct per-repo metadata fetch was
not available; stars/license/pushed-date come from the search endpoint instead).

## Triage note

Banded P2 challenger — its "Overlaps with" cell names GSD, a STACK pick, so the
mechanical band applies. But GSD is an interactive context-engineering loop
(Discuss→Plan→Execute→Verify→Ship) run inside a session with restricted-tool
subagents, while ai-sdlc-factory is a ticket-triggered pipeline that runs disposable
sandboxed role agents end-to-end and deliberately keeps deterministic code, not an
agent's own judgement, as the gate on what ships. That's a meaningfully different
shape (automation trigger, sandbox isolation, and a non-agent decision gate), not a
confident redundancy call, so this is **left at `discovery-log`** rather than SKIPped
— it deserves a real hands-on eval, not a mechanical "redundant with GSD" verdict.

_Triaged 2026-11-27 by the daily discovery routine (new lead, same-day triage)._
