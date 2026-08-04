# Evaluation: Evolver (EvoMap)

**Repo:** [EvoMap/evolver](https://github.com/EvoMap/evolver)
**Stars:** 8,714 | **Last updated:** 2026-06-18 (pushed) | **License:** GPL-3.0 (⚠️ future releases moving to source-available) | **Language:** Node.js (npm: `@evomap/evolver`)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context (agent self-improvement) — Reflect
**Layer:** Tooling (CLI engine; core behind the EvoMap network)

---

## What it does

Evolver is **a GEP-powered self-evolution engine for AI agents** that "turns ad hoc prompt tweaks into auditable, reusable evolution assets." Its thesis (paper-backed: *From Procedural Skills to Strategy Genes*, arXiv:2604.15097) is that documentation-style **Skill** packages give sparse, unstable learning signal, whereas a compact **Gene** representation under the **GEP protocol** delivers stronger, more robust, accumulable experience — reporting CritPt lifts from 9.1%→18.57% and 17.7%→27.14% on paired base models. It encodes agent experience as **Genes and Capsules** (protocol-constrained, with an audit trail and prompt governance), not ad-hoc prompts or skill docs. Install `npm i -g @evomap/evolver`, run `evolver` in any git repo. It's the core engine behind **EvoMap**, a network where agents "evolve through validated collaboration" (live agent maps, evolution leaderboards). **Note:** open source since 2026-02 (MIT, then GPL-3.0-or-later since 2026-04-09); the maintainers announced future releases will move **from open source to source-available** (citing an unattributed-similarity dispute) — already-published MIT/GPL versions remain usable.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No evolution loop run, the CritPt/benchmark claims not reproduced.

```bash
gh api repos/EvoMap/evolver --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 8714, GPL-3.0, pushed 2026-06-18
gh api repos/EvoMap/evolver/readme --jq '.content' | base64 -d | sed -n '286,342p'        # GEP, Genes/Capsules, arXiv, source-available notice
```

## What worked

- **A real, paper-backed thesis.** "Genes beat skill docs as the carrier for accumulated experience" is a specific, falsifiable claim with an arXiv paper and CritPt numbers behind it — more rigorous than most self-improvement tools' assertions.
- **Auditable, governed evolution.** Encoding experience as protocol-constrained Genes/Capsules with an audit trail and prompt governance directly addresses the controllability problem self-evolving memory usually creates.
- **Distinct from skill/memory peers.** Where ACE curates a Skillbook and hivemind turns traces into skills, Evolver argues for a *compact gene representation* — a genuinely different bet, not a reskin.
- **Low-friction entry.** One npm install, run in any git repo; multilingual docs; strong traction (8.7K stars).

## What didn't work or surprised us

- **License trajectory is a real risk.** Moving **from open source to source-available** for future releases is a significant adoption caveat — you can rely on the current GPL-3.0 version, but the roadmap and best features may not stay open. Plan around the version you can actually use.
- **GPL-3.0 now.** Even before source-available, GPL-3.0 is strong copyleft — a consideration for embedding.
- **Vendor/network gravity.** The full value (validated collaboration, leaderboards) lives in the EvoMap network; the engine alone is the local piece.
- **Self-reported benchmarks + dispute context.** CritPt lifts are vendor/paper-reported; the README also airs a similarity dispute with another project — useful transparency, but signals a contested, fast-moving space.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Gene-encoded experience reportedly lifts task accuracy (CritPt 9.1%→18.57%); reuses what worked. |
| Speed | + / neutral | Reusing genes shortcuts re-derivation; the evolution loop itself costs iterations. |
| Maintainability | neutral | Audit trail + governance aid inspectability; another (GPL/soon source-available) component to manage. |
| Safety | neutral | Protocol-constrained, auditable evolution is a plus; self-evolution remains a surface to govern. |
| Cost Efficiency | + / neutral | "Tokens rise then fall" as reasoning compresses into genes; engine free today, network value is hosted. |

## Verdict

**SKIP** — the licence trajectory forecloses it. Two facts from the read above compound:

1. The current release is **GPL-3.0**, and this catalog's adoption bar is permissive OSS.
2. The project has **announced a move from open source to source-available** for future versions.

Either alone would be a caveat. Together they mean the best case is pinning to a copyleft snapshot and
watching the interesting work happen behind a licence you cannot build on — which is not a foundation
to put in a stack, however good the engineering is.

Worth being clear that this is *not* the P4 mechanical rule. P4 scopes copyleft to vendored
`skill`/`plugin` types whose text is copied into your repo; `evolver` is a `tool`, and GPL alone would
not dispose it (`firecrawl` was left standing under AGPL in this same pass for exactly that reason).
It is the announced relicensing that decides this one.

The idea is the interesting part and survives independently: compact, auditable **Genes** under the
GEP protocol as a carrier for accumulated experience, versus the skill-doc evolution `ACE` and
`hivemind` bet on. That comparison stays live through those rows, both of which are permissively
licensed. CritPt benchmark lifts are paper-reported and unverified here.

Re-open if the licence resolves permissively.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [evolver](https://github.com/EvoMap/evolver) | tool | GEP-powered self-evolution engine for AI agents (GPL-3.0, ⚠️ moving source-available) — encodes agent experience as compact "Genes"/"Capsules" (an auditable, protocol-constrained alternative to skill docs) rather than ad-hoc prompt tweaks; arXiv-backed, `npm i -g @evomap/evolver`, runs in any git repo | Ad-hoc prompt/skill tweaks give sparse, unstable learning signal; want reusable, auditable, governed evolution assets | ACE, hivemind, MemOS, memind, pro-workflow |
