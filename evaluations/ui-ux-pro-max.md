# Evaluation: ui-ux-pro-max

**Repo:** [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
**Stars:** 113,533 | **Last updated:** 2026-08-03 (pushed) | **License:** MIT
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement (build/refine frontend UI) + Review (UI quality/a11y audit)
**Layer:** Process (design knowledge + rules) with a Tooling component (Python search/reasoning engine + validators)

---

## What it does

Catalog one-liner: "Design intelligence for professional UI/UX across platforms." The mechanism is a **searchable design-knowledge database fronted by a reasoning engine**, not just a prompt. The flagship feature (v2) is a "Design System Generator": from a one-line brief ("build a landing page for a beauty spa") it runs ~5 parallel searches over bundled datasets — 161 product types, 67 UI styles, 161 color palettes, 24 landing-page patterns, 57 font pairings — ranks results (the README cites BM25), filters industry-specific anti-patterns, and emits a tailored design system: recommended pattern, style, color tokens, typography pairing with Google Fonts links, key effects, an "AVOID" anti-pattern list, and a pre-delivery checklist.

Structurally it is a **bundle of 7 Claude Code skills** under `.claude/skills/`: `ui-ux-pro-max` (the core design-intelligence skill), plus `brand`, `design`, `design-system`, `ui-styling`, `slides`, and `banner-design`. The core `SKILL.md` carries a priority-ordered rule taxonomy (10 categories, Accessibility/Touch/Performance ranked CRITICAL→LOW) with concrete, checkable rules: contrast ≥4.5:1, touch targets 44×44pt / 48×48dp, CLS <0.1, animation 150–300ms, base 16px / line-height 1.5, SVG-not-emoji icons, `prefers-reduced-motion`, semantic color tokens. The datasets and reasoning live in Python/CJS scripts (`generate-slide.py`, `search-slides.py`, `html-token-validator.py`, token validators, `extract-colors.cjs`), and there is a `uipro-cli` npm package. Installs as a Claude Code marketplace plugin (`.claude-plugin/plugin.json`, v2.5.0) or via the CLI. It explicitly scopes itself OUT of backend/API/DevOps/non-visual work.

## How we tested it

**Evidence:** RUN

**Hands-on** — cloned `nextlevelbuilder/ui-ux-pro-max-skill` at `56ea9cf` (2026-10-15, plugin v2.5.0 era; the skill now advertises 79 styles/192 palettes/74 pairings/119 UX rules) into `/tmp`, ran the bundled Python engine (`search.py --design-system`, `validate_data.py`, the 164-test unittest suite) on Python 3.11, and fed the generator 12 fixed briefs. The oracle is mechanical: WCAG contrast ratios recomputed from the emitted hex tokens, byte-identical re-runs, and distinctness of output. The comparison arm is a static generic default (Tailwind blue-500 primary, white text). There is no model in the loop, so this measures the deterministic engine and the skill's description text, not what an agent produces with the skill loaded.

```
$ python3 scripts/validate_data.py
OK: validated 12 domain files, 22 stack files, and ui-reasoning.csv
$ python3 -m unittest discover -s scripts/tests
Ran 164 tests in 13.432s   OK
$ python3 measure.py          # 12 briefs, each run twice
beauty spa landing page      primary=#EC4899 style=Soft UI Evolution   font=Playfair Display / Inter
fintech banking dashboard    primary=#F59E0B style=Minimalism & Swiss  font=IBM Plex Sans / IBM Plex Sans
developer documentation portal primary=#0F172A style=Minimalism & Swiss font=JetBrains Mono / IBM Plex Sans
... (12 rows)
contrast pairs >=4.5: 84/84
distinct primaries 11 / 12 distinct typography 12
deterministic 12 / 12
median latency 0.17s
baseline generic default: distinct palettes 1; on-primary contrast 3.68; fg/bg 17.85
$ python3 trig.py             # lexical proxy over the SKILL.md description
should-match 4 / 6
shouldnt-match (false hits) 0 / 6
negative/skip clause in description: False
```

## Test design

- **Task/corpus:** 12 fixed product briefs (spa landing page, fintech dashboard, kids game app, law firm site, esports platform, grocery store, developer docs portal, meditation app, luxury watch showcase, B2B analytics dashboard, restaurant reservations, healthcare patient portal); 7 text/background token pairs per design system (on-primary/primary, on-secondary/secondary, on-accent/accent, foreground/background, card-foreground/card, muted-foreground/muted, on-destructive/destructive); a 6+6 hand-written triggering prompt set.
- **Baseline:** a single static generic default design system (Tailwind blue-500 `#3B82F6` primary, white on-primary, white background, slate-900 foreground) standing in for "no design guidance". It is a deliberately naive stand-in, not a model-generated arm.
- **Metric:** WCAG 2.x contrast ratio >= 4.5 per pair (pass count out of pairs); byte-identical output across two runs; count of distinct primaries and typography pairings; median wall-clock per call.
- **Reproduce:** `git clone --depth 1 https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`, then for each brief `python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<brief>" --design-system -p T` and recompute contrast from the printed hex tokens.

### Test design — skills (required when Type is skill or plugin)

- **Triggering:** a lexical proxy only (no model credentials in the sandbox, so no `claude -p` run): 6 should-fire UI prompts matched 4/6 against the description's vocabulary (the two misses were "fix the low-contrast text on our pricing cards" and "add keyboard navigation and focus rings to the modal"); 6 shouldn't-fire backend prompts (SQL migration, CI workflow, Go race condition, REST schema, Postgres latency, log-rotation script) produced 0/6 false hits. The "Skip it for pure backend logic" clause lives in the SKILL.md body, which loads only after the skill fires; the description has no negative clause.
- **Output A/B:** applied to the deterministic engine only. With the skill's generator: 84/84 contrast pairs pass, 11 distinct primaries and 12 distinct font pairings over 12 briefs, identical output on re-run. Generic-default baseline: 1 palette, on-primary text at 3.68:1 (fails 4.5:1). A with-skill-vs-baseline comparison of model-written UI was not run.

```
cd /tmp/eval-ui-ux-pro-max && python3 measure.py && python3 trig.py
```

## What worked

- **The engine runs offline and clean.** Python 3 stdlib only; the data validator passes and all 164 bundled tests pass in 13.4s; each design-system call returns in ~0.17s median.
- **Emitted palettes are accessible by construction.** 84/84 recomputed text/background pairs meet 4.5:1, including the on-color tokens; the naive baseline's white-on-blue-500 is 3.68:1.
- **Output is deterministic and differentiated.** 12/12 briefs reproduced byte-identically; 11 distinct primaries and 12 distinct typography pairings across 12 briefs, so it is not emitting one template.
- **Concrete, checkable rules ranked by impact.** The 10-category taxonomy is priority-ordered with explicit thresholds (contrast 4.5:1, touch 44×44pt, CLS <0.1, motion 150–300ms, base 16px) and paired anti-patterns. This is the format an LLM can apply deterministically — the same strength impeccable and taste-skill earn — and the a11y/touch coverage is unusually thorough (VoiceOver labels, Dynamic Type, safe-area awareness, drag thresholds).
- **Knowledge breadth and platform reach.** 161 product types and 67 styles across 15 stacks (React, Next.js, Vue, Svelte, Astro, SwiftUI, React Native, Flutter, Jetpack Compose, Tailwind, shadcn/ui) is broader than impeccable or taste-skill, and it explicitly covers **native mobile** (iOS HIG, Material) where the others are web-centric.
- **Retrieval-based recommendation, not just a prompt.** The Design System Generator picks style/palette/typography from a curated database via search+ranking, so output is anchored to vetted combinations rather than free-form model taste. This is a genuinely different mechanism from a pure rules prompt.
- **Clean scoping gates.** SKILL.md spells out Must-Use / Recommended / Skip with a one-line decision criterion ("if it changes how a feature looks, feels, moves, or is interacted with"). Good triggering hygiene that limits firing on backend work.
- **Strong provenance and traction.** 93.9K stars (the most-starred entry in the whole frontend-design cluster), MIT, named maintainer org, dedicated docs site (uupm.cc), `uipro-cli` on npm with download metrics, and a large fork/translation ecosystem. Not abandonware.

## What didn't work or surprised us

- **It recommends styles its own data flags as risky.** The "healthcare patient portal" and "meditation wellness mobile app" briefs both returned Neumorphism, and the printed accessibility field for that style reads `risk:high`; the checklist asks for 4.5:1 contrast but the style choice works against it. Token contrast passes (84/84) while the style recommendation is still a questionable pick for a patient portal.
- **No scope refusal in the engine.** A backend brief ("Rust CLI argument parser backend service") still returns a Hero + Features + CTA landing-page pattern; the Skip rule is prose for the model, not enforced by the script.
- **Triggering description is positive-only.** 4/6 lexical should-fire hits and no negative clause in the description (see Test design). The proxy is crude and a model may fire more or less reliably.
- **Self-reported counts moved.** The skill's description now claims 79 styles (50 active), 192 palettes, 74 pairings; the earlier README review quoted 67/161/57. We did not audit the datasets row by row.
- **Not covered:** whether an agent with the skill loaded produces better UI than one without; BM25 relevance (is the picked palette the right one); the other six bundled skills; the `uipro-cli` npm install.
- **No deterministic anti-pattern detector + edit hook.** This is the key gap versus impeccable. ui-ux-pro-max ships token validators and an HTML token validator, but the anti-pattern "AVOID" lists are model-applied guidance, not a 44-rule no-LLM detector that re-runs after every UI edit. impeccable closes the inner/outer loop; ui-ux-pro-max mostly informs the first draft.
- **Heavy, multi-skill footprint.** Seven skills plus large Python/CJS scripts and CSV datasets (slide generators, color extractors, token validators) is a meaningfully larger install than a single design prompt, and several bundled skills (slides, banner-design) are off-topic for general frontend work.
- **Counts are self-reported and version-inconsistent.** README/badges and the two manifests disagree (50+ vs 67 styles; "161 reasoning rules" badge vs 99 UX guidelines vs 161 palettes). The numbers are marketing-forward and I did not audit dataset quality or ranking relevance.
- **Subjective, unverifiable quality signal.** As with the whole cluster, "professional design" has no objective check beyond the a11y/contrast/CLS rules; recommendation quality (does BM25 pick the *right* palette?) is unmeasured here.
- **Direct overlap with the cluster.** It targets the same gap as impeccable, taste-skill, frontend-design, garden-skills, open-design, huashu-design, and baoyu-design — "AI generates generic/ugly UI." This is a consolidation question, not an independent adopt.
- **Donation/monetization-forward repo.** Heavy PayPal/cross-promo framing in the README; benign, but a maintenance-incentive signal worth noting.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Emitted palettes pass 84/84 contrast pairs in our run. For frontend work the contrast/touch/CLS/focus rules and a11y audit catch real defects (sub-4.5:1 text, <44px targets, layout shift); no effect outside the frontend |
| Speed | + | One-pass generation of a tailored design system (style + palette + type + checklist) beats hand-deriving them, for the greenfield-frontend slice; review/audit passes cost time |
| Maintainability | + | Pushes semantic color tokens, a design-system map, and consistency rules toward a documented system rather than one-off styles |
| Safety | neutral | Prompt + local Python/CJS scripts (token/HTML validators, color extraction); no credentials or network calls implied, but a larger local-script execution surface than a prose-only skill |
| Cost Efficiency | - | Seven skills plus datasets and on-invoke reference loads are a large context/footprint; justified only when a polished frontend is the deliverable |
| Verifiability | + | Palettes are checkable: every emitted hex pair can be recomputed to a contrast ratio (84/84 >= 4.5:1) and runs are byte-identical, so a human can confirm the tokens quickly; whether the resulting UI is good stays a subjective call |

## Verdict

**discovery-log — tentative read** — ran the engine on 12 fixed briefs: 84/84 contrast pairs pass, output is deterministic (12/12) and varied (11 distinct primaries), tests pass 164/164. What blocks a real read: no model credentials, so a with-skill-vs-baseline UI comparison and a real triggering test were not possible, and the engine recommends a `risk:high` accessibility style (Neumorphism) for a healthcare brief. It remains a partial overlap with impeccable (enforcement) and frontend-design; the keep decision from the earlier review stands.

## Triage note

Left at `discovery-log`. ★103.6K and MIT — the most-starred entry in the frontend-design cluster and, by
some distance, one of the largest rows in the catalog. Nothing a bulk lane should touch.

The cluster it heads is the densest in this stage: `impeccable`, `taste-skill`, `huashu-design`,
`baoyu-design`, `garden-skills`, `open-design` and the `frontend-design` plugin all answer "make the AI
design well". This pass left every one of them, because the sibling evals do something better than a
redundancy test could — they separate the cluster by *kind*. This row and `impeccable` are lean
taste/design-language guidance with no toolchain; `huashu-design` and `baoyu-design` are full
produce-and-export pipelines with executable benches; `taste-skill` is a narrow anti-templating dial set.
Those are different risk and cost profiles, not competing implementations.

What distinguishes this row specifically is *breadth of knowledge* rather than enforcement: a curated
design database (styles, palettes, font pairings, product types) plus a Design System Generator, an
impact-ranked rule taxonomy, and unusually good accessibility and **native-mobile** coverage — the last
being genuinely rare here.

The measurable claim, if it is ever run, is the one the whole cluster shares and none has evidenced: does
a design skill change what the agent produces, measured as a with-skill-vs-baseline A/B? That is the
`TEMPLATE.md` skill-dimension requirement detector S tracks, and it is P0 work.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | skill | Design intelligence for professional UI/UX across platforms — curated styles/palettes/fonts + reasoning engine, strong a11y and native-mobile coverage | AI generates ugly or generic UIs without design guidance | impeccable, taste-skill, frontend-design plugin |
