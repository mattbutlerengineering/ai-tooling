# Evaluation: Autoloom

**Repo:** [GanyuanRan/Autoloom](https://github.com/GanyuanRan/Autoloom)
**Stars:** 241 | **Last updated:** 2026-10-06 (pushed) | **License:** NOASSERTION (GitHub records "other"; no clear permissive grant found)
**Last verified:** 2026-10-06
**Last triaged:** 2026-10-06  <!-- triaged: bulk -->
**Dev loop stage:** Implement / Dev Workflow
**Layer:** Process

---

## What it does

A free desktop AI-coding client, by the same author as the catalogued `Aegis` skill pack, that
builds Aegis-style governance directly into the execution client — baseline-aware changes,
evidence-backed delivery, with any model — per the repo description.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the GitHub
repository description, topics, and metadata. That is sufficient to compare it against the
already-dispositioned `Aegis` row, not to judge the desktop client's behavior hands-on.

## Verdict

**SKIP** — redundant with [`GSD`](https://github.com/open-gsd/gsd-core) (STACK, `MEASURED`, ADOPT). Autoloom packages the same baseline-before-risky-changes / evidence-before-completion governance as the author's own `Aegis` skill pack, which this catalog already SKIPped — by its own self-description, Aegis is a "Superpowers upgrade," redundant with `superpowers`/GSD. Moving that identical methodology from a skill pack into a standalone desktop client changes the delivery mechanism, not the content; it is still the same principles contending for the same job GSD already covers in STACK.

## Triage note

P2 challenger — the row's `Overlaps with` cell names `GSD`, a STACK pick. This is a direct
extension of an already-settled disposition rather than a fresh judgment call: `Aegis`'s own
eval (`evaluations/aegis.md`) SKIPped it as "redundant with `superpowers`/GSD... by its own
self-description." Autoloom is the same author's packaging of that exact methodology as a desktop
client. Absent a stated capability beyond "the same governance, now in a GUI," the prior reasoning
carries over.

If a future version of Autoloom demonstrates something GSD/Aegis genuinely lack (e.g. a verified
baseline/evidence enforcement mechanism no skill pack can replicate), that would be new information
warranting a real eval — this triage note does not foreclose that, it just finds nothing here yet to
distinguish it.

_Triaged 2026-10-06 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Autoloom](https://github.com/GanyuanRan/Autoloom) | harness | Free desktop AI-coding client (⚠️ license NOASSERTION), same author as Aegis — Aegis-style governance built into execution: baseline-aware changes, evidence-backed delivery, any model | Aegis's discipline is a skill pack bolted onto whatever harness you use; want the same baseline/evidence governance built into the execution client itself | Aegis, superpowers, GSD |
