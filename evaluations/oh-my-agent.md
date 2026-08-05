# Evaluation: oh-my-agent

**Repo:** [first-fluke/oh-my-agent](https://github.com/first-fluke/oh-my-agent)
**Stars:** 1,205 | **Last updated:** 2026-08-03 (pushed) | **License:** MIT
**Dev loop stage:** Implement, with declared coverage of PM/QA/DevOps/security roles across the loop
**Layer:** Harness (vendor-agnostic; targets Claude Code, Codex, Cursor, OpenCode)
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A portable, vendor-agnostic agent harness shipping 68+ built-in skills (PM, QA, DevOps, security
audit) that it claims to align to a project's own conventions, runnable across Claude Code, Codex,
Cursor and OpenCode.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and its "Overlaps with" cell. Enough to place and to band it; not enough for
any verdict, and none is offered.

## Triage note

Left at `discovery-log` — **and it is the near-miss of this pass.** At a glance it is the same
kitchen-sink shape that just disposed `agency-agents` (68+ bundled skills vs 271 bundled personas),
under a rule `WORKFLOW.md` has already codified. Applying it here would have been wrong.

What `WORKFLOW.md`'s exclusion actually tests is **undifferentiated breadth**: *"Too broad. Use
targeted skills … instead of a kitchen-sink plugin."* `agency-agents` fails it because it is a menu
of single-file personas with **no runtime and no orchestration** — its own eval's words. oh-my-agent
claims the opposite structure: a harness that runs the skills, portable across four hosts, aligned to
project conventions. Whether that claim survives contact is unknown, because nothing here has been
read at source. The count is a headline number, not the test, and a SKIP written on it would be this
lane applying a rule it had not actually checked.

MIT, ★1.2K, pushed 2026-08-03 — active. Left for a real look at the source.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [oh-my-agent](https://github.com/first-fluke/oh-my-agent) | harness | Portable, vendor-agnostic agent harness (MIT, ★1.2K) — 68+ built-in skills (PM, QA, DevOps, security audit) aligned to project conventions; works with Claude Code, Codex, Cursor, OpenCode | Specialist skill teams are rebuilt per harness; want one portable set aligned to your codebase standards | oh-my-claudecode, agent-orchestrator, ECC, agents (wshobson) |
