# Evaluation: rtk

**Repo:** [rtk-ai/rtk](https://github.com/rtk-ai/rtk)
**Stars:** 63,902 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Last verified:** 2026-07-08  <!-- source-grounded re-check; not a hands-on re-verification -->
**Dev loop stage:** Implement / Verify (intervenes on every Bash tool call across the inner loop)
**Layer:** Infrastructure

---

## What it does

CLI proxy that reduces LLM token consumption by 60-90% on common dev commands. rtk (Rust Token Killer) is a single Rust binary that wraps 100+ shell commands — `git`, `ls`, `cat`/`read`, `grep`/`rg`, `find`, the major test runners (`cargo test`, `pytest`, `go test`, `jest`, `vitest`), linters (`eslint`, `ruff`, `clippy`, `tsc`), package managers, `docker`/`kubectl`, `gh`, and `aws` — and rewrites their verbose output into a compact form before it reaches the agent's context. It claims `<10ms` overhead and ships with zero runtime dependencies.

The mechanism is output rewriting, not interception of the LLM stream. rtk applies four strategies per command type: smart filtering (drops comments/whitespace/boilerplate), grouping (aggregates files by directory, errors by type), truncation (keeps relevant context, cuts redundancy), and deduplication (collapses repeated log lines with counts). Examples from the README: `git push` collapses 15 lines of progress chatter to `ok main`; `rtk read file.rs -l aggressive` strips function bodies and returns signatures only; a failing `cargo test` returns ~20 lines (failures only) instead of 200+.

For Claude Code, integration is a **PreToolUse hook** installed via `rtk init -g`. The hook transparently rewrites Bash tool calls — `git status` becomes `rtk git status` before execution — so the agent gets compact output without ever calling `rtk` explicitly. Crucially, the hook only fires on the **Bash tool**; Claude Code's built-in `Read`, `Grep`, and `Glob` tools bypass it, so those paths get no rtk filtering unless you call `rtk read`/`rtk grep`/`rtk find` or shell equivalents directly. On failure, a `tee` mechanism saves the full unfiltered output to a local log file and tells the agent where to find it, so a compressed result that dropped a needed detail is recoverable for the failing case without re-running the command.

## How we tested it

**Evidence:** REVIEW

Architecture-review evaluation. Method: inspected the GitHub repo metadata, the full README (token-savings table, "How It Works", the per-command reference, the auto-rewrite hook section, config, and the "Supported AI Tools" matrix), the org/contributor data, and the overlapping catalog entries (headroom = CONDITIONAL, caveman = ADOPT) for calibration. **Not installed and not exercised in a live Claude Code session** — no commands were run through it, so all savings figures below are the project's own published estimates, not measured here. The 60-90% headline is rtk's claim; their own table carries the footnote "Estimates based on medium-sized TypeScript/Rust projects. Actual savings vary by project size."

```bash
gh api repos/rtk-ai/rtk --jq '{stars,license,description,pushed_at,forks,open_issues}'
gh api repos/rtk-ai/rtk/readme --jq '.content' | base64 -d
gh api orgs/rtk-ai --jq '{name,type,created_at,public_repos}'
gh api repos/rtk-ai/rtk/contributors --jq '.[].login'
# Verify the headroom <-> rtk bundling relationship:
gh api repos/chopratejas/headroom/readme --jq '.content' | base64 -d | grep -i -A2 -B2 rtk
# Calibration against overlapping evals:
#   evaluations/headroom.md (CONDITIONAL), evaluations/caveman.md (ADOPT)
```

## What worked

- **Lowest-friction adoption in its catalog cluster.** `brew install rtk && rtk init -g`, restart Claude Code, done. No Rust/ONNX/HuggingFace build chain (unlike headroom), no MCP slot consumed (unlike token-optimizer-mcp), no per-turn mode toggle to remember (unlike caveman). The PreToolUse hook makes it transparent: the agent keeps writing `git status` and gets compact output for free, including in subagents.
- **Targets the highest-volume, highest-noise outputs precisely.** The savings table maps to real workloads: `git add/commit/push` -92%, test runners -90%, `git status`/`grep`/`ls` -80%. These are exactly the commands an agent runs dozens of times per session and whose raw output (progress bars, passing-test lines, boilerplate) carries near-zero signal. This is a well-chosen, surgical scope.
- **The tee fallback is a real correctness safety net for the failure case.** When a wrapped command fails, rtk writes the full unfiltered output to a local log and points the agent at it (`[full output: ~/.local/share/rtk/tee/...]`). So the most dangerous compression scenario — a failing build/test where the agent needs the full trace — degrades gracefully rather than losing information.
- **Strong, broadening maturity signals.** 63.9K stars, Apache-2.0, an actual **organization** (`rtk-ai`) with multiple human contributors (not a single-author project), Homebrew + curl + Cargo + pre-built binaries, a real docs site (rtk-ai.app), security CI, config file with per-command excludes and tee modes, and 14 supported agents. Pushed the day of evaluation.
- **Independently validated by a peer tool.** Headroom — the broadest tool in this cluster — *bundles* rtk and calls it "a first-class part of our stack" for shell-output rewriting, compressing everything downstream of it. That is strong external evidence that rtk's command-output rewriting is best-in-class for its narrow scope.
- **`rtk gain` / `rtk discover` close the feedback loop.** Built-in analytics report actual token savings and surface missed-savings opportunities, which turns the Cost Efficiency claim into something measurable per project rather than a leap of faith.

## What didn't work or surprised us

- **Scope is CLI command outputs only — it does not see the biggest context sinks.** rtk compresses Bash output. It does **not** touch large file reads via the `Read` tool, `Grep`/`Glob` results, MCP tool responses, RAG payloads, or conversation history. The README is explicit that the hook bypasses Claude Code's built-in tools. In agent sessions where most context comes from reading source files (the common case), rtk's reach is limited unless the agent is steered toward `rtk read`/`rtk grep`, which fights the agent's default tool selection.
- **Compression is one-way for the success case.** Unlike headroom's reversible Compress-Cache-Retrieve, rtk has no general retrieve path — the tee fallback only fires on *failure*. If a *successful* command's compact output silently drops a detail the agent later needs, it must re-run the raw command. Lower risk given the conservative, type-specific filters, but it is not the recoverable design headroom offers.
- **It is on the critical path of every Bash call.** As a PreToolUse hook rewriting commands before execution, an rtk bug, parse failure, or version mismatch can degrade or break command execution agent-wide, not just reduce context quality. The high open-issue count (1,271) is consistent with the large surface area of wrapping 100+ heterogeneous command formats. Per-command `exclude_commands` config mitigates this for known-problematic commands.
- **Name collision footgun.** The README warns that an unrelated `rtk` (Rust Type Kit) exists on crates.io; `cargo install rtk` gets the wrong package. Use Homebrew or `cargo install --git`.
- **Overlap is real but rtk is a strict subset of headroom.** Headroom's own comparison matrix is accurate: rtk = "CLI command outputs / CLI wrapper / local: yes / reversible: no." headroom = "all context / proxy+library+MCP / local+reversible." rtk is not a peer of headroom; it is one (excellent) layer that headroom subsumes and bundles. Versus caveman (output *prose* compression, model-side) and token-optimizer-mcp (MCP-tool-output, MCP-only), rtk and those address different, non-overlapping context sources.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Conservative type-specific filters plus tee-on-failure preserve full output for the dangerous case; but successful-command compression is one-way and could silently drop a needed detail |
| Speed | + | Fewer input tokens per Bash turn means faster responses and more headroom before compaction; `<10ms` claimed rewrite overhead is negligible |
| Maintainability | neutral | Org-backed, multi-contributor, well-documented — but it sits on the critical path of every Bash call, and 1,271 open issues reflect the breadth of commands wrapped |
| Safety | + | Runs fully local (no data leaves the machine); `aws` filters strip secrets/policy documents; tee fallback prevents information loss on failures |
| Cost Efficiency | + | The core value: project-claimed 60-90% token reduction on the highest-volume dev commands, with `rtk gain` providing measured per-project verification |

## Verdict

**CONDITIONAL**

Adopt rtk when you run AI coding agents that lean heavily on shell commands — git-heavy workflows, frequent test/lint runs, container/cloud inspection — and want a near-zero-friction token win with no build chain and no MCP slot. It is the lightest, most surgical tool in its cluster: a single `brew install` + `rtk init -g`, transparent via the PreToolUse hook, with a tee safety net for failures and built-in `rtk gain` analytics to verify the savings on your own projects. The maturity is strong (63.9K stars, an actual org with multiple contributors, Apache-2.0, peer-validated by headroom bundling it).

It stops short of ADOPT for two reasons. First, scope: rtk only compresses Bash command outputs and explicitly bypasses Claude Code's `Read`/`Grep`/`Glob` tools and all MCP/file/history context — so in file-read-heavy sessions its reach is partial unless you actively steer the agent to `rtk read`/`rtk grep`. Second, it is a strict subset of headroom, which bundles rtk and adds reversible compression across all content types; if you are already running headroom you get rtk's command rewriting for free and a standalone install is redundant. Choose rtk over headroom when you want exactly this narrow scope without headroom's heavy install and critical-path proxy. Skip it if your agent's context is dominated by file reads rather than shell output, or if you only use a provider's native compaction. It is complementary to caveman (output prose) and token-optimizer-mcp (MCP outputs), not a substitute.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [rtk](https://github.com/rtk-ai/rtk) | tool | CLI proxy that reduces LLM token consumption by 60-90% on common dev commands | Dev commands produce verbose output that wastes tokens | headroom, caveman, token-optimizer-mcp |
