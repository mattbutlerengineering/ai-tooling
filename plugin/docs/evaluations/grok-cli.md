# Evaluation: grok-cli

**Repo:** [superagent-ai/grok-cli](https://github.com/superagent-ai/grok-cli)
**Stars:** 3,158 | **Last updated:** 2026-06-17 (pushed; created 2025-07-14) | **License:** MIT
**Dev loop stage:** Inner loop, all stages — it is a full terminal coding agent (Plan, Implement, Verify) with an outer-loop tilt via `--verify` smoke checks, scheduled overnight runs, and remote (Telegram) drive-by-phone.
**Layer:** Tooling (a standalone TypeScript/Bun coding-agent CLI you install and run; it owns the agent loop, tools, and TUI — not a plugin on top of another harness)

---

## What it does

grok-cli is a community-built, open-source terminal coding agent wired to **xAI's Grok API** (the README is explicit that it is *not* affiliated with or endorsed by xAI). It is the Grok-native peer of gemini-cli / qwen-code / opencode / goose: an interactive OpenTUI (React-in-terminal) agent loop with bash-first tools (`bash`, `file`, `grep`, `computer`, `schedule`), plus a headless `--prompt`/`-p` mode that emits a newline-delimited JSON event stream (`step_start`, `text`, `tool_use`, `step_finish`, `error`) for scripting and CI.

Beyond the table stakes, it leans hard into Grok-specific and autonomy features: live `search_x` and `search_web` tools; built-in `generate_image`/`generate_video` tools inside chat; **sub-agents on by default** (foreground `task` delegation for explore/general/computer, background read-only `delegate`); a built-in `computer` sub-agent backed by [agent-desktop](https://github.com/lahfir/agent-desktop) for macOS host desktop automation via accessibility snapshots and stable refs; `/verify` (sandbox build/test/boot + browser smoke checks with screenshots/video); a scheduler daemon (`grok daemon --background`) for recurring or one-shot headless runs; MCP server support (`/mcps`, `.grok/settings.json`); Agent Skills under `.agents/skills/<name>/SKILL.md`; persistent sessions (`--session latest`); a `--batch-api` mode that routes unattended runs through xAI's lower-cost Batch API; and **Telegram remote control** — pair once, then DM the agent from your phone while the CLI keeps running.

## How we tested it

**Source-grounded inspection — not installed, not run.** No `install.sh` was executed, no Grok API key was supplied, and no agent loop, sub-agent, scheduler, or Telegram bridge was exercised. There is no xAI API key in this environment, so every capability and pricing claim below is the authors' README/source framing, not measured behavior. The "lower-cost" and "fast" descriptions are theirs.

```bash
gh api repos/superagent-ai/grok-cli --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/superagent-ai/grok-cli/readme --jq '.content' | base64 -d | head -205
gh api "repos/superagent-ai/grok-cli/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # src/{agent,tools,mcp,telegram,daemon,audio}
gh api repos/superagent-ai/grok-cli/commits --jq 'length'     # 30 (page-1 cap; active)
gh api repos/superagent-ai/grok-cli/releases --jq 'length'    # 30 tagged releases (npm grok-dev)
gh api repos/superagent-ai/grok-cli --jq '.forks_count'       # 393 forks, ~20 contributors
```

## What worked

- **Genuinely full-featured for a 3.2K-star community CLI.** The source tree backs the README: real `src/agent/` loop with compaction, delegations, reasoning, sandbox, and vision-input modules — each with co-located `.test.ts` files. This is not a thin Grok wrapper; it is a coding agent with internal structure.
- **Strong release and test discipline.** 30 tagged releases, published to npm as `grok-dev`, with CI for typecheck and security, husky pre-commit, biome, and tests beside the code. Unusually well-maintained for the category.
- **Headless JSON event stream is the right CI primitive.** Semantic step-level events (`tool_use`, `step_finish`, `error`) make it scriptable and observable, not just a chat box — directly useful for the Verify/Ship stages.
- **Autonomy features are coherent, not bolted on.** Scheduler daemon + `--batch-api` + Telegram remote + `--verify` form a believable "run it overnight, ping me from my phone, prove it works" loop that goes past what most peers ship.
- **Sub-agents default-on and MCP/Skills support** mean it plugs into the same skill/MCP ecosystem as the rest of this catalog rather than being a Grok island.

## What didn't work or surprised us

- **Single-vendor lock-in.** The whole point is the Grok API — you need an x.ai key and you pay xAI. Unlike opencode/goose (model-agnostic) or gemini-cli (generous free tier), there is no escape hatch to another provider. Value is entirely contingent on Grok models being the ones you want.
- **Not affiliated with xAI.** Community-built against a public API and using a trademarked name — a governance/continuity risk if xAI changes API terms or objects. No first-party backing like gemini-cli (Google) or qwen-code (Alibaba).
- **`computer` sub-agent is macOS-only and intrusive.** Host desktop automation needs Accessibility permission for your terminal; agent-desktop targets macOS only. Powerful, but a real safety/blast-radius surface that runs *outside* any sandbox.
- **Bun + modern-terminal requirement narrows reach.** Interactive OpenTUI is recommended only on WezTerm/Alacritty/Ghostty/Kitty; install leans on Bun. Headless works anywhere, but the flagship UX has hard terminal expectations.
- **Breadth is also surface area.** Telegram bridge, scheduler daemon, media generation, computer use — a lot of moving parts and network reach for a young single-org project; more to trust, more to break.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Real agent loop with compaction/reasoning/delegation + `--verify` sandbox build/test/boot/browser smoke checks; correctness ceiling tracks Grok model quality, which we did not measure. |
| Speed | + | Default sub-agents parallelize work; headless `-p` and JSON stream script cleanly; OpenTUI is keyboard-driven. Offset by Grok API latency. |
| Maintainability | + | 30 releases, npm-published, CI (typecheck + security), husky/biome, tests co-located with source — strong repo hygiene. |
| Safety | − | macOS `computer` sub-agent automates the host desktop with Accessibility access (outside sandbox); Telegram bridge + scheduler daemon add network/background reach. `/verify` does sandbox its checks. |
| Cost Efficiency | + / − | `--batch-api` explicitly targets lower-cost unattended runs; but you are locked to paid xAI Grok billing with no free/local tier like gemini-cli's. |

## Verdict

**CONDITIONAL — adopt only if Grok is your model of record.** grok-cli is one of the more complete and better-maintained entries in the open coding-CLI category: a true agent loop, sub-agents on by default, MCP/Skills, headless JSON, a scheduler, `--verify`, and Telegram remote control, all with 30 releases and real tests. The disqualifier for general use is hard single-vendor lock-in plus the unaffiliated-community-vs-xAI governance risk — you are betting on xAI's API and Grok model quality, which this evaluation did not test.

Compared to neighbors: it is a direct peer of **gemini-cli**, **qwen-code**, **opencode**, and **goose** — all CONDITIONAL alternative coding CLIs. **gemini-cli** wins on first-party backing and a no-credit-card free tier; **opencode**/**goose** win on model-agnosticism; **qwen-code** matches it as a vendor-native CLI. grok-cli's differentiators are its autonomy stack (scheduler + batch + Telegram + `--verify`) and live X/web search — pick it specifically when you want a Grok-native agent and value drive-from-phone overnight runs, not as a default coding CLI.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [grok-cli](https://github.com/superagent-ai/grok-cli) | platform | Open-source Grok-native terminal coding agent — sub-agents on by default, X/web search, media gen, `--verify` sandbox checks, scheduler, and Telegram remote control | Want a feature-complete coding-agent CLI wired to xAI's Grok API, with overnight/headless autonomy and drive-from-phone control | gemini-cli, qwen-code, opencode, goose (alternative coding CLIs); DeepSeek-Reasonix, oh-my-pi |
