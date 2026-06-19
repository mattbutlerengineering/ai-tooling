# Evaluation: claude-code-system-prompts

**Repo:** [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts)
**Stars:** 11,225 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Discover, Reflect (outer loop)
**Layer:** Infrastructure

---

## What it does

A continuously-updated, exhaustive extraction of *every* string Claude Code uses as a prompt — pulled directly from the compiled npm package, not guessed or reconstructed. As of Claude Code v2.1.182 (June 18, 2026) it covers 515 prompts (up from 350 a week earlier), each shipped as an individual Markdown file with a measured token count: the main system prompt, all 27 builtin tool descriptions (`Write`, `Bash`, `TodoWrite`, `Glob`, `Grep`, etc.), sub-agent prompts (Explore, Plan-mode-enhanced), the creation assistants (agent-creation architect, CLAUDE.md creation, statusline-setup), the slash-command prompts (`/code-review` in nine parts, `/security-review`, `/simplify`, `/batch`, `/schedule`, `/review-pr`), and the AI-powered utilities (conversation summarization/compaction, session-title generation, bash-command description writer, bash-command prefix/injection detection, memory-file selection, "dream" memory consolidation and pruning).

It also maintains a `CHANGELOG.md` tracking prompt changes across 214 Claude Code versions since v2.0.14, and is updated "within minutes of each release," with GitHub releases that notify stargazers. It is from the team behind Piebald (an agentic IDE) and the sibling tool [tweakcc](https://github.com/Piebald-AI/tweakcc), which patches these exact strings in a local install.

## How we tested it

Method: GitHub-API source inspection only. I did **not** clone the repo, run the extraction script, or diff against a live Claude Code install. Findings come from repo metadata, the full README (the 515-prompt matrix, per-prompt token counts, the extraction-from-compiled-source claim, the v2.1.182 freshness note), and cross-reference against the catalog neighbors.

```bash
gh api repos/Piebald-AI/claude-code-system-prompts \
  --jq '{desc:.description,stars:.stargazers_count,pushed:.pushed_at[0:10],license:.license.spdx_id}'
gh api repos/Piebald-AI/claude-code-system-prompts/commits --jq '.[0].commit.committer.date'
gh api repos/Piebald-AI/claude-code-system-prompts/readme --jq '.content' | base64 -d | head -120
```

## What worked

- **Provenance is the whole story.** These are extracted from the compiled JS, so they are "guaranteed to be exactly what Claude Code uses" — not a leak, not a jailbreak, just decompilation of a freely-distributed npm artifact. That removes the authenticity doubt that hangs over chat-leak collections.
- **Granularity is exceptional.** 515 separately-named files with token counts each, not one blob. You can study just the `/code-review` finder-angle/verification design, or just the bash prefix-injection detector, in isolation — directly useful as a prompt-engineering reference for anyone building agent harnesses, sub-agent dispatch, or LLM-as-judge verification loops.
- **Best-in-class freshness for the Claude-Code slice.** Updated within minutes of each release, pinned to a named version, with a 214-version changelog. Nothing else in the catalog tracks Claude Code's internals this tightly.
- **Maps onto the user's own stack.** The extracted `/code-review`, `/security-review`, `/simplify`, and statusline-setup prompts are the literal source of skills the user already runs — reading them clarifies how those tools actually behave under the hood.
- **MIT licensed**, low ethical friction (own-tool decompilation), actively maintained, mentioned in Awesome Claude Code.

## What didn't work or surprised us

- **Narrow by design — Claude Code only.** No coverage of competing tools (Cursor, Codex, Gemini CLI) or the underlying claude.ai model prompts. For cross-tool comparison you need a broader collection (see Verdict).
- **Reference, not a tool you "run."** Value is purely study/learning; there is no install-and-use loop. The companion `tweakcc` is the actionable piece, and it lives in a separate repo.
- **Decompiled prompts contain interpolation artifacts.** The README warns that many prompts embed runtime variables (tool-name references, available-subagent lists), so the static token counts drift ±~20 tokens from a live session and the text is not always verbatim-final.
- **Inherent staleness risk between releases.** Because it pins to a version, a prompt you study may already be superseded; the changelog mitigates this but you must check the pinned version against your installed one.
- **Reading internal prompts can mislead.** They encode Anthropic's harness assumptions (tool set, dispatch model), not transferable best practice — copying them wholesale into your own agent would import coupling you don't have.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Studying the actual `/code-review` verification phases and bash-injection detector informs how to design reliable agent prompts and judges. |
| Speed | neutral | Pure reference; no automation or workflow acceleration. |
| Maintainability | + | Reveals how Claude Code structures sub-agent and utility prompts — useful when building your own maintainable harness prompts. |
| Safety | + | Includes the real bash command-prefix/injection-detection and `/security-review` prompts — concrete, current examples of safety prompting. |
| Cost Efficiency | + | Per-prompt token counts make the context cost of each Claude Code subsystem legible. |

## Verdict

**CONDITIONAL** (lean ADOPT as a bookmark)

The most authoritative, freshest, most granular reference for Claude Code's internal prompts that exists — extracted from compiled source rather than leaked, MIT-licensed, version-pinned, and updated within minutes of each release. The catch is scope: it is Claude-Code-only and is a study artifact, not a runnable tool, so it earns CONDITIONAL rather than ADOPT. Bookmark and consult it when designing your own agent/sub-agent prompts, when investigating how a Claude Code skill behaves, or when reading the changelog after an upgrade. Against its neighbors: `system-prompts-leaks` (asgeirtj, CC0, 43K stars) and `system-prompts-and-models` (x1xhlol) are far **broader** (Anthropic + OpenAI + Google + xAI) but their Claude Code coverage is thinner and second-hand; this repo wins decisively on Claude-Code depth, provenance, and freshness. Use this one for "how does Claude Code work?" and the broad collections for "how do competing tools compare?"

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | reference | All 515 of Claude Code's prompts extracted from compiled source, version-pinned with token counts and a 214-version changelog | Want authoritative, current visibility into Claude Code's internal architecture and prompts | system-prompts-and-models, system-prompts-leaks, learn-claude-code |
