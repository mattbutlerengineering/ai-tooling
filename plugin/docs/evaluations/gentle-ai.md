# Evaluation: Gentle-AI (supersedes Agent Teams Lite)

**Repo:** [Gentleman-Programming/gentle-ai](https://github.com/Gentleman-Programming/gentle-ai)
**Stars:** 4,100 | **Last updated:** 2026-06-19 (pushed; created 2026-02-27) | **License:** MIT | **Releases:** 30
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Cross-cutting (configures the whole inner loop — Plan→Implement→Review — across many agents)
**Layer:** Tooling (Go CLI/installer; pure-Markdown skills + config it injects)

---

## What it does

Gentle-AI is an **"ecosystem configurator"** for AI coding agents — explicitly *not* an agent installer. It takes whatever agent(s) you already use and supercharges them with: **persistent memory** (via Engram, the author's memory tool, installed + configured), **Spec-Driven Development** workflow (a 9-phase SDD orchestration + "judgment-day" review), a curated **skill registry**, **MCP servers** (e.g. Context7), an **AI provider switcher**, a **teaching-oriented persona with security-first permissions**, and **per-phase model assignment** (each SDD step can run on a different model). It's the active successor to **Agent Teams Lite** (now archived), with better install, auto-updates, backup/rollback, config sync, permission management, and a TUI installer.

Its headline reach is breadth: **15 supported agents** — Claude Code, OpenCode, Kilo Code, Gemini CLI, Cursor, VS Code Copilot, Codex, Windsurf, Antigravity, Kimi Code, Kiro IDE, Qwen Code, OpenClaw, Trae, Pi (+ detect-only Hermes) — each mapped to its native delegation model (full sub-agent support where available, solo-agent otherwise). It also encodes **delegation triggers**: explicit rules for when the orchestrator should stop and delegate or run a phase boundary (reading 4+ files → delegate exploration; touching 2+ non-trivial files → one writer + fresh review; commit/push/PR → fresh review unless trivial; git/worktree accidents → stop and audit). The stated goal: "keep one responsible orchestrator and one writer thread; avoid accidental chaos without ceremony." Install is a one-line script (macOS/Linux/Windows) or Homebrew.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No install performed, no agent configured. Claims come from the repository (GitHub metadata, README agent table + delegation triggers, 30 releases) and the archived predecessor's migration notes — the project's own documentation, not observed behavior.

```bash
gh api repos/Gentleman-Programming/gentle-ai --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/Gentleman-Programming/gentle-ai/readme --jq '.content' | base64 -d   # 15 agents, SDD, delegation triggers
gh api repos/Gentleman-Programming/gentle-ai/releases --jq 'length'             # 30
gh api repos/Gentleman-Programming/agent-teams-lite/readme --jq '.content' | base64 -d   # deprecation → gentle-ai
```

## What worked

- **Cross-agent breadth is the standout.** 15 agents mapped to their *native* delegation models (not a lowest-common-denominator wrapper) is unusually thorough — you get one SDD/skills/memory configuration that follows you across Claude Code, Cursor, Codex, Gemini, etc.
- **Delegation triggers are genuinely good practice.** Codifying "4+ files → delegate," "commit/push → fresh review," "git accident → stop and audit" turns vague best-practice into explicit orchestrator rules — the kind of guardrail most setups leave implicit.
- **Per-phase model assignment** (cheap model for scaffolding, strong model for review) is a smart cost/quality lever baked into the workflow.
- **Batteries included + reversible.** Engram memory, Context7 MCP, persona, provider switcher, plus auto-updates, backup/rollback, and config sync/migration — it manages its own footprint, which most "setup" repos don't.
- **Mature and active:** ★4100, 30 releases, pushed the day of evaluation, MIT, by a known author (also behind Engram); clean Crystal→Nimbalyst-style succession from the archived ATL.

## What didn't work or surprised us

- **Large, opinionated surface that mutates many config files.** It writes into `~/.claude`, `~/.cursor`, `~/.gemini`, `~/.qwen`, `~/.kimi`, etc. across 15 agents — powerful, but a lot of machine state to trust one tool with. Backup/rollback mitigates this; still, review what it injects.
- **Opinionated methodology.** The 9-phase SDD + persona + permission model is a worldview; teams with their own workflow may find it heavy or conflicting. It's a framework, not a neutral utility.
- **Value depends on buying into the ecosystem.** Engram memory + the SDD persona + provider switcher are most valuable together; cherry-picking pieces is possible but dilutes the point.
- **Breadth vs. depth risk.** Supporting 15 agents' native delegation models is a big maintenance surface; per-agent fidelity (especially the "experimental"/"solo-agent"/"detect-only" tiers) will vary and isn't verified here.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Delegation triggers force fresh review on commits/PRs and audits on git accidents; SDD phases + judgment-day add review gates. |
| Speed | + / neutral | One config supercharges any agent and per-phase model routing optimizes each step; offset by SDD ceremony on small tasks. |
| Maintainability | + | Encourages thin orchestrator + single writer + spec-driven structure; manages/rolls back its own config. |
| Safety | + / − | Security-first permission model + explicit "stop and audit" triggers (+); but it mutates many agents' config dirs — broad machine-state surface to trust (−, mitigated by backup/rollback). |
| Cost Efficiency | + | Per-phase model assignment lets cheap models do cheap phases; free/MIT. |

## Verdict

**CONDITIONAL** — adopt if you want a **single, opinionated, cross-agent configuration** that gives any of 15 coding agents persistent memory, a spec-driven workflow, curated skills, MCP tools, and — best of all — **codified delegation/review triggers**, with reversible install. It's mature, active, MIT, and the breadth + delegation-rules combo is genuinely differentiated. Hold off if you already have a workflow you like (it's heavy and opinionated) or are uneasy letting one tool write across many agents' config dirs (use the backup/rollback and review the injected config). Strongest for someone standardizing a team across multiple agents, or a solo dev who wants gstack-style structure but agent-agnostic.

Compared to neighbors: **superpowers**/**gstack**/**ECC** are opinionated Claude Code-centric harnesses; **omnigent** is a meta-harness that swaps agent backends. Gentle-AI is the **cross-agent ecosystem configurator** — it doesn't replace your agent, it standardizes SDD + memory + skills + delegation rules *across* 15 of them, with the most explicit delegation-trigger discipline of the group. (Catalogued under its live name; `agent-teams-lite` is the archived predecessor.)

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gentle-ai](https://github.com/Gentleman-Programming/gentle-ai) | harness | Cross-agent ecosystem configurator — injects SDD workflow, persistent memory (Engram), curated skills, MCP servers, a teaching persona, per-phase model routing, and explicit delegation/review triggers into 15 coding agents (formerly Agent Teams Lite) | Installed an agent but "it's just a chatbot" — want memory, spec-driven workflow, skills, and review discipline standardized across whatever agent(s) you use | superpowers, gstack, ECC, omnigent |
