# Evaluation: HolyClaude

**Repo:** [CoderLuii/HolyClaude](https://github.com/CoderLuii/HolyClaude)
**Stars:** 2,352 | **Last updated:** 2026-06-19 (pushed; created 2026-03-22) | **License:** MIT | **Run:** `docker compose up`
**Dev loop stage:** Agent Orchestration (a containerized coding workstation)
**Layer:** Platform (Docker stack bundling agent + web UI + tools)

---

## What it does

HolyClaude is a **one-command, containerized AI coding workstation**: Claude Code + a web UI + **8 AI CLIs** + a headless browser + **50+ dev tools**, all packaged so you `docker compose up` instead of spending hours wiring a setup. "Stop configuring. Start building." It works with your existing Claude Code subscription (Max/Pro plan or API key) and bundles the surrounding toolchain (browser, CLIs, dev utilities) into one reproducible environment, with a web UI front end.

## How we tested it

**Source-grounded inspection — not installed, not run.** No container brought up, no agent driven. Capabilities come from the README and metadata, not observed usage.

```bash
gh api repos/CoderLuii/HolyClaude --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 2.4K, MIT
gh api repos/CoderLuii/HolyClaude/readme --jq '.content' | base64 -d | head -15   # docker compose, Claude Code + web UI + 8 CLIs + browser + 50+ tools
```

## What worked

- **Zero-setup reproducible environment.** Bundling Claude Code, multiple AI CLIs, a headless browser, and 50+ tools into one `docker compose up` removes a genuine, recurring pain (environment drift and hours of manual wiring).
- **BYO subscription.** Using your existing Claude Code plan/API key (no markup) is the right posture.
- **Containerized = isolated + portable.** A reproducible workstation is easy to spin up, tear down, and run consistently across machines.
- **Web UI + many CLIs in one place** is convenient for people who hop between agents/tools. MIT, ~2.4K stars, heavy i18n, pushed daily.

## What didn't work or surprised us

- **Convenience bundle, not a new capability.** It packages existing tools; the value is the curated, containerized setup, not novel agent behavior.
- **Heavy, opinionated environment.** A Docker stack with 50+ tools and 8 CLIs is a lot of surface to trust, update, and secure — and you adopt someone else's tool choices.
- **Overlaps orca and the multiplexers.** orca is an agent-development *environment* (worktree fan-out, mobile, design mode); HolyClaude is a *containerized toolchain bundle* with a web UI — different emphases, similar "one place to run agents" goal.
- **Container browser + many CLIs = broad attack/credential surface** to keep patched.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | A packaged environment; doesn't change agent output quality. |
| Speed | + | Eliminates setup time and environment drift; everything ready in one command. |
| Maintainability | neutral / − | Reproducible container is a plus; a 50+-tool opinionated stack is a lot to keep current. |
| Safety | neutral / − | Containerization isolates, but a bundled headless browser + 8 CLIs + your subscription is a broad surface to secure. |
| Cost Efficiency | + / neutral | BYO subscription (no markup); container resource overhead otherwise. |

## Verdict

**CONDITIONAL** — HolyClaude is a convenient, MIT, **containerized AI coding workstation** that turns "two hours of manual setup" into `docker compose up` — Claude Code + web UI + 8 AI CLIs + headless browser + 50+ tools, using your existing subscription. Adopt it if you want a reproducible, batteries-included environment (e.g. onboarding, ephemeral dev boxes, or hopping between agents) and are comfortable adopting its opinionated tool choices and keeping a broad container surface patched. It's a packaging/convenience win, not a new agent capability — and overlaps orca (the heavier ADE) for the "one place to run many agents" goal.

Compared to neighbors: **orca** is a full agent-development environment (worktree fan-out, mobile, design mode); **claude-squad** a TUI session manager. HolyClaude's distinguishing pitch is the **one-command containerized toolchain bundle** (agent + web UI + CLIs + browser + 50+ tools).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [HolyClaude](https://github.com/CoderLuii/HolyClaude) | platform | One-command containerized AI coding workstation (MIT) — Claude Code + web UI + 8 AI CLIs + headless browser + 50+ tools via `docker compose up`, using your existing subscription | Setting up a full agent dev environment takes hours and drifts; want a reproducible, batteries-included container | orca, claude-squad |
