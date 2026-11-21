# Evaluation: openfabriq

**Repo:** [openfabriq/openfabriq](https://github.com/openfabriq/openfabriq)
**Stars:** 28 | **Last updated:** 2026-11-19 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-21
**Last triaged:** 2026-11-21  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An "AI software factory, as code": agents that triage, implement, review, and fix a
GitHub repository, described in readable files and run with Claude Code on your own
machine or a team server — a standing, repo-level multi-agent pipeline rather than a
within-session workflow.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the CATALOG one-liner plus repo metadata. Sufficient to place the lead, not to
confirm how its multi-role pipeline behaves in practice.

## Triage note

Banded P2 (challenges `GSD`). GSD is a context-engineering Discuss->Plan->Execute
->Verify->Ship loop used *within* a single agent session; openfabriq instead
describes a standing, file-configured pipeline of separate triage/implement/review/
fix agent roles operating continuously on a repo — closer to an autonomous repo
bot than to GSD's in-session discipline. That difference is real enough, on the
one-liner alone, to withhold a redundancy SKIP. Left at discovery-log for a
hands-on look at whether it earns a place beside GSD or the `ralph-claude-code`/
`proof-of-done-loop` autonomous-loop cluster.

_Triaged 2026-11-21 by the P2 challenger band._
