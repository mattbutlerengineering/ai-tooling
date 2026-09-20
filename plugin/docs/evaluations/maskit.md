# Evaluation: maskit

**Repo:** [xiaYuTian11/maskit](https://github.com/xiaYuTian11/maskit)
**Stars:** 128 | **Last updated:** 2026-09-11 (pushed) | **License:** AGPL-3.0
**Last verified:** 2026-09-11
**Last triaged:** 2026-09-11  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

A local privacy-redaction proxy ("Data Maskit") for LLM tooling — it sits between a
Base-URL-configurable client (Cursor, Claude Code, Codex, Pi) and the model provider,
masking PII in outbound requests and streaming the original values back into the
response.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata (license, stars, description). That is sufficient for a SKIP that turns
on license, not on the tool's behaviour — a question the license answers directly. It
would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — AGPL-3.0. This catalog's license bar treats copyleft as disqualifying for
adoption (only permissive, MIT-like OSS is adoptable); a permissively-licensed
alternative (`presidio`, `superagent`) already covers PII redaction for LLM traffic.

_Triaged 2026-09-11 by the daily discovery pass — license bar._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [maskit](https://github.com/xiaYuTian11/maskit) | tool | ⚠️ AGPL-3.0 — local privacy-redaction proxy masking PII in requests/responses for Cursor, Claude Code, Codex, and any Base-URL-configurable LLM tool | Coding-agent traffic to hosted LLM APIs can leak PII/secrets in prompts and responses; want automatic mask-on-request, stream-restore-on-reply | presidio, superagent, secretguard-mcp |
