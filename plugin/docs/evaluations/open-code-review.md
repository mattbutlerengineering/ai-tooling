# Evaluation: open-code-review

**Repo:** [alibaba/open-code-review](https://github.com/alibaba/open-code-review)
**Stars:** 18,770 | **Last updated:** 2026-08-04 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Go code-review tool from Alibaba with a hybrid architecture: deterministic rule pipelines (NPE,
thread-safety, XSS, SQL injection) run alongside an LLM agent that produces line-level comments.
OpenAI- and Anthropic-compatible, described by its authors as battle-tested at Alibaba's scale.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`PR-Agent`, `kodus-ai`, `code-review`). Enough to
place it against the STACK picks it was banded with; not enough for any verdict, and none is
offered.

## Triage note

Left at `discovery-log`, not SKIPped — unlike `PR-Agent` and `kodus-ai`, the two rows it shares an
"Overlaps with" cell with, which this same pass disposed as redundant with
[`code-review`](https://github.com/anthropics/claude-plugins-official) (STACK) plus
[`claude-code-action`](https://github.com/anthropics/claude-code-action) (STACK).

The split is principled rather than a hedge. PR-Agent and kodus-ai are LLM PR reviewers end to end,
so the incumbents cover them completely. open-code-review is *hybrid*: half of it is an LLM
reviewer that is indeed redundant, and the other half is a deterministic rule engine with a
built-in multi-language ruleset. Nothing in STACK provides that half — `brooks-lint` was explicitly
excluded (#37), and a probabilistic reviewer is the wrong instrument for "does this null-deref".
Disposing the whole tool as redundant would assert something only true of one half.

The adoption facts back a real look rather than a bulk call: Apache-2.0, ★18.8K and rising, pushed
today, and a rule set derived from production review at scale. Note the CATALOG one-liner's star
figure was stale by roughly half (★9.8K recorded against ★18.8K live) and has been corrected.

What a P0 read has to answer: do the deterministic rules fire on TypeScript/Python work, or is the
useful ruleset JVM-shaped like its provenance suggests? That decides whether the non-redundant half
reaches this stack at all.

_Triaged 2026-08-04 by the P2 challenger band ([#267](https://github.com/mattbutlerengineering/ai-tooling/issues/267))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [open-code-review](https://github.com/alibaba/open-code-review) | tool | Hybrid code review from Alibaba (Apache-2.0, ★18.8K, Go) — deterministic pipelines + LLM agent with line-level comments and fine-tuned rules (NPE, thread-safety, XSS) | Code review needs both rule-based precision and LLM reasoning; combines both in one tool | PR-Agent, kodus-ai, code-review |
