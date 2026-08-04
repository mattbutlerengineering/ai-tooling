# Evaluation: browser-act/skills

**Repo:** [browser-act/skills](https://github.com/browser-act/skills)
**Stars:** 4,236 | **Last updated:** 2026-07-08 (pushed) | **License:** MIT
**Dev loop stage:** Verify (browser automation)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A browser-automation agent skill offering anti-bot bypass, parallel multi-session control, and
human handoff when a flow needs a person.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04)
plus the CATALOG one-liner and "Overlaps with" cell (`agent-browser`, `playwright-skill`,
`opencli`). Sufficient for a SKIP that turns on redundancy with catalogued incumbents; not
sufficient for a positive verdict, and none is offered.

## Verdict

**SKIP** — redundant on the dev-loop capability, and its actual differentiator is not one.

Driving a browser from an agent is already covered three ways in this catalog:
[`agent-browser`](https://github.com/vercel-labs/agent-browser) is a P0 lead with the highest
pressure in Verify, [`playwright-skill`](https://github.com/lackeyjb/playwright-skill) wraps the
standard driver, and [`opencli`](https://github.com/jackwener/opencli) turns an authenticated
session into a CLI. Against those, the three claims here are anti-bot bypass, parallel isolated
sessions, and human handoff.

Only the first is unique, and it is a capability for scraping sites that do not want to be
scraped — an acquisition concern, not a step in writing or verifying your own software. Verifying
your own app in a browser never needs to defeat a bot wall. Parallel sessions and human handoff are
ordinary Playwright configuration.

MIT and ★4.2K, so the SKIP is about fit, not quality.

Re-open if the anti-bot layer turns out to matter for testing your *own* app behind a WAF or bot
manager — that would be a dev-loop reason, and a measurable one.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [browser-act/skills](https://github.com/browser-act/skills) | skill | Browser-automation agent skill — anti-bot bypass, parallel multi-session, human handoff | Driving real browsers from agents past anti-bot walls and across isolated sessions is bespoke | agent-browser, playwright-skill, opencli |
