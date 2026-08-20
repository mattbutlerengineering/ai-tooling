# Evaluation: omp-best-of

**Repo:** [wolfiesch/omp-best-of](https://github.com/wolfiesch/omp-best-of)
**Stars:** 50 | **Last updated:** 2026-08-20 (pushed) | **License:** MIT
**Last verified:** 2026-08-20
**Last triaged:** 2026-08-20  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Best-of-N coding-agent runs for Oh My Pi (MIT) — isolated git
worktrees, LLM-as-a-Verifier ranking, winner-only patch application." Runs several
agent attempts at one task in isolated git worktrees against the Oh My Pi harness,
scores each resulting trajectory with an independent LLM-as-a-Verifier, and applies
only the winning patch to the working tree.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata, README, and the CATALOG "Overlaps with" cell.

## Triage note

P3 backlog — no STACK pick cited in "Overlaps with." It is an extension of the
already-catalogued `oh-my-pi` harness (SKIP, ★13,501) rather than a standalone
competitor. Left at `discovery-log`; stamped only.

_Triaged 2026-08-20 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [omp-best-of](https://github.com/wolfiesch/omp-best-of) | tool | Best-of-N coding-agent runs for Oh My Pi (MIT) — isolated git worktrees, LLM-as-a-Verifier ranking, winner-only patch application | A single agent run can land a mediocre patch; want parallel attempts scored by an independent verifier with only the winner merged | oh-my-pi, moire, worktrunk |
