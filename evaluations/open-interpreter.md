# Evaluation: open-interpreter

**Repo:** [openinterpreter/openinterpreter](https://github.com/openinterpreter/openinterpreter)
**Stars:** 64,057 | **Last updated:** 2026-06-19 (pushed; created 2023-07-14) | **License:** Apache-2.0
**Dev loop stage:** Inner-loop **Implement** (and adjacent Verify via its QA skill) — a terminal coding agent that plans, edits, and runs code on your machine.
**Layer:** Tooling/Infrastructure (a standalone Rust TUI binary with native OS sandboxing; you bring your own model/provider)

---

## What it does

The catalog mental model for Open Interpreter is the old fame: "natural language → run code locally." That description is now **stale and misleading**. As inspected, the repo is a **complete Rust rewrite, explicitly "a fork of OpenAI's Codex,"** repositioned as "a coding agent for low-cost models like Deepseek, Kimi, and Qwen." The original Python `interpreter.chat()` library that earned the 64K stars has been **handed off to a community fork** (`endolith/open-interpreter`) and no longer lives here. So the star count is historical goodwill attached to what is effectively a brand-new Codex-derivative TUI.

The defining feature of the current product is **harness emulation**: `/harness` switches the active agent loop between `native`, `claude-code`, `claude-code-bare`, `kimi-cli`, `qwen-code`, `deepseek-tui`, `swe-agent`, and `minimal` — i.e. it tries to reproduce whichever prompt/tool scaffold gets the best performance out of a given cheap model. `/model` swaps providers in-session. It runs commands "inside native sandboxing on macOS, Linux, and Windows," ships a **QA skill** that drives web apps via `agent-browser` and native apps via `trycua`, speaks the **Agent Client Protocol** (`interpreter acp`) for editor embedding, and supports `exec`, MCP, skills, hooks, permissions, and `AGENTS.md`. Config and session state stay local under `~/.openinterpreter`. The `.codex/` tree in the repo (skills like `babysit-pr`, `code-review`, `codex-issue-digest`) is the inherited Codex development harness, confirming the lineage.

## How we tested it

**Source-grounded inspection — not installed, not run.** No `curl … | sh` install, no `interpreter` session, no `/harness` switch, no code executed on a host. The "best performance out of low-cost models" and "native sandboxing" claims are the authors' README framing; I did not benchmark model quality or audit the sandbox implementation. Every claim below comes from GitHub metadata, the README, and the recursive file tree.

```bash
gh api repos/openinterpreter/openinterpreter --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id,topics}'
# desc: "A lightweight coding agent for open models like Deepseek, Kimi, and Qwen"; 64,057 stars; 5,551 forks; Apache-2.0
# topics: coding-agent, deepseek, interpreter, kimi, qwen, rust, tui
gh api repos/openinterpreter/openinterpreter/readme --jq '.content' | base64 -d | head -120   # Rust rewrite, "fork of OpenAI's Codex"
gh api "repos/openinterpreter/openinterpreter/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # .codex/ harness, Bazel build
gh api repos/openinterpreter/openinterpreter/releases --jq 'length'   # 30 (page-1 cap; actively released)
```

## What worked

- **Honest model-cost focus with a concrete mechanism.** "Harness emulation" is a real, differentiated idea: cheap open models underperform with a generic loop, so OI lets you borrow the `claude-code` or `qwen-code` scaffold that suits them. Most catalog coding agents are model-agnostic in name only; this one is built around squeezing weak models.
- **Native OS sandboxing as a first-class feature, not a bolt-on.** For an agent that runs arbitrary commands, sandboxing on all three desktop OSes plus a permissions/approvals layer is exactly the right design — a meaningful improvement over the old Python project, which ran code in your live environment with a y/N prompt.
- **Standards-forward surface.** ACP for editor embedding, MCP, skills, hooks, and `AGENTS.md` mean it plugs into the same ecosystem as Claude Code and the opencode/qwen-code cohort rather than inventing its own walled garden.
- **Built-in QA skill spanning web and native apps** (agent-browser + trycua) gives it a Verify-stage reach most terminal agents lack.
- **Codex lineage is a quality signal.** Forking a mature harness (visible in the inherited `.codex/` skills and Bazel build) is a sounder foundation than a from-scratch loop.

## What didn't work or surprised us

- **The stars are a brand bait-and-switch.** 64K stars accrued to a Python NL-to-code library that is now a community fork elsewhere; the thing in this repo is a young Codex derivative. Anyone adopting on reputation is adopting a different product than the one that earned the reputation.
- **Heavy overlap with tools already in the catalog.** A model-agnostic terminal coding agent emphasizing cheap open models is precisely the niche occupied by **opencode, goose, qwen-code, gemini-cli, oh-my-pi, and DeepSeek-Reasonix**. OI's only genuine differentiator is harness emulation; on every other axis it is one more entrant in a crowded lane.
- **Safety is the headline risk and unverifiable here.** It executes code and shell commands on the host. The README asserts native sandboxing and approvals, but I did not test escape resistance, and "low-cost models" are exactly the ones most likely to emit a destructive command. The sandbox is the whole safety story and it is unaudited.
- **Curl-to-shell install** (`curl … | sh`) is the documented path — convenient, but a supply-chain footgun for a host-executing agent.
- **Rust rewrite is young.** Despite the old creation date, the current codebase is recent; high open-issue count (270) and an in-flight rewrite mean rougher edges than the star count implies.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Harness emulation can lift weak/cheap models toward usable output; but correctness is bounded by the (deliberately low-cost) model you point it at, not by OI itself. |
| Speed | + | TUI Implement loop with in-session model/harness switching; ACP embedding avoids context-switching out of the editor. Offset by setup and the iteration cost of cheaper models. |
| Maintainability | neutral | Codex-fork foundation and Apple/Linux/Windows sandboxing are well-structured; effect on *your* codebase is the same as any coding agent — depends on review discipline. |
| Safety | − (load-bearing) | Executes arbitrary code/shell on the host. Native sandbox + permissions exist but are unaudited here; cheap models raise the odds of bad commands. This is the dominant risk. |
| Cost Efficiency | + | The entire premise: get acceptable results from Deepseek/Kimi/Qwen at provider rates instead of frontier-model prices. Strongest signal in its favor. |

## Verdict

**CONDITIONAL — adopt only if your goal is cheap open-model coding in a sandboxed terminal, and only after vetting the sandbox.** The current Open Interpreter is a credible, standards-forward Codex fork with a real differentiator (harness emulation) and the right safety posture on paper (native sandboxing + approvals). But the 64K stars belong to a retired Python project, it executes code on your host, and its core niche is already filled by several catalog entries. It earns a place as the **cost-optimized, sandboxed member of the open-model terminal-agent cohort** — not a default.

Compared to neighbors: **qwen-code** and **DeepSeek-Reasonix** are model-native agents tuned to one provider; OI is broader (any cheap model + emulated harness) but less deeply optimized for any single one. **opencode** and **goose** are the general-purpose open alternatives to Claude Code with larger communities and no host-execution sandbox emphasis; **gemini-cli** wins on backing and free tier. OI's unique pitches are (1) harness emulation and (2) first-class native sandboxing — pick it when *those two specifically* matter; otherwise opencode/goose/gemini-cli are safer defaults.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [open-interpreter](https://github.com/openinterpreter/openinterpreter) | harness | Rust terminal coding agent (a Codex fork) with "harness emulation" to get the best out of low-cost open models (Deepseek/Kimi/Qwen), native OS sandboxing, ACP/MCP/skills | Want a sandboxed terminal agent tuned to run cheap open models well, not frontier-priced ones | opencode, goose, qwen-code, gemini-cli, DeepSeek-Reasonix, oh-my-pi |
