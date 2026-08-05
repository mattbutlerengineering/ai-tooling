# Evaluation: ACE (agentic-context-engine)

**Repo:** [kayba-ai/agentic-context-engine](https://github.com/kayba-ai/agentic-context-engine)
**Stars:** 2,528 | **Last updated:** 2026-07-08 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

A persistent learning loop in which Agent, Reflector, and SkillManager roles curate a "Skillbook"
of strategies extracted from execution traces — no fine-tuning and no vector DB, just distilled
in-context guidance. Claims 2× consistency on Tau2 and 49% fewer tokens; runs against 100+
providers via LiteLLM.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this framework. This evaluation is source-grounded only: repo
metadata plus the CATALOG one-liner and "Overlaps with" cell. That is enough to place the lead
against the STACK incumbent it implies and to record what a real evaluation would have to settle;
it is not enough for any positive verdict, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped — the top-scoring lead in the Memory & Context P2 band
(overlap pressure 8) and the one whose relationship to a STACK pick most needs a real look.

Its loop — mine execution traces, distil what worked, feed it back as reusable in-context guidance
— is the same thesis as [`claude-reflect`](https://github.com/BayramAnnakov/claude-reflect) (STACK,
Tier 1, `MEASURED`), which turns session corrections into persistent `CLAUDE.md` rules. But they
sit at different altitudes: claude-reflect is a Claude Code plugin editing one file in one harness,
ACE is a provider-agnostic Python framework you build an agent *inside*. That is not obviously a
substitution in either direction, and calling it redundant from a README would be guessing.

Two claims make this worth measuring rather than filing: **2× consistency on Tau2** and **49% fewer
tokens**, both unverified. The second falls squarely under
`evaluations/token-savings-protocol.md`. A P0/eval-runner candidate.

_Triaged 2026-08-04 by the P2 challenger band ([#264](https://github.com/mattbutlerengineering/ai-tooling/issues/264))._
