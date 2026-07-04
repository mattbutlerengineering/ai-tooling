# Evaluation: oh-my-claudecode

**Repo:** [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)
**Stars:** 36,643 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan + Implement + Verify + Review (a full-loop orchestration layer)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Teams-first multi-agent orchestration for Claude Code." The one-liner undersells the scope. OMC is a large, native Claude Code **plugin plus an npm CLI** (`oh-my-claude-sisyphus`, aliases `oh-my-claudecode` / `omc`) that wraps Claude Code with a full orchestration layer: 40 in-session skills, 19 specialized agents (architect, planner, executor, critic, verifier, security-reviewer, qa-tester, etc., each with model-tier variants), a bundled MCP bridge server, hooks for session events, a HUD statusline, model routing (Haiku/Sonnet/Opus by task), skill-learning/extraction, and notification/observability integrations.

Concretely, two surfaces exist. (1) **In-session skills** (`/team`, `/autopilot`, `/ralph`, `/ultrawork`, `/ultraqa`, `/deep-interview`, `/ask`, `/skillify`, etc.) installed via the Claude Code marketplace (`/plugin marketplace add` then `/plugin install oh-my-claudecode`). These run inside a normal Claude Code session and orchestrate Claude's *native* sub-agent/Task machinery — "teams" uses the experimental `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` flag and a staged pipeline (`team-plan → team-prd → team-exec → team-verify → team-fix` loop). (2) **Terminal CLI** (`omc ...`) installed via npm, which can additionally spawn *real tmux worker panes* running `claude`/`codex`/`gemini`/`grok`/`cursor-agent` CLIs as cross-model workers that die on completion. The "teams-first" framing means Team mode (coordinated Claude agents on a shared task list) is the canonical orchestration entrypoint as of v4.1.7, replacing the older `swarm` keyword.

So it is genuinely *both* a real Claude Code plugin (skills/agents/hooks/MCP via the marketplace) and an optional separate runtime (the npm CLI with tmux workers). It is not a standalone harness that replaces Claude Code — it sits on top of it.

## How we tested it

**Evidence:** REVIEW

Architecture/source review against the repo, not a hands-on installed run. A full OMC install mutates `~/.claude` (skills, agents, hooks, settings, an experimental teams flag, MCP bridge server, statusline), and the most differentiated modes (`omc team` tmux workers) require tmux plus optional Codex/Gemini/Grok CLIs and their paid plans — too invasive to install into this session's environment just to evaluate. Verdict rests on inspecting the plugin manifest, MCP bridge config, agent definitions, the documented mode mechanics, the committed benchmark scaffold, and the maturity signals below.

```bash
gh api repos/Yeachan-Heo/oh-my-claudecode --jq '{stars,license,description,created,pushed}'
gh api repos/Yeachan-Heo/oh-my-claudecode/readme --jq '.content' | base64 -d
gh api "repos/Yeachan-Heo/oh-my-claudecode/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/Yeachan-Heo/oh-my-claudecode/contents/.claude-plugin/plugin.json --jq '.content' | base64 -d
gh api repos/Yeachan-Heo/oh-my-claudecode/contents/.claude-plugin/marketplace.json --jq '.content' | base64 -d
gh api repos/Yeachan-Heo/oh-my-claudecode/contents/.mcp.json --jq '.content' | base64 -d
gh api repos/Yeachan-Heo/oh-my-claudecode/contents/benchmark/predictions/omc/stats.json --jq '.content' | base64 -d
gh api repos/Yeachan-Heo/oh-my-claudecode/releases --paginate --jq '.[].tag_name' | wc -l   # 233
gh api repos/Yeachan-Heo/oh-my-claudecode/contributors --paginate --jq '.[].login' | wc -l    # 110
curl -s https://api.npmjs.org/downloads/point/last-month/oh-my-claude-sisyphus                # ~30,891/mo
```

## What worked

- **Real, first-class Claude Code integration — not a separate harness.** `plugin.json` declares 40 skills, a `commands/` dir, and an MCP bridge server (`bridge/mcp-server.cjs`); `marketplace.json` ships a schema-valid marketplace manifest. Install is the native `/plugin marketplace add` + `/plugin install` flow. This is exactly the surface area the catalog rewards: it lives *inside* the dev loop.
- **Exceptional maturity for the catalog.** 36.6k stars, 233 tagged releases since 2026-01-09, ~3,294 commits, 110 contributors, ~31k npm downloads/month, active CI (auto-label, pr-check, upgrade-test, stale, release workflows), multilingual READMEs, a website, and a Discord. This is one of the most actively maintained tools in the entire catalog — the opposite of the single-author/days-old profile of architect-loop.
- **Coherent multi-mode model with sensible role separation.** The Team pipeline (plan → prd → exec → verify → fix-loop) plus dedicated `critic`/`verifier`/`qa-tester`/`security-reviewer` agents encode the "don't trust the builder's green" discipline that disciplined multi-agent setups need. `/ralph` (persist until verified) and `/ultraqa` (cycle until tests/lint/typecheck pass) target real correctness failure modes.
- **Cost-routing is built in.** Smart model routing (Haiku for simple, Opus for complex) and a model×agent compatibility matrix with premium/balanced/budget presets directly target Cost Efficiency — claimed 30–50% token savings.
- **Cross-model orchestration without a hard dependency.** Codex/Gemini/Grok/Cursor are *optional* advisors via `/ask` and `omc team N:codex` tmux panes; OMC works fully Claude-only. This is a softer, more flexible posture than architect-loop's hard Codex requirement.
- **Honest, detailed docs.** The README flags real footguns (npm `prebuild-install` deprecation warning from `better-sqlite3`, the `oh-my-claudecode` vs `oh-my-claude-sisyphus` package-name split, the experimental teams flag, tmux requirement, `/goal` evaluator caveats). Self-aware about its own deprecations and migration paths.

## What didn't work or surprised us

- **Enormous surface area = real adoption cost and lock-in.** 40 skills, 19 agents, hooks, an MCP bridge, a statusline, and dozens of `omc` subcommands. This mutates `~/.claude` substantially and introduces a heavy layer with its own vocabulary (ralph, ulw, ccg, ultragoal, skillify, deepinit…). The "zero learning curve / don't learn Claude Code" pitch is marketing — the README itself is thousands of words of modes and caveats. Overlapping modes (autopilot vs ralph vs ultrawork vs team vs pipeline vs goal) invite decision paralysis and ceremony.
- **The committed benchmark is not evidence of a win — and looks bad at face value.** `benchmark/predictions/omc/stats.json` shows 5/5 **failed**, 0% success, `total_tokens: 0`; vanilla shows 5/5 completed, 100%. These are clearly a SWE-bench *sanity-test scaffold* checkpoint (zero tokens, sub-5s durations — the OMC harness errored/timed out in setup, it didn't actually solve-and-lose), so they are inconclusive rather than damning. But there is **no published, credible benchmark demonstrating OMC beats vanilla Claude Code** on a coding task. The headline value claim is unverified.
- **The most differentiated runtime needs extra infrastructure.** `omc team` tmux workers require tmux (psmux on Windows) and, for cross-model panes, the Codex/Gemini/Grok CLIs and their paid plans ("3 Pro plans ~ $60/mo"). The Claude-only in-session path is the realistic default for most users, and that path is "Claude's native teams + a lot of prompt scaffolding."
- **Relies on an experimental Claude Code flag.** Team mode depends on `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`; if Anthropic changes that machinery, the canonical surface is exposed to churn (the project already churns fast — 233 releases in ~5 months, frequent breaking deprecations like `swarm` removal).
- **Single creator, broad delegation risk.** Despite 110 contributors, it is one creator/lead's vision with a very high release cadence; the breadth raises the odds of half-baked or rapidly-deprecated modes (the README already lists several legacy/deprecated shims).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (potential) | Staged Team pipeline with dedicated critic/verifier/qa-tester agents and `/ralph` + `/ultraqa` verify-fix loops target "ship unmergeable green" failures — but no benchmark confirms a real gain over vanilla |
| Speed | +/- | Automatic parallelization across agents/tmux workers can speed large parallelizable work; multi-stage pipelines and mode ceremony add overhead for small tasks |
| Maintainability | + | Skill-learning/`/skillify` extracts reusable patterns; analytics, HUD, and session/replay artifacts improve observability of agent runs |
| Safety | +/- | Dedicated security-reviewer/verifier agents and read-only verifier are positives; offset by a large hooks/MCP-bridge install that mutates `~/.claude` and forwards session events to external gateways (OpenClaw/Discord/Slack) when configured |
| Cost Efficiency | + | Built-in Haiku/Sonnet/Opus model routing with budget presets, claimed 30–50% token savings; cross-model advisors can spread load (though multi-agent fan-out can also raise spend) |

## Verdict

**CONDITIONAL**

Adopt when you (1) regularly do large, parallelizable, PR-sized work and want a turnkey multi-agent + model-routing layer rather than hand-rolling sub-agent prompts, and (2) are willing to take on a heavy, fast-moving plugin with its own vocabulary that substantially modifies `~/.claude`. Unlike most multi-agent tools in the catalog, this one is genuinely a native Claude Code plugin, exceptionally well-maintained (233 releases, 110 contributors, ~31k npm downloads/month), and integrates real cost-routing and verify-fix discipline — all of which can move quality signals inside the dev loop. It does *not* hard-depend on a second paid subscription (cross-model is optional), which makes it a softer commitment than architect-loop.

It is not an unconditional ADOPT because the headline "beats vanilla / zero learning curve" claims are unproven (the committed benchmark scaffold actually shows OMC failing the harness), the install footprint and overlapping-mode complexity are large, and the canonical Team surface rides an experimental Claude Code flag amid a very high breaking-change cadence. Solo users doing small/inline changes get mostly ceremony; teams doing heavy autonomous build loops get the most value. Re-evaluate to ADOPT if a credible vanilla-vs-OMC coding benchmark materializes and the mode surface consolidates.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) | harness | Teams-first multi-agent orchestration for Claude Code | Need team-oriented multi-agent coordination beyond solo use | claude-squad, agent-orchestrator |
