# Evaluation: kilocode

**Repo:** [Kilo-Org/kilocode](https://github.com/Kilo-Org/kilocode)
**Stars:** 22,863 | **Last updated:** 2026-06-19 (pushed; created 2025-03-10) | **License:** MIT
**Dev loop stage:** Inner-loop **Implement** primarily (in-editor agentic coding), reaching into Review (automated PR reviews) and Ship (cloud agents / "KiloClaw" always-on runner).
**Layer:** Tooling (a VS Code / JetBrains extension + CLI in the Cline/Roo lineage) sitting on a hosted platform (model router, cloud agents, PR reviews)

---

## What it does

Kilo Code is "the open source coding agent for building with AI in VS Code, JetBrains, or the CLI." It descends from the **Cline / Roo Code** lineage of agentic VS Code extensions — an in-editor assistant that reads your repo, plans, edits files, runs commands, and iterates inside the IDE, now extended to JetBrains, a CLI (`@kilocode/cli`, `brew install Kilo-Org/tap/kilo`), a web cloud agent, and an always-on runner ("KiloClaw"). The pitch is **reach plus open pricing**: "meets you everywhere you work," "500+ models," "switch between them mid-task," and "pay the model provider's rate with zero markup … No API keys required to start."

So the product is really two things: (1) an **open-source agentic editor extension/CLI** (the MIT-licensed code in this monorepo) and (2) a **hosted platform** behind it — a model router/marketplace (`kilo.ai`), automated **PR code reviews** (`app.kilo.ai/code-reviews`), and cloud/always-on agents (`app.kilo.ai/cloud`, `app.kilo.ai/claw`). The repo is a large, professionally-operated monorepo: changesets-based release flow, CodeQL (incl. Kotlin for the JetBrains plugin), Bun toolchain, 21+ translated READMEs, a Python SDK publish workflow, and a sizeable `.github/workflows/disabled/` graveyard signaling an actively churning CI surface. 803 open issues and ~2.7K forks indicate heavy real-world use.

## How we tested it

**Source-grounded inspection — not installed, not run.** No extension installed in VS Code/JetBrains, no `kilo` CLI session, no model routed through `kilo.ai`, no PR review or cloud agent exercised. The "500+ models," "zero markup," and "most popular open source coding agent" claims are the vendor's README marketing, not measured. Pricing/markup in particular depends on the hosted platform, which I did not audit. Everything below comes from GitHub metadata, the README, and the recursive file tree.

```bash
gh api repos/Kilo-Org/kilocode --jq '{desc,stars:.stargazers_count,forks:.forks_count,open_issues:.open_issues_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id,topics}'
# 22,863 stars; 2,728 forks; 803 open issues; MIT; created 2025-03-10
# topics: ai-coding, ai-developer-tools, claude, cli, gemini, jetbrains, sonnet, vscode, vscode-extension
gh api repos/Kilo-Org/kilocode/readme --jq '.content' | base64 -d | head -120   # VS Code / JetBrains / CLI / cloud; 500+ models; Cline/Roo lineage
gh api "repos/Kilo-Org/kilocode/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # monorepo: changesets, CodeQL, Bun, disabled-workflows graveyard
gh api repos/Kilo-Org/kilocode/releases --jq 'length'   # 30 (page-1 cap; very active release cadence)
```

## What worked

- **Genuine multi-surface reach.** One agent across VS Code, JetBrains, a CLI, and a cloud runner is a real differentiator — most catalog coding agents are terminal-only (opencode, goose, qwen-code, gemini-cli) or desktop-chat (cherry-studio). Kilo is the **in-editor** option with IDE-native context (open files, diffs, terminal).
- **Open-pricing model marketplace.** 500+ models, mid-task switching, provider-rate billing with claimed zero markup, and no-API-key onboarding lower the barrier and avoid lock-in to a single model vendor — attractive for teams who want to A/B models without rewiring.
- **Mature, well-operated repo.** Changesets release flow, CodeQL for both TS and Kotlin, a CLI on npm + Homebrew + AUR, signed release binaries per platform, and broad i18n point to a funded, sustained operation rather than a hobby fork.
- **Spans more of the loop than a pure Implement agent.** Built-in automated PR reviews (Review) and cloud/always-on agents (Ship) extend it past the editor — overlapping the dev-workflow and code-review categories.
- **Cline/Roo lineage** means a proven agentic-edit core and a migration path for users of those tools.

## What didn't work or surprised us

- **Open-core, not fully open.** The MIT repo is the client; the value-adds (model router/marketplace, PR reviews, cloud agents, KiloClaw) are **hosted services on kilo.ai**. "Open source with open pricing" undersells that the platform is the product and the repo is the on-ramp. You can self-host the agent against your own keys, but the marketed experience routes through their service.
- **"Zero markup" is an unverifiable platform claim.** Billing happens through their router; I could not confirm the markup story from source. Treat as marketing until validated against an invoice.
- **Crowded in-editor niche, and the leaders aren't catalogued as direct peers.** Its real competitors are Cline, Roo, Cursor, and Copilot (in-editor agents) — Kilo's edge over its own ancestors (Cline/Roo) is breadth (JetBrains + CLI + cloud) and the marketplace, not a fundamentally better edit loop.
- **803 open issues / large disabled-workflow graveyard** suggest fast growth with operational churn — features and CI are clearly in flux.
- **Safety follows the in-editor agent norm:** it edits files and runs commands in your workspace. Less host-exposed than a raw terminal agent that curls-to-shell, but still executes in your dev environment, and cloud/always-on agents widen the trust surface (your code reaches their infrastructure).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Proven Cline/Roo agentic-edit core with IDE-native context; correctness is ultimately bounded by the routed model. Automated PR reviews add a Review-stage check. |
| Speed | + | In-editor agent removes the terminal context-switch; mid-task model switching and cloud/always-on agents speed iteration and offload long-running work. |
| Maintainability | neutral / + | Effect on your codebase depends on review discipline like any agent; the *tool* itself is well-maintained (changesets, CodeQL, multi-platform CLI). |
| Safety | − / neutral | Edits files and runs commands in your workspace (IDE-scoped, milder than host-curl agents). Cloud/always-on agents and the hosted router widen the trust/data surface. |
| Cost Efficiency | + (claimed) | 500+ models at provider rates with claimed zero markup and no-key onboarding — strong if true; unverified from source, depends on the hosted platform. |

## Verdict

**CONDITIONAL — strong pick if you want an in-editor (VS Code/JetBrains) agent and accept an open-core hosted platform.** Kilo Code is a mature, well-funded, MIT-licensed agentic editor in the Cline/Roo lineage whose real differentiators are multi-surface reach (editor + JetBrains + CLI + cloud) and an open-pricing model marketplace. The catch is that the marketed experience is open-*core*: the agent is open source, but the router, PR reviews, and cloud agents are hosted services, and the "zero markup" claim is unverifiable from the repo. Adopt for the in-editor niche our terminal-heavy catalog lacks; route through your own model keys if you want to avoid the platform dependency.

Compared to neighbors: against the terminal cohort (**opencode, goose, qwen-code, gemini-cli**), Kilo's edge is that it lives *inside* the IDE with native context rather than in a TUI. Against **cherry-studio** and **lobehub** (desktop/ops platforms), Kilo is a coding-focused editor agent, not a general assistant studio or fleet manager. Against **OpenHands** (full hosted dev platform), Kilo is lighter-weight and editor-embedded rather than a standalone environment. Its closest true peers — Cline, Roo, Cursor — aren't yet catalog entries; Kilo is effectively the catalog's representative of the in-editor agentic-extension category.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [kilocode](https://github.com/Kilo-Org/kilocode) | platform | Open-source in-editor coding agent (Cline/Roo lineage) for VS Code, JetBrains, and CLI, plus a hosted model marketplace (500+ models), automated PR reviews, and cloud/always-on agents | Want an agentic coding assistant inside your IDE with model choice and open pricing, not just a terminal CLI | opencode, goose, OpenHands, cherry-studio, qwen-code, gemini-cli |
