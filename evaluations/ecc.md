# Evaluation: ECC (Everything Claude Code)

**Repo:** [affaan-m/ECC](https://github.com/affaan-m/ECC)
**Stars:** 218,088 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** All stages (Plan, Implement, Verify, Review, Ship, Reflect) — a full harness layer
**Layer:** Tooling + Infrastructure (skills/agents/rules + a hook runtime, memory store, and CLI control-plane)

> **Note on scope / duplication.** A prior evaluation of this same repo already exists at
> [`everything-claude-code.md`](everything-claude-code.md) (verdict CONDITIONAL, skill-breadth angle).
> This file is the **harness-and-footprint** evaluation requested separately: it focuses on ECC's
> "instincts"/memory/security layers, its hook runtime, and the conflict surface against this
> user's existing OMEGA + GSD + claude-mem + superpowers stack — angles the breadth eval barely
> touches. The two reach the same verdict (CONDITIONAL) for different reasons. If the catalog only
> wants one ECC eval, merge these and keep the duplication flagged here.

---

## What it does

Catalog one-liner: "Agent performance optimization with skills, instincts, memory, and security." ECC ("Everything Claude Code" — the acronym is never spelled out in the current README but the legacy name is hard-coded into the hook bootstrap, which falls back to both `ecc` and `everything-claude-code` plugin directories) is the largest Claude Code enhancement bundle in the catalog by raw scale: **67 agents, 271 skills, 92 commands, ~29 rules across 6+ language packs, and a ~10-hook PreToolUse runtime** plus PreCompact/SessionStart/Stop hooks. v2.0.0 adds a Rust "control-plane" prototype (`ecc2/`), a Tkinter desktop dashboard, a SQLite session/state store, and an `orch-*` orchestrator family.

Mechanically it installs as a Claude Code plugin (`/plugin marketplace add … && /plugin install ecc@ecc`) or via a manifest-driven `install.sh` (note: the README's `npx ecc-install` is not a published npm package — it resolves to 404, so the plugin-marketplace path is the working one) with profiles (`minimal`/`core`/`full`) and `--with`/`--without` component selection. The plugin drops SKILL.md files, agent definitions, slash commands, and `hooks/hooks.json` into the agent surface; **rules cannot be distributed via plugins** (an upstream Claude Code limitation), so you manually `cp -r rules/common ~/.claude/rules/ecc/` plus one language pack. The four named "layers" the catalog calls out map to concrete mechanisms:

- **Skills** — 271 SKILL.md files (coding standards, language patterns, TDD/verification, security-review, plus operator/content skills like `brand-voice`, `investor-materials`, `ito-market-intelligence`).
- **Instincts (continuous learning v2)** — a Stop/observe-hook pipeline (`pre:observe`, `evaluate-session.js`) that captures tool-use observations and extracts confidence-scored "instincts" stored under `~/.local/share/ecc-homunculus`, which `/evolve` clusters into new skills. `/skill-create` generates skills from git history.
- **Memory** — session-lifecycle hooks (`session-start-bootstrap.js`, `session-end.js`, `pre-compact.js`) that persist/reload session summaries, aliases, and metrics under `~/.claude` (or `ECC_AGENT_DATA_HOME`); SessionStart injects up to 8000 chars of additional context by default.
- **Security** — a `pre:bash` GateGuard dispatcher that blocks destructive shell commands (`rm`, force `git checkout`, `find -exec`) before they run; a `pre:edit-write:gateguard-fact-force` hook that blocks the *first* edit per file until "investigation" is done; `config-protection` (blocks edits to linter/formatter configs); secret detection; and AgentShield (`npx ecc-agentshield scan`), a separate 102-rule static auditor for your `.claude` config.

## How we tested it

**Evidence:** REVIEW

**Method: inspected the repo, full README (1,850 lines), `hooks/hooks.json`, the HEAD tree, license, npm download stats, and contributor/commit history via the GitHub API and npm registry. Did NOT install or run it.** This is a deliberate non-install evaluation. ECC's plugin install auto-loads a ~10-entry PreToolUse hook runtime plus SessionStart/PreCompact/Stop hooks into the live Claude Code session, mutates `~/.claude` (skills, agents, commands, hooks, a SQLite state store, `~/.local/share/ecc-homunculus`), and the rules step copies files into `~/.claude/rules/ecc/`. That is far too invasive to drop into this session merely to evaluate, and it would collide head-on with the user's running OMEGA coordination hooks, claude-mem observation hooks, GSD, and superpowers skills (see conflict analysis below). All counts below are from live API/registry calls; no metrics are invented, and any benchmark-style figures (test counts, "%" claims) are quoted as the project's own self-reported numbers, not reproduced here.

```bash
gh api repos/affaan-m/ECC --jq '{stars,license:.license.spdx_id,description,created_at,pushed_at,forks,open_issues}'
# 218,088 stars; MIT; created 2026-01-18; pushed 2026-06-19; 33,451 forks; 48 open issues
gh api repos/affaan-m/ECC/readme --jq '.content' | base64 -d                 # full 1,850-line README
gh api repos/affaan-m/ECC/contents/hooks/hooks.json --jq '.content' | base64 -d   # ~10 PreToolUse + PreCompact/SessionStart/Stop hooks
gh api 'repos/affaan-m/ECC/git/trees/HEAD' --jq '.tree[].path'               # .claude/.codex/.cursor/.opencode/agents/skills/hooks/ecc2/...
gh api 'repos/affaan-m/ECC/contributors?per_page=10' --jq '.[]|"\(.login): \(.contributions)"'  # affaan-m: 1470, next: 47
gh api 'repos/affaan-m/ECC/commits?per_page=1' -i | grep -i '^link:'         # ~2,180 commits; first commit 2026-01-18
curl -s https://api.npmjs.org/downloads/point/last-month/ecc-universal       # 13,239/mo
curl -s https://api.npmjs.org/downloads/point/last-month/ecc-agentshield     # 31,412/mo
```

Reviewed: README (English, full), `hooks/hooks.json`, the recursive HEAD tree, the changelog (v1.2 → v2.0.0), the rules layout, contributor/commit distribution, and the two npm packages' download counts. Also cross-checked the existing sibling evaluation [`everything-claude-code.md`](everything-claude-code.md), which spot-read 4 SKILL.md files for content quality.

## What worked

- **The security layer is genuinely substantive and hook-enforced, not just prose.** GateGuard blocks destructive shell commands *before execution* (real exit-2 gating, not a checklist), `config-protection` stops the agent from weakening linter configs to make errors disappear, and `gateguard-fact-force` blocks the first edit per file until the agent has investigated importers/schemas/instructions. AgentShield is a real 102-rule static auditor (self-reported 1282 tests, 98% coverage) that scans *your* `.claude` config for secrets/permission/hook-injection risks — and it's usable standalone (`npx ecc-agentshield scan`) without adopting the rest of ECC.
- **The instinct/memory machinery is a coherent self-improvement loop.** observe-hook → confidence-scored instincts → `/evolve` clusters them into skills → `/skill-create` mines git history. This is a real "continuous learning" pipeline with import/export/prune and a 30-day TTL, not a slogan.
- **Mature, fast-shipping, and unusually well-documented about its own footguns.** ~2,180 commits since 2026-01-18, 14 releases to a stable v2.0.0, ~242 contributors, self-reported "997 internal tests passing." The README documents the duplicate-hooks trap, the "do not stack install methods" failure mode, `ECC_HOOK_PROFILE`/`ECC_DISABLED_HOOKS`/`ECC_SESSION_START_CONTEXT` runtime gates, a dry-run uninstaller, and a `doctor`/`repair` lifecycle. That self-awareness is rare in this class of bundle.
- **Real cross-harness packaging.** One repo ships translated configs for Claude Code, Cursor, Codex, OpenCode, Gemini, Zed, and Copilot, with a DRY hook adapter so Cursor reuses the same `scripts/hooks/*.js`. Useful for a polyglot, multi-harness team.
- **Granular install controls make a scoped trial feasible.** `--profile minimal --without baseline:hooks`, `npx ecc consult "<need>"` component advisor, and per-component manual copy mean you can take just AgentShield, or just one language's rules, without the hook runtime.

## What didn't work or surprised us

- **It IS a duplicate of the user's existing setup, twice over.** (1) ECC's `rules/common/` files — `coding-style.md` (immutability/file-org), `testing.md` (80% coverage, TDD), `security.md` (mandatory checks), `git-workflow.md`, `performance.md` (model selection), `patterns.md`, `hooks.md`, `agents.md` — are the *same documents* already present in this user's `~/.claude/rules/common/`. The user is effectively already running a curated subset of ECC's rules. (2) A prior catalog evaluation of this exact repo already exists ([`everything-claude-code.md`](everything-claude-code.md)), and the catalog separately lists `everything-claude-code` as its own entry (CATALOG.md line 143). Installing ECC wholesale would re-add content the user already has.
- **Heavy, auto-loading hook runtime collides directly with OMEGA + claude-mem + GSD.** ECC auto-loads ~10 PreToolUse hooks plus SessionStart/PreCompact/Stop. Its `pre:observe`/`evaluate-session` (continuous-learning capture), `session-start-bootstrap` (context injection), and `pre:compact` (state save) occupy the *same lifecycle slots* as the user's OMEGA coordination hooks and claude-mem observation hooks. Running both means double SessionStart context injection (ECC adds up to 8000 chars), two competing memory stores (ECC's `~/.local/share/ecc-homunculus` + `~/.claude` session-data vs OMEGA + claude-mem), and overlapping compaction/Stop handlers — added latency, context bloat, and conflicting "memory" sources of truth. The `gateguard-fact-force` first-edit block in particular would fight any agent the user already drives.
- **Stars are wildly inflated relative to substance and age.** 218K stars / 33K forks on a repo created **2026-01-18** (five months old) with ~2,180 commits and a single dominant author (`affaan-m`: 1,470 commits; next contributor: 47) is not an organic code-quality signal — it tracks heavy X promotion, a hackathon win, and a sponsorship/Pro funnel (ECC Pro $19/seat/mo, GitHub Sponsors, three business sponsors in the README). npm reality is far smaller: ~13K/mo for `ecc-universal`. Assess on substance, not the headline number.
- **Effectively a solo project with a commercial surface.** ~242 "contributors" but 97% of commits are one person; the README is a marketing document (pricing table, sponsor logos, "first plugin to maximize every major AI coding tool," X-thread guides as primary docs). Bus-factor and over-promise risk are real.
- **271 skills + 67 agents is a large context/maintenance surface with an unverifiable long tail.** Spot-checks (per the sibling eval) show high quality, but 271 skills inevitably include filler and operator/content skills (`investor-outreach`, `ito-market-intelligence`, `brand-voice`) irrelevant to this catalog's coding-dev-loop focus. `/multi-*` commands silently require a *separate* `ccg-workflow` runtime to work at all.
- **No neutral benchmark for the "performance optimization" claim.** As with every bundle in the catalog, there is no third-party evidence ECC beats vanilla Claude Code on a real task. The "harness performance system" framing rests on the (plausible) mechanics of its hooks/skills plus self-reported test counts.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | `gateguard-fact-force` (investigate-before-edit), language reviewer agents, TDD/verification skills, and per-language security rules target real failure modes; offset by an unverifiable 271-skill long tail |
| Speed | +/- | Skills/agents automate planning/review/ship, but ~10 auto-loaded PreToolUse hooks + SessionStart context injection add per-tool latency, and ceremony for small changes |
| Maintainability | + | Consistent SKILL.md format, per-language rules, `doctor`/`repair`/dry-run-uninstall lifecycle, and instinct→skill evolution; offset by a huge surface to keep current |
| Safety | + | GateGuard destructive-command blocking, config-protection, secret detection, and the standalone AgentShield 102-rule auditor are real, hook-enforced guardrails — the strongest part of ECC |
| Cost Efficiency | +/- | Documents token-optimization settings (sonnet default, `MAX_THINKING_TOKENS`, autocompact override) and strategic-compact; offset by SessionStart context injection, large skill surface, and Agent-Teams spend warnings |

## Verdict

**CONDITIONAL** (cherry-pick, do not install wholesale) — aligning with the prior [`everything-claude-code.md`](everything-claude-code.md) verdict but for footprint/overlap reasons rather than breadth reasons.

ECC is the most substantial security-and-self-improvement bundle in the catalog: GateGuard's pre-execution destructive-command blocking, the fact-force investigate-before-edit gate, config-protection, and the standalone AgentShield auditor are real, hook-enforced guardrails, and the instinct→skill continuous-learning loop is a coherent mechanism, not a slogan. The engineering is mature for a five-month-old repo (v2.0.0, ~2,180 commits, documented runtime gates, dry-run uninstall). Those pieces earn a CONDITIONAL.

It is **not** ADOPT for this user, for two decisive reasons. **First, it is largely redundant:** ECC's `rules/common/` are the same documents the user already runs in `~/.claude/rules/common/`, its TDD/review/verification skills duplicate superpowers, and the repo already has a catalog evaluation. **Second, the hook footprint actively conflicts with the user's stack:** ECC's auto-loaded `pre:observe`/`session-start`/`pre:compact`/Stop hooks occupy the same lifecycle slots as OMEGA's coordination hooks and claude-mem's observation hooks, producing duplicate SessionStart context injection, two competing memory stores, and overlapping compaction handlers. Installing the full plugin would be invasive and would create conflicting memory sources of truth. The headline 218K stars are promotion-and-funnel-driven (one author at 1,470 of ~2,180 commits, ~13K npm downloads/mo), so the verdict rests on substance.

**Sensible path:** treat ECC as a parts bin, not a harness to adopt. Run **AgentShield standalone** (`npx ecc-agentshield scan` against the user's own `.claude` config — purely additive, no install, no hook conflict). Optionally cherry-copy a single language rule pack or a specific reviewer agent. Do **not** enable the ECC hook runtime alongside OMEGA/claude-mem; if ever trialed, do so with `--profile minimal --without baseline:hooks` on a throwaway project. Re-evaluate toward ADOPT only if the user drops OMEGA/claude-mem in favor of ECC's memory/instinct system wholesale (a harness swap, not an enhancement) and a hands-on run shows its guardrails beat the current setup.

**Differentiation:** vs. **gstack** (CONDITIONAL) — both are mature celebrity/promotion-inflated bundles whose substance holds up; gstack leads on role-based sprint methodology and real-browser QA, ECC leads on hook-enforced security guardrails and cross-harness breadth; both heavily overlap the user's superpowers/OMEGA stack and are cherry-pick CONDITIONALs. vs. **superpowers** (the user already has it) — superpowers is a portable skill collection (TDD/debug/review/verification) that lives cleanly inside the loop without a heavy hook runtime; ECC's same skills are redundant against it and its hooks are the conflict surface superpowers doesn't have. vs. **claude-night-market / oh-my-claudecode** — same cherry-pick posture; ECC is the broadest and most security-focused but also the most invasive to install.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ECC](https://github.com/affaan-m/ECC) | harness | "Everything Claude Code": 271 skills, 67 agents, per-language rules, hook-enforced security (GateGuard + AgentShield), and an instinct/memory continuous-learning loop; cross-harness (218K stars are promotion-driven) | Want a turnkey, security-hardened, self-improving Claude Code bundle — but most of it overlaps an existing skills/memory stack | superpowers, gstack, ruflo, everything-claude-code, oh-my-claudecode |
