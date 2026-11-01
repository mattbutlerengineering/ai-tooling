# Evaluation: paddock

**Repo:** [vakovalskii/paddock](https://github.com/vakovalskii/paddock)
**Stars:** 26 | **Last updated:** 2026-10-30 (pushed) | **License:** MIT
**Last verified:** 2026-11-01
**Last triaged:** 2026-11-01  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A self-hosted web cockpit (MIT) for coding agents: an isolated container per user, up to 4 chats side by side, harness-agnostic (Codex today, OpenCode/pi/omp coming), 2FA, and an egress proxy chain.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (CodeRail, cedr, t3code). That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead. It shares the "cockpit for coding agents" job with `CodeRail` and `cedr` (both added yesterday, both still `discovery-log` themselves — neither is a STACK pick), differentiated by multi-tenant isolation (per-user container, 2FA) rather than CodeRail's single-user remote-control angle.

## Triage note

No STACK-pick overlap. P3 backlog — left at `discovery-log` with a stamp.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [paddock](https://github.com/vakovalskii/paddock) | tool | Self-hosted web cockpit (MIT) for coding agents — isolated per-user container, side-by-side chats, harness-agnostic | Running several coding-agent chats across users needs an isolated, multi-tenant cockpit instead of one shared desktop session | CodeRail, cedr, t3code |
