# Evaluation: pm-claude-skills

**Repo:** [mohitagw15856/pm-claude-skills](https://github.com/mohitagw15856/pm-claude-skills)
**Stars:** 1,255 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Plan (product artifacts)
**Layer:** Tooling

---

## What it does

A large product-management skill pack — PRDs, launches, postmortems, compliance, CVs — packaged as
`SKILL.md` and installable across Claude, ChatGPT, Gemini, Cursor and Codex. Listed in Anthropic's
plugin directory; the repo's own description now claims 848 skills against the 244 our catalog row
records.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`pm-skills`, `agent-skills`, `mattpocock/skills`).
Sufficient for a SKIP that turns on *redundancy with catalogued incumbents*; not sufficient for a
positive verdict, and none is offered.

## Verdict

**SKIP** — redundant with [`agent-skills`](https://github.com/addyosmani/agent-skills) (STACK,
`ADOPT`) on the slice that is dev-loop work, and off-scope on the rest. `agent-skills` already runs
the lifecycle from `/spec` through `/ship`, which is where a PRD and a postmortem actually attach
to the loop this catalog maps; `mattpocock/skills` covers the vertical-slicing half of the same
job.

What remains after that — launches, compliance, CVs, the bulk of a 244-to-848-skill pack — is
product/business practice. That is the same scope call `MineContext` and
`alirezarezvani/claude-skills` got: a real capability aimed somewhere other than the dev loop.

Sheer count also cuts against it here. Skill-selection surface is the scarce resource in an agent's
context, so hundreds of non-engineering skills is a cost paid on every turn for capability that
never fires.

Re-open if this catalog widens past the dev loop, or if a specific PRD/postmortem skill proves it
beats the `agent-skills` lifecycle equivalents — which needs exercising, not a bulk pass.

_Triaged 2026-08-04 by the P2 challenger band ([#263](https://github.com/mattbutlerengineering/ai-tooling/issues/263))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pm-claude-skills](https://github.com/mohitagw15856/pm-claude-skills) | skill | 244 professional skills (PRDs, launches, postmortems, compliance, CVs) — one SKILL.md, installable across Claude/ChatGPT/Gemini/Cursor/Codex | Product-management deliverables an engineering skill pack does not cover | pm-skills, agent-skills, mattpocock/skills |
