# Evaluation: Pi-Remote

**Repo:** [Xpropel/Pi-Remote](https://github.com/Xpropel/Pi-Remote)
**Stars:** 277 | **Last updated:** 2026-11-03 (pushed) | **License:** MIT
**Last verified:** 2026-11-03
**Last triaged:** 2026-11-03  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Infrastructure

---

## What it does

Mirrors a live `pi` coding-agent terminal session to any browser over a self-hosted,
end-to-end-encrypted relay, so a developer can watch a run, answer an agent's prompts,
and send it commands from a phone or tablet without SSH access to the machine running
the session.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. It is harness-specific (the `pi` coding agent), so
whether the mirroring/relay actually works as advertised is untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today, no STACK-pick overlap.
Not examined further in this pass.

_Triaged 2026-11-03 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Pi-Remote](https://github.com/Xpropel/Pi-Remote) | tool | Mirrors live pi coding-agent terminal sessions to any browser (MIT), end-to-end encrypted over a self-hosted relay | Watching or steering a pi coding-agent session away from its own terminal means SSH or nothing | CodeRail, paddock, codex-mobile-bridge |
