# Evaluation: baoyu-skills

**Repo:** [jimliu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)
**Stars:** 23,360 | **Last updated:** 2026-07-04 (pushed) | **License:** MIT
**Dev loop stage:** Skills & Plugins (skill collection)
**Layer:** Process
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A general agent-skills collection from the author of `baoyu-design`.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus the
CATALOG one-liner and "Overlaps with" cell. Overlaps cited: `anthropics/skills`,
`vercel-labs/agent-skills`, `baoyu-design`. Enough to place it; not enough for a positive verdict, and
none is offered.

## Triage note

Left at `discovery-log`. MIT, ★23.4K, pushed 2026-07-04 — a large, active collection from the same author as
`baoyu-design`, which is catalogued separately and was also examined in this pass.

The two rows are the same relationship this triage keeps meeting from the other direction: a pack and one of
its components, entered as independent leads. Here the pack is `baoyu-skills` and the component is
`baoyu-design`. In the Plan and Verify slices it was `mattpocock/skills` with `implement`, `diagnosing-bugs`
and `codebase-design` split out. Whichever way round it falls, the effect is the same — the queue counts one
artifact more than once, and a redundancy verdict between the two would be meaningless.

Not disposed. Its named peers are `anthropics/skills` and `vercel-labs/agent-skills`, both of which are
first-party collections and neither of which is adopted; being one of several large general skill collections
is a crowding observation, not a supersession argument. The measured comparison the whole group needs —
which collection actually changes agent behaviour, by triggering rate and with-skill A/B — is the
`TEMPLATE.md` skill-dimension work detector S tracks, and it is P0.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [baoyu-skills](https://github.com/JimLiu/baoyu-skills) | skill | Large community agent-skills collection (Claude/Codex/OpenClaw), ★22K but content largely non-English and unvetted | Want a broad ready-made skill grab-bag, though quality needs human review before use | anthropics/skills, vercel-labs/agent-skills, baoyu-design |
