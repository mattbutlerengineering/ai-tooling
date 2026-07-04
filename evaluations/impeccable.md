# Evaluation: impeccable

**Repo:** [pbakaus/impeccable](https://github.com/pbakaus/impeccable)
**Stars:** 39,641 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
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

**Evidence:** REVIEW

Source-grounded review over the GitHub API. I did NOT install the skill or run any `/impeccable` command on a live project, and I generated no before/after UI. I read the repository metadata, the full `README.md`, the complete `SKILL.md`, the file tree, the plugin manifest, and verified the detector rule count by counting rule IDs in the antipatterns registry. Any judgement about output quality below is reasoning about the rules and structure, not a measured rendering result. The "44 deterministic rules" figure is the repo's own claim, which I confirmed against the source; I did not independently audit each rule's correctness.

```bash
gh search repos impeccable --limit 20 --json fullName,description,stargazersCount,url
gh api repos/pbakaus/impeccable --jq '{description, stars:.stargazers_count, license:.license.spdx_id, pushed:.pushed_at, created:.created_at, homepage}'
gh api "repos/pbakaus/impeccable/git/trees/HEAD?recursive=1" --jq '.tree[] | "\(.type)\t\(.size)\t\(.path)"'
gh api "repos/pbakaus/impeccable/contents/README.md"                         --jq '.content' | base64 -d
gh api "repos/pbakaus/impeccable/contents/.agents/skills/impeccable/SKILL.md" --jq '.content' | base64 -d
gh api "repos/pbakaus/impeccable/contents/.claude-plugin/plugin.json"         --jq '.content' | base64 -d
gh api "repos/pbakaus/impeccable/contents/.agents/skills/impeccable/scripts/detector/registry/antipatterns.mjs" --jq '.content' | base64 -d | grep -cE "id:\s*['\"]"   # -> 44
grep -in "impeccable" /Users/mbutler/github/ai-tooling/CATALOG.md
```

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
- **Not verified hands-on.** The verdict rests on reading the skill and confirming the rule count, not on measured UI output. The case-study before/afters live on the author's site and are self-selected.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | For frontend work, the contrast floors, a11y/responsive audits, and the deterministic detector catch real defects (sub-4.5:1 text, overflow, clipped dropdowns) that ship broken UI; no effect outside the frontend |
| Speed | neutral | Adds critique/audit/polish passes and a detector run that cost time; offsets rework from generic output — roughly a wash, leaning slower per task but fewer redesign loops |
| Maintainability | + | PRODUCT.md/DESIGN.md plus extracted tokens/components push toward a consistent, documented design system instead of one-off styles |
| Safety | neutral | Prompt + local Node detector with no network/API key; the edit hook executes a bundled script on file edits (a small added execution surface), but no credentials or external calls |
| Cost Efficiency | neutral | Larger always-available skill and per-command reference loads add tokens; the detector itself is free (no LLM), and fewer generic-output redesign cycles can offset the overhead |

## Verdict

**CONDITIONAL**

impeccable is the strongest entry in the catalog's crowded "make AI design well" cluster: it pairs a concrete, refusable rule set and a 23-command shared vocabulary with a genuinely deterministic 44-rule detector and an edit-time feedback hook — the inner/outer loop pattern, applied to frontend design, with no API key needed. Provenance is excellent (39.6K stars, Apache-2.0, named author, active same-day maintenance, broad multi-harness support).

Adopt it **when the project has a real frontend** and visual quality is a deliverable — landing pages, dashboards, product UI, component libraries. It is dead weight on backend-only or CLI/library work, it is a heavier install than a typical skill, and it overlaps directly with ui-ux-pro-max / frontend-design / huashu-design / baoyu-design — if the catalog consolidates that cluster, impeccable is the one to keep. It does not belong in a universal default stack (most repos aren't frontend-heavy), but for frontend-focused work it is a default-grade pick. The existing CATALOG.md entry is accurate and needs no change.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [impeccable](https://github.com/pbakaus/impeccable) | skill | Design language that makes AI better at visual design | AI struggles with aesthetics and design consistency | ui-ux-pro-max, frontend-design plugin |
