# Evaluation: CLIProxyAPI

**Repo:** [router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)
**Stars:** 46,193 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT | ⚠️ provider-ToS gray-area
**Last verified:** 2026-09-14
**Last triaged:** 2026-09-14  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Go proxy exposing OpenAI/Gemini/Claude/Codex/Grok-compatible API endpoints over coding-agent CLI accounts via OAuth, with multi-account load-balancing.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (via `repo-metadata.json`, fetched 2026-08-04) plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — not previously examined; picked up as one of the oldest untriaged leads in the P3 backlog this pass.

## Triage note

P3 backlog. At ★46.2K this is one of the largest tools in the catalog — clearly significant, not a mechanical-disposition candidate. Its provider-ToS gray-area status (reusing CLI-subscription auth to serve an OpenAI-compatible API) is a real adoption caveat that a hands-on eval, not a bulk pass, should weigh. Left at discovery-log.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI) | tool | Go proxy exposing OpenAI/Gemini/Claude/Codex/Grok-compatible API endpoints over coding-agent CLI accounts via OAuth, with multi-account load-balancing (⚠️ provider-ToS gray-area) | Coding-agent CLI subscriptions are locked to their own clients; want to reach them from any SDK/tool through a standard API | claude-code-router |  |
