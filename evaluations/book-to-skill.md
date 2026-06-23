# Evaluation: book-to-skill

**Repo:** [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill)
**Stars:** 6,047 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Plan / Implement
**Layer:** Tooling

---

## What it does

A Claude Code skill (also works with GitHub Copilot CLI and Amp) that converts PDF, EPUB, DOCX, Markdown, HTML, RTF, and MOBI files into structured agent skills. Running `/book-to-skill your-book.pdf` produces a full skill directory: a ~4,000-token `SKILL.md` with core mental models and a chapter index, on-demand chapter files (~1,000 tokens each), a glossary, a patterns file, and a cheatsheet. Chapter files load only when you ask about that topic — the full book never sits in context.

The mechanism is a 10-step pipeline: validate inputs → detect book type (technical vs prose) → extract text via Python parsers (Docling for technical PDFs with tables/code, pdftotext for prose) → analyze structure → generate per-chapter summaries → generate supporting files → write skill to disk → cleanup. A fold-in mode (Mode 4) lets you update an existing skill with new material by merging chapters, glossaries, and patterns.

## How we tested it

**Evidence:** REVIEW

Architecture review of the SKILL.md (634 lines), Python extraction package (`book_to_skill/` with 7 format-specific parsers), test suite, benchmarking tools, and README. Did not run a full conversion (no test PDF on hand), but assessed the extraction pipeline code, quality rules, output format, and discovery-tax benchmarks.

```bash
gh api repos/virgiliojr94/book-to-skill --jq '.description, .stargazers_count, .updated_at, .license.spdx_id'
gh api repos/virgiliojr94/book-to-skill/contents/SKILL.md --jq '.content' | base64 -d | wc -l
# 634-line SKILL.md with 10 steps, 4 modes of operation, 8 quality rules
```

## What worked

- **On-demand loading is well-designed.** The SKILL.md core (~4K tokens) plus one chapter (~1K) is 24–51× cheaper than context-dumping the whole book, per their measured benchmarks. The topic index routes Claude to the right chapter file without scanning the full text.
- **Real extraction infrastructure.** Not just a prompt — ships a Python package with 7 format-specific parsers (PDF via Docling/pdftotext/PyPDF2/pdfminer, EPUB via ebooklib, DOCX, HTML, RTF, MOBI via Calibre), a `--check` command for dependency validation, and a pytest suite.
- **Quality rules are specific and correct.** "Extract structure, not summaries" and "never copy raw book text" prevent the most common failure mode (skill becomes a bad summary). "Preserve the author's precision" prevents framework name drift. "Practitioner voice" ensures output is actionable ("Use X when Y" not "The book explains X").
- **Fold-in mode for iterative knowledge building.** Mode 4 lets you add new papers or chapters to an existing skill, merging glossaries and chapter indices. This is how a research cluster grows over time — genuinely novel compared to one-shot converters.
- **Cross-agent portability.** Follows the open Agent Skills standard. One skill works with Claude Code, Copilot CLI, and Amp without modification.

## What didn't work or surprised us

- **Not hands-on tested.** The pipeline is code-reviewed but not run through a full conversion in this evaluation. The extraction code and benchmarks look legitimate, but the quality of generated skills depends on Claude's synthesis quality during the conversion step.
- **~$1/book conversion cost.** A 400-page book costs roughly $1 in Claude API tokens to convert. Not expensive, but the user needs to understand this isn't free — the extraction invokes the LLM for analysis and summarization.
- **Chapter auto-detection requires explicit headings.** Books using section titles or roman numerals instead of "Chapter N" patterns won't auto-segment cleanly. The README is honest about this limitation.
- **Python dependency surface.** Full capability requires Docling, ebooklib, beautifulsoup4, python-docx, striprtf, and optionally Calibre. The `--check` command helps, but it's a heavier install than most skills.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Grounded answers from actual book content prevent hallucination about frameworks and chapter locations |
| Speed | + | 24–51× fewer tokens per query vs context-dumping; answers without PDF navigation loops |
| Maintainability | + | Knowledge persists as versioned files; fold-in mode keeps skills current as new material arrives |
| Safety | neutral | No security implications; copyright responsibility stays with the user |
| Cost Efficiency | + | ~$1 one-time conversion amortized across all future sessions vs recurring per-session token cost |

## Verdict

**CONDITIONAL**

Use when you repeatedly reference the same technical books, internal docs, or research papers across coding sessions. The compile-once-query-forever model pays back quickly for books you'd otherwise re-read or context-dump. Skip for one-off reads where a plain PDF agent is sufficient. The Python dependency chain and ~$1 conversion cost are minor but real barriers.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [book-to-skill](https://github.com/virgiliojr94/book-to-skill) | skill | Turn any technical book PDF into a Claude Code skill for reference while working | Want domain knowledge from a book available as agent context without manual extraction | gentleman-book-mcp (complementary: gentleman = fixed book, book-to-skill = any book) |
