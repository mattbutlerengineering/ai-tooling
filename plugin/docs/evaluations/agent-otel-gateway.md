# Evaluation: agent-otel-gateway

**Repo:** [lhchingit/agent-otel-gateway](https://github.com/lhchingit/agent-otel-gateway)
**Stars:** 1 | **Last updated:** 2026-09-21 (pushed) | **License:** MIT
**Last verified:** 2026-09-26
**Last triaged:** 2026-09-26  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Infrastructure

---

## What it does

An OpenTelemetry gateway plus Grafana dashboard (MIT) that normalizes usage metrics from six
different coding-agent CLIs — Claude Code, Gemini CLI, Codex, OpenCode, Pi, and Antigravity —
into one OTel schema with per-user attribution.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (openinference, logfire, ccusage). That is sufficient to
note the overlap with existing observability tooling, not to judge whether its cross-harness OTel
normalization is materially better or redundant — it would not support an ADOPT, and this eval
offers none.

## Triage note

`triage.py` bands this P2 (challenges `ccusage`, a STACK pick) on citation alone, but the two
tools solve different problems: `ccusage` is a single-CLI local report generator parsing session
logs for Claude Code, while `agent-otel-gateway` is an OTel collector + Grafana pipeline
normalizing six different coding-agent CLIs' usage into one schema with per-user attribution —
infrastructure for a team dashboard, not a local cost report. Not clearly dominated by the
incumbent; left at `discovery-log` for a first-time hands-on eval rather than SKIPped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-otel-gateway](https://github.com/lhchingit/agent-otel-gateway) | tool | OpenTelemetry gateway + Grafana dashboard (MIT) normalizing usage metrics across six coding-agent CLIs into one schema | Claude Code, Gemini CLI, Codex, OpenCode, Pi, and Antigravity each report usage differently; want one OTel schema with per-user attribution | openinference, logfire, ccusage |
