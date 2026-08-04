# Evaluation: company-os-starter-kit

**Repo:** [workflowsio/company-os-starter-kit](https://github.com/workflowsio/company-os-starter-kit)
**Stars:** 80 | **Last updated:** 2026-04-06 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Plan (workflow scaffolding)
**Layer:** Process

---

## What it does

A "Company OS" starter for Claude Code: a `CLAUDE.md` template, five go-to-market skills, a
workflow plugin, safety hooks, and a blueprint tying them together. Aimed at running a *business*
out of an agent, with the engineering workflow as one part of it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata plus the CATALOG
one-liner and "Overlaps with" cell (`GSD`, `compound-engineering`, `orchestkit`). Sufficient for a
SKIP that turns on *redundancy with a catalogued incumbent*; not sufficient for a positive verdict,
and none is offered.

## Verdict

**SKIP** — redundant with [`GSD`](https://github.com/obra/superpowers) (STACK) on the half that is
a development workflow, and off-scope on the half that is not. Its workflow plugin and CLAUDE.md
scaffold cover ground GSD's milestone/phase planning already owns in this stack, with far more
adoption behind it; the five GTM skills are a marketing capability this catalog does not map.

Adoption is the other half of the call. At 80 stars and last pushed 2026-04 — four months stale in
a category where the harness spec itself moves monthly — a starter kit is exactly the artifact that
ages worst, because its whole value is being current scaffolding.

Re-open if this catalog widens past the dev loop, or if the kit resumes releases.

_Triaged 2026-08-04 by the P2 challenger band ([#263](https://github.com/mattbutlerengineering/ai-tooling/issues/263))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [company-os-starter-kit](https://github.com/workflowsio/company-os-starter-kit) | plugin | Build a Company OS with Claude Code (MIT, ★72) — CLAUDE.md template, 5 GTM skills, workflow plugin, safety hooks | Starting a whole company workflow on Claude Code from a template rather than from scratch | GSD, compound-engineering, orchestkit |
