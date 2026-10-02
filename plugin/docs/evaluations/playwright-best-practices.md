# Evaluation: playwright-best-practices

**Repo:** [currents-dev/playwright-best-practices-skill](https://github.com/currents-dev/playwright-best-practices-skill)
**Stars:** 386 | **Last updated:** 2026-07-21 | **License:** MIT
**Last verified:** 2026-10-02
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A large, activity-routed reference skill for writing, debugging and maintaining Playwright tests in TypeScript, published by currents.dev (a Playwright test-dashboard vendor). It installs on its own with `npx skills add https://github.com/currents-dev/playwright-best-practices-skill`. skills.sh listed **89K installs** on 2026-10-02, which is high relative to the repo's ★386 because installs, not stars, are where skills.sh traffic shows up.

The mechanism is **progressive disclosure at scale**. `playwright-best-practices/SKILL.md` (303 lines, frontmatter `version: "1.2"`) is a router only: activity tables ("Writing E2E tests → `core/test-suite-structure.md`, `core/locators.md`, `core/assertions-waiting.md`") and a large decision tree map what the agent is doing to one or two of **57 reference documents** in eight folders: `core/`, `testing-patterns/`, `advanced/`, `browser-apis/`, `debugging/`, `frameworks/` (React, Angular, Vue, Next.js), `architecture/`, `infrastructure-ci-cd/`. The reference set is about 770 KB, loaded only on demand. The router ends with a **test validation loop**: `npx playwright test --reporter=list`, read the trace on failure, fix, re-run, and `--repeat-each=5` for critical tests. The repo lints its own skill in CI with [agnix](https://github.com/agent-sh/agnix) (pinned by commit hash).

## How we tested it

**Evidence:** REVIEW

Source-grounded review — not run hands-on. I listed the full tree (74 entries), read the whole `SKILL.md`, the README, `core/locators.md`, the CI workflow and the license, and grepped three of the longest references (`reporting.md`, `parallel-sharding.md`, `flaky-tests.md`, 371–496 lines each) for vendor promotion. I compared it with [webapp-testing.md](webapp-testing.md), [playwright-skill.md](playwright-skill.md) and [playwright-mcp.md](playwright-mcp.md). No Playwright suite was written or run with it loaded.

```bash
R=currents-dev/playwright-best-practices-skill
gh api repos/$R --jq '{stars:.stargazers_count, license:.license.spdx_id, pushed:.pushed_at}'
gh api "repos/$R/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/$R/contents/playwright-best-practices/SKILL.md --jq .content | base64 -d
gh api repos/$R/contents/playwright-best-practices/core/locators.md --jq .content | base64 -d
gh api repos/$R/commits?per_page=5 --jq '.[]|.commit.author.date+" "+.commit.message'
```

## Test design — skills

- **Triggering:** not measured — no should-fire / shouldn't-fire prompt set was built.
- **Output A/B:** not measured — no with-skill vs baseline A/B; every finding below is from reading the source.
- **Not run?** Yes — see the disclaimer above.

## What worked

- **Depth that generic TDD and browser skills don't have.** Locator priority (role > label > text > test-id > CSS/XPath), web-first assertions, fixtures vs POM, sharding, clock mocking, OAuth popups, websockets, Electron and extensions: this is Playwright-specific knowledge an agent otherwise half-remembers, and flaky-test guidance is where agent-written E2E suites most often go wrong.
- **Progressive disclosure done properly.** A routing-only SKILL.md over 57 on-demand files keeps the per-trigger cost small despite about 770 KB of content. It is a good reference example of the pattern.
- **Little vendor promotion.** Apart from the README banner and frontmatter `author`, the three references grepped mention currents.dev zero times, including `reporting.md` and `parallel-sharding.md`, the two places a dashboard vendor would most want to.
- **Quality-controlled.** agnix lint in CI, a CodeRabbit-reviewed restructure that fixed `waitForTimeout` misuse and pinned Docker/Action versions, and clean MIT text.

## What didn't work or surprised us

- **The description is a keyword list.** Its frontmatter `description` lists about 50 topics. That aims at broad triggering but is long and may compete with any other testing skill on "debug this failure". Triggering wasn't measured.
- **TypeScript Playwright only.** No Python/Java/.NET coverage, the opposite of [webapp-testing](webapp-testing.md), which is Python only.
- **Guidance, not tools.** It ships no scripts or server helper, so the agent still needs a running app and a working Playwright install. It shapes the tests the agent writes. It doesn't drive the browser itself.
- **Small maintainer surface.** ★386, last push 2026-07-21, and a vendor's marketing incentive behind it. The quality is good today, but its future depends on one company's priorities.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Role-based locators, web-first waits and the `--repeat-each` loop target the flake classes agent-written E2E tests hit |
| Speed | + | Routed references save rediscovering Playwright idioms per task |
| Maintainability | + | POM/fixture architecture guidance and CI sharding produce suites that scale |
| Safety | + | Includes XSS/CSRF/auth security-testing patterns; no executable code shipped |
| Cost Efficiency | + | Router-only SKILL.md; ~770 KB of references loaded only on demand |
| Verifiability | + | Output is a standard `@playwright/test` suite with traces and reports any reviewer can re-run |

## Verdict

**discovery-log — tentative read** — the strongest Playwright-specific *authoring* skill in this scan, and a clean example of progressive disclosure: a router SKILL.md over 57 references, MIT, agnix-linted, with almost no vendor promotion in the content. It complements rather than replaces [webapp-testing](webapp-testing.md) (drive and inspect a running app with Python scripts) and the [playwright](playwright-mcp.md) MCP server (drive a browser through tool calls). This one shapes the TypeScript test suite you keep. It wasn't exercised, so it gets no real verdict. A hands-on eval should measure triggering against other testing skills and the flake rate of a suite written with and without it.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [playwright-best-practices](https://github.com/currents-dev/playwright-best-practices-skill) | skill | Activity-routed Playwright TypeScript testing guide: one router SKILL.md over 57 on-demand references (MIT) | Agents write flaky, brittle Playwright tests and half-remember locator, fixture, mocking and CI idioms | webapp-testing, playwright-skill, playwright |
