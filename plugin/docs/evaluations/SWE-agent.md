# Evaluation: SWE-agent

**Repo:** [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent)
**Stars:** 19,995 | **Last updated:** 2026-08-03 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement (autonomous issue resolution)
**Layer:** Tooling

---

## What it does

Princeton's autonomous GitHub-issue solver: give it an issue and a repo and it produces a fix
through a purpose-built agent-computer interface. It is the reference agent behind SWE-bench, and
the same machinery is used offensively for security work as EnIGMA.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`OpenHands`, `aider`, `plandex`,
`claude-code-action`). Sufficient for a SKIP that turns on *redundancy with a catalogued
incumbent*; not sufficient for a positive verdict, and none is offered.

## Verdict

**SKIP** — redundant with
[`claude-code-action`](https://github.com/anthropics/claude-code-action) (STACK, `RUN`) for the job
this stack would use it for. Issue in, patch out, from CI, is precisely what the incumbent does, and
it does it inside the harness that already holds this repo's context, permissions and review flow.

The distinction worth recording is what SWE-agent *is*. It is a research artifact first — the
reference implementation the SWE-bench leaderboard is defined against — and its lasting contribution
is the agent-computer interface idea (that the tools you hand a model matter as much as the model),
which has since been absorbed into every serious harness including the incumbent. Installing the
reference implementation to get a capability the harness already ships is the wrong way to consume
it.

SKIP is a statement about the install list, not the catalog. The row stays, and its value is as
reference: MIT, ★20K, actively maintained, and the right thing to read when the question is how
agent-computer interfaces are evaluated rather than which one to run.

Re-open if benchmarking against SWE-bench becomes work this repo does — at which point SWE-agent is
the instrument, not the tool under test.

_Triaged 2026-08-04 by the P2 challenger band ([#262](https://github.com/mattbutlerengineering/ai-tooling/issues/262))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) | harness | Autonomous GitHub-issue solver from Princeton (MIT, ★20K) — takes an issue and a repo and produces a fix via an agent-computer interface; the reference agent behind SWE-bench, also usable offensively for security (EnIGMA) | Want an autonomous agent that resolves a GitHub issue end to end | OpenHands, aider, plandex, claude-code-action |
