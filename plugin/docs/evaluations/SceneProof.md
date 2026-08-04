# Evaluation: SceneProof

**Repo:** [ReyJ94/SceneProof](https://github.com/ReyJ94/SceneProof)
**Stars:** 39 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Dev loop stage:** Verify (visual inspection)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Source-grounded visual inspection for UI and Three.js scenes — gives a coding agent sight of what
actually rendered, at full render quality.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata fetched fresh for this
pass on 2026-08-04 (the slug had no cached record) plus the CATALOG one-liner and "Overlaps with"
cell (`midscene`, `passmark`, `agent-browser`). Enough to place it; not enough for a positive
verdict, and none is offered.

## Triage note

Left at `discovery-log`. MIT, pushed today, and ★39 — new enough that the star count carries no
signal in either direction, which is itself the reason not to dispose it on one.

The capability is real and thinly covered here: agents edit UI code blind, and WebGL/Three.js is the
worst case, because the DOM tells you nothing about what a shader drew. `midscene` does visual
assertions against web and mobile UI, but a rendered 3D scene at full quality is a different
verification problem. Whether that gap is worth a tool or is just a screenshot in a loop is exactly
what a hands-on run would answer.

The honest read is that this is the youngest kind of lead in the queue — a plausible idea with no
adoption evidence yet. The right disposition is to leave it and let time supply the signal a
one-liner cannot.

Metadata record added to `repo-metadata.json` in this pass; it had none before.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [SceneProof](https://github.com/ReyJ94/SceneProof) | tool | Source-grounded visual inspection for UI and Three.js scenes, giving coding agents sight at full render quality | Agents can't verify what a UI or WebGL/Three.js scene actually renders; want grounded visual inspection, not blind edits | midscene, passmark, agent-browser |
