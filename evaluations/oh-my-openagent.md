# Evaluation: oh-my-openagent (OmO / formerly oh-my-opencode)

**Repo:** [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)
**Stars:** 62,845 | **Last updated:** 2026-06-19 | **License:** Sustainable Use License 1.0 (SUL-1.0 — source-available, non-commercial; NOT OSI open source)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan + Implement + Verify (a full inner-loop harness layer)
**Layer:** Tooling (an alternative agent harness, plus a Codex CLI plugin edition)

---

## What it does

Catalog one-liner: "Token-efficient agent harness optimized for complex codebases." That captures the marketing tag ("the coding agent for tokenmaxxers") but undersells and slightly mis-frames it. Ground truth: **OmO is a large, opinionated agent harness layer that runs on OpenCode (Ultimate edition) and OpenAI Codex CLI (Light edition) — not a Claude Code plugin.** It was originally named **oh-my-opencode** (the npm package and `omo` binary are still `oh-my-opencode`) and is mid-rename to oh-my-openagent as it refactors toward supporting multiple harnesses (OpenCode, Codex, Pi, and "Claude Code and others" per the ROADMAP — Claude Code support is aspirational/in-progress, not shipped).

Despite the name, it is **a different project by a different author** than `oh-my-claudecode` (Yeachan-Heo). OmO is by `code-yeongyu` / Sisyphus Labs. The two share a Greek-myth/"discipline agent" aesthetic and an `ultrawork`/`ralph-loop` vocabulary (both clearly inspired by the same Sisyphus framing — confusingly, oh-my-claudecode's npm package is literally `oh-my-claude-sisyphus`), but they are separate codebases targeting different harnesses (oh-my-claudecode wraps Claude Code; OmO wraps OpenCode/Codex).

Mechanically, the Ultimate edition (`bunx oh-my-openagent install`) registers a plugin in `opencode.json` and lands: 11 named agents (Sisyphus orchestrator, Hephaestus deep worker, Prometheus planner, Oracle, Librarian, Explore, Multimodal Looker, etc.), 54+ lifecycle hooks (61 with Team Mode), 5 built-in MCPs (Exa web search, Context7 docs, Grep.app GitHub search, git-bash, LSP), slash commands, Team Mode (lead + up to 8 parallel tmux-visualized members with `team_*` tools), `ultrawork`/`ulw-loop` persistence loops, and a hash-anchored ("Hashline") edit tool. Each agent is matched to a model by *category* (`quick`, `deep`, `ultrabrain`, `visual-engineering`) rather than picked manually, routing across Opus/GPT-5.5/Kimi-K2.6/GLM. The Light edition (`npx lazycodex-ai install`, also branded "LazyCodex") ships only the portable components into `~/.codex/` for Codex CLI: rules injection, comment-checker, git-bash, LSP, `ultrawork`, `ulw-loop`, start-work continuation, telemetry, and a few MCPs — no agent orchestration or `team_*` tools.

The "token-efficient" claim is grounded in concrete mechanisms, not just a slogan: (1) **skill-embedded MCPs** that spin up on demand and tear down after the task, so MCP tool schemas don't permanently occupy the context window; (2) `/init-deep`, which auto-generates **hierarchical `AGENTS.md`** files so agents pull only directory-scoped context; (3) **category-based model routing** so cheap models handle cheap work; (4) experimental **aggressive truncation** and auto-resume on context-limit; (5) **Hashline** edits (`LINE#ID` content-hash anchors) that cut wasted re-reads and failed-edit retries (README cites Grok Code Fast 1 going 6.7% → 68.3% edit-success purely from the edit-tool change).

## How we tested it

**Evidence:** REVIEW

**Method: inspected the repo, README, license, and source tree via the GitHub API. Did NOT install or run it.** This is a deliberate non-install evaluation. OmO is an *alternative harness*, not a Claude Code add-on: the Ultimate edition requires Bun + OpenCode and mutates `~/.config/opencode/`; the Light edition mutates `~/.codex/config.toml` and writes component CLIs into `~/.local/bin`. Both want multiple paid model subscriptions (the README's own "works well" baseline is ChatGPT $20 + Kimi $19 + GLM $10). Installing it would replace the front-end of this catalog's Claude Code dev loop rather than extend it, and would not run against the harness (Claude Code) this catalog standardizes on. So the verdict rests on the repo, license, maturity signals, and documented mechanics. No metrics below are invented; star/commit/download counts are from live API calls, and any benchmark figures are quoted as the project's own self-reported claims.

```bash
gh api repos/code-yeongyu/oh-my-openagent --jq '{stars:.stargazers_count,license:.license.spdx_id,description,created_at,pushed_at,language,topics}'
# 62,845 stars; NOASSERTION (SUL-1.0); TypeScript; created 2025-12-03; pushed 2026-06-19
gh api repos/code-yeongyu/oh-my-openagent/readme --jq '.content' | base64 -d        # full README
gh api repos/code-yeongyu/oh-my-openagent/contents/LICENSE.md --jq '.content' | base64 -d  # Sustainable Use License 1.0
gh api "repos/code-yeongyu/oh-my-openagent/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # .agents/.opencode/.codex/.claude/packages/...
gh api repos/code-yeongyu/oh-my-openagent/releases --paginate --jq '.[].tag_name' | wc -l   # 202
gh api repos/code-yeongyu/oh-my-openagent/contributors --paginate --jq '.[].login' | wc -l  # 277
gh api repos/code-yeongyu/oh-my-openagent/commits --paginate --jq '.[].sha' | wc -l         # 9,301
curl -s https://api.npmjs.org/downloads/point/last-month/oh-my-opencode   # 266,909/mo
curl -s https://api.npmjs.org/downloads/point/last-month/lazycodex-ai     # 21,019/mo
```

Reviewed: README (English), LICENSE.md, the recursive file tree (`.agents/skills/*`, `.opencode/`, `.codex/`, `.claude/`, `packages/`), the Highlights/Features/Configuration sections, and the maturity signals above.

## What worked

- **Exceptional maturity for the catalog.** 62.8k stars, 202 tagged releases since 2025-12-03, ~9,300 commits, 277 contributors, ~267k npm downloads/month on `oh-my-opencode` (+21k on `lazycodex-ai`). This is one of the highest-signal projects in the entire inventory — far past the abandonware/days-old risk most catalog entries carry.
- **The token-efficiency mechanisms are real and specific, not vapor.** Skill-embedded on-demand MCPs (avoid permanent schema bloat), hierarchical `AGENTS.md` via `/init-deep`, category→model routing, and Hashline content-hash edits each target a concrete cost/correctness failure mode. The Hashline approach (credited to oh-my-pi / "The Harness Problem") is a genuinely good idea: a stable verifiable line identifier that rejects stale edits before they corrupt a file.
- **Coherent role separation and verify discipline.** Dedicated planner (Prometheus, interview-mode), architecture/debug (Oracle), search (Librarian/Explore), plus Team Mode skills like `hyperplan` (5 hostile critics tear apart a plan pre-code) and `security-research` (hunters + PoC engineers). These encode the "don't trust the builder's green" pattern.
- **Provider-agnostic, anti-lock-in posture.** Works across Opus / GPT-5.5 / Kimi-K2.6 / GLM and explicitly aims to orchestrate cheap open models rather than a single premium provider — directly aligned with Cost Efficiency for users not on a single Claude subscription.
- **Honest, detailed docs about its own footprint.** README documents the package/binary rename split (`oh-my-opencode` vs `oh-my-openagent`), the `omo` bin-name collision warning (a *different* unrelated npm package owns `omo` — do not `npx omo`), default-on telemetry with opt-out env vars, and a full uninstall procedure. Self-aware about footguns.

## What didn't work or surprised us

- **It is NOT a Claude Code tool — the catalog framing is the central caveat.** OmO runs on OpenCode (Ultimate) and Codex CLI (Light). "Claude Code Compatibility" means it *consumes* the Claude Code config format (hooks, commands, skills, MCPs work *inside OmO*); it does **not** mean you install OmO into Claude Code. There is no Claude Code plugin/skill/MCP to adopt into an existing Claude Code session today. For this catalog's standardized Claude Code dev loop, adopting OmO means *switching harnesses*, which is a large commitment, not an enhancement.
- **The license is not open source.** SUL-1.0 (Sustainable Use License) restricts use to "internal business purposes or non-commercial or personal use" and bans paid redistribution. That is a meaningful constraint vs. the MIT/Apache tools in the catalog — fine for an individual dev, a real legal review item for a company building a commercial product on top of it.
- **Enormous surface area + heavy install + fast churn.** 11 agents, 54-61 hooks, 5 MCPs, Team Mode, tmux visualization, its own vocabulary (ultrawork, ulw-loop, ralph-loop, hyperplan, init-deep, IntentGate, Hashline). 202 releases and 9.3k commits in ~6 months signals a very high breaking-change cadence and the same single-creator-vision concentration risk as oh-my-claudecode.
- **Mid-rename / mid-refactor instability.** The project is simultaneously renaming (opencode → openagent) and doing a "multi-harness Agent OS refactor." Package names, plugin entry names, and config basenames all have legacy/new dual forms with compatibility warnings. Anyone adopting now rides through churn.
- **The headline win claims are self-reported and provider-shifting.** "Kimi K2.6 + GPT-5.5 already beats vanilla Claude Code" and the Grok edit-success jump are the project's own claims/quotes, not independently reproduced here. Marketing leans heavily on a confrontational "Anthropic blocked OpenCode because of us" narrative and X testimonials.
- **Default-on telemetry.** Anonymous daily-active pings to PostHog are on by default (opt-out via `OMO_DISABLE_POSTHOG=1` etc.). SHA256-hashed and minimal, but worth knowing.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (potential) | Hashline content-hash edits reject stale edits before corruption; Prometheus planning + hyperplan hostile critics + dedicated verify/security agents target "ship unmergeable green" — but the win is self-reported, not reproduced here |
| Speed | +/- | Parallel background agents / Team Mode can speed large parallelizable work; multi-agent + multi-stage + tmux ceremony adds overhead for small tasks |
| Maintainability | +/- (and not for *this* loop) | Hierarchical AGENTS.md and comment-checker improve agent navigation/output, but it replaces the harness rather than integrating into the Claude Code dev loop; SUL license + fast churn add maintenance/legal friction |
| Safety | +/- | Dedicated security-research agents and scoped skill permissions are positives; offset by a large hooks/MCP install that mutates harness config and default-on telemetry |
| Cost Efficiency | + | The core pitch: skill-embedded on-demand MCPs, hierarchical context, category model-routing to cheap open models, aggressive truncation — all aimed squarely at token spend across non-premium providers |

## Verdict

**SKIP** (for *this* catalog's Claude Code dev loop) — but **steal the ideas**, and re-evaluate if Claude Code support actually ships.

OmO is an impressive, exceptionally mature project (62.8k stars, ~267k npm downloads/month, 277 contributors) with genuinely good token-efficiency engineering — Hashline edits, skill-embedded on-demand MCPs, hierarchical `AGENTS.md`, and category-based model routing are all worth understanding and partially borrowing. But for a catalog standardized on Claude Code, it is a SKIP as an *installable artifact*: it is an alternative harness running on OpenCode / Codex CLI, not a Claude Code plugin. "Claude Code Compatible" means OmO ingests the Claude Code config format, not that you bolt OmO onto Claude Code — adopting it means switching front-ends, which doesn't extend the existing loop. The SUL-1.0 (non-commercial / no paid redistribution) license, the heavy multi-subscription install footprint, default-on telemetry, and the in-flight rename/refactor churn all reinforce holding off.

**Differentiation:** vs. `oh-my-claudecode` (the deceptively similarly-named, separate-author CONDITIONAL entry) — OmO targets OpenCode/Codex while oh-my-claudecode is a *real* Claude Code plugin you install via the marketplace; if you must pick one for a Claude Code stack, oh-my-claudecode is the integrated choice and OmO is not. vs. `humanlayer` (SKIP) — both are alternative harnesses you'd switch *to* rather than add; humanlayer's transferable value was its `.claude/commands` prompt library, whereas OmO's transferable value is its harness-engineering ideas (Hashline, on-demand MCPs, hierarchical context). vs. `superpowers` — superpowers is a portable Claude Code skill collection that lives inside the loop; OmO replaces the loop.

Re-evaluate to CONDITIONAL/ADOPT if (a) the ROADMAP's Claude Code harness support ships as an actual installable plugin, or (b) the user's stack is OpenCode/Codex rather than Claude Code (in which case OmO becomes a strong CONDITIONAL on its own terms), and the licensing fits their commercial posture.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) | harness | Token-efficient multi-agent harness for OpenCode/Codex CLI (formerly oh-my-opencode); not a Claude Code plugin | Want a token-frugal, provider-agnostic agent harness for large codebases without single-provider lock-in | oh-my-claudecode, humanlayer, superpowers |
