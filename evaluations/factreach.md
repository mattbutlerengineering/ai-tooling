# Evaluation: FactReach

**Repo:** [simonlin1212/FactReach](https://github.com/simonlin1212/FactReach)
**Stars:** 25 | **Last updated:** 2026-09-04 (pushed) | **License:** MIT
**Last verified:** 2026-09-09
**Last triaged:** 2026-09-09  <!-- triaged: bulk -->
**Dev loop stage:** Reflect / Plan (research & discovery)
**Layer:** Process

---

## What it does

Internet search skill for AI agents spanning 23 channels — general web, X, Xiaohongshu,
Douyin, Weibo, Bilibili, Reddit, YouTube, GitHub, WeChat public accounts, and more —
zero-auth first where possible.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on
redundancy with a catalogued incumbent, not on the tool's behaviour — a question the overlap
answers directly. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `last30days-skill`. last30days-skill
is scoped to recency-based sentiment/discussion research (Reddit/X/YouTube/HN/Polymarket);
FactReach is a broader, always-available search skill across 23 channels including several
Chinese platforms last30days-skill doesn't cover, with a stated zero-auth-first design.
Different scope and channel coverage — worth a real side-by-side rather than a mechanical SKIP.

_Triaged 2026-09-09 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [FactReach](https://github.com/simonlin1212/FactReach) | skill | Internet search skill for AI agents (MIT) spanning 23 channels — web, X, Reddit, YouTube, GitHub, and more — zero-auth first | Wiring web/social search into an agent means juggling per-channel APIs and keys; want one skill covering 23 channels with no auth by default | Agent-Reach, last30days-skill, webclaw |
