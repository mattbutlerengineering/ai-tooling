# Evaluation: nanobot

**Repo:** [HKUDS/nanobot](https://github.com/HKUDS/nanobot)
**Stars:** 44,465 | **Last updated:** 2026-06-19 (pushed) | **License:** MIT | **Package:** PyPI `nanobot-ai` (Python ≥3.11)
**Dev loop stage:** Agent Orchestration (general-purpose own-it agent harness; tangential to the coding dev loop)
**Layer:** Harness (small readable core + bundled WebUI + chat-channel connectors)

---

## What it does

nanobot is an **ultra-lightweight, own-it personal AI agent** from HKUDS. The design goal is to keep the agent core small and readable while bundling the practical pieces for real long-running work: a packaged **WebUI workbench**, **chat-app channels** (Telegram, Discord, Slack, WeChat, Email, Matrix), **tools**, **memory**, **MCP**, **model routing with fallbacks**, **automation**, and **deployment**. It installs from PyPI (`nanobot-ai`) and emphasizes a no-terminal onboarding path for non-technical users.

Recent releases ("Workbench Release" v0.2.1) added Thought/response timelines, live file-edit activity, project workspaces, model/context controls, sustained-goal stability, CLI Apps + MCP extensions, idle-timeout handling for long Codex streams, and broader provider/channel support.

## How we tested it

**Source-grounded inspection — not installed, not run.** No package installed, no agent launched, no channel connected. Capabilities come from the repository README, release notes, and metadata, not observed behavior.

```bash
gh api repos/HKUDS/nanobot --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 44.5K, MIT
gh api repos/HKUDS/nanobot/readme --jq '.content' | base64 -d | head -70   # WebUI, channels, MCP, model routing, release timeline
```

## What worked

- **"Own it" philosophy with a small core.** A readable, self-hostable agent you fully control — versus a closed assistant — is a genuine value proposition, and HKUDS is a credible source (also behind CLI-Anything and gortex in this catalog).
- **Broad surface in one package.** WebUI workbench + memory + MCP + model routing/fallback + automation + multi-channel connectors is a lot of batteries-included capability for an MIT project.
- **MCP and model routing** make it interoperable rather than a walled garden; Langfuse hookup and OpenAI-compatible providers are first-class.
- **Very active and very popular** (~44K stars, daily pushes, frequent releases) with strong i18n and onboarding for non-technical users.

## What didn't work or surprised us

- **Personal-assistant focus, not a coding dev loop.** The headline use cases are chat-channel assistants (Telegram/WeChat/Feishu/Email) and long-running personal goals — it's a ChatGPT-style own-it assistant more than a Plan→Implement→Review coding harness. Codex stream support exists but coding isn't the center of gravity.
- **Overlaps existing catalog entries.** It sits squarely alongside CowAgent (self-evolving multi-channel super assistant) and nanoclaw (containerized agent with messaging-app integration) — same "own-it multi-channel agent" category, not a new one.
- **Batteries-included = broad dependency + config surface** (providers, channels, MCP, automation) to secure and maintain; the README leans on sponsored model providers.
- **Star count outpaces maturity.** Pre-1.0 (v0.2.x); capable but still stabilizing sustained goals and streaming per its own release notes.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | General agent harness; not focused on the correctness of shipped code. |
| Speed | neutral | Multi-channel personal automation; not a dev-loop throughput tool. |
| Maintainability | neutral / − | Small readable core is a plus; broad channel/provider/MCP surface is a maintenance cost. |
| Safety | neutral / − | Self-hostable and MIT (good), but chat-channel connectors + automation + model routing widen the trust/credential surface. |
| Cost Efficiency | neutral / + | Model routing with fallbacks can steer cheaper models; otherwise spend depends on usage. |

## Verdict

**CONDITIONAL** — nanobot is a popular, MIT-licensed, ultra-lightweight **own-it personal AI agent** with an impressive batteries-included surface (WebUI workbench, chat channels, memory, MCP, model routing, automation) from a credible lab. Adopt it if you want a small, self-hostable agent you fully control across messaging channels for long-running personal/enterprise workflows. For the AI-assisted **coding** dev loop specifically, it's tangential and overlaps CowAgent and nanoclaw — pick it for the readable own-it core and multi-channel reach, not as a coding harness. Pre-1.0, so pilot before depending on it.

Compared to neighbors: **CowAgent** is a self-evolving multi-channel "super assistant"; **nanoclaw** is a containerized agent runtime with WhatsApp/Telegram/Slack/Discord/Gmail. nanobot's distinguishing pitch is a **deliberately small, readable, truly-owned core** with a polished WebUI workbench and first-class MCP/model-routing.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [nanobot](https://github.com/HKUDS/nanobot) | harness | Ultra-lightweight own-it personal AI agent (MIT) — small readable core + WebUI workbench, chat-app channels (Telegram/Discord/Slack/WeChat/Email), tools, memory, MCP, model routing/fallback, automation | Want a small, self-hostable agent you fully control across chat channels rather than a closed assistant | CowAgent, nanoclaw |
