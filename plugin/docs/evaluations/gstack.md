# Evaluation: gstack

**Repo:** [garrytan/gstack](https://github.com/garrytan/gstack)
**Stars:** 111,392 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Plan + Implement + Verify + Review + Ship + Reflect (a full-sprint workflow)
**Layer:** Process (with a Tooling browser/eval substrate underneath)

---

## What it does

Catalog one-liner: "Garry Tan's Claude Code setup: 23 opinionated agent tools (CEO, Designer, Eng Manager, etc.)". The "23 tools" count is now outdated — at v1.58.3.0 it ships ~53 slash-command skills plus 73 standalone `bin/` CLIs. gstack turns Claude Code into a role-based virtual engineering team: each skill is a markdown SKILL.md that puts the agent into a specific specialist persona with a specific methodology — `/office-hours` (YC-style product interrogation), `/plan-ceo-review` (4 scope modes: Expansion/Selective/Hold/Reduction), `/plan-eng-review` (architecture lock, ASCII data-flow diagrams, test matrix), `/plan-design-review` (0-10 design-dimension scoring, "AI slop" detection), `/review` (staff-engineer diff review for SQL safety, LLM trust-boundary violations, conditional side effects), `/cso` (OWASP Top 10 + STRIDE with a confidence gate and false-positive exclusions), `/qa` (real-browser click-through with auto-generated regression tests), `/ship` and `/land-and-deploy` (test/coverage/PR/merge/deploy-verify), plus power tools (`/codex` cross-model second opinion, `/careful`/`/freeze`/`/guard` safety, `/learn` persistent memory).

Mechanically it installs as a Claude Code **skills pack**, not a marketplace plugin: `git clone … ~/.claude/skills/gstack && ./setup` symlinks per-skill directories under `~/.claude/skills/`, and you add a `## gstack` section to CLAUDE.md listing the available commands. Each SKILL.md carries real frontmatter — `allowed-tools`, `triggers` (voice-friendly phrases), `version`, a `preamble-tier`, and `gbrain` context-query blocks that pull prior CEO plans / design docs / review history from `~/.gstack/projects/{slug}/` into context. A bash "preamble" runs first to do the throttled auto-update check, session tracking, and proactive-suggestion bookkeeping. State (learnings, plans, retros, taste profile, telemetry JSONL) lives in `~/.gstack/`. It also ships its own anti-bot Chromium ("GStack Browser") with a layered ML prompt-injection defense, optional GBrain memory backend (PGLite/Supabase), iOS live-device QA over USB, and a `--host` flag that installs the same skills into Codex/Cursor/OpenCode/Factory/Kiro and 4 other agents. The pitch is "one process — Think → Plan → Build → Review → Test → Ship → Reflect — where each skill feeds the next."

## How we tested it

**Evidence:** REVIEW

Repo, README, SKILL.md, CI-workflow, and changelog inspection via the GitHub API — **not a hands-on installed run**. The install mutates `~/.claude/skills/` with ~53 symlinked skills, writes a `~/.gstack/` state tree, adds a per-session auto-update preamble and proactive-suggestion hooks, edits CLAUDE.md, and (for the browser/QA path) builds a bundled Chromium with a 22MB ML classifier — far too invasive to drop into this session just to evaluate, and it would collide with the user's existing OMEGA + superpowers + skills setup. Findings rest on the manifest of skill directories, two full SKILL.md files (`plan-ceo-review`, `review`), the E2E eval CI workflow, the version/changelog cadence, commit/PR history, and the docs/designs ADR set.

```bash
gh api repos/garrytan/gstack --jq '{stars,license,description,pushed_at,created_at,forks,open_issues}'
# 111,392 stars, MIT, 16,559 forks, 705 open issues, created 2026-03-11, pushed 2026-06-18
gh api repos/garrytan/gstack/readme --jq '.content' | base64 -d
gh api "repos/garrytan/gstack/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # 62 SKILL.md, 73 bin/, 574 test paths
gh api repos/garrytan/gstack/contents/plan-ceo-review/SKILL.md --jq '.content' | base64 -d   # frontmatter + gbrain queries
gh api repos/garrytan/gstack/contents/review/SKILL.md --jq '.content' | base64 -d            # SQL/LLM-trust/side-effect review
gh api repos/garrytan/gstack/contents/.github/workflows/evals.yml --jq '.content' | base64 -d # Docker E2E eval gate on PRs
gh api repos/garrytan/gstack/contents/VERSION --jq '.content' | base64 -d   # 1.58.3.0
gh api repos/garrytan/gstack/contributors --paginate --jq '.[].login' | wc -l   # 9
gh api 'repos/garrytan/gstack/commits?per_page=1' -i | grep -i '^link:'          # ~323 commits, PRs numbered to #2047
```

## What worked

- **The skills are substantive methodology, not persona theater.** `/review`'s SKILL.md explicitly targets "SQL safety, LLM trust boundary violations, conditional side effects"; `/cso` is OWASP Top 10 + STRIDE with a confidence gate and 17 false-positive exclusions; `/investigate` enforces an "Iron Law: no fixes without investigation" and stops after 3 failed fixes; `/plan-eng-review` forces ASCII data-flow diagrams and a test matrix. The CEO/Designer/Eng-Manager framing is a memorable wrapper around real review checklists, not the whole substance. This is the key differentiator from "agency-of-personas" gimmick bundles.
- **Genuinely mature engineering for its age.** Created 2026-03-11, already at v1.58.3.0 with ~323 commits, PRs numbered past #2047, a CHANGELOG, and a real CI gate: a Docker-based E2E **evals** workflow (`evals.yml`, `evals-periodic.yml`) plus actionlint, version-gate, make-pdf-gate, windows-setup-e2e, and a skill-docs generator. ~574 test paths in the tree, including real-Chromium stealth tests (80 passing in the v1.58.3.0 changelog). It carries `docs/designs/` ADR-style specs (SELF_LEARNING, ML_PROMPT_INJECTION_KILLER, PLAN_TUNING) and `docs/spikes/`. This is among the most rigorously built entries in the catalog.
- **Cohesive feed-forward pipeline.** `/office-hours` writes a design doc that `/plan-ceo-review` reads; `/plan-eng-review` writes a test plan `/qa` picks up; `/review` finds bugs `/ship` verifies fixed. `/autoplan` chains CEO→design→eng→DX review automatically and surfaces only taste decisions. The gbrain `context_queries` in each SKILL.md make the feed-forward concrete (prior plans/reviews are pulled into context), not just narrative.
- **Real cross-model and safety substrate.** `/codex` runs an independent OpenAI Codex review and produces a cross-model overlap analysis; `/careful`/`/freeze`/`/guard` are opt-in destructive-command and edit-scope guards; the sidebar browser ships a layered local prompt-injection defense (ML classifier + Haiku transcript vote + canary token + 2-of-3 verdict combiner). PR #1911 "fix wave: 8 community bugs (4 security guards failing open)" shows the safety claims get real scrutiny and fixes.
- **Multi-host and parallel-sprint design.** One `./setup --host <name>` installs the same skills into 10 agents (Codex/Cursor/OpenCode/Factory/Kiro/etc.), and the workflow is explicitly built to run 10-15 parallel Claude Code sprints under Conductor. Telemetry is opt-in (default off), with the schema published and local-only analytics available.

## What didn't work or surprised us

- **The star count is wildly inflated relative to substance and age.** 111K stars and 16,559 forks on a 3-month-old solo-led repo with 9 contributors and ~323 commits is not organically explicable by code quality — it tracks Garry Tan's (YC president) celebrity and a heavy promotional README (Karpathy quote, "810× my 2013 pace," "we're hiring at YC"). The engineering is genuinely good, but the stars are a popularity signal, not a quality signal; do not let the 111K number drive the verdict. Compare oh-my-claudecode (36.6K, 110 contributors) and superpowers — gstack's commit-to-star ratio is the inverse of a community-validated project.
- **Effectively a solo/small-team project with a marketing surface.** 9 contributors against 705 open issues. The README's productivity claims (`~810×`, `240× the entire 2013 year`) are self-reported with a caveats doc, not third-party validated, and read as personal-brand content. Bus-factor and over-promise risk are real even though the code is more rigorous than most.
- **Heavy, opinionated install that fights an existing setup.** It owns `~/.claude/skills/`, injects a per-session auto-update preamble + proactive-suggestion prompts, edits CLAUDE.md, and writes a `~/.gstack/` state tree. For a user already running OMEGA (coordination hooks), superpowers (TDD/review/debugging skills), and a curated skills set, large fractions of gstack (`/review`, `/investigate`, `/ship`, TDD, debugging, memory via `/learn` vs GBrain vs OMEGA) directly **duplicate** existing tools — overlap, not addition. The `--no-prefix` default (`/qa`, `/review`, `/ship`) risks command-name collisions with other packs (it offers `--prefix` to namespace).
- **Big optional infra footprint to get full value.** The differentiated pieces — GStack Browser (bundled Chromium + 22MB/721MB ML classifiers), GBrain (Supabase/PGLite), iOS USB QA, Codex CLI second-opinion, Conductor for parallelism — each need extra setup, keys, or paid plans. The Claude-only skills-pack core is the realistic default, and much of that core overlaps the user's stack.
- **No neutral benchmark.** As with every bundle in the catalog, there's no third-party evidence it beats vanilla Claude Code on a real task; the value case rests on the (plausible, well-built) mechanics of its review/QA/ship checklists plus the author's self-reported throughput.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | `/review` (SQL safety, LLM trust-boundary, side-effect checks), `/investigate` "no fix without investigation," `/qa` auto-generated regression tests, and `/codex` cross-model review target real production-bug failure modes |
| Speed | +/- | `/autoplan` and `/ship`/`/land-and-deploy` automate multi-step plan/review/ship; offset by a large skill surface, per-session preamble overhead, and ceremony for small changes |
| Maintainability | + | `/document-release` keeps READMEs/ARCHITECTURE/CLAUDE.md in sync from the diff with a Diataxis coverage map; `/learn` + GBrain compound project knowledge; design-slop detection in review |
| Safety | +/- | Real `/cso` OWASP+STRIDE audit, opt-in `/careful`/`/freeze`/`/guard` destructive-command + edit-scope guards, layered browser prompt-injection defense; offset by an invasive `~/.claude` install with an auto-updating preamble from a small team |
| Cost Efficiency | +/- | `gstack-model-benchmark` and `/codex` can route to cheaper models / spread load; offset by browser ML classifiers, multi-stage review pipelines, and 10-15 parallel sprints that raise spend |

## Verdict

**CONDITIONAL**

Adopt selectively, on a project where you want a turnkey role-based sprint process — `/office-hours` → `/autoplan` → implement → `/review` → `/qa` → `/ship` — and are not already invested in an overlapping skills stack. gstack is the rare celebrity bundle whose substance holds up: the skills are real methodology (OWASP+STRIDE security, SQL/LLM-trust-boundary diff review, investigate-before-fix, real-browser QA with regression tests), the engineering is unusually mature for a 3-month-old repo (Docker E2E eval CI, ~574 test paths, ADR-style design docs, weekly versioned releases), and it lives natively inside the dev loop. The `--prefix` / `--no-prefix` and `--host` options plus opt-in safety guards make a scoped trial feasible.

It is **not** ADOPT for this user because (1) the 111K stars are celebrity- and marketing-driven, not a community-quality signal (9 contributors, 705 open issues, self-reported "810×" claims) — assess on substance, which earns CONDITIONAL, not on the number; and (2) it heavily duplicates tools the user already runs — superpowers (TDD/review/debug/verification), OMEGA and `/learn`/GBrain (memory), and the user's own commit/review skills — while owning `~/.claude/skills/` with an auto-updating preamble that risks conflicts. Installing the whole pack would be redundant and invasive; the sensible path is a namespaced (`--prefix`) trial on one project, cherry-picking the genuinely additive skills (`/cso` security audit, `/qa` real-browser QA, `/design-shotgun`→`/design-html` design pipeline, `/codex` cross-model second opinion) that superpowers/OMEGA don't already cover. Re-evaluate toward ADOPT if a hands-on run on a real project shows the QA/security skills outperform the user's existing stack, or if it grows genuine multi-contributor validation. It is more substantive than persona-only bundles (agency-agents, claude-code-staff-engineer) and comparable in rigor to claude-night-market / oh-my-claudecode — same CONDITIONAL/cherry-pick posture as those.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gstack](https://github.com/garrytan/gstack) | harness | Garry Tan's Claude Code skills pack: ~53 role-based sprint skills (CEO/Designer/Eng-Manager/QA/Security/Release) plus browser, GBrain memory, and cross-model review | Want a curated, opinionated full-sprint process (plan→review→QA→ship) as ready-made specialist roles instead of a blank prompt | superpowers, ECC, claude-night-market, oh-my-claudecode, compound-engineering, agency-agents |
