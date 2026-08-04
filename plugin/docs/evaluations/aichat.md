# Evaluation: aichat

**Repo:** [sigoden/aichat](https://github.com/sigoden/aichat)
**Stars:** ~10,200 | **Last updated:** 2026-02-23 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An all-in-one LLM CLI tool written in Rust. AIChat packs several modes into one fast binary: a **Shell Assistant** (turn natural language into shell commands), **CMD and REPL** modes, **RAG**, and **AI tools & agents** — with access to many providers (OpenAI, Claude, Gemini, Ollama, Groq, and more).

Mechanically it's a single, scriptable CLI you install via cargo/brew/pacman. The Shell Assistant generates and optionally runs shell commands from plain English; REPL/CMD modes give interactive or one-shot chat; RAG lets you ground responses on your documents; and the tools/agents support lets it call functions/agents. The appeal is consolidation — one cross-provider CLI for chat, shell help, RAG, and agents rather than separate tools per task.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and feature list (Shell Assistant, CMD/REPL, RAG, tools/agents; multi-provider; cargo/brew/pacman install). Confirmed the all-in-one, cross-provider, single-binary positioning. Last push ~2026-02 (mature, stable; somewhat less frequent updates). Not run live, so condition-gated.

```bash
gh api repos/sigoden/aichat --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/sigoden/aichat/readme --jq '.content' | base64 -d
```

## What worked

- **One fast binary, many modes.** Shell assistance + REPL + RAG + agents across providers in a single Rust CLI is genuinely convenient — less tool-juggling, fast startup.
- **Shell Assistant.** Natural-language-to-shell is a high-frequency, high-value use for a terminal CLI.
- **Provider-agnostic + easy install.** OpenAI/Claude/Gemini/Ollama/Groq support and package-manager installs lower friction.

## What didn't work or surprised us

- **Breadth vs. depth.** A do-everything CLI is handy but won't match a dedicated coding agent (Claude Code/opencode) for deep, multi-file code work.
- **Shell-command execution risk.** Generating and running shell commands warrants the usual care (review before running).
- **Maintenance cadence.** Last push ~2026-02 is slower than the most active CLIs — stable, but watch momentum.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Depends on the model; RAG grounding helps |
| Speed | + | Single fast Rust binary; quick shell/chat/RAG access |
| Maintainability | + | One tool replaces several per-task CLIs |
| Safety | - | Shell Assistant runs generated commands — review before executing |
| Cost Efficiency | + | Free/OSS; use cheaper/local providers (Ollama) as needed |

## Verdict

**discovery-log — tentative read**

Adopt as a fast, scriptable, all-in-one terminal LLM CLI — shell assistance, REPL/CMD, RAG, and agents across providers in one Rust binary — when you want consolidation over a pile of single-purpose tools. For deep multi-file coding, a dedicated agent (Claude Code/opencode) does more. Mind the Shell Assistant's command-execution risk and the moderate maintenance cadence.

## Triage note

Left at `discovery-log`. Apache-2.0, ★10.3K, pushed 2026-02-23 (~5 months — the second-oldest in this
slice, but well short of the dormancy that decided `plandex`).

Scope-checked rather than redundancy-checked, because it is a different shape from the cluster: an
all-in-one terminal **LLM** CLI (shell assistance, REPL, RAG, agents) rather than a coding agent. Its
own eval concedes the point — "for deep multi-file coding, a dedicated agent … does more" — which
positions it beside the coding harnesses rather than against them.

The Safety note in its eval is the one to keep: the Shell Assistant executes commands, so it carries
the same class of risk as any agent with shell access, in a tool whose framing is a convenience CLI.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [aichat](https://github.com/sigoden/aichat) | harness | All-in-one LLM CLI tool (Apache-2.0, ★10K, Rust) — Shell Assistant (natural-language → shell commands), CMD & REPL modes, RAG, and AI tools/agents in one binary; access OpenAI/Claude/Gemini/Ollama/Groq and more | Want one fast, scriptable CLI for chat, shell assistance, RAG, and agents across providers, not separate tools per task | gptme, opencode, llm (ext.), aider-style (ext.) |
