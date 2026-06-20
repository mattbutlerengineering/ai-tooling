# Evaluation: Phantom

**Repo:** [ghostwright/phantom](https://github.com/ghostwright/phantom)
**Stars:** 1,432 | **Last updated:** 2026-06-16 (pushed; created 2026-03-26) | **License:** Apache-2.0
**Dev loop stage:** Cross-cutting / autonomous operations (a persistent self-directed agent, not a single dev-loop stage)
**Layer:** Infrastructure (deployable TypeScript agent platform on the Claude Agent SDK; Docker)

---

## What it does

Phantom is **"an AI co-worker with its own computer."** Built on the Claude Agent SDK, it's a persistent, self-directed agent that runs on a dedicated machine of its own — it installs software, spins up databases, builds dashboards, keeps long-term memory, **creates its own tools**, and builds infrastructure **"without asking for permission."** The thesis: today's agents are disposable (every session is day one); give the agent its own computer and persistent memory and it compounds over time. Your laptop stays yours; the agent's workspace is its own.

It's not a chatbot — it runs on **Slack, Telegram, Email, Webhook, and a web chat at `/chat`**, has its own **email address** (Resend), and can **extend itself with channels it didn't ship with** (the README describes a Phantom building its own Discord integration on request, then going live). Memory is backed by **Qdrant** with an Ollama-pulled embedding model. It has a **self-evolution pipeline** with "evolution judges," secure credential collection (magic-link token submission), and the ability to register APIs it builds as MCP tools for future sessions and other agents.

**Bring-your-own-model**: seven providers via one YAML block — Anthropic (default), Z.AI (GLM, ~15× cheaper than Opus), OpenRouter, Ollama, vLLM, LiteLLM, or any Anthropic-Messages-compatible endpoint. Quick start is `docker compose up` with `ANTHROPIC_API_KEY` + Slack tokens.

## How we tested it

**Source-grounded inspection — not installed, not deployed.** No container run, no Phantom provisioned. Claims (including the "production Phantom built a 28.7M-row ClickHouse analytics stack unprompted" anecdotes) come from the repository's own README/marketing — they are **not independently verified**.

```bash
gh api repos/ghostwright/phantom --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/ghostwright/phantom/readme --jq '.content' | base64 -d   # idea, channels, BYO-model, Docker socket note
```

## What worked

- **Persistent-agent-with-its-own-computer is a genuinely different framing.** Separating the agent's workspace from the user's machine, plus durable memory and self-built tools, is a coherent answer to "every session is day one" — and isolating it from your laptop is the right instinct.
- **Multi-channel + own identity is unusual and practical.** Slack/Telegram/Email/Webhook/web-chat with its own email address makes it a real "co-worker" surface rather than a CLI; self-extending channels (built its own Discord) is a striking capability if it holds up.
- **Strong BYO-model story.** Seven providers via two lines of YAML, with the Z.AI ~15×-cheaper option, gives real cost control; the same tools/memory/evolution pipeline run regardless of brain.
- **Self-evolution with judges + registering built APIs as MCP tools** is a concrete take on compounding capability over time.
- **Apache-2.0, Docker-first**, BYO-model — permissively licensed and not vendor-locked.

## What didn't work or surprised us

- **🚩 Large, autonomous safety surface — the central caveat.** An agent that builds infrastructure "without asking permission," collects credentials, has its own email, and **mounts the Docker socket** (`/var/run/docker.sock`) to spawn sibling containers is effectively root-equivalent on its host. This is powerful but a serious blast radius; it must run on isolated, throwaway infrastructure with scoped credentials — never near anything you can't afford it to touch.
- **Unverified, marketing-heavy claims.** The headline anecdotes (28.7M-row dataset, self-built Discord/monitoring) are self-reported with no reproducible benchmark; impressive if true, but taken on faith here.
- **Operational weight + ongoing cost.** A persistent always-on agent with its own VM, Qdrant, Ollama, and channels is real infrastructure to stand up and pay for continuously — not a drop-in dev-loop tool.
- **No releases; young.** 0 tagged releases, created late March 2026 — early-stage stability for something you'd grant this much autonomy.
- **Tangential to the inner dev loop.** It's an autonomous-operations co-worker, not a code-review/test/implement aid; value is in standing autonomy, which is a different adoption decision than the rest of the catalog.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Output quality depends on the underlying model + its self-built tools; no verification layer described, self-evolution "judges" aside. |
| Speed | + | An always-on co-worker that builds and remembers can offload standing tasks; high autonomy parallelizes human time. |
| Maintainability | neutral / − | Self-built tools/infra it generates are themselves unreviewed artifacts that someone must eventually own. |
| Safety | − | 🚩 Docker-socket mount + "builds without asking permission" + credential collection + email identity = root-equivalent, large blast radius; isolation is mandatory. |
| Cost Efficiency | − / neutral | Always-on VM + memory/embeddings infra is continuous spend; BYO-model (Z.AI ~15× cheaper) materially mitigates token cost. |

## Verdict

**CONDITIONAL** — adopt only as a deliberately-isolated autonomous co-worker, never as a casual dev-loop tool. The "AI with its own computer + persistent memory + self-evolution + multi-channel identity" concept is genuinely novel and the BYO-model/Apache-2.0 story is strong. But the safety surface is the defining factor: an agent that mounts the Docker socket, builds infra without permission, and holds credentials and an email identity is root-equivalent on its host — run it on throwaway, network-isolated infrastructure with scoped, revocable credentials and treat its self-built artifacts as unreviewed. The marquee capability claims are self-reported and unverified. Best for experimenters wanting a standing autonomous agent; not for anyone who can't fully sandbox it.

Compared to neighbors: catalog harnesses like **superpowers/ECC/gstack** *structure how Claude Code operates within your repo*; **ralph-claude-code/deer-flow** run autonomous loops *on a task*; Phantom is further out — a **persistent, self-hosted agent that lives on its own machine and operates continuously across channels**, closer to an autonomous platform (goose/OpenHands) than a per-task harness, with a correspondingly larger safety footprint.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [phantom](https://github.com/ghostwright/phantom) | platform | Persistent "AI co-worker with its own computer" on the Claude Agent SDK — own VM, durable memory (Qdrant), self-evolution, self-built MCP tools, multi-channel (Slack/Telegram/Email/web) + email identity, BYO-model | Agents are disposable (every session is day one); want a standing, self-improving agent with its own isolated machine and memory | ruflo, deer-flow, ralph-claude-code, goose |
