# Evaluation: addyosmani/web-quality-skills

**Repo:** [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills)
**Stars:** ~25K (collection) | **Last updated:** 2026-06 | **License:** MIT
**Dev loop stage:** Verify / Review
**Layer:** Tooling

---

## What it does

Six focused skill files covering web quality disciplines: `accessibility` (29.6K installs), `seo` (27.1K), `performance` (17.7K), `web-quality-audit` (11.3K), `core-web-vitals` (11.3K), and `best-practices` (10.5K). Each skill is a standalone SKILL.md loaded into context when invoked — a dense reference document rather than an executable workflow. `web-quality-audit` acts as an umbrella that cross-links to the other five. The collection encodes Lighthouse audit methodology (performance, accessibility, SEO, best practices categories) plus Google's Core Web Vitals spec (LCP, INP, CLS thresholds and fix patterns).

Unlike `addyosmani/agent-skills` (the lifecycle collection), these are domain reference skills — they expand the agent's knowledge base on a topic rather than directing multi-step workflows. Invoking `/accessibility` loads WCAG 2.2 criteria, HTML patterns, testing commands, and an impact-ranked issue checklist. Invoking `/core-web-vitals` loads the LCP/INP/CLS thresholds, per-metric fix patterns, framework-specific examples (Next.js, React, Vue), and measurement code.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured** — installed all six skills globally, checked each SKILL.md's coverage, and ran a **planted-defect A/B against a strong automated baseline** to measure the `accessibility` skill's load-bearing claim: that its value is *current WCAG 2.2 knowledge and semantic judgment a linter structurally cannot provide*. Also compared against the two overlapping catalog skills (`web-design-guidelines`, `ui-ux-pro-max`) to assess differentiation.

### Measured A/B — skill checklist vs automated linter

Built `/tmp/a11y-ab/page.html` with **8 planted defects** split into two classes, then ran [`html-validate`](https://html-validate.org) (a dedicated, deterministic a11y/HTML linter — the objective oracle, independent of agent judgment) over it and compared its findings against the `accessibility` SKILL.md checklist:

| # | Planted defect | WCAG | `html-validate` v8 (automated baseline) | `accessibility` skill checklist |
|---|----------------|------|------------------------------------------|----------------------------------|
| D1 | `<img>` missing `alt` | 1.1.1 | **caught** (`wcag/h37`) | covered |
| D2 | input with no associated `<label>` | 1.3.1/4.1.2 | **missed** (flagged only the unrelated missing `type`) | covered (`aria-label`/`label for` patterns) |
| D3 | duplicate `id` | 4.1.1 | **caught** (`no-dup-id`) | covered |
| D4 | `<div onclick>` — non-interactive, no role/tabindex | 2.1.1/4.1.2 | **missed** | covered — SKILL.md line 164 shows this *exact* antipattern + the native-`<button>` fix |
| D5 | target size 16×16px | 2.5.8 (new in 2.2) | **missed** | covered — line 232, explicit 24×24 rule |
| D6 | drag-only control, no single-pointer alternative | 2.5.7 (new in 2.2) | **missed** | covered — line 254 |
| D7 | "retype your email" redundant entry | 3.3.7 (new in 2.2) | **missed** | covered — line 333 |
| D8 | arithmetic cognitive test as auth, no accessible alternative | 3.3.8 (new in 2.2) | **missed** | covered — line 349 |

```
cd /tmp/a11y-ab && npx html-validate@8 page.html   # deterministic oracle, exit 1
# → catches D1, D3 + bonus structural (missing lang, missing <title>, implicit input/button types)
# → catches 0 of 4 WCAG 2.2 criteria (D5–D8) and 0 of 2 semantic-interaction defects (D2, D4)
```

**Result:** the strong automated baseline catches **2/8** planted defects — exactly the *syntactic/structural* class (and adds real structural finds the skill's prose also covers: missing `lang`, missing `<title>`). It detects **0 of the 4 WCAG 2.2 criteria** and **0 of the 2 semantic-interaction defects**. The `accessibility` checklist explicitly enumerates **all 6 the linter cannot see** (verified by line reference in the installed SKILL.md). This objectively isolates the skill's value: not duplicating what a linter already does, but supplying the *recent-spec coverage and semantic judgment* (drag alternatives, cognitive-load auth, native-element preference) that automated tooling structurally misses. A linter and this skill are complements, not substitutes.

### Content inspection (depth/accuracy spot-checks)

```
npx skills add addyosmani/web-quality-skills@accessibility -g -y
npx skills add addyosmani/web-quality-skills@seo -g -y
npx skills add addyosmani/web-quality-skills@performance -g -y
npx skills add addyosmani/web-quality-skills@web-quality-audit -g -y
npx skills add addyosmani/web-quality-skills@core-web-vitals -g -y
npx skills add addyosmani/web-quality-skills@best-practices -g -y
```

Installed to `~/.agents/skills/` with symlinks into `~/.claude/skills/` (Claude Code's pick-up path). All six installed cleanly; PromptScript failed as expected (unsupported for global install — irrelevant).

**Spot-checking content quality:**

- `accessibility`: WCAG 2.2 coverage is current and complete — includes the four new 2.2 criteria (2.5.7 dragging movements, 2.5.8 target size, 3.2.6 consistent help, 3.3.7 redundant entry, 3.3.8 accessible authentication). The keyboard pattern section explicitly warns against adding keydown handlers to native `<button>` elements — a real footgun that most references miss.

- `core-web-vitals`: `scheduler.yield()` is the recommended chunking API with an explicit fallback explanation for why `setTimeout(0)` loses priority — accurate as of 2026. The `PerformanceObserver` snippet for INP debugging uses `durationThreshold: 40` with a comment explaining why 16 (one frame) is too noisy — practical nuance not found in generic docs.

- `seo`: Includes an `llms.txt` section explicitly flagging it as unproven (adoption ~0.015%, no confirmed vendor support) — honest rather than hype-driven. AI search visibility section is measured.

- `best-practices`: Covers Trusted Types (Baseline 2026), the polyfill.io 2024 supply-chain compromise, and `sourcesContent` stripping from source maps — up-to-date on incidents that post-date most skill training data.

- `performance`: Speculation Rules API coverage is current with `eagerness` trade-off table and `prerenderingchange` event guidance. HTTP 103 Early Hints with the Cloudflare performance data cited. View Transitions API with both same-document and cross-document patterns.

**Comparison against existing overlapping skills:**

`web-design-guidelines` (Vercel): fetches Vercel's Web Interface Guidelines on each invocation — a different problem domain. It's about UI/UX conventions (layout, typography, interaction patterns), not measurable quality signals (Lighthouse scores, CWV thresholds). Minimal overlap in practice — these skills operate on orthogonal axes.

`ui-ux-pro-max`: Design aesthetics, component patterns, platform-specific guidelines. No coverage of WCAG, CWV, robots.txt, structured data, or security headers. Complementary, not redundant.

`claude-seo` (in catalog): 25 SEO sub-skills + 18 sub-agents with E-E-A-T, GEO/AEO, and reporting. Substantially deeper SEO coverage than `seo` here. If SEO is the primary concern, `claude-seo` is the right tool. The `seo` skill here is solid for technical SEO basics but won't replace a dedicated SEO system.

## What worked

- Content is genuinely current — references APIs, incidents, and browser baseline status from 2025-2026 that most training data doesn't contain. The `scheduler.yield()` guidance, polyfill.io compromise note, and Trusted Types "Baseline 2026" flag are examples where the skill adds value over base model knowledge.
- The skills are tightly scoped. Each addresses one quality dimension; the `web-quality-audit` umbrella cross-links all five without duplicating their content. This avoids context bloat compared to loading a single kitchen-sink document.
- WCAG 2.2 coverage in `accessibility` is complete and accurate for the new 2.2 criteria — a meaningful knowledge update since WCAG 2.2 shipped in October 2023 and many agents still operate on 2.1.
- The Core Web Vitals content is the strongest skill in the set. The per-phase INP breakdown (input delay / processing / presentation), `durationThreshold` explanation, and `web-vitals/attribution` build tip are practitioner-level guidance.
- Checklists are prioritized by severity — Critical / High / Medium / Low or equivalent tiering appears in every skill. This makes the audit output immediately actionable.
- MIT license. Multi-agent compatible (installed to `~/.agents/skills/`, not Claude Code-specific).

## What didn't work or surprised us

- The skills are reference documents, not workflows. Invoking `/web-quality-audit` loads a dense checklist but the agent has to drive the actual audit — there's no structured multi-step process like `addyosmani/agent-skills` provides. For teams that want a guided audit workflow, this needs to be paired with a workflow skill or explicit prompting.
- `seo` overlaps significantly with `claude-seo` in the catalog. If you already have `claude-seo` installed, the `seo` skill here adds little on technical SEO and nothing on E-E-A-T, entity SEO, or reporting. The two shouldn't be installed together.
- `best-practices` doubles as a security skill (CSP, HSTS, Trusted Types, SRI). It's good content, but it creates overlap with `security-best-practices` (also installed globally from a prior evaluation). The naming is ambiguous — "best practices" sounds like a catch-all, but the actual content is mostly web security and browser compatibility, not general engineering hygiene.
- No `web-design-guidelines` overlap as the catalog entry implies — the two skills are addressing entirely different concerns. The catalog entry's "Overlaps with" field should be updated to reflect `claude-seo` and `security-best-practices` as the actual overlaps, not `web-design-guidelines`.
- Install count disparity is puzzling: `accessibility` (29.6K) and `seo` (27.1K) have 2-3× the installs of `core-web-vitals` (11.3K) despite `core-web-vitals` being arguably the most technically dense and high-ROI skill. Suggests the collection is being partially installed rather than adopted wholesale.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | **Measured:** on an 8-defect planted page, a dedicated automated linter (`html-validate`) caught 2/8 and **0 of 4 WCAG 2.2 criteria**; the `accessibility` checklist explicitly covers all 6 the linter missed (D2, D4–D8). WCAG 2.2 criteria, scheduler.yield() API, and 2024-2025 incident data are accurate and would otherwise require the agent to hallucinate or fall back on stale training data |
| Speed | neutral | No workflow automation; adds context load but doesn't change task throughput |
| Maintainability | + | Consistent audit checklists (severity-tiered) produce structured findings that are easier to track and fix sprint-over-sprint |
| Safety | + | `best-practices` covers Trusted Types, SRI pinning, polyfill.io risk, and source map exposure — security guidance grounded in real incidents |
| Cost Efficiency | neutral | Skills add tokens to context when invoked; ROI depends on how frequently web quality audits are needed in the project |

## Verdict

**ADOPT** (conditional on web project type)

The collection is well-authored, current, and genuinely differentiated from the existing catalog entries. The real value is factual accuracy on rapidly-evolving specs (WCAG 2.2, Core Web Vitals INP, Speculation Rules, Trusted Types) where base model knowledge is stale — and the measured A/B confirms it: against a dedicated automated linter the `accessibility` skill is a complement, not a duplicate, covering the 4 WCAG 2.2 criteria and 2 semantic-interaction defects the linter structurally cannot catch. For any project shipping web UIs — especially ones subject to accessibility requirements or SEO visibility goals — the `accessibility` and `core-web-vitals` skills are clear adopts.

The condition: these are domain reference skills for web projects. Backend-only or CLI projects get no value. Also avoid installing `seo` alongside `claude-seo` — the dedicated SEO skill covers the same ground and more. Recommended install pattern: `accessibility` + `core-web-vitals` + `web-quality-audit` as the core trio, adding `performance`, `seo`, and `best-practices` based on project needs.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [web-quality-skills](https://github.com/addyosmani/web-quality-skills) | skill | Web quality audit suite: accessibility, SEO, performance, Core Web Vitals, best practices | Agent produces web UIs without checking accessibility, perf, or SEO | claude-seo (SEO overlap), security-best-practices (security headers overlap) |
