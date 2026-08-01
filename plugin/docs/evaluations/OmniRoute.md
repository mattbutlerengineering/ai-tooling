# Evaluation: OmniRoute

**Repo:** [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute)
**License:** MIT
**Last verified:** 2026-07-31
**Last triaged:** 2026-07-31  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Free AI gateway — 231+ providers, RTK+Caveman token compression (15-95%, self-reported),
auto-fallback, MCP/A2A support. A single LLM endpoint that routes across free and paid
providers with built-in token savings.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (litellm, bifrost, Portkey-gateway, CLIProxyAPI). That is
sufficient for a SKIP that turns on redundancy with a catalogued incumbent, not on the tool's
behavior — a question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Verdict

**SKIP** — redundant with `litellm` (open-source AI gateway, 100+ providers, unified OpenAI
format, routing/fallbacks/budgets/caching, self-hostable). Both solve the same job — a
multi-provider LLM gateway with routing and cost control — and litellm is the more established,
broadly-adopted incumbent already covering it in this catalog. OmniRoute's self-reported token
compression numbers are also unverified (see this repo's token-savings-protocol.md), which
would need hands-on measurement before it could displace the incumbent even on that axis.

_Triaged 2026-07-31 by the P3 backlog band._
