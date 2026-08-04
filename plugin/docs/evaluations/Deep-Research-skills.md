# Evaluation: Deep-Research-skills

**Repo:** [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills)
**Stars:** 1,860 | **Last updated:** 2026-05-07 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Research & Discovery
**Layer:** Process

---

## What it does

A structured deep-research skill for Claude Code, opencode and Codex — a multi-step research
workflow with explicit human-in-the-loop review gates rather than a single search-and-summarize
turn.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`autoresearch`, `storm`, `last30days-skill`). Enough
to place it against the STACK incumbent; not enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`, not SKIPped. The STACK pick it was banded against,
[`last30days`](https://github.com/mvanhorn/last30days-skill) (`MEASURED`), answers a
recency-scoped question — what has been said about X lately, engagement-weighted across
Reddit/X/YouTube/HN. This is a *procedure*: decompose a question, gather, gate on human review,
synthesize. Recency lookup and structured multi-step research are different jobs, and the tool it
actually competes with is `storm`, which is not a STACK pick.

The human-in-the-loop framing is what makes it worth a look rather than a dispose. This catalog's
whole triage design turns on the same principle — bands that declare what an agent may conclude,
with escalation instead of silent judgement — and a research skill built around review gates is
the closest external analogue in the catalog.

Two facts to weigh in a real read: it is a skill, so its value is entirely in the prose quality of
the `SKILL.md` (a triggering test plus a with/without A/B is the only honest measurement, per
`TEMPLATE.md`), and it was last pushed 2026-05-07 — three months, which is aging for a skill whose
tool-use instructions have to track harness behaviour.

_Triaged 2026-08-04 by the P2 challenger band ([#267](https://github.com/mattbutlerengineering/ai-tooling/issues/267))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) | skill | Structured deep-research skill for Claude Code/Codex with human-in-the-loop control | Ad-hoc agent research lacks structure and review gates; want a guided HITL research workflow | autoresearch, storm, last30days-skill |
