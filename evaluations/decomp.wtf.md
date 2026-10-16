# Evaluation: decomp.wtf

**Repo:** [i12bp8/decomp.wtf](https://github.com/i12bp8/decomp.wtf)
**Stars:** 425 | **Last updated:** 2026-10-15 (archived) | **License:** MIT
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

"What The Function" — an AI agent that decompiles games you own into byte-exact-matching C,
run locally, for match-the-binary decompilation projects.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. Source-grounded only: the public GitHub repo page.
The repo's own archived banner, fetched 2026-10-16, reads "This repository was archived by the
owner on Oct 15, 2026. It is now read-only." The README states "stays up as it is, under the MIT
license," confirms the last installable version as 0.10.6, and invites forks ("If you want to
fork it and keep going with it, you can") — but names no successor project, fork, or replacement
that continues the work.

## Triage note

`repo-metadata.json` has no cached record for this slug, so `triage.py` placed this lead in P3
rather than the structural P1 successor-check band — the archival (as of **2026-10-15**, the day
before this pass) predates any metadata refresh. Checked by hand per the P1 rule ("archived
usually means moved, so check for one first"): no successor is named anywhere in the repo. Its
own catalog row cites `eleven` as the closest overlap — an actively maintained, broader
agent-first reverse-engineering tool (568★, Apache-2.0) covering adjacent ground (binaries,
Android apps, GPU kernels) — but `eleven` is a different project, not a fork or rename, so it is
named here as the active alternative rather than claimed as a literal successor.

## Verdict

**SKIP** — archived 2026-10-15, no successor. The repo is explicitly discontinued by its own
owner with no replacement named; `eleven` is the closest active peer for agent-driven
reverse-engineering work, though it is not a successor to this specific byte-exact
decompilation niche.

_Triaged 2026-10-16 by the P1 successor-check disposition (band mislabeled P3 by `triage.py`
pending a metadata refresh for this slug; archival status confirmed by hand against the live
repo page)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [decomp.wtf](https://github.com/i12bp8/decomp.wtf) | tool | AI agent decompiles owned games into byte-exact-matching C, run locally (MIT) — matching decompilation, not approximate | Game-decompilation projects need byte-exact C from a slow, manual match-the-binary loop with no agent assist | eleven, awesome-reverse-engineering |
