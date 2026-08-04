---
name: triage-lead
description: Drive ONE discovery-log lead to a durable state — SKIP with a stated reason, or leave at discovery-log — under the eliminate-only rule. Never writes ADOPT/KEEP/CONDITIONAL. Use when disposing a single lead from a bulk band. Triggers - "/triage-lead <tool>", "triage this lead", the command NEXT-EVALS.md prints for P1/P2/P3.
disable-model-invocation: true
---

# Triage Lead

Disposes **one** `discovery-log` lead end-to-end. This is the tool the P1/P2/P3
bands in `NEXT-EVALS.md` point at, so the protocol lives here once instead of being
re-derived in every fan-out prompt.

## The eliminate-only contract (read first)

An unattended bulk pass may **reject** a lead but never **promote** one. You may write:

- **`SKIP`** with a stated reason, or
- **leave the lead at `discovery-log`** (stamp that you looked, change no verdict).

You may **never** write `ADOPT`, `KEEP`, or `CONDITIONAL`. A false SKIP is cheap and
reversible; a false ADOPT poisons STACK. Detector Q (`audit-evals.py --bulk-triage`)
enforces this mechanically: any eval carrying the bulk marker
(`<!-- triaged: bulk -->`) whose headline verdict exceeds `SKIP` fails `make check`.
The marker is your signature that this was a bulk disposition, not a hands-on eval.

## Inputs

- **tool** — a `discovery-log` lead name, exactly as it appears in `NEXT-EVALS.md` /
  `CATALOG.md` (required). Only `discovery-log` rows are candidates.

## Steps

1. **Resolve the lead.** Find its `CATALOG.md` row (`grep -inE "\[?<tool>\b" CATALOG.md`)
   and its `COMPARISON.md` row. If the COMPARISON row's Evaluated cell is **not**
   `discovery-log`, this lead is already dispositioned — **stop**, it is not a triage
   candidate. Note its CATALOG "Overlaps with" cell and its `repo-metadata.json` record
   (`license_spdx`, `archived`, `pushed_at`, `stars`).

2. **Read the eval, if any** (`evaluations/<slug>.md`). Take its **headline** verdict —
   the first non-blank line under `## Verdict`. Key on that line only, **never** on
   every verdict word in the section: `trailofbits/skills` reads "Held at CONDITIONAL
   rather than ADOPT", so a set-based check would misread it as an ADOPT.

3. **Guard — never overrule a substantive human read.** Read the headline **together with
   the eval's `**Evidence:**` field**; the verdict word alone does not tell you whether a
   real read happened.
   - `ADOPT`/`KEEP` → **stop and escalate**, at any Evidence level. A positive read is out
     of bounds for this lane. (`triage.py` already excludes these from the bulk bands.)
   - `CONDITIONAL`/`DEFER` at Evidence **`MEASURED`/`RUN`** → someone exercised the tool and
     reached a real verdict the `discovery-log` row hasn't caught up to. Promoting the row
     to match is a **human/non-bulk** action — **escalate** (leave a note; do not SKIP and
     do not promote). This is the `#259` category.
   - `CONDITIONAL`/`DEFER` at Evidence **`REVIEW`/`SOURCE-ONLY`** → **proceed.** This is not
     a verdict. Per [ADR-0005](../../../docs/adr/0005-verdict-vocabulary.md) and
     `COMPARISON.md`'s legend, a real CONDITIONAL requires a tool we *actually exercised*
     (MEASURED/RUN) or a genuine `adopt-if:` condition; on an unexercised lead the same word
     is the "tentative read … notes, not a recommendation" that `discovery-log` denotes.
     Treating it as untouchable is not caution — it is a no-op: **304** `discovery-log` rows
     carry a CONDITIONAL headline, so that reading would freeze the entire bulk-triage
     program. Detector D excludes `discovery-log` rows precisely because this is the normal
     state, not a mismatch.

   Proceed only when there is **no eval**, or the eval's headline is itself `SKIP` /
   genuinely tentative in the sense just defined.

4. **Decide the disposition** (judgement, inside eliminate-only authority):
   - **SKIP** when the lead is clearly not worth a first-time hands-on eval —
     *redundant* with a named STACK/catalog incumbent that already covers the same job,
     *archived with its successor already catalogued*, or otherwise plainly dominated.
     The reason must **name the incumbent or successor**. A SKIP with no recorded
     reason is the evidence-free verdict this repo exists to prevent.
   - **Leave at `discovery-log`** when the lead is significant or differentiated enough
     to deserve a real eval (don't SKIP a major tool as "redundant"), or when you can't
     make a defensible call. Stamping records that it was examined; the absence of a
     stronger claim keeps it honest.

5. **Apply — SKIP.**
   - *Eval exists:* set `## Verdict` to `**SKIP** — <reason naming the incumbent>`; add
     `**Last triaged:** <today>  <!-- triaged: bulk -->` to the header; ensure the
     "How we tested it" section carries an honesty disclaimer (`**Evidence:**
     SOURCE-ONLY` + an explicit "did not install / source-grounded only" sentence).
   - *No eval:* write a short stub (see template below) with the `SKIP` verdict, the
     reason, `Evidence: SOURCE-ONLY`, an honesty disclaimer, and the stamped header.
   - Flip the `COMPARISON.md` row's Evaluated cell from `discovery-log` to `SKIP`
     (leave the trailing Evidence cell alone — `backfill-evidence.py` regenerates it).

6. **Apply — leave at `discovery-log`.**
   - *No eval:* write a minimal stub (template below) with **no `## Verdict`** (or an
     explicit `discovery-log`), a "Triage note" saying why it was left, `Evidence:
     SOURCE-ONLY`, the honesty disclaimer, and the stamped header — marker included. The
     row stays `discovery-log`.
   - *Eval exists, no `## Verdict`:* same — stamp
     `**Last triaged:** <today>  <!-- triaged: bulk -->` and add a `## Triage note`.
   - *Eval exists **with** a headline verdict (the step-3 `REVIEW`/`SOURCE-ONLY`
     CONDITIONAL case):* stamp the **date only — omit the `<!-- triaged: bulk -->`
     marker** — and add a `## Triage note` saying why it was left. Leave the existing
     `## Verdict` untouched; the row stays `discovery-log`.

     The marker is not decoration: detector Q reads it as *"this lane disposed this lead"*
     and allows nothing above `SKIP` (`BULK_ALLOWED = {"SKIP"}`). Stamping it beside a
     CONDITIONAL headline this pass did not write fails `make check` for a claim nobody
     made. Leaving a lead is not a disposition, so there is nothing to sign — the date
     alone records that the lane looked, which is all `**Last triaged:**` ever asserts.
     Every one of the 72 marker-bearing evals is a `SKIP` or a verdict-less stub; keep it
     that way.

7. **Regenerate and gate.** Run `make fix` — it reconciles counts, regenerates the
   derived files (Evidence, tiers, `NEXT-EVALS.md`, `WATCHLIST.md`), syncs `plugin/docs/`,
   then runs `check` (the exact order lives in the `Makefile`; don't restate it here). A
   clean exit means: detector Q allows the
   verdict, detector D agrees the row matches the eval, detector B accepts the honesty
   disclaimer, `NEXT-EVALS.md` has dropped the SKIPped lead, and the plugin docs are in
   sync. If `make check` is red, fix the eval — never the gate.

## Stub template (no-eval lead)

Model on `evaluations/roo-code.md`. Pull stars/license/pushed from `repo-metadata.json`.

```markdown
# Evaluation: <Name>

**Repo:** [<slug>](https://github.com/<slug>)
**Stars:** <n> | **Last updated:** <pushed date> (pushed) | **License:** <spdx>
**Last verified:** <today>
**Last triaged:** <today>  <!-- triaged: bulk -->
**Dev loop stage:** <stage>
**Layer:** <layer>

---

## What it does

<1–3 sentences from the CATALOG one-liner + README skim.>

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Verdict

**SKIP** — redundant with `<incumbent>` (<why the incumbent dominates>). <incumbent>
already covers this job in STACK; a second tool for it earns nothing.

_Triaged <today> by the P2 challenger band._
```

For the **leave** outcome, drop the `## Verdict` section and replace it with a
`## Triage note` explaining why the lead was left at `discovery-log` (e.g. "significant
standalone tool — deserves a real hands-on eval, not a mechanical SKIP; left for the
P0/eval-runner lane").

## Guardrails recap

- Never write `ADOPT`/`KEEP`/`CONDITIONAL` — detector Q will fail the build, and the
  point of the lane is to *eliminate*, not to adopt.
- Never overrule an eval that already reads `ADOPT`/`KEEP` — stop and escalate.
- Key on the **headline** verdict, never the set of verdict words.
- Every SKIP names an incumbent or successor. No evidence-free SKIPs.
- Stamp `**Last triaged:**` in **both** outcomes; it is written only when the lane
  actually examines a lead and is **never** backfilled onto untouched leads.
