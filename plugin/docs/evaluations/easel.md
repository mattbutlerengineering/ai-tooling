# Evaluation: easel

**Repo:** [The-Sentience-Company/easel](https://github.com/The-Sentience-Company/easel)
**Stars:** 47 | **Last updated:** 2026-08-17 (pushed) | **License:** GPL-3.0
**Last verified:** 2026-08-18
**Last triaged:** 2026-08-18  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A local review board for work an agent wants a human to look at: the agent publishes,
a human annotates in the browser, and the feedback flows back to the agent as JSON.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (license) is sufficient for a license-disqualifying SKIP, not on the tool's
behaviour. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — GPL-3.0. A copyleft license here means the tool cannot be adopted under this
catalog's permissive-only bar (MIT-like OSS only); the underlying human-in-the-loop
review-board pattern is already covered by `facet` (MIT-adjacent, no-license caveat
aside) and `plannotator` without the copyleft exposure.

_Triaged 2026-08-18 by the P4 mechanical-skip band — license is the reason, not quality._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [easel](https://github.com/The-Sentience-Company/easel) | tool | Local review board (⚠️ GPL-3.0) where an agent publishes work, a human annotates in-browser, and feedback returns as JSON | Agents need human sign-off mid-task but only have blocking chat prompts, not a structured review surface | facet, plannotator, hubo |
