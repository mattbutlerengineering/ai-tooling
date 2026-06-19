# Evaluation: opendocswork-mcp

**Repo:** [Aimino-Tech/opendocswork-mcp](https://github.com/Aimino-Tech/opendocswork-mcp)
**Stars:** 149 | **Last updated:** 2026-06-16 (pushed; created 2026-05-26) | **License:** GPL-3.0 (README also claims MIT/Apache-2.0 — see flags)
**Dev loop stage:** Implement / Ship (generating and processing Office artifacts — reports, decks, spreadsheets, filled PDF forms)
**Layer:** Tooling (a Rust-native MCP server exposing document read/write/transform tools)

---

## What it does

The catalog one-liner (already in the catalog): "Rust-native Office document processing — Excel, Word, PowerPoint at sub-millisecond speed." The README brands it "office-oxide-mcp," "the open source Aspose," and adds PDF form-filling as a headline use case.

The mechanism: a single Rust binary that speaks MCP over stdio (or other transports) and exposes a broad tool suite for reading and writing Office formats without going through Python libraries or a headless Office install. Reads use `calamine` (XLSX), `rdocx`/`office_oxide` (DOCX/PPTX), and `lopdf` (PDF), parsing the ZIP+XML containers directly via `quick-xml` (zero-copy) and `zlib-ng` (SIMD). The toolset spans: **AI reading** (`office_read` → Markdown/JSON/chunks/text, `excel_schema`, `coherence_check`); **Excel write** (create, write cell/range, format, charts, pivots, sheets, conditional formatting); **Word write** (create, md→docx, replace, styles, tables, images, headers/footers, TOC, comments, tracked-changes accept); **PPT write** (create, slides, layouts, text boxes, charts, images); **PDF** (read, list/fill AcroForm+XFA fields, analyze layout, overlay text at coordinates on flat/scanned PDFs, export). It also ships a "Skills System" (`skill_run`/`skill_list`/`skill_register`) and a "Coherence Engine" (`office_propagate_edit`, `office_check_consistency`) backed by an entity DAG with BFS propagation and stale detection — the latter is the genuinely novel claim: edit one value and have dependent cells/fields update consistently. Installs via `cargo install office-oxide-mcp` or a release binary; configured into Claude Desktop / Cursor / VS Code as a stdio server.

## How we tested it

**Source-grounded inspection — not installed, not run.** No `cargo install`, no binary executed, no document read/written, no PDF form filled. All claims below come from the repository (GitHub metadata, README, file tree, `Cargo.toml` presence, commit/release counts). The performance benchmark table (e.g. "~46× faster PPTX read", "<50ms cold start") is **the author's self-reported benchmark from the README — not measured by me**, and the comparison baselines (openpyxl, FastMCP) are unverified.

```bash
gh api repos/Aimino-Tech/opendocswork-mcp --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id,lang:.language}'
gh api repos/Aimino-Tech/opendocswork-mcp/readme --jq '.content' | base64 -d
gh api "repos/Aimino-Tech/opendocswork-mcp/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/Aimino-Tech/opendocswork-mcp/commits --jq 'length'        # 18 (default page)
gh api repos/Aimino-Tech/opendocswork-mcp/releases --jq 'length'       # 0
gh api repos/Aimino-Tech/opendocswork-mcp/contributors --jq '[.[].login]'  # 2 (xdnaimino, tamnguyen08)
```

## What worked

- **Native Rust, no Python/Office dependency.** Reading/writing Office formats by parsing the ZIP+XML directly avoids the openpyxl/python-docx/python-pptx stack and any headless LibreOffice. For an agent that just needs to emit a spreadsheet or deck, a single fast binary is an attractive, dependency-light footprint.
- **Genuinely broad write surface.** Most "Office MCP" servers are read-only or Excel-only. This covers create/format/chart/pivot for Excel, full Word authoring including TOC and tracked-changes acceptance, and PPTX slide construction — plus a real showcase directory of generated XLSX/DOCX/PPTX artifacts checked into the repo (verifiable evidence the write path produces files).
- **PDF form-filling is a strong, concrete niche.** AcroForm + XFA field fill, field listing, layout analysis, and coordinate-based text overlay for *flat/scanned* PDFs is a real, painful problem (repetitive bureaucratic forms) that few MCP servers address. The "LLM reads the form, you approve, it fills" flow is well-scoped.
- **Coherence Engine is the differentiator.** An entity DAG with BFS propagation and stale detection (`office_propagate_edit`/`office_check_consistency`) is more ambitious than a dumb writer — if it works, editing a source value and propagating it through a document is a real Correctness/Maintainability lever for generated reports.
- **Local-first.** Operates on local files via stdio; no document content leaves the machine through the server itself, which is the right posture for sensitive business documents.

## What didn't work or surprised us

- **Identity is confused — naming and license both inconsistent.** The repo is `opendocswork-mcp`, the README titles it `office-oxide-mcp`, the install command is `cargo install office-oxide-mcp`, and several links point at a separate `Aimino-Tech/office-oxide-mcp` repo. **The license contradiction is internal to the repo, not just the README (verified in source):** the `LICENSE` file is the full **GPL-3.0** text (and GitHub classifies the repo GPL-3.0), while `Cargo.toml` declares `license = "MIT OR Apache-2.0"`. So the LICENSE file and the package manifest disagree outright. GPL-3.0 is copyleft and materially different from MIT/Apache; until the maintainer reconciles the two, a consumer should treat it as **GPL-3.0 (the most restrictive, and what the LICENSE file actually says)**. This is a real, unresolved adoption blocker for any redistribution or proprietary use.
- **Self-reported benchmarks, no independent verification.** The "~10–46× faster than Python / <50ms cold start" table is the author's own; baselines and methodology aren't reproducible from the repo. Treat as a marketing claim, not a measured result.
- **Demo/placeholder tools shipped in the public toolset.** `increment` and `get_value` ("counter (demo)") are listed in the tool overview — a sign the tool surface isn't fully curated for production.
- **Low maturity: 0 releases, 2 authors, ~3 weeks old.** Created 2026-05-26, 18 commits, **zero GitHub releases/tags** despite a `cargo install` instruction (so the install path depends on crates.io publishing that the repo doesn't tag). Two contributors. The ambition (six formats + PDF + skills + coherence DAG) is large relative to the team and age — high surface, thin track record.
- **Overlap with existing catalog tools.** Directly overlaps the catalog's **powerpoint** and **powerpoint-ppt** skills (deck creation) and competes with Python-based document tooling teams may already run; its edge is speed and breadth, not a unique capability except the PDF-form and coherence pieces.
- **Safety: file-write reach.** It writes to arbitrary `output_path`s and overlays/fills PDFs — a misdirected agent can clobber files or produce incorrect filled forms. Lower blast radius than a network tool, but it is a write-capable local tool, not a read-only one.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Coherence Engine (entity DAG + stale detection) targets consistent propagation of edits across a document; offset by unverified maturity and demo tools still in the suite. |
| Speed | + | Native Rust ZIP+XML parsing (calamine/quick-xml/zlib-ng) is plausibly much faster than openpyxl/python-pptx and a single binary has near-zero cold start — though the specific multipliers are self-reported. |
| Maintainability | neutral | A dependency-light single binary is easy to operate; but generated documents themselves aren't more maintainable, and the license/naming confusion adds operational risk. |
| Safety | neutral / - | Local-first (content stays on machine) is a plus, but it writes to arbitrary output paths and fills/overlays PDFs — a write-capable tool an errant agent can misuse. |
| Cost Efficiency | + | No API/LLM cost in the server itself; fast local processing avoids cloud document services (and Aspose-style per-document licensing). |

## Verdict

**CONDITIONAL** — adopt when you specifically need fast, local, dependency-light Office *writing* from an agent (generating XLSX/DOCX/PPTX reports or decks) or **PDF form-filling**, AND you have first resolved the GPL-3.0-vs-MIT/Apache license conflict for your use case. For read-only or occasional document needs, an existing Python tool or the catalog's `powerpoint` skills are lower-risk given this project's age and zero releases.

Compared to neighbors: the catalog's **powerpoint** and **powerpoint-ppt** entries cover deck creation but are PPTX-focused and Python/MCP-based; opendocswork-mcp is broader (six Office formats + PDF) and faster (native Rust), and adds two capabilities those lack — coordinate-level PDF form-filling and an edit-propagation coherence engine. That breadth and the PDF niche are the reason to consider it. But it is not an ADOPT: a 3-week-old, 2-author project with zero tagged releases, demo tools in the public surface, and a self-contradicting license is too unsettled to default to. Pilot it on the PDF-form/Office-generation use case behind output review, and re-evaluate once releases and licensing stabilize.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [opendocswork-mcp](https://github.com/Aimino-Tech/opendocswork-mcp) | MCP server | Rust-native Office (Excel/Word/PowerPoint/PDF) read+write MCP server — fast, local-first, with PDF form-filling and an edit-propagation coherence engine | AI agents can't natively read or write Office documents or fill PDF forms without a heavy Python/Office stack | powerpoint, powerpoint-ppt (complementary: those create PPTX decks, opendocswork covers six formats + PDF in native Rust) |
