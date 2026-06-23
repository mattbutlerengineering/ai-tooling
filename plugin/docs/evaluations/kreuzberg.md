# Evaluation: kreuzberg

**Repo:** [kreuzberg-dev/kreuzberg](https://github.com/kreuzberg-dev/kreuzberg)
**Stars:** ~8,500 | **Last updated:** 2026-06-20 | **License:** source-available (repo SPDX returns NOASSERTION)
**Dev loop stage:** Implement (document ingestion for RAG / Memory & Context)
**Layer:** Infrastructure

---

## What it does

A polyglot document-intelligence framework with a Rust core that extracts text, metadata, transcripts, and **code intelligence** from messy real-world documents at native speed without a GPU.

Per the README: it handles **96 file formats** (PDF, Office, images, HTML, XML, email, archives, academic formats); extracts **code intelligence** (functions, classes, imports, symbols, docstrings) from **306 programming languages** via tree-sitter with semantic chunking; does **audio/video transcription** (Whisper ONNX, offline-capable); supports OCR (Tesseract incl. WASM, PaddleOCR, EasyOCR, and VLM OCR via GPT-4o/Claude/Gemini/Ollama); and offers structured JSON extraction with schema constraints plus embeddings via 143 LLM providers (including local engines). It runs as a library (native bindings for 15 languages), CLI, REST API, or **MCP server**. The pitch: clean, structured input for RAG/agents from any document, fast and locally.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the feature matrix (96 formats, 306-language code intelligence via tree-sitter, OCR backends, transcription, schema extraction, library/CLI/REST/MCP deployment). Confirmed the Rust-core/GPU-free positioning and the multi-format + code-aware extraction. License resolves to NOASSERTION via the API — confirm exact terms before commercial use. Not run on live documents, so condition-gated.

```bash
gh api repos/kreuzberg-dev/kreuzberg --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/kreuzberg-dev/kreuzberg/readme --jq '.content' | base64 -d
```

## What worked

- **Broad, fast, GPU-free extraction.** 96 formats with a Rust core and SIMD/parallelism is a strong ingestion layer for RAG — the unglamorous-but-critical "get clean text out of any document" problem.
- **Code intelligence is a differentiator.** Tree-sitter-based function/class/symbol extraction across 306 languages (with semantic chunking) makes it useful for code-RAG, not just prose documents.
- **Flexible deployment incl. MCP.** Library/CLI/REST/MCP means agents can call it directly, and the polyglot bindings fit any stack.

## What didn't work or surprised us

- **License unresolved.** NOASSERTION via the API — pin the exact terms before relying on it commercially.
- **Extraction quality varies.** OCR/VLM and exotic-format extraction are inherently lossy; validate output on your document mix.
- **Overlaps RAG ingestion in LightRAG/cocoindex.** It's the extraction layer feeding retrieval; pair with a RAG/index tool rather than expecting end-to-end retrieval.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Clean, structured text/metadata improves downstream RAG grounding |
| Speed | + | Rust core, GPU-free, SIMD/parallel; fast multi-format extraction |
| Maintainability | + | One framework for 96 formats vs. stitching per-format parsers |
| Safety | + | Local processing (no GPU/cloud needed); data stays on machine |
| Cost Efficiency | + | GPU-free local extraction avoids hosted document-AI costs |

## Verdict

**CONDITIONAL**

Adopt as the document-ingestion layer when you need clean text, metadata, and structure (including code intelligence) from many formats to feed RAG or agents — fast and locally, without a GPU. Pin the license terms first, and validate OCR/VLM output quality on your document mix. Pair with a retrieval/index tool (LightRAG/PageIndex); kreuzberg is the extraction front-end, not end-to-end RAG.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [kreuzberg](https://github.com/kreuzberg-dev/kreuzberg) | tool | Polyglot document-intelligence framework (Rust core, ★8.5K; SPDX unverified) — extract text, metadata, transcripts (Whisper), and code intelligence (tree-sitter, 306 langs) from 96 formats; OCR + 143 LLM providers; library/CLI/REST/MCP | RAG/agents need clean text + structure from messy documents; want fast, GPU-free, multi-format extraction with OCR and code parsing | LightRAG, PageIndex, cocoindex-code, ref-tools-mcp |
