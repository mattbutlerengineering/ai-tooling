# Evaluation: unslopovich

**Repo:** [erkamyaman/unslopovich](https://github.com/erkamyaman/unslopovich)
**Stars:** 195 | **Last updated:** 2026-11-17 (pushed) | **License:** MIT
**Last verified:** 2026-11-17
**Last triaged:** 2026-11-17  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An agent skill that finds and fixes AI-looking UI/UX — generic layouts, components, and
copy that read as machine-generated — across mobile apps (Expo, React Native, Flutter,
SwiftUI, Jetpack Compose), web apps, and websites.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG one-liner. That is sufficient to place the lead, not to judge
whether its fixes actually read as less generic — it would not support an ADOPT, and this
eval offers none.

## Triage note

No STACK incumbent does this specific job: `phyll` reviews UX drift against an *existing*
design (overcoding past the intended look), `anti-slop`/`sloptrim`/`nopus` target AI-looking
*prose*, not UI/UX, and `pixelpact` checks a build against a *reference* design contract
rather than detecting generic-AI-look on its own. "AI-looking UI/UX" across five mobile
frameworks plus web is differentiated enough, and new enough (pushed today, 195 stars), to
leave at `discovery-log` for a real eval rather than disposing it mechanically.

_Triaged 2026-11-17 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [unslopovich](https://github.com/erkamyaman/unslopovich) | skill | Agent skill (MIT) that finds and fixes AI-looking UI/UX across mobile, web, and websites | AI-built interfaces read as generic and AI-generated with no dedicated skill catching and fixing that drift | phyll, anti-slop, pixelpact |
