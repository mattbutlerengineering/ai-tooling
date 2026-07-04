# Evaluation: gptme

**Repo:** [gptme/gptme](https://github.com/gptme/gptme)
**Stars:** ~4,330 | **Last updated:** 2026-06-20 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A personal AI agent that lives in your terminal, equipped with local tools: it writes code, runs shell commands, browses the web, and edits files. The pitch is to make your own persistent, autonomous agent on top of it — lightweight, hackable, local-first, any model.

Mechanically it's a terminal coding agent with a small, transparent tool set (shell, file editing, web browsing, code execution) that you can extend. Unlike heavyweight or cloud-locked harnesses, gptme is designed to be simple and self-hosted — you own the loop and can build persistent autonomous agents on top. It supports multiple model providers and runs entirely on your machine.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the stated capabilities (terminal agent with shell/file/web/code tools, any model, local-first, extensible into persistent autonomous agents). Confirmed the lightweight, hackable, self-hosted positioning. Not run live, so condition-gated.

```bash
gh api repos/gptme/gptme --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/gptme/gptme/readme --jq '.content' | base64 -d
```

## What worked

- **Lightweight and hackable.** A small, transparent tool set you can read and extend — appealing if you want to understand and control your agent rather than use a black box.
- **Local-first, any model.** Runs on your machine with your choice of model; good for privacy and for building custom persistent agents.
- **Established and active.** ~4.3K stars, MIT, actively maintained — a credible terminal-agent option.

## What didn't work or surprised us

- **Crowded terminal-agent space.** Overlaps opencode, oh-my-pi, Claude Code, aider, and others; gptme's edge is minimalism and hackability, not a unique capability.
- **DIY tradeoff.** "Build your own agent on top" means more assembly than a batteries-included harness for users who just want results.
- **Capability ceiling vs. flagship harnesses.** A minimal tool set is more transparent but less feature-rich than Claude Code/Codex.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Depends on the model; tool set is straightforward |
| Speed | + | Lightweight terminal loop; no cloud round-trip |
| Maintainability | + | Small, transparent, extensible codebase you control |
| Safety | neutral | Shell/file tools carry the usual agent-execution risk |
| Cost Efficiency | + | Local-first, any model; no platform fees |

## Verdict

**CONDITIONAL**

Adopt if you want a minimal, hackable, local-first terminal agent you fully control and can extend into custom persistent agents — rather than a heavyweight or cloud-locked harness. For maximal capability out of the box, flagship harnesses (Claude Code/Codex/opencode) do more; gptme's appeal is transparency and ownership. A good base for tinkerers building bespoke agents.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gptme](https://github.com/gptme/gptme) | harness | Personal terminal agent with local tools (MIT, ★4.3K) — writes code, runs shell, browses the web, edits files; build your own persistent autonomous agent on top, any model, local-first | Want a lightweight, hackable terminal coding agent you fully control and extend, not a heavyweight or cloud-locked harness | opencode, oh-my-pi, tabby, aider-style (ext.) |
