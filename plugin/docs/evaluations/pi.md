# Evaluation: pi

**Repo:** [earendil-works/pi](https://github.com/earendil-works/pi)
**Stars:** 83,710 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Last verified:** 2026-09-02
**Last triaged:** 2026-09-02  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An AI agent toolkit — unified LLM API, agent loop, TUI, and a coding agent CLI in one
lightweight package.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata and the CATALOG "Overlaps with" cell (`repo-metadata.json`, fetched 2026-08-04).

## Triage note

Bands as a P2 challenger against `opencode` (an installed/supported harness alongside
Claude Code, per `CLAUDE.md`), but per the triage-lead guidance not to SKIP a major tool
as "redundant" — pi is a large, actively-developed general agent toolkit (83.7K★) with
its own unified LLM API and TUI, not a thin opencode clone. Left at `discovery-log` for a
real evaluation rather than a mechanical SKIP.

_Triaged 2026-09-02 by the P2 challenger band (daily discovery-and-triage routine, bulk,
eliminate-only). Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pi](https://github.com/earendil-works/pi) | harness | AI agent toolkit (MIT, ★67K) — unified LLM API, agent loop, TUI, and a coding agent CLI in one lightweight package | Want a batteries-included agent toolkit with a built-in coding agent CLI | command-code, aider, opencode, oh-my-pi |
