# Evaluation: Hermes Agent

**Repo:** [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
**Stars:** ~197,700 (unusually high — reported as-is, unverified) | **Last updated:** 2026-06-20 (pushed; created 2025-07-22) | **License:** MIT | **Forks:** ~35K
**Dev loop stage:** Agent Orchestration (general self-improving personal agent; tangential to the coding dev loop)
**Layer:** Harness (CLI + gateway + TUI; runs on VPS/GPU/serverless)

---

## What it does

Hermes Agent is **Nous Research's self-improving personal AI agent**. Its headline differentiator is a **built-in learning loop** — it's pitched as "the only agent with a built-in learning loop": it **creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions.**

Operationally it's "own-it" and portable: run it on a $5 VPS, a GPU cluster, or near-zero-cost serverless; it's not tied to your laptop and you can talk to it from Telegram while it works on a cloud VM. It's aggressively **model-agnostic** — Nous Portal, OpenRouter (200+ models), NovitaAI, NVIDIA NIM, Xiaomi MiMo, z.ai/GLM, Kimi, MiniMax, Hugging Face, OpenAI, or your own endpoint — switched with `hermes model`, no code changes, no lock-in. A one-line installer provisions uv, Python 3.11, Node, ripgrep, ffmpeg, and a bundled portable Git Bash on Windows.

## How we tested it

**Source-grounded inspection — not installed, not run.** No installer executed, no agent launched, no learning loop observed. Capabilities (and especially the "self-improving" claims) come from the repository README and metadata, not behavior. The star/fork counts are reported verbatim from the GitHub API and are unusually high; treat them as unverified popularity signals, not a quality guarantee.

```bash
gh api repos/NousResearch/hermes-agent --jq '{stars,forks,license:.license.spdx_id,created:.created_at,pushed:.pushed_at}'
gh api repos/NousResearch/hermes-agent/readme --jq '.content' | base64 -d | head -30   # learning loop, model-agnostic, run-anywhere
```

## What worked

- **The learning loop is the real idea.** Skill-creation-from-experience + self-improvement + knowledge persistence + searching its own history + a cross-session user model is a more ambitious memory/learning story than most "persistent memory" tools, which only recall.
- **Genuinely model-agnostic, no lock-in.** First-class support for a long list of providers (incl. your own endpoint), switchable with one command, is exactly the right posture for an own-it agent.
- **Runs anywhere, detached from the laptop.** VPS/GPU/serverless + Telegram access makes it a persistent background agent rather than a terminal session.
- **Credible source + MIT.** Nous Research is a well-known lab; permissive license; turnkey cross-platform installer (incl. native Windows with bundled MinGit).

## What didn't work or surprised us

- **Anomalous metrics.** ~197K stars / ~35K forks / ~22K open issues for a repo created mid-2025 is extraordinary — possibly viral, possibly inflated. Don't treat the number as proof of maturity; the ~22K open issues also hint at heavy churn.
- **Personal agent, not a coding dev-loop harness.** Like nanobot and CowAgent, its center of gravity is an own-it personal assistant (Telegram-first, long-running goals) — the Plan→Implement→Review coding loop isn't the focus.
- **Self-improvement is powerful and opaque.** An agent that rewrites its own skills and persists knowledge autonomously is a controllability/safety surface — what it learns and acts on needs governance, and none of that is evaluated here.
- **Broad install footprint.** The one-liner provisions a whole toolchain; convenient, but a lot of surface to trust and maintain.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | General agent; not focused on the correctness of shipped code. Self-improvement *could* help or drift. |
| Speed | neutral | Long-running personal automation, not a dev-loop throughput tool. |
| Maintainability | neutral / − | Self-hostable and model-agnostic (good), but a self-modifying skill store + broad toolchain is a maintenance/trust surface. |
| Safety | − | Autonomous skill-rewriting, knowledge persistence, and cloud/Telegram operation widen the trust and credential surface; governance needed. |
| Cost Efficiency | + / neutral | Runs cheaply (VPS/serverless/idle), and model-agnostic routing can pick cheaper providers. |

## Verdict

**CONDITIONAL** — Hermes Agent is a distinctive, MIT-licensed, **model-agnostic self-improving personal agent** from a credible lab, whose **built-in learning loop** (skills-from-experience + knowledge persistence + cross-session user model) is more ambitious than the catalog's recall-only memory tools, and which runs detached on cheap infra with Telegram access. Adopt it if you want a long-running, own-it personal agent that compounds over time and refuses model lock-in. For the AI-assisted **coding** dev loop specifically it's tangential (it overlaps nanobot/CowAgent as an own-it assistant), the self-modifying behavior is a real governance surface, and its headline popularity metrics are anomalous — pilot in a sandbox and watch what it persists before trusting it.

Compared to neighbors: **nanobot** and **CowAgent** are own-it multi-channel assistants; **hivemind** turns execution traces into reusable skills; **claude-reflect** learns from corrections into CLAUDE.md. Hermes' distinguishing pitch is a **closed-loop self-improving agent** (creates *and* refines its own skills, persists knowledge, models the user) that runs anywhere with any model.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | harness | NousResearch's self-improving own-it agent (MIT) — built-in learning loop (creates/refines skills from experience, persists knowledge, searches its own history, models you across sessions); model-agnostic (no lock-in), runs on VPS/GPU/serverless with Telegram access | Want a self-hostable agent that actually learns and compounds across sessions rather than resetting each time, without model lock-in | nanobot, CowAgent, hivemind, claude-reflect |
