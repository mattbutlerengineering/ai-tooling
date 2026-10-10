# Evaluation: pullboard

**Repo:** [pullboard-dev/pullboard](https://github.com/pullboard-dev/pullboard)
**Stars:** 83 | **Last updated:** 2026-10-10 (pushed) | **License:** MIT
**Last verified:** 2026-10-10
**Last triaged:** 2026-10-10  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A local coordination queue (MIT) for AI coding agents working on one git repo. A
human approves requirements in `SPEC.md` and house rules in `DOCTRINE.md`; agents
claim items from a shared board, each in its own git worktree/lane, and submit only
after the repo's own gate command (e.g. `npm test`) passes. A different agent then
verifies that exact commit and accepts or rejects it with a reason. Git hooks
enforce machine-checkable rules, every claim/submission/verdict is logged, and the
board itself is a SQLite file inside `.git`. The tool does not call a model itself —
the agents do.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only
(repo README plus metadata), consistent with an unattended discovery pass.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog — no overlap pressure (`Overlaps with`: stargate, hermes-conductor,
groundcrew; none is a STACK pick). The claim/verify/worktree-lane shape is
differentiated enough (independent-agent verification before acceptance, not
self-reported done) to deserve a real hands-on eval rather than a mechanical
disposition. Left at `discovery-log`; stamped as examined.

_Triaged 2026-10-10 by the P3 backlog band._
