# Evaluation: uncut

**Repo:** [Balanov/uncut](https://github.com/Balanov/uncut)
**Stars:** 528 | **Last updated:** 2026-11-02 (pushed) | **License:** MIT
**Last verified:** 2026-11-02
**Last triaged:** 2026-11-02  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A lossless, headless coding-agent harness shipped as one ~7MB static binary with four tools and plain stdin/stdout — no framework, no silent truncation of agent output.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner, repo metadata, and the "Overlaps with" cell. That is sufficient to
place the lead in a triage band; it would not support an ADOPT, and this eval offers
none.

## Triage note

Left at `discovery-log` — newly catalogued today, no STACK-pick overlap (P3 backlog).
A minimal, single-binary harness is a genuinely different design point from the
feature-rich harnesses already in STACK (pi, gptme-style toolkits); worth a first-time
hands-on look rather than a mechanical SKIP, but not examined further in this pass.

_Triaged 2026-11-02 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [uncut](https://github.com/Balanov/uncut) | harness | Lossless, headless coding-agent harness (MIT) — one 7MB static binary, four tools, plain stdin/stdout, no silent truncation | Want a minimal, scriptable coding-agent harness without a heavyweight framework or hidden cuts to agent output | pi, gptme, phi |
