# Evaluation: llm-council

**Repo:** [karpathy/llm-council](https://github.com/karpathy/llm-council)
**Stars:** 21,052 | **Last updated:** 2026-06-19 | **License:** None (unlicensed)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Research & Discovery
**Layer:** Tooling

---

## What it does

A local web app that sends your query to multiple LLMs via OpenRouter, collects their responses, has each LLM rank the others' anonymized outputs, then asks a "Chairman" model to synthesize a final answer. Three-stage pipeline: (1) parallel first opinions, (2) anonymized cross-review with parsed rankings, (3) chairman synthesis. Built with FastAPI + React, stores conversations as JSON files.

The mechanism is straightforward: `council.py` orchestrates async parallel queries, anonymizes responses as "Response A/B/C/D", prompts each model to evaluate and rank, parses `FINAL RANKING:` blocks with regex, computes aggregate rankings, and feeds everything to a chairman model for synthesis.

## How we tested it

**Evidence:** REVIEW

Architecture review of the full codebase (6 backend Python files, React frontend). Read `council.py` (the core 280-line orchestration), `config.py` (model configuration), `openrouter.py` (API client). Did not run the app (requires OpenRouter API key with credits).

```
gh api repos/karpathy/llm-council/contents/backend/council.py --jq '.content' | base64 -d
gh api repos/karpathy/llm-council/contents/backend/config.py --jq '.content' | base64 -d
```

## What worked

- The 3-stage pipeline (collect → anonymized review → synthesis) is a genuinely useful pattern for high-stakes questions where model blind spots matter
- Anonymization during cross-review prevents models from playing favorites — a subtle but important design choice
- Aggregate ranking calculation across all models gives a quantitative signal beyond just "ask one model"
- Clean async implementation — parallel queries to all council members, no sequential bottleneck
- Default council (GPT-5.1, Gemini 3.0 Pro, Claude Sonnet 4.5, Grok 4) covers the major providers

## What didn't work or surprised us

- **No license** — legally unusable in commercial contexts; can't even redistribute modifications
- **Self-described "99% vibe coded" with "I'm not going to support it"** — the author explicitly disclaims any maintenance commitment
- **No MCP server, no CLI, no skill** — it's a standalone web app, not something that integrates into an agent workflow
- **4× the cost of a single query** (4 models × 3 stages = 12+ API calls per question) with no cost controls or budget limits
- **Ranking parser is fragile** — regex-based `FINAL RANKING:` extraction; models that deviate from the exact format silently produce empty rankings
- **No streaming** — must wait for all 12+ calls to complete before seeing any results
- **Not usable from Claude Code** — would need to be rewritten as an MCP server or skill to fit the workflow

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Cross-model verification catches individual model errors and hallucinations |
| Speed | - | 12+ sequential API calls (3 stages × 4 models) adds significant latency vs single query |
| Maintainability | neutral | Clean code but unmaintained by design; no tests |
| Safety | neutral | No safety-relevant features |
| Cost Efficiency | - | 4× minimum cost multiplier, higher with chairman synthesis stage |

## Verdict

**SKIP** — no licence, and dormant. GitHub reports **NONE** for
[`karpathy/llm-council`](https://github.com/karpathy/llm-council): the repo is live and declares no
grant, so the default is exclusive copyright and nothing here is adoptable whatever the ★22.5K says.
That is the same disposition `autoresearch` got in the long-tail pass — also karpathy, also
unlicensed.

Dormancy is the second half. Last pushed 2025-11-22, over eight months, which is consistent with
what the repo is: a demonstration of an idea rather than a maintained tool.

The idea does survive the SKIP, and it is a good one — several models answering independently, then
ranking each other's answers. This catalog already carries it in maintained, licensed form:
`design-council` (MIT) runs role-specialized peer agents over technical decisions, and
`claude-octopus` (MIT) enforces a real cross-provider consensus gate. Both are the way to reach the
pattern.

Re-open if a licence is added.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [llm-council](https://github.com/karpathy/llm-council) | tool | Multiple LLMs work together to answer the hardest questions | Single model has blind spots; committee of models is more reliable | design-council (similar multi-perspective approach) |
