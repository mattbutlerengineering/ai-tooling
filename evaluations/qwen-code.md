# Evaluation: Qwen Code

**Repo:** [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code)
**Stars:** 25,365 (2,536 forks) | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan + Implement + Verify (a full inner-loop terminal agent — but a *replacement* front-end, not a Claude Code add-on)
**Layer:** Tooling (an alternative agent harness / standalone CLI), backed by Infrastructure (Alibaba's Qwen models)

---

## What it does

Catalog one-liner: "Alibaba's open-source terminal coding agent powered by Qwen." That is accurate as far as it goes, but understates the scope. Ground truth: **Qwen Code is a standalone, multi-provider terminal coding agent — a fork of Google's Gemini CLI (v0.8.2) that diverged at Qwen Code v0.1 into an independently developed, multi-protocol agent framework.** It is its own binary (`qwen`) that you install and run *instead of* `claude`, not a Claude Code plugin, skill, or MCP you bolt onto an existing Claude Code session.

Mechanically, you get a terminal TUI pair-programmer with: interactive mode (`qwen`), headless one-shot (`qwen -p "..."`) for CI/CD, a daemon/ACP server mode (`qwen serve`, multi-client shared agent over HTTP+SSE, experimental), and IM-bot channels (`qwen channel` → Telegram/DingTalk/WeChat/Feishu). It ships SubAgents, Agent Teams, Auto-Memory, Auto-Skills, Hooks, MCP client support, Plan Mode, LSP integration, sandbox, git-worktree support, computer-use/desktop automation, IDE plugins (VS Code, JetBrains, Zed), a Desktop GUI app, and SDKs in TypeScript, Python, and Java. Skills live in `.qwen/skills/` (built-ins include `bugfix`, `codegraph`, `create-issue`, and a set of `agent-reproduce-*` skills the project uses to reverse-engineer and match other agents' behavior). Crucially, it is **multi-protocol**: it speaks the OpenAI, Anthropic, Gemini, and Qwen APIs and works with any third-party provider or local model (Ollama / vLLM), switchable at runtime via `/auth`. So while it is "powered by Qwen," it is not locked to Qwen models.

The README is explicit that it is chasing Claude Code feature parity ("If you know Claude Code, you already know Qwen Code") and links a self-authored comparison report. Its differentiators over Claude Code per its own table: open-source model *and* framework, multi-protocol provider support, an "Agent Arena" (multi-model head-to-head on the same task), daemon mode, and IM channels.

**One genuinely relevant interop angle — and the reason this is not a flat SKIP like claurst.** The ecosystem section ships **"Qwen Code Claw"** ([openclaw/acpx](https://github.com/openclaw/acpx)): a skill that lets *other agents (Claude, Codex, etc.) delegate coding tasks to Qwen Code via ACP*. You paste a prompt that fetches `.qwen/skills/qwen-code-claw/SKILL.md`, and your Claude Code session can then offload coding work to a Qwen-backed subagent through `acpx`. That is an *into-Claude-Code* usage pattern — Qwen Code as a cheaper/secondary executor driven from Claude Code — distinct from "run it instead of Claude Code."

## How we tested it

**Evidence:** REVIEW

**Method: inspected the repo, README, recursive file tree, license, release history, and maturity signals via the GitHub API and npm registry API. Did NOT install or run it.** This is a deliberate non-install evaluation, consistent with the `claurst` and `oh-my-openagent` evaluations. Qwen Code is an *alternative harness* — the primary install (`curl ... | bash`, `npm i -g @qwen-code/qwen-code`, or `brew install qwen-code`) gives you a separate coding agent that replaces the front-end of this catalog's standardized Claude Code dev loop rather than extending it. Running it interactively would not exercise the harness (Claude Code) this catalog standardizes on, and it wants its own provider/API-key config via `/auth`. So the verdict rests on the repo, the documented mechanics, the multi-protocol/ACP interop story, the license, and the maturity signals below. No metrics are invented; star/fork/release/contributor counts are from live API calls and npm download numbers are from the npm registry API.

```bash
gh api repos/QwenLM/qwen-code --jq '{stars,forks,license:.license.spdx_id,description,created_at,pushed_at}'
# 25,365 stars; 2,536 forks; Apache-2.0; created 2025-06-26; pushed 2026-06-19
gh api repos/QwenLM/qwen-code/readme --jq '.content' | base64 -d                 # full README
gh api "repos/QwenLM/qwen-code/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # .qwen/skills/*, packages/sdk-{typescript,python,java}, docs/, CLAUDE.md, AGENTS.md
gh api repos/QwenLM/qwen-code/contents --jq '.[].name'                           # top-level layout
gh api repos/QwenLM/qwen-code/releases --paginate --jq '.[].tag_name' | wc -l    # 493
gh api repos/QwenLM/qwen-code/releases/latest --jq '{tag,published_at}'          # v0.18.3, 2026-06-17
gh api repos/QwenLM/qwen-code/contributors --paginate --jq '.[].login' | wc -l   # 416
curl -s https://api.npmjs.org/downloads/point/last-month/@qwen-code/qwen-code    # 442,814/mo
```

Reviewed: README (English), the recursive file tree (`.qwen/skills/*` including `qwen-code-claw`, `codegraph`, `bugfix`, `agent-reproduce-*`; `packages/sdk-{typescript,python,java}`; `CLAUDE.md`; `AGENTS.md`; `docs/`, `docs-site/`), the capabilities/parity table, the ecosystem section (Qwen Code Claw ACP delegation, AionUi, desktop apps), the Gemini CLI fork provenance acknowledgment, and the maturity signals above.

## What worked

- **Very high maturity and corporate backing.** 25.4k stars, 2.5k forks, 493 tagged releases (active nightly + preview cadence), 416 contributors, and ~443k npm downloads/month — one of the most-adopted standalone agents in the catalog, ahead of claurst (~626/mo) and in the same league as oh-my-openagent (~267k/mo). Apache-2.0 (permissive, commercially clean) and maintained by Alibaba's Qwen team, which removes the abandonware/single-hobbyist concentration risk that dogs most alternative-agent entries.
- **Multi-protocol and no model lock-in.** Despite the "powered by Qwen" framing, it speaks OpenAI/Anthropic/Gemini/Qwen and any third-party or local model (Ollama/vLLM), switchable at runtime. The framework is decoupled from the model — you can run it against the same Anthropic models Claude Code uses, or against cheap/local models.
- **A real into-Claude-Code interop path (Qwen Code Claw / acpx).** The ACP delegation skill lets a Claude Code session offload coding tasks to a Qwen-backed executor. This is the one usage pattern that *extends* the Claude Code loop rather than replacing it, and it is the basis for the CONDITIONAL rather than a flat SKIP.
- **Broad surface and clean engineering.** Headless mode, ACP daemon, three official SDKs, IDE plugins, sandbox, git worktrees, and a committed skills directory (`codegraph`, `bugfix`, `agent-reproduce-*`). The `agent-reproduce-*` skills (trace capture, normalization, alignment) are an interesting reference artifact in their own right — tooling for reverse-engineering and matching another agent's behavior.
- **Free-tier on-ramp.** Qwen provides an OAuth free tier for its own models, lowering the barrier to trying agentic coding without a paid key — relevant for cost-sensitive or evaluation use.

## What didn't work or surprised us

- **It is primarily NOT a Claude Code tool — this is the central caveat.** The default, documented mode is a standalone agent you run *instead of* Claude Code. Adopting it as your harness means switching front-ends (runtime, config, `/auth`, skills format), which is a large commitment, not an enhancement to the existing loop. This is the same disqualifier that placed claurst and oh-my-openagent at SKIP for the primary use case.
- **Feature parity is self-asserted, not independently verified.** The "Qwen Code vs Claude Code" capability table and the linked "improvement report" are authored by the project / a community contributor, not an independent benchmark. The README even notes Qwen Code uses itself (its own agent + models) to file issues and PRs — impressive dogfooding, but the parity and quality claims are the project's own.
- **Provenance is a Gemini CLI fork.** It began as a fork of Google Gemini CLI v0.8.2 and stopped syncing at v0.1. Apache-2.0 keeps this clean legally, but it means a lot of the harness lineage is inherited Gemini-CLI code rather than ground-up design, and divergence from upstream means it carries its own maintenance burden.
- **Large, fast-moving surface.** 493 releases with active nightly/preview channels signals a high change cadence; SubAgents, Agent Teams, daemon mode, computer-use, and IM channels are a wide footprint to track, and `qwen serve` (ACP daemon) is explicitly experimental.
- **Install path and provider data flow.** Primary install is `curl | bash` from an Alibaba OSS bucket. Default model routing sends code/context to Alibaba's Qwen API unless you reconfigure the provider — a data-residency/governance consideration for some orgs (mitigable via local models or another provider, but worth flagging).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral / unknown (for this loop) | Claims Claude Code parity via self-authored comparison; no independent benchmark shows it matches Claude Code on real tasks. As a Claw-delegated executor, correctness depends on the chosen model |
| Speed | + (potential) | Headless `-p`, ACP daemon, and Agent Teams enable parallel/scripted work; via Claw, can offload bulk coding off the main Claude Code session — but unverified here |
| Maintainability | - (as a harness) / neutral (as Claw executor) | Adopting it as the harness replaces the Claude Code front-end (separate runtime/config to maintain); used only via Claw/acpx it adds an external dependency but does not displace the loop |
| Safety | +/- | Apache-2.0 + sandbox + plan mode are positives; offset by `curl \| bash` install and default routing of code to Alibaba's Qwen API unless reconfigured |
| Cost Efficiency | + | Multi-protocol routing to cheap/local models, a Qwen free OAuth tier, and Claw-based delegation (run cheap models for grunt work, keep Claude for orchestration) all target token spend — the strongest fit |

## Verdict

**CONDITIONAL** — SKIP as a *replacement* for the Claude Code harness, but a legitimate **CONDITIONAL** for two narrow uses: (1) as a Claw/acpx-delegated secondary executor driven *from* Claude Code, and (2) for users whose stack is Qwen-centric or who want an open, multi-provider, self-hostable agent.

Qwen Code is a high-maturity, Apache-2.0, Alibaba-backed standalone terminal agent (25.4k stars, ~443k npm downloads/month, 493 releases) — far past the maturity bar that placed claurst and oh-my-openagent at SKIP on quality grounds. For a catalog standardized on the Claude Code dev loop, its *default* mode (a standalone agent you run instead of `claude`) is still the SKIP category: adopting it as your harness means switching front-ends, not extending the loop. What lifts it to CONDITIONAL rather than a flat SKIP is the **Qwen Code Claw / acpx ACP delegation path**, which lets a Claude Code session offload coding tasks to a Qwen-backed executor — a genuine *into-Claude-Code* pattern aimed squarely at Cost Efficiency (run cheap/local models for grunt work, keep Claude for orchestration). Use it when (a) you want a cheaper delegated executor under Claude Code via Claw, or (b) your stack is Qwen-centric / you want an open, provider-agnostic, self-hostable agent — in which case it competes strongly on its own terms with opencode/oh-my-pi/claurst and is arguably the most mature of that cluster.

**Differentiation from the standalone-agent cluster:**
- vs. **claurst** (SKIP) — same category (Claude Code-alternative terminal agent), but Qwen Code is vastly more mature (Apache-2.0 vs GPL-3.0; ~443k vs ~626 npm downloads/month; corporate-backed vs single-author beta) and, unlike claurst, ships a documented into-Claude-Code delegation path (Claw). That interop is exactly why this is CONDITIONAL and claurst is SKIP.
- vs. **oh-my-openagent** (SKIP) — OmO is a harness layer on OpenCode/Codex; Qwen Code is a self-contained agent with its own models and an ACP delegation skill. OmO's transferable value is harness-engineering ideas; Qwen Code's is a runnable, model-bundled, delegatable executor.
- vs. **opencode / oh-my-pi / goose** (the standalone-alternative cluster) — Qwen Code is the same *kind* of thing; its distinguishing angles are first-party Qwen model bundling + free tier, multi-protocol runtime switching, and the Claw delegation path. On adoption/maturity it leads much of this cluster.
- vs. **oh-my-claudecode** (CONDITIONAL) — sharp contrast in *kind*: oh-my-claudecode is a real Claude Code plugin that lives inside the loop; Qwen Code is a separate agent that only touches the loop via Claw delegation. If you must pick one to install *into* Claude Code, oh-my-claudecode; if you want a cheap delegated executor or a Qwen-stack agent, Qwen Code.

Re-evaluate to ADOPT (within its niche) if (a) the Claw/acpx delegation pattern proves reliable and economical in hands-on use, or (b) the user's primary stack is Qwen — and after independent (non-self-authored) evidence of Claude Code parity emerges.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Qwen Code](https://github.com/QwenLM/qwen-code) | platform | Alibaba's open-source, multi-protocol terminal coding agent (Gemini-CLI fork) powered by Qwen; standalone, with ACP delegation from Claude Code via "Qwen Code Claw" | Want an open, provider-agnostic, self-hostable terminal coding agent — or a cheap Qwen-backed executor to delegate coding tasks to from Claude Code | claurst, opencode, oh-my-pi, goose, oh-my-openagent |
