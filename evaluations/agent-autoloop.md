# Evaluation: agent-autoloop

**Repo:** [KKKKhazix/agent-autoloop](https://github.com/KKKKhazix/agent-autoloop)
**Stars:** 2082 | **Last updated:** 2026-11-04 (pushed) | **License:** MIT
**Last verified:** 2026-11-04
**Last triaged:** 2026-11-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement (autonomous agent loop)
**Layer:** Tooling

---

## What it does

A background loop for CLI coding agents: it keeps picking up queued work and following
through on its own, without interrupting the user for routine progress. It only
surfaces a card for human sign-off when it hits something it is genuinely unsure
about, rather than escalating on every decision.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. The claimed uncertainty-detection (knowing when to
escalate vs. proceed) is untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today. Cites no STACK pick in
`Overlaps with` (ralph, ralph-claude-code, durable-harness are all catalogued leads, not
STACK picks). Not examined further in this pass.

_Triaged 2026-11-04 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-autoloop](https://github.com/KKKKhazix/agent-autoloop) | harness | Autonomous background loop (MIT) for CLI coding agents — keeps picking up and following through on work, surfacing a card only when it's genuinely unsure | Babysitting a CLI agent between tasks wastes attention; want it to keep working on its own, escalating only on real uncertainty | ralph, ralph-claude-code, durable-harness |
