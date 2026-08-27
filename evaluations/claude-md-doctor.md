# Evaluation: claude-md-doctor

**Repo:** [agent-clinic/claude-md-doctor](https://github.com/agent-clinic/claude-md-doctor)
**Stars:** 4 | **Last updated:** 2026-08-26 (pushed) | **License:** MIT
**Last verified:** 2026-08-27
**Last triaged:** 2026-08-27  <!-- triaged: bulk -->
**Dev loop stage:** Plan (agent-instruction diagnostics)
**Layer:** Tooling

---

## What it does

A doctor-style checkup for CLAUDE.md/AGENTS.md files: audits size, flags dead
references, flags claims that have drifted from the code they describe, and
backtests each rule against the repo's own session history to see which rules
actually get followed, ignored, or never invoked — a report that cites its
evidence rather than a lint pass on prose alone.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place
the lead and check it against catalogued incumbents, not to validate the
backtesting claim against a real session corpus.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`. `triage.py` places this in P3 backlog — no catalogued
STACK pick's "Overlaps with" cell names it, so there is no structural redundancy
signal. It is closest in spirit to `reporails/cli` (AI-instructions diagnostics)
but differs in a specific way worth a real eval: it claims to backtest rules
against actual session history rather than only statically lint the instruction
file. Very early (4 stars, created three days before this pass) — worth watching
rather than escalating today.

_Triaged 2026-08-27 by the daily discovery pass (P3 backlog band)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-md-doctor](https://github.com/agent-clinic/claude-md-doctor) | tool | Doctor-style CLAUDE.md/AGENTS.md checkup (MIT) — size vitals, dead references, drifted claims, rule backtesting against session history | Instruction files rot silently — stale references, drifted claims, rules nobody follows; want an evidence-citing audit | reporails/cli, agnix, ACMM |
