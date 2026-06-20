# Evaluation: logfire

**Repo:** [pydantic/logfire](https://github.com/pydantic/logfire)
**Stars:** ~4,300 | **Last updated:** 2026-06-20 | **License:** MIT (SDK); server is closed source
**Dev loop stage:** Reflect (Outer Loop / observability)
**Layer:** Infrastructure

---

## What it does

AI/application observability platform from the Pydantic team. The open-source repo is the Python SDK plus docs; the recording/dashboard server is closed source and SaaS (with a free tier).

Mechanically, Logfire is an opinionated wrapper around OpenTelemetry. You `pip install logfire`, `logfire auth`, `logfire.configure()`, and then either emit manual spans/logs (`logfire.info(...)`, `with logfire.span(...)`) or auto-instrument popular packages (`logfire.instrument_fastapi(app)`, HTTPX, many others). Because it's OTel under the hood, it captures full traces/metrics/logs and works for virtually any language via standard OTel instrumentation. Differentiators: Python-centric insights (rich Python-object display, event-loop telemetry, code/DB profiling), built-in Pydantic-model validation analytics, and — notably — **data is queryable with standard SQL**, so existing BI tools and DB libraries work against it.

## How we tested it

Architecture review against the README and the documented SDK surface. Confirmed the OTel foundation (traces/metrics/logs), the manual-tracing and auto-instrumentation paths, the Pydantic-model analytics integration, and the SQL query model. Verified the open/closed split (SDK + docs open, server closed). Not run against a live app — honest observability numbers require a real workload and a multi-day window, so this is condition-gated.

```bash
gh api repos/pydantic/logfire --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/pydantic/logfire/readme --jq '.content' | base64 -d
```

## What worked

- **OpenTelemetry, not a walled garden.** Built on OTel signals, so you reuse existing instrumentation and aren't locked into a proprietary agent — easier to adopt and to leave than bespoke LLM-observability tools.
- **SQL query model.** Querying telemetry in standard SQL means no new query language and direct compatibility with BI/DB tooling — a real ergonomics edge over dashboard-only competitors.
- **Python-native depth.** Event-loop telemetry, profiling, and Pydantic-validation analytics are differentiators for Python LLM/agent stacks (and pair naturally with pydantic-ai).

## What didn't work or surprised us

- **Server is closed/SaaS.** The repo is the SDK; you don't self-host the backend (free tier + paid plans). For a fully OSS, self-hosted stack, langfuse/opik fit better.
- **Crowded category.** Overlaps langfuse, opik, Helicone, and Weave; the edge is OTel-nativeness + SQL + Pydantic depth, not unique LLM features.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Tracing/eval visibility surfaces failures and validation issues |
| Speed | + | Auto-instrumentation; profiling pinpoints slow code/DB queries |
| Maintainability | + | OTel-standard + SQL means portable, low-lock-in telemetry |
| Safety | neutral | Observability aids incident response; not a guardrail |
| Cost Efficiency | ✓/$ | Free tier; backend is paid SaaS at scale |

## Verdict

**CONDITIONAL**

Strong pick for Python/Pydantic LLM and agent stacks that want OTel-standard observability with a SQL query surface and minimal lock-in. If you require a fully self-hosted OSS backend, prefer langfuse or opik. Pairs especially well with pydantic-ai and FastAPI services.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [logfire](https://github.com/pydantic/logfire) | platform | AI observability built on OpenTelemetry (MIT SDK, by Pydantic) — Python-centric insights, full traces/metrics/logs, SQL-queryable data, auto-instrumentation; server is closed/SaaS | Want LLM/agent + app observability on OTel standards with plain SQL, not a bespoke query language | langfuse, opik, Helicone, weave |
