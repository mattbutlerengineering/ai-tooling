# Evaluation: CLIProxyAPI

**Repo:** [router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)
**Stars:** 46,193 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Last verified:** 2026-08-28
**Last triaged:** 2026-08-28  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

A Go proxy exposing OpenAI/Gemini/Claude/Codex/Grok-compatible API endpoints over coding-agent CLI accounts via OAuth, with multi-account load-balancing. Its own CATALOG one-liner flags it as ⚠️ provider-ToS gray-area — it routes SDK/tool traffic through subscription accounts rather than metered API keys.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the disposition below, which turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Overlaps cell names `claude-code-router` only, which is not a STACK pick, so this lead falls in the P3 backlog band with no structural signal to act on. The provider-ToS gray-area flag already disclosed in its CATALOG one-liner is a reason a human might SKIP it on a hands-on pass, but is not itself a mechanical P4 ground (no vendored-license issue — MIT, and it's a `tool` Type that runs rather than a skill/plugin that's copied in) so this bulk lane leaves the call to a real eval. Left at `discovery-log`.

_Triaged 2026-08-28 by the P3 backlog band._
