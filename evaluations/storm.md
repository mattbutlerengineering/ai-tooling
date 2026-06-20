# Evaluation: storm

**Repo:** [stanford-oval/storm](https://github.com/stanford-oval/storm)
**Stars:** ~28,800 | **Last updated:** 2025-09-30 | **License:** MIT
**Dev loop stage:** Reflect (Research & Discovery)
**Layer:** Tooling

---

## What it does

STORM ("Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking") is an LLM-powered knowledge-curation system from Stanford OVAL. It researches a topic using internet search and writes a Wikipedia-like, **cited** full-length article from scratch.

Mechanically, STORM's distinctive move is **multi-perspective question asking**: it simulates different personas/perspectives interrogating the topic to surface a broader, more complete outline before drafting — then grounds the article in retrieved sources with citations. **Co-STORM** (EMNLP 2024) extends this to human-AI collaborative knowledge curation, letting a person steer the information-seeking. It's distributed as the `knowledge-storm` Python package (`pip install knowledge-storm`), supports multiple LLMs and retrievers (Bing/You/Vector RM, including grounding on your own documents via `VectorRM`), recently added litellm integration, and ships a Streamlit demo. The authors are explicit that output is a strong *pre-writing* draft, not publication-ready.

## How we tested it

Architecture review against the README and the documented pipeline (multi-perspective question asking → retrieval → outline → cited article; Co-STORM for human-in-the-loop). Confirmed the `knowledge-storm` package, multi-LLM/retriever support (incl. VectorRM grounding and litellm), and the honest "pre-writing, not publication-ready" framing. Last push ~2025-09 (mature, stable research codebase). Not run on a live topic, so condition-gated.

```bash
gh api repos/stanford-oval/storm --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/stanford-oval/storm/readme --jq '.content' | base64 -d
```

## What worked

- **Multi-perspective question asking is the differentiator.** Simulating personas to broaden the outline produces more complete coverage than a single-shot "write about X" prompt — a genuinely clever curation step.
- **Grounded + cited.** Retrieval-grounded with citations (and `VectorRM` for your own docs) makes outputs traceable, not hallucinated prose.
- **Honest scope + peer-reviewed.** The authors openly state it's a pre-writing aid; Co-STORM is EMNLP-published. Credible, not overhyped.

## What didn't work or surprised us

- **Not publication-ready.** By design, output needs editing; it's a research/pre-writing accelerator, not a finished-doc generator.
- **Search/LLM cost.** Multi-perspective questioning + retrieval spends tokens and search calls per article.
- **Overlaps deep-research / gpt-researcher.** Several tools auto-research and draft; STORM's edge is the perspective-driven outline and academic grounding.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Retrieval-grounded with citations; perspective coverage reduces blind spots |
| Speed | + | Automates hours of pre-writing research/synthesis |
| Maintainability | neutral | A generation tool; not part of a codebase |
| Safety | + | Citations make claims auditable rather than ungrounded |
| Cost Efficiency | neutral | Token + search cost per article; offset by time saved |

## Verdict

**CONDITIONAL**

Reach for STORM when you need a grounded, cited long-form draft on a topic — documentation, literature surveys, internal research briefs — and will edit the output. The multi-perspective outline and academic grounding set it apart from generic research agents. For the project's own deep-research workflow it overlaps the installed deep-research skill; STORM shines for Wikipedia-style synthesis with citations.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [storm](https://github.com/stanford-oval/storm) | tool | LLM knowledge-curation system (MIT, ★29K, by Stanford OVAL) — researches a topic via internet search + multi-perspective question asking and writes a Wikipedia-like, cited article; Co-STORM adds human-AI collaboration; `pip install knowledge-storm` | Writing a grounded long-form report means hours of search + synthesis; want an automated pre-writing pipeline with citations | deep-research, ARIS, PaperOrchestra, AutoResearchClaw |
