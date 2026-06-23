# Evaluation: markitdown

**Repo:** [microsoft/markitdown](https://github.com/microsoft/markitdown)
**Stars:** 156,022 | **Last updated:** 2026-05-26 (pushed; created 2024-11-13) | **License:** MIT
**Dev loop stage:** Plan / Code Understanding — a pre-ingestion utility. It sits *upstream* of the agent loop: it turns PDFs, Office docs, images, audio, and HTML into Markdown so an LLM (or a retrieval index) can read them. It does not touch your source code; it conditions the *other* artifacts (specs, design docs, RFCs, transcripts) you want the agent to reason over.
**Layer:** Tooling (a Python library + `markitdown` CLI + an optional MCP server in `packages/markitdown-mcp`; runs locally with the privileges of the calling process)

---

## What it does

The repo description: "Python tool for converting files and office documents to Markdown." Built by Microsoft's AutoGen team, MarkItDown is a lightweight converter whose explicit goal is **LLM ingestion**, not human-facing fidelity. The README is blunt: output "is meant to be consumed by text analysis tools — and may not be the best option for high-fidelity document conversions for human consumption." It positions itself against `textract`, but with a focus on *preserving document structure* — headings, lists, tables, links — because mainstream LLMs natively "speak" Markdown and it is token-efficient.

Supported inputs (per README): PDF, PowerPoint, Word, Excel, images (EXIF + OCR), audio (EXIF + speech transcription), HTML, CSV/JSON/XML, ZIP (iterates contents), YouTube URLs, EPub, "and more." It is a monorepo of packages: `markitdown` (core), `markitdown-mcp` (an MCP server exposing the conversion to any MCP client — directly relevant to agent tooling), `markitdown-ocr` (a plugin adding OCR-augmented DOCX/PDF/PPTX/XLSX converters), and a sample plugin. Optional dependency extras (`[pdf]`, `[docx]`, `[pptx]`, `[az-doc-intel]`, `[az-content-understanding]`, `[audio-transcription]`, `[youtube-transcription]`) let you install only the format handlers you need. CLI is Unix-friendly: `markitdown file.pdf > out.md`, `-o` for output, and stdin piping.

## How we tested it

**Evidence:** MEASURED

**Ran hands-on** on 2026-06-22 (macOS arm64, Python 3.11.4) — **hands-on**, verified live. Installed `markitdown[all]` into a clean venv and converted **three different formats** — the repo's own 27,308-byte HTML deck, plus a generated XLSX and PPTX — capturing byte counts and structural fidelity for each. markitdown **0.1.6** installed and ran with no API key and no cloud calls (the formats tested are pure-local converters).

```bash
python3 -m venv /tmp/mk && /tmp/mk/bin/pip install 'markitdown[all]'   # clean install
/tmp/mk/bin/markitdown --version                                       # markitdown 0.1.6
```

**Test 1 — HTML (this repo's own slide deck).** `presentations/development-process/Development process.dc.html`:

```bash
/tmp/mk/bin/markitdown "presentations/development-process/Development process.dc.html" > out.md
#   input  27,308 bytes HTML  (exit 0, empty stderr)
#   output  2,318 bytes / 147 lines Markdown   →  ~91.5% reduction
```

The HTML/CSS/JS boilerplate was stripped while the document hierarchy survived intact: the top heading came through as `# Our development process`, and the six section headings as proper `## …` (`## One loop, six stages`, `## Plan and scope`, `## Build`, `## Review and integrate`, `## Ship and observe`, `## Principles`) — verified with `grep -nE '^#{1,6} '` on the output. The ordered stage list (`01 Plan … 06 Observe`) was preserved as text. Clean confirmation of the core claim: non-code artifact → structure-preserving, token-efficient Markdown.

**Test 2 — XLSX (Office spreadsheet path).** A 3-row sheet built with `openpyxl`, then converted:

```bash
/tmp/mk/bin/markitdown /tmp/sheet.xlsx          # exit 0, empty stderr
```
```markdown
## Q2
| Stage | Owner | Status |
| --- | --- | --- |
| Plan | Ana | done |
| Build | Lee | wip |
```

The worksheet name became an `## Q2` heading and the cells rendered as a correct GitHub-flavoured Markdown pipe table — header row, separator, and data rows all aligned. Table fidelity (the format most prone to degradation) was exact on this simple sheet.

**Test 3 — PPTX (Office slides path).** A one-slide deck built with `python-pptx`:

```bash
/tmp/mk/bin/markitdown /tmp/deck.pptx           # exit 0, empty stderr
```
```markdown
<!-- Slide number: 1 -->
# Dev Loop
Plan
Build
Review
```

The slide title became an `# ` heading, body bullets came through as text, and markitdown emitted an `<!-- Slide number: 1 -->` provenance comment — useful when feeding multi-slide decks to an agent.

**Measured results.** 3/3 formats converted with `exit 0` and empty stderr. HTML achieved ~91.5% byte reduction with full heading hierarchy preserved; XLSX produced an exact Markdown table; PPTX preserved slide structure with title-as-heading. This is a genuine run of the install command in `STACK.md`/`CATALOG.md` against real inputs across the three most common non-code formats. (PDF and OCR/audio/Azure paths were not exercised here; complex-table/multi-column PDF fidelity still varies per the README and remains unverified.) Prior source-only commands retained below for provenance:

```bash
gh api repos/microsoft/markitdown --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
# desc: "Python tool for converting files and office documents to Markdown" | 156022 stars | MIT
gh api repos/microsoft/markitdown/readme --jq '.content' | base64 -d | head -120
gh api "repos/microsoft/markitdown/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # monorepo: core, -mcp, -ocr, sample-plugin
gh api repos/microsoft/markitdown/commits --jq 'length'      # 30 (page-1 cap; very active)
gh api repos/microsoft/markitdown/releases --jq 'length'     # 19 tagged releases (PyPI-published)
gh api repos/microsoft/markitdown/contributors --jq '[.[].login]|length'  # 30+
```

## What worked

- **Exactly the right output target for LLMs.** Markdown is near-plain-text, structure-preserving, and token-efficient, and frontier models are heavily trained on it. Converting a 40-page PDF spec to Markdown before handing it to an agent is strictly better than pasting raw extracted text or asking the model to parse a binary it can't read.
- **Broad, practical format coverage in one tool.** PDF, the full Office trio, images-with-OCR, audio transcription, HTML, structured text, ZIP traversal, and YouTube transcripts — one CLI replaces a pile of bespoke extractors. The extras system keeps installs lean. Verified hands-on across HTML, XLSX, and PPTX — all three clean, no per-format flags needed.
- **Ships an MCP server out of the box.** `packages/markitdown-mcp` means an agent can convert documents as a tool call, not just a shell pipe — a clean fit for Claude Code / MCP-based harnesses, and a reason this could equally sit in the MCP Servers category.
- **Real maintenance and provenance.** Microsoft / AutoGen team, MIT-licensed, 19 tagged PyPI releases, pre-commit + tests CI workflows, OCR plugin, Dockerfile, devcontainer, and a published security section. This is engineered software, not a weekend script.
- **Honest about its own scope.** The README repeatedly disclaims human-grade fidelity and warns about untrusted input. That candor makes it easy to scope correctly.

## What didn't work or surprised us

- **It does not understand *code* — it is not a repomix/opensrc substitute.** This is the most important boundary. MarkItDown conditions *documents* (specs, slides, transcripts), not your repository. For feeding source to an agent, repomix (serialize repo), opensrc (dependency source), and context7 (live library docs) are the tools; MarkItDown is complementary, sitting beside them at the Plan/ingestion edge.
- **Fidelity is format-dependent; PDF/OCR paths unverified here.** Complex PDF tables, multi-column layouts, and figure captions are exactly where Markdown extraction degrades. The authors flag this; my run covered HTML/XLSX/PPTX (all clean) but not PDF or OCR. Treat PDF output as lossy until checked on your real documents.
- **Some "conversions" are heavyweight, not local string munging.** Audio transcription, OCR, and the Azure Document Intelligence / Content Understanding extras invoke models or cloud services — cost, latency, and an external dependency hide behind the same simple CLI. (The HTML/XLSX/PPTX paths I ran are pure-local and fast.)
- **A genuine security surface.** The README's prominent warning is warranted: `convert()` is permissive (local files, remote URIs, byte streams), so on untrusted input it can be steered to fetch internal/metadata URLs (SSRF) or arbitrary paths. The mitigation — call the narrowest `convert_local()`/`convert_stream()`, sanitize inputs — is real work the integrator must do.
- **Star count reflects "Microsoft + name + LLM hype," not a quality ceiling.** 156K stars on a converter is virality; it says the problem is widely felt, not that every format path is robust.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / − | Structured Markdown the model can actually read beats raw/binary input (verified: HTML headings, XLSX table, PPTX slide structure all preserved); but lossy extraction on complex tables/layouts can silently drop or mangle facts the agent then reasons on. |
| Speed | + | One CLI/MCP call replaces hand-rolled per-format extractors; pipes straight into a prompt or index. The HTML/XLSX/PPTX conversions were near-instant locally. Offset only by OCR/transcription/cloud paths. |
| Maintainability | neutral | A pre-processing utility outside your codebase — no effect on the maintainability of code you ship. |
| Safety | − | Permissive `convert()` is an SSRF / arbitrary-fetch surface on untrusted input; cloud extras add external data flow. Must scope to `convert_local`/`convert_stream` and sanitize. |
| Cost Efficiency | + / − | Markdown is token-cheap vs. dumping raw text (~91% byte reduction measured on the HTML deck); but OCR/audio/Azure paths incur compute or per-call cloud cost. |

## Verdict

**ADOPT (scoped) — the default doc→Markdown converter for agent ingestion, used deliberately.** MarkItDown does one upstream job well: turn the *non-code* artifacts your agent needs (PDFs, slides, Word docs, transcripts) into structure-preserving, token-efficient Markdown, via a clean CLI and a ready-made MCP server. Verified hands-on: a real 27 KB HTML deck collapsed to 2.3 KB of clean headed Markdown (~91% smaller), and the XLSX/PPTX paths produced a correct pipe table and a slide-structured heading respectively. It's Microsoft-maintained, MIT, released on a cadence, and honest about its limits. Adopt it as the standard converter at the Plan/Code-Understanding edge — but pin it to `convert_local()`/`convert_stream()` on untrusted input, verify PDF/OCR fidelity on your real documents, and remember it is *complementary* to, not a replacement for, the code-ingestion tools.

Compared to neighbors: it does **not** overlap with repomix or opensrc in function — those serialize *code* (your repo, your dependencies); MarkItDown serializes *documents*. context7 fetches live library docs over the network; MarkItDown converts files you already hold. The cleanest mental model is a pipeline: MarkItDown (arbitrary docs → Markdown) feeds the same prompt/index that repomix (repo), opensrc (deps), and context7 (live docs) populate. Within Code Understanding it earns a place as the missing "everything-else-becomes-Markdown" front door.

## Catalog entry

Target category: **Code Understanding**

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [markitdown](https://github.com/microsoft/markitdown) | tool | Converts PDF/Office/images/audio/HTML to structure-preserving Markdown for LLM ingestion; CLI + library + bundled MCP server | Agents can't read binary docs (PDF, DOCX, PPTX, audio) — need them as token-efficient Markdown before reasoning | repomix, opensrc, context7 (complementary: those ingest code/deps/docs, markitdown ingests arbitrary documents) |
