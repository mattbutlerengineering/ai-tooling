# Evaluation: vercel-labs-agent-skills

**Repo:** [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)
**Stars:** 28,119 | **Last updated:** 2026-06-10 (pushed; created 2025-12-08) | **License:** none declared
**Dev loop stage:** Implement + Review — the skills are coding guidance (React/Next.js, React Native, view transitions, web design, prose) applied while writing and reviewing UI/docs, plus a Verify-adjacent Vercel cost/perf audit. Frontend- and Vercel-leaning, not a general-purpose roster.
**Layer:** Process (a small collection of `SKILL.md` instruction-and-script packages installed into an agent's skills directory; no runtime of its own — installed via the sibling `npx skills` CLI)

---

## What it does

Vercel's official collection of agent skills in the [agentskills.io](https://agentskills.io/) `SKILL.md` format. As inspected, it ships **9 skills**, tightly focused on Vercel's own stack and craft standards rather than broad dev coverage:

- **vercel-optimize** — audits a deployed Vercel project for cost/perf/reliability/caching/function usage/billing; collects Vercel metrics *first*, then investigates only the routes those metrics point to. This is the standout: a real, evidence-driven audit, backed by a `vercel-optimize-tests` package with dozens of `.mjs` tests and real-CLI-output fixtures.
- **react-best-practices** — 40+ React/Next.js perf rules in 8 impact-ranked categories (waterfalls, bundle size, server-side perf, data fetching, re-renders, rendering, micro-opts); backed by a `react-best-practices-build` TypeScript package (parser, validate, migrate, extract-tests) and a `test-cases.json`.
- **web-design-guidelines** — 100+ rules for accessibility, focus states, forms, animation, typography, images, perf, navigation/state, dark mode, touch, i18n.
- **writing-guidelines** — 80+ rules from the Vercel writing handbook (voice/tone by content type, structure, code samples, typography, AI-disclosure workflow).
- **react-native-skills / react-view-transitions / composition-patterns / deploy-to-vercel / vercel-cli-with-tokens** — mobile RN patterns, the React View Transition API, component composition, and two Vercel-deploy/CLI skills.

The defining trait: most skills are **build-backed** — generated/validated from source rule sets with their own test suites and CI (`react-best-practices-ci.yml`), not hand-waved markdown. The repo also ships `AGENTS.md` and `CLAUDE.md` for agent consumption.

## How we tested it

**Source-grounded inspection — not installed, not run.** No skill was installed via `npx skills`, none was activated in any agent, and no Vercel project was audited. Every claim comes from the repository (GitHub metadata, README, recursive file tree, `SKILL.md` paths, and the `packages/` build/test directories), not from observed skill behavior. The rule counts ("40+", "100+", "80+") and "from Vercel Engineering" framing are the README's own; I confirmed the *structure* (9 skills, build packages, test suites) but did not measure rule efficacy.

```bash
gh api repos/vercel-labs/agent-skills --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'  # 28,119; license null
gh api repos/vercel-labs/agent-skills/readme --jq '.content' | base64 -d | head -130
gh api "repos/vercel-labs/agent-skills/git/trees/HEAD?recursive=1" --jq '.tree[]|select(.path|endswith("SKILL.md")).path'  # 9 skills
gh api "repos/vercel-labs/agent-skills/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # packages/react-best-practices-build, packages/vercel-optimize-tests/*
gh api repos/vercel-labs/agent-skills --jq '{forks:.forks_count, openissues:.open_issues_count}'  # forks 2534, open issues 150
```

## What worked

- **Small, curated, and authoritative for its niche.** 9 skills from Vercel Engineering covering exactly the surface Vercel knows best — React/Next.js perf, web UI quality, RN, view transitions, and Vercel-project economics. No 200-file menu to curate down; every skill earns its place.
- **Build-backed and tested, not prose-ware.** `react-best-practices-build` (parser/validate/migrate/extract-tests + `test-cases.json`) and `vercel-optimize-tests` (dozens of `.mjs` tests with real-CLI fixtures) mean the rules are derived and regression-tested. This is the rarest property in skill collections — most are unverified markdown. It directly raises trust.
- **vercel-optimize is genuinely differentiated.** "Collect metrics first, then investigate only what the data points to" is a real methodology, not a checklist — and it touches Cost Efficiency, a signal almost nothing else in the catalog moves.
- **Format-native and pairs cleanly with `npx skills`.** Conforms to agentskills.io `SKILL.md`; installs in one command across 70+ agents via its sibling CLI. `AGENTS.md`/`CLAUDE.md` included for direct agent consumption.
- **Strong traction and active maintenance.** 28.1K stars, ~2.5K forks, only 150 open issues (low for the reach), recent pushes, CI on the React skill.

## What didn't work or surprised us

- **Narrow by design — Vercel/React-shaped, not a general dev kit.** 4 of 9 skills are React/Next/RN; two more are Vercel-deploy/CLI specific. If you are not on the Vercel/React stack, perhaps half the collection is irrelevant. This is a quality trade (focus over breadth), but it is a real fit constraint vs. broad collections.
- **No declared license.** `license` is `null` — same blocker as the sibling CLI. "Official Vercel" framing doesn't substitute for explicit terms when you are installing it into client work.
- **Vendor-aligned guidance.** The advice optimizes for the Vercel/Next.js way (and `deploy-to-vercel`/`vercel-cli-with-tokens` are outright platform plumbing). Excellent if you're on Vercel; mild lock-in pull if you're evaluating neutrally.
- **Rule counts are self-reported.** "40+/100+/80+ rules" and impact rankings are the authors' claims; the test suites validate parsing/extraction, not that following every rule improves real outcomes. Treat the rankings as informed opinion, not measured.
- **Two of the nine are thin platform skills.** `deploy-to-vercel` and `vercel-cli-with-tokens` are convenience/credential plumbing, not craft guidance — they pad the count more than the value.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Build-backed, test-validated rule sets (react-best-practices, web-design-guidelines) catch real perf/a11y/UI defects during Implement and Review. |
| Speed | + | Ready-made, impact-ranked guidance means the agent applies known-good patterns instead of re-deriving them; vercel-optimize triages by metrics first. |
| Maintainability | + | web-design-guidelines, writing-guidelines, and composition-patterns push consistent, reviewable UI/prose/component conventions. |
| Safety | neutral | Pure instruction/script skills; no runtime reach of their own. `vercel-cli-with-tokens` touches credentials — handle per normal token hygiene. (No license is a governance, not runtime, concern.) |
| Cost Efficiency | + | vercel-optimize is purpose-built to cut Vercel cost/function usage — one of the few catalog entries that directly targets spend. |

## Verdict

**ADOPT (for Vercel/React stacks) — cherry-pick vercel-optimize, react-best-practices, and web-design-guidelines; CONDITIONAL otherwise.** This is the highest-trust skill collection inspected so far: small, curated, Vercel-authored, and — uniquely — build-backed with real test suites instead of unverified markdown. If you ship on Vercel/Next.js, vercel-optimize (metrics-first cost/perf audit) and the React/web-design rule sets are immediately worth installing. The only real caveats are the missing license and the deliberate narrowness — outside the Vercel/React orbit, only web-design-guidelines and writing-guidelines fully generalize.

Compared to neighbors: **addyosmani/agent-skills** is broader "production-grade engineering" coverage but markdown-only (not test-backed); Vercel wins on verification, addy on breadth. **mattpocock/skills** is a working dev's general-purpose kit (TDD, module design, debugging) — more stack-agnostic, less specialized. **gstack** is a *harness* (~53 curated skills + CLIs) — a whole setup vs. a focused 9-skill collection. **wshobson/agents** and **agency-agents** are large persona rosters you curate down; vercel-labs/agent-skills is the opposite philosophy — few skills, each tested. For Vercel/React work specifically, this beats all of them on trust per skill.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | skill | Vercel's official 9-skill collection (React/Next perf, web-design & writing guidelines, RN, view transitions, metrics-first Vercel cost/perf audit) — uniquely build-backed with real test suites | Want authoritative, test-validated React/Next/Vercel coding and UI/cost guidance rather than unverified markdown skills | addyosmani/agent-skills, mattpocock/skills, ECC, web-quality-skills (vercel-optimize ↔ Vercel cost) |
