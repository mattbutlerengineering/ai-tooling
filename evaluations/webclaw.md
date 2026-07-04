# Evaluation: webclaw

**Repo:** [0xMassi/webclaw](https://github.com/0xMassi/webclaw)
**Stars:** 1,445 | **Last updated:** 2026-06-17 (pushed; created 2026-03-10) | **License:** ⚠️ AGPL-3.0 (strong copyleft)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Research & Discovery (web content acquisition for agents/RAG; feeds Plan/Implement)
**Layer:** Tooling (Rust CLI + MCP server + REST API + SDKs; hosted option at webclaw.io)

---

## What it does

webclaw **turns websites into clean Markdown, JSON, and LLM-ready context** — a web extraction engine for AI agents and RAG pipelines. Give it a URL and it returns content your tools can actually use, instead of the two bad outputs most scrapers give an agent: a blocked/login-walled/empty app shell, or raw HTML full of nav/scripts/ads/boilerplate.

```bash
webclaw https://example.com --format markdown   # clean markdown
webclaw https://docs.anthropic.com --format llm  # LLM-optimized text
```

It's available four ways from one open-source engine: a **CLI**, an **MCP server** (wire into Claude Code/Desktop, Cursor, Windsurf, OpenCode, Codex CLI via `npx create-webclaw`, which auto-detects clients and configures the server), a self-hostable **REST API**, and **SDKs**. Distribution is broad — Homebrew tap, prebuilt macOS/Linux/Windows binaries, Docker image, and `cargo install`. A hosted API (webclaw.io) exists for those who don't want to self-host. Core capabilities are scrape (single page), crawl (multi-page), and structured-data extraction, with main-content isolation to strip boilerplate.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No binary installed, no page scraped. Claims come from the repository (GitHub metadata, README usage/install/format examples, 30 tagged releases) — the project's own documentation, not observed extraction quality.

```bash
gh api repos/0xMassi/webclaw --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/0xMassi/webclaw/readme --jq '.content' | base64 -d   # formats, MCP/CLI/REST install, capabilities
gh api repos/0xMassi/webclaw/releases --jq 'length'              # 30
```

## What worked

- **Solves the right problem for agents.** "Clean main-content Markdown, not raw HTML or a blocked shell" is exactly what an agent or RAG pipeline needs; the dedicated `--format llm` output shows the LLM use case is first-class, not an afterthought.
- **Local-first, Rust, self-hostable.** A fast native engine you can run entirely on your own infra (CLI/binary/Docker) means no per-call API dependency and no data leaving your machine — a real advantage over hosted-only scrapers.
- **One engine, four surfaces.** CLI + MCP + REST + SDK from the same core, with `npx create-webclaw` auto-configuring MCP clients, makes it easy to slot into whatever you already run.
- **Actively maintained, broadly distributed.** 30 releases in ~3 months; Homebrew/Docker/binaries/cargo cover every platform.

## What didn't work or surprised us

- **AGPL-3.0 is a significant license caveat.** Strong copyleft with a network clause: if you self-host the server and expose it as a service, AGPL's source-availability obligations can extend to your modifications. Fine for internal/CLI/agent use; **read the license before embedding it in a product or SaaS.** Materially more restrictive than the MIT/Apache tools around it.
- **Open-core tension.** The hosted webclaw.io API is the commercial surface; expect the most convenient/robust path (anti-bot, scale) to favor the hosted tier, with self-hosting carrying more operational burden.
- **Scraping is inherently brittle and legally sensitive.** Anti-bot defenses, login walls, and rate limits are an arms race; extraction quality and "doesn't get blocked" claims are unverified here, and scraping responsibilities (robots/ToS) fall on the user.
- **Crowded niche.** Competes with markitdown (doc→Markdown), Agent-Reach (social/web access), and hosted extractors; differentiation is the local-first Rust engine + multi-surface delivery, not a new capability.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Clean main-content extraction gives agents better input than raw HTML/blocked shells, reducing garbage-in errors. |
| Speed | + | Native Rust engine, local, with crawl support — fast acquisition for RAG/agent context. |
| Maintainability | neutral | A content-acquisition dependency, not part of your codebase structure. |
| Safety | neutral / − | Local-first keeps data on your infra (+); AGPL-3.0 network copyleft is a legal constraint, and scraping carries ToS/robots responsibility (−). |
| Cost Efficiency | + / neutral | Self-host free (your compute); hosted tier is paid; avoids per-call costs of hosted-only scrapers. |

## Verdict

**SKIP** (license) — Disqualified by this catalog's permissive-OSS adoption bar (#36, ADR 0001): the license is **AGPL-3.0** (network copyleft — source-availability obligations can extend to a hosted service). License alone removes it from the adoptable set. _Prior technical assessment retained for reference — it would otherwise be CONDITIONAL:_ adopt if your agents or RAG pipelines need clean, LLM-ready web content and you want a fast, local-first, self-hostable engine that drops into MCP clients with one command. It's actively developed, broadly distributed, and purpose-built for agent consumption. Two real gates: **the AGPL-3.0 license** (vet carefully before embedding in any product/SaaS — internal/CLI/agent use is the comfortable zone), and the usual unverified scraping concerns (anti-bot robustness, ToS/robots compliance are on you). For doc/file conversion rather than live web pages, prefer markitdown; for social-platform reach, Agent-Reach.

Compared to neighbors: **markitdown** converts *files* (PDF/DOCX/…) to Markdown; **Agent-Reach** focuses on social/web platforms without paid APIs; webclaw is the **local-first, Rust web-page extraction engine** with MCP/CLI/REST/SDK delivery — the strongest "URL → clean agent context" option of the set, modulo its license.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [webclaw](https://github.com/0xMassi/webclaw) | tool | Local-first Rust web-extraction engine — URL → clean Markdown/JSON/LLM-text via CLI, MCP server, REST API, and SDKs (AGPL-3.0) | Scrapers hand agents blocked shells or boilerplate-laden raw HTML; need clean, LLM-ready content for RAG/agent context | markitdown, Agent-Reach, last30days-skill |
