# Evaluation: google-workspace-mcp

**Repo:** [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp)
**Stars:** ~2,700 | **Last updated:** 2026-06-18 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (MCP server)
**Layer:** Infrastructure

---

## What it does

A feature-complete Google Workspace MCP server giving AI assistants natural-language control of Gmail, Calendar, Drive, Docs, Sheets, Slides, Forms, Tasks, Contacts, and Chat — across all MCP clients, AI assistants, and developer tools.

Mechanically it exposes Workspace operations as MCP tools, with fine-grained editing (not just read), and is built for production/multi-user use: **remote OAuth 2.1 multi-user support**, stateless mode, and external auth server support, so an organization can host one secure instance centrally. It includes a full CLI and "Code Mode" for use with Claude Code/Codex, and claims the most extensive Workspace coverage of any such server (including Chat/Spaces), across all free Google accounts and Workspace plans.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the documented coverage (10 Workspace apps, fine-grained editing, OAuth 2.1 multi-user, stateless mode, CLI/Code Mode). Confirmed the breadth-and-auth positioning that distinguishes it from minimal Gmail/Calendar MCPs. Not connected to a live Workspace (which requires OAuth setup), so condition-gated.

```bash
gh api repos/taylorwilsdon/google_workspace_mcp --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/taylorwilsdon/google_workspace_mcp/readme --jq '.content' | base64 -d
```

## What worked

- **Breadth + fine-grained editing.** Covering 10 Workspace apps with real editing (not just read) lets agents actually do work in your Workspace, not just fetch data.
- **Org-hostable auth.** Remote OAuth 2.1 multi-user, stateless mode, and external auth support make it deployable for a whole team securely — a real differentiator over single-user MCPs.
- **CLI + Code Mode.** First-class use from Claude Code/Codex via a CLI and Code Mode, beyond just chat clients.

## What didn't work or surprised us

- **OAuth setup overhead.** Workspace OAuth (and multi-user/central hosting) is non-trivial to configure securely — budget setup time.
- **High-trust surface.** Granting an agent fine-grained Gmail/Drive/Docs write access is powerful and risky; scope credentials and review actions.
- **Marketing superlatives.** "Different class / most feature-complete in existence" is vendor framing — validate the specific operations you need.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Fine-grained, native Workspace operations vs. brittle scraping |
| Speed | + | Agents act directly on Workspace via MCP tools |
| Maintainability | + | Standard MCP + OAuth 2.1; org-hostable centrally |
| Safety | neutral | OAuth 2.1 is sound, but write access to mail/drive is high-trust — scope it |
| Cost Efficiency | + | Free/OSS; self-hostable, pay only model usage |

## Verdict

**CONDITIONAL**

Adopt when you want agents to act on Google Workspace (Gmail/Calendar/Drive/Docs/etc.) with fine-grained editing and need secure, org-hostable, multi-user OAuth — the most complete Workspace MCP available, with CLI/Code Mode for Claude Code/Codex. Budget OAuth setup and treat the write-access surface as high-trust (scope credentials, review actions). For single-user read-only needs, a lighter Gmail/Calendar MCP may suffice.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [google-workspace-mcp](https://github.com/taylorwilsdon/google_workspace_mcp) | MCP server | Most feature-complete Google Workspace MCP (MIT, ★2.7K) — natural-language control of Gmail/Calendar/Drive/Docs/Sheets/Slides/Forms/Tasks/Contacts/Chat across all MCP clients, with remote OAuth 2.1 multi-user, stateless mode, and CLI/Code Mode for Claude Code/Codex | Agents can't act on your Google Workspace; want secure, org-hostable, fine-grained Workspace access via MCP | github-mcp-server, ref-tools-mcp, firecrawl-mcp |
