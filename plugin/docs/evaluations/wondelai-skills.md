# Evaluation: wondelai/skills

**Repo:** [wondelai/skills](https://github.com/wondelai/skills)
**Stars:** 1,838 | **Last updated:** 2026-07-22 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** All stages (cross-domain)
**Layer:** Tooling

---

## What it does

Fifty skills and twelve guided journeys derived from bestselling business, marketing, UX and coding
books, packaged for Claude Code, Codex, Cursor and other agentskills.io-compatible agents.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`anthropics/skills`, `vercel-labs/agent-skills`,
`agent-skills`). Sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*; not
sufficient for a positive verdict, and none is offered.

## Verdict

**SKIP** — redundant with [`agent-skills`](https://github.com/addyosmani/agent-skills) (STACK,
`ADOPT`) on the coding slice, and off-scope on the rest. Its own framing is "Business, Marketing,
UX & Coding Frameworks from Bestselling Books": the coding quarter competes with an installed
lifecycle pack that covers `/spec` → `/ship`, and the other three quarters are business practice
this catalog does not map.

The differentiator it does claim — skills distilled from named books — is a *provenance* claim, not
a capability claim. It says where the advice came from, not that the agent behaves better for
having it, and nothing in this catalog's verdict vocabulary rewards provenance on its own. That is
the gap a measured triggering / with-skill-vs-baseline A/B would close, which is P0 work.

Re-open if a measured eval shows a book-derived skill outperforming the `agent-skills` equivalent,
or if this catalog widens past the dev loop.

_Triaged 2026-08-04 by the P2 challenger band ([#263](https://github.com/mattbutlerengineering/ai-tooling/issues/263))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [wondelai/skills](https://github.com/wondelai/skills) | skill | Agent-skills collection for Claude Code and agentskills.io-compatible agents | Wanting book-derived business/UX/coding frameworks as installable agent skills | anthropics/skills, vercel-labs/agent-skills, agent-skills |
