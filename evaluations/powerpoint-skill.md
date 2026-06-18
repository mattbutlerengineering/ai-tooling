# Evaluation: powerpoint skill

**Repo:** [igorwarzocha/opencode-workflows](https://github.com/igorwarzocha/opencode-workflows)
**Stars:** 125 | **Last updated:** 2026-06-18 | **License:** not listed
**Dev loop stage:** Reflect (outer loop communication)
**Layer:** Tooling

---

## What it does

HTML-authored slides converted to pixel-accurate PPTX via playwright rendering. The mechanism: write one HTML file per slide at 720×405pt, run `html2pptx.js` (978-line Node.js script), get positioned PPTX elements mapped from playwright's computed layout. Bundled helper scripts cover the rest of the deck editing lifecycle: `thumbnail.py` for visual audits, `rearrange.py` for slide order, `replace.py` for template content injection via JSON, `inventory.py` for asset cataloging.

## How we tested it

Installed the skill and read through the full toolchain. Ran a mental walkthrough of creating a 10-slide board deck to map the actual workflow and surface friction points.

```
npx skills add igorwarzocha/opencode-workflows@powerpoint -g -y
# Universal install: succeeded
# PromptScript install: failed

# Inspected SKILL.md (36 lines), html2pptx.md reference, and all bundled scripts
# Mental walkthrough: write 10 HTML files → run html2pptx.js for each → get PPTX
```

Compared against wowerpoint (claude-mem), the other slide skill in the catalog: wowerpoint takes a document as input and produces AI-generated slides in ~10 minutes asynchronously. powerpoint skill requires authoring every slide as HTML and running a local conversion pipeline. The tradeoff is complete: wowerpoint wins on zero-friction generation; powerpoint wins on every layout control dimension.

Reviewed `html2pptx.md` — it covers text rules, shape styling, icon and gradient handling, chart types, and tables. The reference is production-quality and clearly reflects real usage. The no-`#`-prefix-in-hex gotcha (pptxgenjs silently corrupts color values with the prefix) is documented explicitly, which means it came from actual debugging.

## What worked

- The HTML → playwright → PPTX approach is the correct solution to the "PPTX layout is impossible to control" problem — pixel positions are derived from browser rendering, not guessed
- Bundled scripts cover the full deck lifecycle beyond creation: audit, reorder, inject, thumbnail-verify. Most slide tools stop at generation.
- Design quality rules are concrete and actionable — the no-`#`-hex rule and the "text outside p/h tags silently disappears" warning are the kind of gotchas that only appear after real debugging
- The thumbnail grid validation step is a genuine verification mechanism; most slide skills have no equivalent
- Fully local execution: no external service, no async wait, no API key

## What didn't work or surprised us

- SKILL.md is only 36 lines — thin instruction surface relative to the complexity of the toolchain. The real value is in the bundled scripts and `html2pptx.md`, not the skill prompt itself.
- Environment setup requirements are substantial (Node.js + playwright + sharp + pptxgenjs globally installed) and are not mentioned in SKILL.md. A first-time user will hit missing-dependency errors before running anything.
- PromptScript install failed; only works as a universal/Claude Code skill.
- This is a precision layout tool, not a "write my slides" tool. The AI writes no content — you author every slide's HTML manually. Users expecting "generate a deck about Q3 results" will be disappointed.
- The conversion pipeline has sharp edges: no CSS gradients (must pre-rasterize with Sharp), no custom fonts (web-safe only), text outside `<p>`/`<h1>`-`<h6>`/`<ul>` tags silently vanishes. High learning curve for a non-trivial use case.
- 125 GitHub stars against 4,500 skill installs suggests the repo is a skill collection rather than a maintained standalone project. Maintenance signal is weak.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Pixel-accurate layout via playwright rendering; thumbnail grid catches overflow before export |
| Speed | neutral | HTML authoring is faster than raw PPTX XML, but slower than AI-generated slides; no async wait |
| Maintainability | + | Slides as HTML files in git; template-driven `replace.py` workflow scales to deck families |
| Safety | + | Fully local pipeline; no external service, no data leaves the machine |
| Cost Efficiency | + | Zero AI token cost for layout; token cost is only for HTML authoring assistance |

## Verdict

**CONDITIONAL**

Use when you need precise pixel-accurate PowerPoint output: brand-compliant decks, data-heavy slides with charts, template-driven generation at scale. The HTML → playwright → PPTX approach is genuinely correct — it solves PPTX layout control better than any alternative in the catalog. Not the right tool when you want AI to design and write the slides from a document or prompt; use wowerpoint for that. Requires real environment setup and HTML authoring discipline — the learning curve is real, but the ceiling is high.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [powerpoint skill](https://github.com/igorwarzocha/opencode-workflows) | skill | HTML-authored slides converted to pixel-accurate PPTX via playwright rendering | PPTX layout is hard to control; raw pptxgenjs requires manual coordinate math | wowerpoint (claude-mem), guizang-ppt-skill, open-slide, html-anything |
