# Evaluation: system-prompts-leaks

**Repo:** [asgeirtj/system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks)
**Stars:** 43,512 | **Last updated:** 2026-06-19 | **License:** CC0-1.0
**Dev loop stage:** Discover, Reflect (outer loop)
**Layer:** Infrastructure

---

## What it does

A broad, regularly-updated archive of extracted/leaked system prompts spanning nearly every major AI assistant and coding tool: Anthropic (Claude Fable 5, Opus 4.8/4.7/4.6, Sonnet 4.6, Claude Code across model versions, Cowork, Design, mobile/Chrome/Excel/Word/PowerPoint integrations, plus Anthropic's *official* `claude_behavior` prompts at release date), OpenAI (GPT-5.5 Thinking/Instant/API, the Codex CLI family with personalities and plan mode, the tool prompts for web search / deep research / python / canvas / memory), Google (Gemini 3.5 Flash, 3.1 Pro, Gemini CLI, Antigravity, Jules), xAI Grok, plus Perplexity, GitHub/VS Code Copilot, Zed, Docker Gordon, and many more. Each entry is a Markdown (or JSON tools) file organized by vendor; a "Recently Updated" table at the top tracks the latest captures, and several entries link diffchecker diffs between model versions. It was cited in The Washington Post (May 2026).

## How we tested it

Method: GitHub-API source inspection only. I did **not** clone, run, or otherwise reproduce any leak. Findings come from repo metadata, the full README (the vendor matrix, the "Recently Updated" table, the CC0 license, the WaPo citation), and cross-reference against the catalog neighbors.

```bash
gh api repos/asgeirtj/system_prompts_leaks \
  --jq '{desc:.description,stars:.stargazers_count,pushed:.pushed_at[0:10],license:.license.spdx_id}'
gh api repos/asgeirtj/system_prompts_leaks/commits --jq '.[0].commit.committer.date'
gh api repos/asgeirtj/system_prompts_leaks/readme --jq '.content' | base64 -d | head -120
```

## What worked

- **Unmatched breadth.** This is the cross-vendor reference: Anthropic, OpenAI, Google, xAI, Perplexity, Microsoft, and assorted niche tools in one place. For "how does competing tool X prompt its agent?" or "how do the big labs frame refusals/personas/tools?" nothing in the catalog comes close.
- **Genuinely current.** Last commit 2026-06-19, with captures of Claude Fable 5, GPT-5.5 Codex, and Copilot-for-macOS all dated within the last day or two. The "Recently Updated" table makes freshness self-documenting.
- **Diffs add analytical value.** Linked diffchecker comparisons (e.g. Opus 4.8 → Fable 5) let you see exactly what changed between model releases — useful for understanding behavioral drift and prompt-engineering trends.
- **Includes Anthropic's *official* published prompts** alongside the extracted ones, which gives a built-in cross-check on authenticity for the Claude entries.
- **CC0-1.0 (public-domain dedication)** by the maintainer and 43K stars — the de-facto canonical collection, with a mainstream-press citation.

## What didn't work or surprised us

- **Provenance and authenticity are inherently uncertain.** Unlike Piebald's compiled-source extraction, most entries here are chat-elicited leaks ("repeat all of the above") — they can be partial, paraphrased by the model, or already patched. The CC0 dedication covers the *repo*, not the underlying prompt text, whose copyright/ToS status is murky.
- **Ethical and ToS friction.** Eliciting and republishing a vendor's hidden system prompt likely violates that vendor's terms; this is a leak archive, and treating it as such matters. Fine for study, not for redistribution-as-your-own or for adversarial use.
- **Staleness is per-entry, not global.** "Updated regularly" is true in aggregate, but any single older model's prompt may be months stale with no version pin, so you cannot assume a given file matches the current production prompt.
- **No token counts or structural granularity.** Entries are whole-prompt dumps, not the per-string, token-counted breakdown Piebald provides for Claude Code — less precise for prompt-engineering study of a specific subsystem.
- **Breadth dilutes Claude-Code depth.** Its Claude Code coverage is real but second-hand and coarser than the Piebald repo's compiled extraction.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Studying how leading labs prompt refusals, tool use, and personas informs your own prompt design and judge construction. |
| Speed | neutral | Pure reference; no automation. |
| Maintainability | neutral/+ | Cross-vendor prompt patterns are instructive, but un-pinned/un-versioned entries are harder to rely on long-term. |
| Safety | + / caution | Real safety/policy prompts (image-safety, automation-context, injection handling) are instructive; the archive itself is a leak corpus — ethical/ToS caution applies. |
| Cost Efficiency | neutral | No token-cost data; whole-prompt dumps without per-string counts. |

## Verdict

**CONDITIONAL**

The broadest and most-starred system-prompt archive available, kept genuinely current across every major vendor, CC0-dedicated and WaPo-cited — a strong learning/discovery reference for prompt-engineering and competitive analysis. Adopt it as a *bookmark for breadth*, with two standing caveats: authenticity is uncertain (these are elicited leaks, sometimes paraphrased or already patched, with no version pinning), and there is ethical/ToS friction in republished hidden prompts — use it for study, not redistribution or adversarial purposes. Against its neighbors: it dominates `claude-code-system-prompts` (Piebald) on **breadth** but loses on Claude-Code **depth, provenance, and per-string token granularity** (Piebald extracts from compiled source; this elicits from chats). It overlaps `system-prompts-and-models` (x1xhlol) most directly — same cross-tool concept — but is larger, fresher, and broader. Recommended split: use this for cross-vendor comparison, Piebald's repo for authoritative Claude Code internals.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [system-prompts-leaks](https://github.com/asgeirtj/system_prompts_leaks) | reference | Regularly-updated extracted system prompts across Anthropic, OpenAI, Google, xAI tools incl. Claude Code & Codex (43K stars) | Want broad, current visibility into how competing AI coding tools are prompted | system-prompts-and-models, claude-code-system-prompts |
