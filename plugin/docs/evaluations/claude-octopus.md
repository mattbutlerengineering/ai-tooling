# Evaluation: claude-octopus

**Repo:** [nyldn/claude-octopus](https://github.com/nyldn/claude-octopus)
**Stars:** 3,646 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Plan + Review (primary) — also spans Implement/Verify/Ship via lifecycle commands
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Run up to 8 AI models in parallel on research, design, or code to surface blindspots before shipping." The repo as of v9.45 actually advertises *nine* providers — Codex (GPT-5.4), Gemini, Antigravity CLI (`agy`), GitHub Copilot, Qwen, Ollama, Perplexity, OpenRouter, and OpenCode — orchestrated alongside Claude, which is the only required one. The pitch is blindspot coverage: every model has gaps, so put several on the same task and gate on agreement before shipping.

Mechanically it is a native Claude Code **plugin** installed from the `nyldn-plugins` marketplace (`claude plugin marketplace add` → `claude plugin install octo@nyldn-plugins` → `/octo:setup`). It ships 49 slash commands (`/octo:*`), 32 personas (agent definitions), and 54 skills, plus lifecycle hooks (session start/end, prompt submit, tool use, compaction, plan mode, worktrees, etc.) declared in `.claude-plugin/hooks.json`. The differentiated multi-model surface is not the four-phase lifecycle commands (`/octo:embrace` = Discover→Define→Develop→Deliver) but the *cross-checking* commands: `/octo:debate` (structured provider debate with consensus), `/octo:council` (3/5/7-persona deliberation with goal modes advice/decision/plan/implement/review, adversarial/red-team styles, quorum + critical-veto gates, budget caps), `/octo:review` (multi-LLM code review with inline PR comments), and `/octo:research` (attributed multi-provider fan-out).

The consensus is not theater-by-prompt. `council.md` mandates that the command shell out to `"$CLAUDE_PLUGIN_ROOT/scripts/orchestrate.sh" council $ARGUMENTS` — the real runner that dispatches to actual provider CLIs/APIs — and explicitly **prohibits** the model from role-playing multiple personas inside one Claude context unless the user passes `--simulate`/`--single-model` (in which case the output must be labeled "single-model simulation"). A documented **75% consensus gate** flags disagreement before work proceeds; an "agent status ledger" (`octopus agent-summary`) reports which providers actually contributed, ran degraded, or failed. Providers authenticate via existing subscriptions/OAuth (Codex via ChatGPT sub, Gemini via Google account, Copilot via GH sub) or per-token API keys; Ollama is local/free.

## How we tested it

Source-and-docs review against the GitHub repo — **not** a hands-on installed run, and no models were actually dispatched. Installing octo mutates `~/.claude` (49 commands, 32 agents, 54 skills, a broad set of lifecycle hooks) and the differentiated multi-model path requires multiple external provider CLIs and their paid subscriptions/API keys to exercise honestly; running it just to evaluate would be both invasive and costly. No consensus results, provider outputs, or benchmark numbers below are invented — the verdict rests on the manifest, the command runner contract, the documented gate mechanics, and the maturity signals. I read the README, `.claude-plugin/plugin.json`, `.claude/commands/council.md`, and the file tree, and queried repo metadata.

```bash
gh api repos/nyldn/claude-octopus --jq '{stars:.stargazers_count,license:.license.spdx_id,description:.description,pushed_at,created_at,forks:.forks_count,open_issues:.open_issues_count}'
gh api repos/nyldn/claude-octopus/readme --jq '.content' | base64 -d
gh api "repos/nyldn/claude-octopus/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/nyldn/claude-octopus/contents/.claude-plugin/plugin.json --jq '.content' | base64 -d
gh api repos/nyldn/claude-octopus/contents/.claude/commands/council.md --jq '.content' | base64 -d
gh api repos/nyldn/claude-octopus/releases --paginate --jq '.[].tag_name' | wc -l   # 242
gh api repos/nyldn/claude-octopus/contributors --paginate --jq '.[].login' | wc -l   # 15
```

## What worked

- **Real multi-model dispatch, not prompted persona role-play.** The council command's "MANDATORY COMPLIANCE" block forces a shell runner (`orchestrate.sh`) and *prohibits* single-model simulation unless explicitly requested and labeled. This is the single most important integrity detail: the blindspot claim depends on genuinely independent models, and the design enforces it rather than faking it with one Claude wearing hats.
- **Genuine consensus/veto machinery.** Documented 75% consensus gate, quorum + critical-veto gates in council mode, and an agent status ledger (`octopus agent-summary`) showing which providers contributed vs. ran degraded vs. failed. Disagreement is surfaced, not averaged away — which is the actual value of cross-model review.
- **Native Claude Code plugin with the rewarded surface area.** Marketplace install, 49 `/octo:*` commands, 32 personas, 54 skills, lifecycle hooks. It lives *inside* the dev loop (Plan/Review especially), which is exactly what this catalog credits.
- **Cost is treated as a first-class constraint.** `--max-cost <usd>`, cost preflight, a `/octo:costs` command, provider-aware prompt preflight to avoid silent oversize failures, `--depth quick|standard|deep`, `--members 3|5|7`, and per-session provider disable (`/octo:model-config disable codex --session`). Five providers cost nothing extra when you already hold the subscriptions; Ollama is free/local.
- **Strong maintenance signals.** v9.45.0, 242 tagged releases, 117 test suites passing, active CI, tracks Claude Code feature flags through v2.1.157 (Opus 4.8). Honest "Trust, Safety, and Limits" section documents hook scope, data locations (`~/.claude-octopus/`, `.octo/`), provider transparency markers, and clean uninstall.
- **Claude-only graceful degradation.** Zero external providers required to install; multi-AI features simply activate as providers are auto-detected. Workflows continue if a provider times out. This makes the *commitment* soft even though the *value* needs providers.

## What didn't work or surprised us

- **The headline value (multi-model blindspot catching) requires multiple paid subscriptions or API keys to actually realize.** With Claude only, you get personas/workflows/skills — i.e., a heavier prompt-scaffolding layer, *not* the cross-model consensus that justifies the tool. To get the differentiated benefit you must wire up Codex/Gemini/etc., each of which either consumes a subscription or bills per token. Running 5–9 models on every task is the explicit design, and that is a real, recurring cost multiplier the catalog one-liner ("vs Cost which it clearly raises") correctly flags.
- **No published benchmark that cross-model consensus beats single-model review.** "117 suites passing" tests the plugin's own code, not whether a 75% gate across 9 models catches more real bugs than one good Claude pass. The blindspot premise is plausible and the plumbing is honest, but its quality payoff is asserted, not measured.
- **Enormous, fast-moving surface.** 49 commands, 32 personas, 54 skills, broad lifecycle hooks, a smart router, freeze/discipline modes, a reaction engine, an OpenClaw/MCP bridge — plus 242 releases since mid-January (~5 months). That is a large install footprint with its own vocabulary and a high breaking-change cadence; overlapping entrypoints (embrace vs factory vs council vs debate vs auto) invite decision paralysis.
- **Effectively single-author.** Despite the breadth, only ~15 contributors; this is one maintainer's rapidly-iterating vision. Bus-factor and half-baked-mode risk are real at this velocity.
- **The "9 providers / consensus gate" framing can become expensive ceremony for small tasks.** For a one-line fix, fanning out to a council is pure overhead. The tool's own docs steer you to Claude-native `/init`/`/review`/`/security-review` first and Octopus only "for escalation" — an honest admission that most tasks don't need it.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (potential) | Real independent multi-model dispatch + 75% consensus/critical-veto gates + adversarial/red-team council styles target blindspots a single model misses; unproven by benchmark but mechanically sound (no simulation faking) |
| Speed | +/- | Parallel provider fan-out for research/review can be faster than serial human cross-checking; multi-model councils and four-phase lifecycle add latency and ceremony for small tasks |
| Maintainability | + | Inline multi-LLM PR review, two-stage review, discipline gates, and persisted run artifacts/ledgers improve review rigor and traceability |
| Safety | +/- | Dedicated security-auditor persona, `/octo:security` OWASP scans, adversarial review, transparent provider markers and clean uninstall are positives; offset by broad lifecycle-hook install and routing prompts/code to multiple external providers (data egress) |
| Cost Efficiency | - | Running up to 9 models per task is a clear cost multiplier; mitigated (not eliminated) by OAuth reuse, free Ollama, `--max-cost`, cost preflight, depth/member caps |

## Verdict

**CONDITIONAL**

Adopt when (1) you already have several model subscriptions (ChatGPT/Codex, Gemini, Copilot) so the marginal cost of fanning out is low, and (2) the work is genuinely high-stakes — architecture decisions, security-sensitive review, pre-merge validation, or research — where a single model's blindspot is expensive and cross-model disagreement is worth paying for. For that profile, octopus is the rare multi-model tool that implements the idea honestly: it dispatches real independent providers and enforces consensus/veto gates rather than role-playing personas inside one context, and it is a well-maintained native Claude Code plugin that lives in the Plan/Review stages this catalog rewards.

It is not an unconditional ADOPT because the differentiating value is unproven by benchmark, gated behind multiple paid providers, and carries a large fast-moving install footprint from an essentially single maintainer — and for routine work it is expensive ceremony the tool itself tells you to skip in favor of Claude-native review.

Differentiation from overlaps: **PR-Agent** does single-model PR review bound to git platforms; octopus's edge is *cross-model* adversarial review with consensus gating, plus full-lifecycle and research commands. It overlaps in spirit with **oh-my-claudecode** (also a heavy native CC orchestration plugin), but OMC is teams-of-Claude orchestration with cost-routing where octopus's thesis is specifically *multiple independent vendors checking each other*.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-octopus](https://github.com/nyldn/claude-octopus) | plugin | Run up to 8 AI models in parallel on research, design, or code to surface blindspots before shipping (3.6K stars) | Single-model review misses blindspots; want cross-model consensus before merge | PR-Agent, code-review-graph |
