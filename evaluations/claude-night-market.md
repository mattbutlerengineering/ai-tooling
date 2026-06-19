# Evaluation: claude-night-market

**Repo:** [athola/claude-night-market](https://github.com/athola/claude-night-market)
**Stars:** 311 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Plan + Implement + Verify + Review + Ship + Reflect (a full-loop marketplace)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "23 plugins: TDD hooks, git/PR workflows, spec-driven dev, multi-LLM delegation (186 skills)." It is a **plugin marketplace for Claude Code** — not one monolithic plugin but 23 independently-installable plugins (198 SKILL.md files, 161 commands, 56 agents, ~70 Python hook scripts) organized into four layers: Foundation (`leyline` auth/quotas/trust, `sanctum` git/PR/sessions, `imbue` TDD/proof-of-work/scope-guard), Utility (`conserve` context/token optimization, `conjure` Gemini/Qwen delegation, `hookify` rules engine, `egregore` agent orchestration, `herald` notifications, `oracle` local ML), Domain (`pensive` review, `attune` lifecycle, `spec-kit`, `parseltongue` Python, `minister` GitHub/DORA, `memory-palace`, `archetypes`, `gauntlet`, `phantom`, `scribe`, `scry`, `tome`, `cartograph`), and Meta (`abstract` skill authoring/eval).

Mechanically, you add the marketplace (`/plugin marketplace add athola/claude-night-market`) and install only the plugins you want (`/plugin install sanctum@claude-night-market`). Plugins declare dependencies in `plugin.json` — e.g. `pensive` depends on `leyline`, which is pulled in automatically — so the shared Foundation runtime installs transitively without forcing the full 23. The headline guardrails are real PreToolUse hooks: `imbue/hooks/tdd_bdd_gate.py` blocks Write/Edit/MultiEdit unless a failing test exists, plus `guard_scope_ramp.py`, `guard_package_hallucination.py`, `vow_no_ai_attribution.py`, and `vow_no_emoji_commits.py`. A repo-root `CONSTITUTION.md` holds immutable rules that override any conflicting skill/hook. The whole thing requires Claude Code 2.1.16+ and Python 3.9+ for the hooks.

## How we tested it

Repo/source review, not a hands-on installed run. Installing even a subset mutates `~/.claude` with PreToolUse/SessionStart hooks across multiple plugins (the TDD gate would block Write/Edit in this very session), and the marketplace spans 198 skills with their own vocabulary — too invasive to install just to evaluate. Findings rest on the repo metadata, README, marketplace manifest, per-plugin `plugin.json` dependency declarations, the `imbue` hook wiring, CI workflows, test/ADR counts, and the CONSTITUTION/STEWARDSHIP governance docs.

```bash
gh api repos/athola/claude-night-market --jq '{stars,license,description,pushed_at,created_at}'
gh api "repos/athola/claude-night-market/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # 3502 paths
gh api repos/athola/claude-night-market/contents/.claude-plugin/marketplace.json --jq '.content' | base64 -d
gh api repos/athola/claude-night-market/contents/plugins/imbue/hooks/hooks.json --jq '.content' | base64 -d
gh api repos/athola/claude-night-market/contents/plugins/pensive/.claude-plugin/plugin.json --jq '.content' | base64 -d   # deps: ['leyline']
gh api repos/athola/claude-night-market/contributors --paginate --jq '.[].login' | wc -l   # 2
gh api "repos/athola/claude-night-market/commits?per_page=1" -i | grep -i '^link:'          # ~1134 commits
# counts from tree: 198 SKILL.md, 161 commands, 56 agents, 70 py hooks, 624 test files, 16 ADRs, 10 CI workflows
```

## What worked

- **Genuine modular marketplace, not a kitchen-sink dump.** Unlike a single mega-plugin, install footprint is opt-in per plugin with declared dependencies (`pensive` → `leyline`), so you can take `sanctum`+`pensive`+`imbue` and skip the other 20. This directly limits blast radius and hook-conflict surface — a meaningfully better posture than all-or-nothing bundles.
- **The headline guardrails are real, code-backed hooks.** `imbue/hooks/tdd_bdd_gate.py` is wired as a PreToolUse matcher on `Write|Edit|MultiEdit`, plus scope-ramp, package-hallucination, and commit-hygiene guards on `Bash`. These are deterministic enforcement, not prompt suggestions — exactly the kind of thing that moves Correctness/Safety.
- **Unusually strong engineering maturity for a 311-star repo.** 624 test files, 16 ADRs, and 10 CI workflows including mutation-testing, security, trust-attestation, python3.9-compat, typecheck, and a "slop-check." `make validate / lint / test` at the root runs every suite. A 1.9.x release line with per-plugin versioning and a CHANGELOG. This is more rigorous than most catalog entries many times its star count.
- **Coherent full-loop coverage with explicit governance.** `CONSTITUTION.md` (immutable override rules) and `STEWARDSHIP.md` (maintenance contract) show deliberate design intent. The `/attune:mission → imbue TDD → /full-review → /prepare-pr → /catchup` flow maps cleanly onto Plan→Implement→Verify→Review→Ship→Reflect.
- **Honest, prominent safety framing.** README leads with a warning that plugins can read/edit the repo, run shell, and call external services, and tells you to review before installing — then describes the three guard layers without overclaiming they replace review.
- **Builds on, and credits, known-good upstreams.** Integrates github/spec-kit and obra/superpowers (with an integration guide), so it is partly a curation+packaging of patterns the user may already value, not a from-scratch reinvention.

## What didn't work or surprised us

- **Effectively a solo project.** 2 contributors and ~1,134 commits against only 311 stars and 27 forks — a very high commit-to-adoption ratio that signals one author moving fast with little external validation or community review. The README's "entrusted to the community / steward not owner" language is aspirational, not yet reality. Bus-factor and abandonment risk are real.
- **Massive, idiosyncratic vocabulary.** 198 skills and 161 commands across 23 thematically-named plugins (leyline, egregore, parseltongue, phantom, scry, gauntlet, oracle, tome…). Discoverability and the learning curve are steep; much of this overlaps with tools the user already runs (superpowers, compound-engineering, commit-commands), so a large fraction is likely redundant or noise rather than additive.
- **Hook-conflict risk with an existing setup.** The TDD gate, scope-ramp, and commit-hygiene hooks fire PreToolUse on Write/Edit/Bash. A user already running superpowers' TDD skill, their own commit hooks, or OMEGA's coordination hooks could see duplicated/competing enforcement. The `vow_no_ai_attribution` / `vow_no_emoji_commits` hooks encode opinionated commit policy that may collide with the user's own attribution/commit conventions.
- **External-service dependencies in some plugins.** `conjure` delegates to Gemini/Qwen, `cartograph` needs the Mermaid Chart MCP, `oracle` does local ML inference, `phantom` is computer-use. These are optional but mean parts of the marketplace need extra keys/infra to deliver their value.
- **No published benchmark or third-party validation.** Like most catalog plugins, there's no evidence it beats vanilla Claude Code on a real task; the value case rests on the (plausible) mechanics of its guards and workflows.
- **Heavy Python-3.9 hook constraint.** Hooks must stay 3.9-compatible (macOS system Python), an unusual maintenance tax that surfaced in a recent "restore py3.9 support" fix commit — a hint that the broad surface is hard to keep green.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | `imbue` TDD/BDD PreToolUse gate blocks implementation without a failing test; `pensive` review + grounded-evidence "citation_verifier" review contract target review accuracy |
| Speed | +/- | `/attune:mission`, `/prepare-pr`, `/do-issue` automate multi-step flows; offset by ceremony and the learning cost of 198 skills / 161 commands |
| Maintainability | + | Scope-guard hooks, additive-bias audits (`leyline`), `scribe` slop/dead-code detection, ADR-driven design, and `/refine-code` / `/unbloat` push back on bloat |
| Safety | +/- | Real destructive-command blockers (`rm -rf`, `git push --force`), package-hallucination guard, CONSTITUTION override layer; offset by a large multi-hook install from a solo author that can run shell and call external services |
| Cost Efficiency | + | `conserve` token/context optimization and `conjure` cheapest-capable Gemini/Qwen delegation directly target token spend |

## Verdict

**CONDITIONAL**

Adopt selectively — install one or two plugins whose mechanics you actually want (most likely `imbue` for hard TDD enforcement, `sanctum` for git/PR, or `pensive` for review) rather than the full marketplace. The modular per-plugin install with declared dependencies makes this safe to do, and the engineering rigor (624 tests, 16 ADRs, mutation testing, security/trust-attestation CI) is genuinely high for the star count, so individual plugins are credible. It earns CONDITIONAL over SKIP because it lives natively inside the dev loop and its headline guards are real, deterministic hooks that move Correctness and Safety.

It is not ADOPT because it is effectively a solo project (2 contributors, 311 stars) with a huge idiosyncratic surface that substantially overlaps tools the user already runs (superpowers, compound-engineering, commit-commands), and its PreToolUse hooks (TDD gate, scope-ramp, opinionated commit-policy vows) carry real conflict risk against an existing hook stack including OMEGA. Installing the whole bundle would be redundant/noisy; cherry-picking is the only sensible path. Re-evaluate toward ADOPT if it grows a real contributor base / external validation, or if a single plugin proves its worth in a hands-on run. Verify hook interaction with the user's existing `~/.claude` setup before installing anything.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-night-market](https://github.com/athola/claude-night-market) | plugin | 23 modular Claude Code plugins (198 skills): per-plugin install for TDD hooks, git/PR, review, spec-driven dev, multi-LLM delegation | Setting up TDD enforcement, review, and workflow automation needs many separate tools, with opt-in install to limit footprint | superpowers, compound-engineering, commit-commands, oh-my-claudecode |
