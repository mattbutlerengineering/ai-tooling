# Evaluation: council-of-high-intelligence

**Repo:** [0xNyk/council-of-high-intelligence](https://github.com/0xNyk/council-of-high-intelligence)
**Stars:** 3,440 | **Last updated:** 2026-07-04 (pushed) | **License:** MIT
**Dev loop stage:** Plan / Review (multi-model deliberation)
**Layer:** Tooling (CLI)
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A CLI that runs a structured, multi-round deliberation across several LLM providers — 18 defined
personas debating a decision across Claude, GPT, Gemini and local models — instead of taking one
model's single-shot answer.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the `CATALOG.md` one-liner and "Overlaps with" cell (`claude-octopus`, `design-council`). Enough to
place and band it; not enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`. Checked its two named overlaps: `claude-octopus` and `design-council` are
both themselves `discovery-log` leads, not STACK picks, so there is no incumbent for a redundancy
SKIP to point at. The three form an un-adjudicated multi-model-deliberation cluster — the same
"several rows, no measured comparison" shape the previous slices recorded for the SDD tools and the
presentation skills. One measured comparison would settle all three; nothing in this band can.

Placement note: it sits in the Skills & Plugins section but is a multi-provider CLI, not a skill or
plugin — it is closer to Agent Orchestration. Not moved here, since re-sectioning a row is a catalog
edit rather than a triage disposition, but the mismatch is why its neighbors in this slice (vendor and
domain skill packs) tell you nothing about it.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [council-of-high-intelligence](https://github.com/0xNyk/council-of-high-intelligence) | tool | Multi-LLM deliberation CLI (MIT, ★2.7K) — 18 AI personas deliberate hard decisions across Claude, GPT, Gemini, and local models | Single-LLM decisions lack diverse perspectives; runs structured multi-round deliberation across providers | claude-octopus, design-council |
