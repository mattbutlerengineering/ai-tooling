# Evaluation: axern

**Repo:** [cofy-x/axern](https://github.com/cofy-x/axern)
**Stars:** 105  <!-- repo-metadata.json, fetched 2026-08-04 -->
**License:** Apache-2.0
**Last verified:** 2026-07-31
**Last triaged:** 2026-07-31  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Open-source sandboxes for AI agents — untrusted code execution and durable services,
Kubernetes-native, self-hosted.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (agent-sandbox, daytona, flue). That is sufficient for a
SKIP that turns on redundancy with a catalogued incumbent, not on the tool's behavior — a
question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `agent-sandbox` (self-hosted, E2B-compatible agent sandboxes,
Apache-2.0, Kubernetes + container isolation, RESTful API + MCP server, multi-tenant). Both
solve the identical job — self-hosted, Kubernetes-native sandboxes for untrusted agent code —
under the same license, and agent-sandbox is the already-catalogued, E2B-compatible incumbent.
axern's "durable services" angle is a differentiator worth revisiting if it develops real
traction, but doesn't clear the bar for a first-time hands-on eval today.

_Triaged 2026-07-31 by today's discovery lead._
