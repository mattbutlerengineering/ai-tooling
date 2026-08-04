# Evaluation: logfire

**Repo:** [pydantic/logfire](https://github.com/pydantic/logfire)
**Stars:** ~4,300 | **Last updated:** 2026-06-20 | **License:** MIT (SDK); server is closed source
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (Outer Loop / observability)
**Layer:** Infrastructure

---

## What it does

AI/application observability platform from the Pydantic team. The open-source repo is the Python SDK plus docs; the recording/dashboard server is closed source and SaaS (with a free tier).

Mechanically, Logfire is an opinionated wrapper around OpenTelemetry. You `pip install logfire`, `logfire auth`, `logfire.configure()`, and then either emit manual spans/logs (`logfire.info(...)`, `with logfire.span(...)`) or auto-instrument popular packages (`logfire.instrument_fastapi(app)`, HTTPX, many others). Because it's OTel under the hood, it captures full traces/metrics/logs and works for virtually any language via standard OTel instrumentation. Differentiators: Python-centric insights (rich Python-object display, event-loop telemetry, code/DB profiling), built-in Pydantic-model validation analytics, and — notably — **data is queryable with standard SQL**, so existing BI tools and DB libraries work against it.

## How we tested it

**Evidence:** REVIEW

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

**discovery-log — tentative read**

Strong pick for Python/Pydantic LLM and agent stacks that want OTel-standard observability with a SQL query surface and minimal lock-in. If you require a fully self-hosted OSS backend, prefer langfuse or opik. Pairs especially well with pydantic-ai and FastAPI services.

## Triage note

Left at `discovery-log`. MIT, Pydantic behind it, OTel-native with a SQL query surface — and it is the
permissively-licensed row that a reader arrives at after this pass SKIPped `phoenix` over Elastic License
2.0 terms, so it now carries more weight in the observability cluster than it did before.

The fit is specific rather than general and the eval is right to scope it: Python and Pydantic stacks,
pairing naturally with `pydantic-ai` (a P0 lead) and FastAPI. Teams needing a fully self-hosted
open-source backend are pointed at `langfuse` or `opik`, both also P0 leads. That triangle —
langfuse/opik for self-hosted, logfire for Python-native, phoenix disposed — is the shape of the cluster
after this pass.

Minimal lock-in through OTel is the durable argument for it: instrument once against a standard and the
backend becomes replaceable. That is a Maintainability property, and one of the few in this category that
does not need a benchmark to believe.

Pushed 2026-07-10.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [logfire](https://github.com/pydantic/logfire) | platform | AI observability built on OpenTelemetry (MIT SDK, by Pydantic) — Python-centric insights, full traces/metrics/logs, SQL-queryable data, auto-instrumentation; server is closed/SaaS | Want LLM/agent + app observability on OTel standards with plain SQL, not a bespoke query language | langfuse, opik, Helicone, weave |
