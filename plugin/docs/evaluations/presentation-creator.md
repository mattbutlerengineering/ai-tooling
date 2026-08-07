# Evaluation: presentation-creator

**Repo:** [getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/presentation-creator)
**Stars:** 850 | **Last updated:** 2026-06-30 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Skills & Plugins (presentations)
**Layer:** Process
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

The presentation-creator skill from Sentry's official developer agent-skills collection.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus the
CATALOG one-liner and "Overlaps with" cell. Overlaps cited: `slidev`, `powerpoint`,
`open-slide`. Enough to place it; not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Apache-2.0, ★850, pushed 2026-06-30 — a small row whose interest is mostly in where
it comes from.

It is one skill out of an **official engineering-org skills collection**, and this catalog has several of
those now (`google/skills`, `microsoft/skills`, `azure-skills`, `gemini-skills`, `vercel-labs/agent-skills`,
`trailofbits/skills`). A company publishing the skills its own engineers use is a different provenance signal
from a community pack, and arguably a better one — the incentive is internal utility rather than stars.

That also makes it the fourth instance in this triage of a single skill catalogued apart from its pack, after
`implement`, `diagnosing-bugs` and `codebase-design` inside `mattpocock/skills`. The pattern is now firmly
established: you do not adopt `presentation-creator`, you install `getsentry/skills` and receive it.

Not disposed alongside the three presentation rows that were: it is maintained, officially published, and
carries the provenance the disposed rows lacked. Whether an eighth deck tool earns catalog space is a
cluster question, not a per-row one.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [presentation-creator](https://github.com/getsentry/skills/tree/main/skills/presentation-creator) | skill | Presentation-creator skill from Sentry's official dev agent-skills collection (Apache-2.0, 850★) | Need an official, maintained agent skill for building presentation decks | slidev, powerpoint, open-slide |
