# Evaluation: claude-code-my-workflow

**Repo:** [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)
**Stars:** 1,388 | **Last updated:** 2026-06-10 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

A ready-to-fork Claude Code project template aimed at academics — LaTeX/Beamer and R scaffolding —
bundled with multi-agent review, quality gates, adversarial QA, and replication protocols.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** fork or run this template. This evaluation is source-grounded only: repo metadata
plus the CATALOG one-liner and "Overlaps with" cell (`claude-code-spec-workflow`,
`compound-engineering`, `superpowers`). That is sufficient for a SKIP that turns on *what the
template contains versus what STACK already installs* — a question the description answers
directly — and not sufficient for any positive verdict, which this eval does not offer.

## Verdict

**SKIP** — split cleanly in two, and neither half earns a slot.

The generic half is redundant with tools already installed. Multi-agent review, quality gates,
and adversarial QA are what [`GSD`](https://github.com/obra/superpowers) (STACK, the phased
spec-to-code framework), [`code-review`](https://github.com/anthropics/claude-plugins-official),
and `pr-review-toolkit` already provide — all three already in STACK, all three exercised. Forking
a template to obtain them would install a competing planning vocabulary alongside GSD for
capability we have.

The differentiated half — LaTeX/Beamer, R, and academic replication protocols — is real and is
the actual reason to use this repo, but it is outside what this catalog stocks. This is an
operating manual for AI-assisted *software development*, organized around dev-loop stages and
code-quality signals; an academic paper-production template moves none of them. That is the same
scope call already recorded for `googleworkspace/cli`.

Note this is *not* the `claude-code-spec-workflow` case, which this catalog deliberately left at
`discovery-log` on the grounds that spec-driven lifecycle frameworks legitimately coexist as
alternatives to GSD. This is not an alternative lifecycle framework — it is a project scaffold
whose in-scope contents duplicate three STACK picks.

Re-open if the catalog's scope ever widens to research/publication workflows.

_Triaged 2026-08-04 by the P2 challenger band ([#265](https://github.com/mattbutlerengineering/ai-tooling/issues/265))._
