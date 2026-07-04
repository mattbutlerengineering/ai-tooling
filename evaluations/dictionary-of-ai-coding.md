# Evaluation: dictionary-of-ai-coding

**Repo:** [mattpocock/dictionary-of-ai-coding](https://github.com/mattpocock/dictionary-of-ai-coding)
**Stars:** 2,273 | **Last updated:** 2026-06-05 | **License:** none declared
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Discover (outer loop)
**Layer:** Process

---

## What it does

A plain-English glossary of AI-coding terminology by Matt Pocock (Total TypeScript / AI Hero). It defines ~68 terms — model, token, harness, agent, context window, compaction, hallucination, attention degradation, MCP, AGENTS.md, grilling, sycophancy — each as its own source markdown file under `dictionary/`, grouped into themed sections (The Model; Sessions, Context Windows & Turns; Tools & Environment; Failure Modes; Handoffs; Memory and Steering, and more). The README is a generated artifact: `internal/generate-readme.ts` stitches the per-term files plus a curriculum ordering into a single navigable page with collapsible section tables of contents.

The editorial angle is its differentiator. The intro frames AI-coding jargon as partly "manufactured" confusion from "a VC-funded economy that benefits from keeping it hard to understand," and sets out to translate the vocabulary into terms a working developer can absorb in an afternoon. Entries are cross-linked (the *Harness* entry links to *Model*, *Agent*, *Tool call*, *Compaction*, etc.) and end with a *Usage* dialogue showing the term in a realistic conversation.

## How we tested it

**Evidence:** REVIEW

Source-grounded inspection only — we read the source files, not the rendered site. Pulled metadata, README, file tree, the full term list, one complete entry (`Harness.md`), and the build scripts via the GitHub API.

```
gh api repos/mattpocock/dictionary-of-ai-coding --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],license:.license.spdx_id}'
gh api repos/mattpocock/dictionary-of-ai-coding/commits --jq '.[0].commit.committer.date'
gh api repos/mattpocock/dictionary-of-ai-coding/contents/dictionary --jq '.[].name'   # 68 terms
gh api repos/mattpocock/dictionary-of-ai-coding/contents/dictionary/Harness.md --jq '.content' | base64 -d
gh api repos/mattpocock/dictionary-of-ai-coding/contents/package.json --jq '.content' | base64 -d
```

## What worked

- **Editorial quality is the highest of any reference glossary in the catalog.** The *Harness* entry is three substantial paragraphs that explain not just what a harness is but *why it matters for diagnosis* ("when behaviour differs, the model is often not the variable — the harness is"). This is teaching, not a one-line gloss.
- **Genuinely conceptual, not Claude-specific.** Terms like attention degradation, smart zone, compaction, parametric vs. contextual knowledge, and primary/secondary source are model-agnostic mental models that apply across any AI-coding harness — exactly the overloaded vocabulary our catalog flags as confusing.
- **Cross-linked and source-of-truth structured.** Each term is its own file; the README is generated (`npm run generate`), so the data is queryable and the rendered page stays consistent. Cross-links turn it into a small concept graph.
- **Authoritative author with distribution.** Matt Pocock has a 62K-developer audience; the dictionary is the open-source backing for aihero.dev's published version, which raises the bar on correctness and upkeep.
- **Usage examples ground each term.** The dialogue snippets ("Same model, why is Claude Code editing files and Claude.ai just answering?") show the term in the wild, which is rare for glossaries.

## What didn't work or surprised us

- **No license declared.** `license.spdx_id` is null. For a reference you'd quote or adapt, the absence of an explicit license is a real friction — reuse rights are unclear.
- **No GitHub description set.** Discovery relies entirely on the README; the API description field is null.
- **Smaller and slightly less fresh than its peers.** ~68 terms and last commit 2026-06-05 (two weeks before this eval) — healthy, but a fast-moving vocabulary will outrun a curated list, and it's the lowest-starred of the reference cluster (2.3K).
- **Reading vs. rendered.** We inspected source markdown; the intended experience is the generated README / aihero.dev page. The substance is in the files, but we did not evaluate the published reading experience.
- **Marketing seam.** The intro and a newsletter CTA are woven into the README; the content is strong enough to stand without the "manufactured confusion" framing, which some readers may find tendentious.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Shared, precise vocabulary reduces miscommunication when reasoning about agent behavior and failures |
| Speed | + | "Learnable in an afternoon" — fast ramp on the concepts behind diagnosis and context management |
| Maintainability | neutral | Glossary — no direct effect on a codebase |
| Safety | + | Failure-mode terms (hallucination, sycophancy, attention degradation) name risks so they can be guarded against |
| Cost Efficiency | + | Terms like cache tokens, compaction, and prefix cache explain *why bills are high* and how to manage context |

## Verdict

**ADOPT**

The reference glossary worth keeping open while you work. Unlike the catalog's awesome-list references (which point at tools), this builds the *conceptual* vocabulary — harness, attention degradation, compaction, parametric knowledge — that makes diagnosing agent behavior and managing cost legible. Editorial quality is exceptional: each entry teaches and cross-links rather than defining in one line, and the model-agnostic framing makes it broadly useful, not Claude-only. The only real caveats are the missing license (limits formal reuse) and the unset GitHub description; neither undercuts its value as the go-to terminology reference. Adopt as the canonical jargon source; cite it when onboarding others to AI-coding concepts.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [dictionary-of-ai-coding](https://github.com/mattpocock/dictionary-of-ai-coding) | reference | ~68 AI-coding terms explained in plain English, cross-linked, by Matt Pocock (2.3K stars) | Terms like "harness", "skill", "agent", "compaction" are overloaded and confusing | — |
