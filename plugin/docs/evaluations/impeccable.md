# Evaluation: impeccable

**Repo:** [pbakaus/impeccable](https://github.com/pbakaus/impeccable)
**Stars:** 55,344 | **Last updated:** 2026-08-04 | **License:** Apache-2.0
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement (build/refine frontend UI) + Review (critique/audit of design quality)
**Layer:** Process (design vocabulary + rules) with a Tooling component (deterministic detector + edit hook)

---

## What it does

A design skill for AI coding agents — "the design language that makes your AI harness better at design." It descends from Anthropic's `frontend-design` skill and targets the specific problem that every model trained on the same SaaS templates emits the same visual tells (Inter everywhere, purple-to-blue gradients, cards-in-cards, gray text on tinted near-white, tiny tracked uppercase eyebrows above every section, hero-metric blocks).

The mechanism has three parts:

1. **One skill, 23 commands.** A single `SKILL.md` (21 KB) plus a `reference/` directory of per-command playbooks loaded on demand (progressive disclosure). Commands form a shared design vocabulary the user invokes as `/impeccable <command> <target>`: `init`, `craft`, `shape`, `document`, `extract` (build); `critique`, `audit` (evaluate); `polish`, `bolder`, `quieter`, `distill`, `harden`, `onboard` (refine); `animate`, `colorize`, `typeset`, `layout`, `delight`, `overdrive` (enhance); `clarify`, `adapt`, `optimize` (fix); and `live` (in-browser variant iteration). `init` writes a `PRODUCT.md` and optional `DESIGN.md` that every later command reads, so the agent knows audience, brand/product register, voice, anti-references, colors, type, and components.

2. **Concrete rules + "absolute bans," not vibes.** `SKILL.md` carries hard, checkable constraints: contrast floors (≥4.5:1 body, ≥3:1 large), line length 65–75ch, display letter-spacing floor ≥ -0.04em, OKLCH-only color, a four-step color-commitment strategy, and a match-and-refuse ban list (side-stripe borders, gradient text, default glassmorphism, hero-metric templates, identical card grids, per-section eyebrows, numbered section markers, ghost-card border+shadow pairs, 32px+ card radii, sketchy SVG, repeating-gradient stripes). It includes a two-altitude "AI slop test" to catch category-reflex output.

3. **44 deterministic detector rules + an edit hook.** A bundled Node detector (`scripts/detector/`) runs anti-pattern checks over local files with no LLM and no API key (verified: 44 rule IDs in the antipatterns registry). It has CLI, static-HTML, regex, and browser engines, plus a project hook (`$impeccable hooks on`) that auto-runs the detector after UI file edits and surfaces findings as system reminders. The repo also ships an `init`/routing flow where a context script recommends the 2-3 highest-value next commands from git/devserver/critique signals.

Installs across many harnesses (`npx impeccable install`): Claude Code, Cursor, Gemini CLI, Codex CLI, Copilot, OpenCode, Pi, and more. It ships a `.claude-plugin/plugin.json` (v3.7.1) so it is installable as a Claude Code marketplace plugin.

## How we tested it

**Evidence:** RUN

**Hands-on** — installed the published CLI with `npm i impeccable` (v4.6.0, Node 22.22) in a scratch directory and ran its deterministic `detect` command against hand-built HTML fixtures with known planted defects.

### Test design

- **Task/corpus:** three single-file HTML pages written for this eval. `slop.html` plants nine known AI-design tells: Inter font, purple-to-blue gradient, gradient-text headline, tracked-caps eyebrow above the hero h1, side-stripe card border, nested cards, 32px card radius, low-contrast gray text (#bbb on #fafafe), and a hero-metric block. `fixed.html` is the same page with each planted defect removed by hand. `clean2.html` and `clean.html` are plain pages (white background and cream background respectively) with readable contrast.
- **Baseline:** none for the model side. No model credentials were available, so the skill prompt (`SKILL.md`, 23 commands) was never driven and this run measures only the bundled deterministic detector; the with-skill-vs-baseline output comparison and the should-fire/shouldn't-fire triggering test are unmeasured.
- **Metric:** per-rule findings from `impeccable detect --json`, scored as planted defects caught out of nine, plus findings on the clean and fixed pages, plus wall-clock.
- **Reproduce:** `mkdir run && cd run && npm init -y && npm i impeccable`, write the fixtures, then `npx impeccable detect --json ../fx/<file>.html`.

```text
$ npx impeccable detect fx/slop.html     -> 11 anti-patterns + 1 advisory (12 in --json), exit 2
  --json rule counts: ai-color-palette 1, gradient-text 2, gray-on-color 1, hero-eyebrow-chip 1,
                      low-contrast 2, nested-cards 1, overused-font 1, side-tab 2, undersized-ui-text 1
$ npx impeccable detect fx/fixed.html    -> 0 findings
$ npx impeccable detect fx/clean2.html   -> 0 findings
$ npx impeccable detect fx/clean.html    -> 1 anti-pattern: cream-palette (rgb(246, 241, 231) page background)
wall-clock per file: 0.59s (slop), 0.54s (clean)
```

Planted-defect result: 7 of 9 caught (Inter, purple palette, gradient text, eyebrow, side-stripe, nested cards, low contrast). Findings are reported with the matched value (for example `1.8:1 (need 4.5:1) — text #bbbbbb on #fafafe`), so each is checkable by hand. Removing the planted defects took the page from 12 findings to 0, so the detector works as a fix-until-clean oracle.

## What worked

- **The rules are concrete and refusable, not abstract taste.** Contrast floors, a -0.04em letter-spacing floor, OKLCH-only, and a match-and-refuse ban list ("if you're about to write a side-stripe border, rewrite the element") are exactly the format an LLM can apply deterministically. This is the same strength stop-slop has for prose, applied to frontend design — and it is far more specific than the abstract "have good design sense" framing most design skills ship.
- **It backs the prompt with a real deterministic detector.** The 44-rule Node detector runs with no LLM and no API key, so the anti-pattern checks are not subject to model whim. The edit hook that re-runs it after UI changes turns the skill from a one-shot prompt into a feedback loop — genuinely the inner/outer loop pattern this catalog cares about.
- **Progressive disclosure done right.** One `SKILL.md` plus per-command `reference/` files loaded on demand keeps the always-loaded footprint reasonable for a 23-command surface; commands only pull their playbook when invoked.
- **Context persistence via PRODUCT.md / DESIGN.md.** `init` writes durable design context every command re-reads, so the agent stays on-brand across a session rather than re-deriving the design language each turn.
- **Strong provenance and maintenance.** 39.6K stars, Apache-2.0, named author (Paul Bakaus), a dedicated docs site, multi-harness installer, and commits the same day as evaluation (v3.7.1, extension v1.2.1). A large fork/port ecosystem (Pencil, Swift, OpenClaw, pi) signals real adoption. Not abandonware.
- **Already correctly cataloged.** Present at CATALOG.md line 151 with the right link, type, and overlaps (ui-ux-pro-max, frontend-design plugin).

## What didn't work or surprised us

- **Scope is frontend UI only.** `SKILL.md` explicitly states "Not for backend-only or non-UI tasks." It moves no signal on backend correctness, tests, or build. For projects with no meaningful frontend it is dead weight.
- **Heavy footprint for what it is.** The repo bundles large detector assets (one browser detector file is ~217 KB; `checks.mjs` ~116 KB). Installed, this is a meaningfully larger skill than a typical prose skill, and the Node detector adds a runtime dependency the agent must shell out to.
- **Strong overlap with several catalog entries.** ui-ux-pro-max, frontend-design plugin, huashu-design, baoyu-design, open-design, and garden-skills all target "AI generates generic/ugly UIs." impeccable is the most-starred and arguably the most rigorous (deterministic detector + ban list), so it is the strongest *implementation* — but this is a consolidation question, not six independent adopts.
- **Some rules are aggressive defaults that need human judgement.** "Cards are the lazy answer," "no bounce/elastic ever," the cream/sand/beige ban, and full-pill radius limits are opinionated stances that are usually right but will occasionally fight a legitimate brief. They are framed as defaults, not laws, but an agent applying them mechanically could over-correct a design the user actually wanted.
- **Two of nine planted defects were missed.** The 32px card radius and the 99.9% hero-metric block, both on `SKILL.md`'s own ban list, produced no finding; the radius appears only inside the `side-tab` snippet text (`border-left: 4px + border-radius: 32px`). The detector's 44 rules are a subset of the prose bans.
- **One opinionated hit on a plain page.** A readable cream-background page was flagged `cream-palette`; the same page on white produced zero findings. That rule is a stated default, but it flags a page with no other tell.
- **Skill effect unmeasured.** The skill prompt's influence on generated UI needs a model; this run measures the detector alone. The edit hook and `live` mode were not exercised either (no devserver or agent loop in the sandbox).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Detector caught 7 of 9 planted defects with 0 findings on a clean white page and on the fixed page. For frontend work, the contrast floors, a11y/responsive audits, and the deterministic detector catch real defects (sub-4.5:1 text, overflow, clipped dropdowns) that ship broken UI; no effect outside the frontend |
| Speed | neutral | Adds critique/audit/polish passes and a detector run that cost time; offsets rework from generic output — roughly a wash, leaning slower per task but fewer redesign loops |
| Maintainability | + | PRODUCT.md/DESIGN.md plus extracted tokens/components push toward a consistent, documented design system instead of one-off styles |
| Safety | neutral | Prompt + local Node detector with no network/API key; the edit hook executes a bundled script on file edits (a small added execution surface), but no credentials or external calls |
| Verifiability | + | Every finding names the rule and the matched value (e.g. `1.8:1 text #bbbbbb on #fafafe`) and the run is deterministic and fast (~0.5s/file), so a human can confirm each one |
| Cost Efficiency | neutral | Larger always-available skill and per-command reference loads add tokens; the detector itself is free (no LLM), and fewer generic-output redesign cycles can offset the overhead |

## Verdict

**discovery-log — tentative read** — the bundled detector works as advertised on a planted-defect fixture (7 of 9 caught, 0 false hits on a clean page, ~0.5s per file, no API key), but the skill prompt that is the other half of the tool needs a model run (with/without violation counts, as the triage note suggests) before any real verdict.

## Triage note

Left at `discovery-log`, and it is the row in the design cluster with the most interesting *mechanism*.

Most of these skills are guidance — text that shapes what the model does. impeccable pairs that with a
**deterministic 44-rule detector and an edit-time feedback hook**: the inner/outer loop pattern applied to
frontend design, with no API key. A rule that can be mechanically checked is a rule you can measure, and
that puts this row in a much smaller group than its star count suggests.

That mechanism is also why it is not disposable as redundant with `ui-ux-pro-max`. One supplies knowledge,
the other enforces rules; they are the two halves of the same problem, and the sibling evals treat them as
such.

Provenance is strong: Apache-2.0, ★45.1K, named author, pushed 2026-07-10, broad multi-harness support.

The unresolved question is the cluster's shared one — does any of this change what gets built, in a way a
with/without run would show. For this row that test is cheaper than for the others, because the detector
gives you an oracle: count rule violations in generated UI with the skill on and off. Worth noting as the
easiest measurement in a cluster that has none.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [impeccable](https://github.com/pbakaus/impeccable) | skill | Design language that makes AI better at visual design | AI struggles with aesthetics and design consistency | ui-ux-pro-max, frontend-design plugin |
