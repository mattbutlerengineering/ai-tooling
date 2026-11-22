# Evaluation: ai4ai

**Repo:** [AI4XE/ai4ai](https://github.com/AI4XE/ai4ai)
**Stars:** 132 | **Last updated:** 2026-11-22 (pushed) | **License:** MIT
**Last verified:** 2026-11-22
**Last triaged:** 2026-11-22  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A cross-harness kit that lets a coding agent manage itself: check its own runtime
status, renew a stale/compacted context, and spin up duplicates of itself across
different agent harnesses. Positioned as agent self-management rather than a
multi-session multiplexer or dispatcher.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner, the repo's own description, and the CATALOG "Overlaps with" cell —
sufficient to check whether a named incumbent covers the same job, not to assess the
tool's own behaviour. It would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — brand-new lead (found in today's discovery pass),
never exercised.

## Triage note

The P2 challenger band flagged this lead against `claude-squad` (STACK), cited in its
CATALOG "Overlaps with" cell. `claude-squad` manages *multiple* AI terminal agents in
parallel panes for visibility across sessions — a multiplexer. `ai4ai`'s own description
is about a *single* agent's self-management (its own runtime status, renewing its own
context, duplicating itself) — a different job from multi-session visibility/dispatch.
The overlap citation does not establish that `claude-squad` dominates this lead's actual
job, so SKIPping it as "redundant with claude-squad" would not be a defensible,
evidence-backed call. Left at `discovery-log` for a real hands-on eval later.

_Triaged 2026-11-22 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ai4ai](https://github.com/AI4XE/ai4ai) | tool | Cross-harness kit (MIT) giving a coding agent runtime status, context renewal, and self-duplication across sessions | Agents have no built-in way to check their own runtime state, refresh a stale context, or spin up copies of themselves across harnesses | claude-squad, foreman (ilkemerol), numbrone |
