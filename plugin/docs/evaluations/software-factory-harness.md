# Evaluation: software-factory-harness (8090-inc)

**Repo:** [8090-inc/software-factory-harness](https://github.com/8090-inc/software-factory-harness)
**Stars:** 8 | **Last updated:** 2026-03-17 (pushed; created 2026-03-17) | **License:** none declared (`/license` → 404; no LICENSE or COPYING in the HEAD tree, re-checked 2026-08-04)
**Dev loop stage:** Spans the SDLC in intent — a shell harness meant to apply agents across plan → implement → review → ship
**Layer:** Harness (shell scripts)
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A shell-based agent harness published alongside the commercial **8090 Software Factory** platform,
intended to apply AI agents across a full SDLC rather than a single task. It is the third artifact in
8090's orbit, beside the MIT `software-factory-plugin` (which publishes the methodology) and the
hosted platform itself.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata and the licence endpoints,
re-checked live on 2026-08-04. The substantive assessment lives in the pack eval
[`8090-software-factory.md`](./8090-software-factory.md), which read all three artifacts together;
this file exists to give the harness row a verdict a detector can see (see the triage note).

## Verdict

**SKIP — no declared license, a single day of history, and its own governing eval already said so.**

This row's disposition was written months ago, inside the pack eval: *"The unlicensed
`software-factory-harness` remains **SKIP** on its own row (no LICENSE → fails the permissive-OSS
bar; reference only)."* It never reached `COMPARISON.md`, which still read `discovery-log`. This pass
propagates a verdict a human already made; it does not invent one.

**Why it never propagated is the finding.** The harness has no eval file of its own — it shares
`8090-software-factory.md` with two siblings holding *different* verdicts (the platform is DEFER, the
plugin CONDITIONAL). Detector D syncs an eval's headline verdict to the row that matches its name, so
a third artifact's disposition buried in the pack's prose is invisible to it, and editing the shared
`## Verdict` to say SKIP would overrule the other two. That is the shape of
[#343](https://github.com/mattbutlerengineering/ai-tooling/issues/343) — a component catalogued apart
from its pack is not an independent lead, but it still needs a row a gate can read. Giving it this
stub file is the repair.

**Re-confirmed live on 2026-08-04**, because this lane does not dispose *on* a license without
re-fetching: `gh api repos/8090-inc/software-factory-harness/license` returns **404**, and no
`LICENSE`/`COPYING` path exists in the HEAD tree. That is a genuine absence of terms, distinct from
the `NOASSERTION` parser artifact that has now four times hidden a license that was actually there.
★8; created and last pushed the same day (2026-03-17); 1 fork, 0 open issues.

Nothing is lost by the SKIP. The adoptable artifact in this orbit is the MIT `software-factory-plugin`
(CONDITIONAL), which publishes the same AI-native SDLC methodology and runs without the hosted
service; the platform itself is DEFER and tracked in `WATCHLIST.md`; and the harness's named overlap
`Trellis` is already SKIP. The row stays as reference, per the `Flowise` precedent.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [software-factory-harness](https://github.com/8090-inc/software-factory-harness) | harness | Shell-based agent harness for applying AI agents across the full SDLC (★6; ⚠️ no license) | Need a harness that structures how AI agents integrate into the complete development lifecycle | software-factory-plugin, 8090 Software Factory, Trellis |
