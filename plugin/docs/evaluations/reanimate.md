# Evaluation: reanimate

**Repo:** [NiazMorshed2007/reanimate](https://github.com/NiazMorshed2007/reanimate)
**Stars:** 288 | **Last updated:** 2026-10-31 (pushed) | **License:** MIT
**Last verified:** 2026-10-31
**Last triaged:** 2026-10-31  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A Claude Code skill (MIT) that reverse-engineers any UI animation frame by frame via Playwright, then proves the recreated copy moves the same.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (webapp-testing, playwright-best-practices, playwright-skill). That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead.

## Triage note

P3 backlog. Left at `discovery-log`; its overlaps (webapp-testing, playwright-best-practices, playwright-skill) are themselves discovery-log leads, not STACK picks, so it doesn't land in P2. Frame-accurate animation-recreation verification is a narrow, differentiated niche within Playwright-based frontend testing and deserves its own look rather than a bulk disposition.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [reanimate](https://github.com/NiazMorshed2007/reanimate) | skill | Claude Code skill (MIT) that reverse-engineers any UI animation frame by frame via Playwright, then proves the copy moves the same | Recreating a UI animation by eye is imprecise, with no way to verify the copy actually matches frame-for-frame | webapp-testing, playwright-best-practices, playwright-skill |
