# Evaluation: cursor-bridge

**Repo:** [hkc5/cursor-bridge](https://github.com/hkc5/cursor-bridge)
**Stars:** 67  <!-- repo-metadata.json, fetched 2026-08-04 -->
**License:** MIT
**Last verified:** 2026-07-31
**Last triaged:** 2026-07-31  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A single Rust binary, zero config, that runs Claude Code on your existing Cursor subscription
instead of a separate Anthropic subscription.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (claude-code-router, CLIProxyAPI, litellm). That is
sufficient for a SKIP that turns on redundancy with a catalogued incumbent, not on the tool's
behavior — a question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Verdict

**SKIP** — redundant with `CLIProxyAPI` (proxy exposing coding-agent CLI subscriptions as
standard API endpoints via OAuth, already flagged in this catalog as "provider-ToS gray-area").
cursor-bridge is a narrower instance of the same subscription-arbitrage pattern — repurposing
one vendor's paid subscription to drive another vendor's CLI — that CLIProxyAPI's eval already
covers the tradeoffs of. Doesn't earn a second catalogued entry for the same risk category.

_Triaged 2026-07-31 by today's discovery lead._
