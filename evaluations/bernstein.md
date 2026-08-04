# Evaluation: bernstein

**Repo:** [sipyourdrink-ltd/bernstein](https://github.com/sipyourdrink-ltd/bernstein)
**Stars:** 788 | **Last updated:** 2026-08-04 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Ship (auditable orchestration)
**Layer:** Infrastructure

---

## What it does

A deterministic orchestrator for CLI coding agents (Claude Code, Codex, Gemini CLI, and ~40 more)
with **no model in the coordination loop** — so parallel runs in per-task git worktrees replay
byte-identically. Adds signed lineage plus an opt-in HMAC audit chain a reviewer can verify offline
without re-running anything, along with cluster mode and air-gapped deployment.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata and repo description
(fetched 2026-08-04) plus the CATALOG one-liner and "Overlaps with" cell (`superpowers`, `ruflo`).
Enough to place it against the STACK incumbent; not enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`, not SKIPped — the banding is a category error.
[`GSD`/superpowers](https://github.com/obra/superpowers) (STACK) is a *process* layer: skills that
enforce milestones, phases, and discovery discussion inside one agent's work. bernstein is an
*orchestrator*: it schedules many agent processes across isolated worktrees. A discipline pack and a
scheduler are complements, not substitutes.

The differentiator worth recording is one the CATALOG row undersells. The row leads with the
HMAC-chained audit log, but the repo's own headline claim is **determinism** — keeping the model
out of the coordination loop so a parallel run replays byte-identically. If that holds, it is a
direct answer to the thing that makes multi-agent orchestration hard to trust: you cannot debug or
re-verify a run you cannot reproduce. The audit chain is the compliance consequence of that
property, not the property itself. Worth a one-liner fix in a pass that is editing CATALOG for
content rather than triage.

Apache-2.0, ★788, pushed today. What a real read has to test is the determinism claim itself — run
the same task set twice and diff the worktrees — because everything else it offers rests on it.

_Triaged 2026-08-04 by the P2 challenger band ([#267](https://github.com/mattbutlerengineering/ai-tooling/issues/267))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [bernstein](https://github.com/sipyourdrink-ltd/bernstein) | harness | Audit-grade multi-agent orchestration with HMAC-chained audit log and signed agent cards | Need compliance-ready agent orchestration with tamper-proof logs | superpowers, ruflo |
