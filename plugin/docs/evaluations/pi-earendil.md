# Evaluation: pi (earendil-works)

**Repo:** [earendil-works/pi](https://github.com/earendil-works/pi)
**Stars:** 83,512 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Dev loop stage:** Implement (terminal coding agent)
**Layer:** Harness
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A terminal coding agent, catalogued alongside `command-code`, `aider`, `opencode` and `oh-my-pi`.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the `CATALOG.md` one-liner and "Overlaps with" cell. Enough to place and band it; not enough for a
positive verdict, and none is offered.

## Triage note

Left at `discovery-log` — and flagged as the member of this cluster most deserving a real look.

At **★83.5K it is the second-most-starred row in the entire terminal-agent cluster**, behind only
`gemini-cli` (★106K), ahead of `open-interpreter` (★67.6K, and see that eval's warning that its stars
belong to a retired predecessor), and far ahead of every vendor CLI in the slice. MIT, pushed today.
Yet it has no evaluation at all — this stub is the first thing written about it.

That gap is itself the finding. `next-evals.py` scores leads on `2*overlap_pressure +
stage_gap_weight + evidence_bonus` and star count is not an input, which is defensible as a general
rule — popularity is not quality, and the catalog is full of well-starred thin repos. But it means a
row can sit unexamined at 83K stars while lower-starred siblings in the same cluster carry full
evaluations, purely because fewer rows happen to cite it in their "Overlaps with" cells.

Not disposed, obviously: there is no read here to dispose on, and eliminating the cluster's
second-largest entry on no evidence would be the exact failure mode the eliminate-only rule guards
against. The correct action is promotion, which this band may not do.

See the cluster note on [`gemini-cli`](./gemini-cli.md) for why no member of this group is redundant
with another on current evidence.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pi](https://github.com/earendil-works/pi) | harness | AI agent toolkit (MIT, ★67K) — unified LLM API, agent loop, TUI, and a coding agent CLI in one lightweight package | Want a batteries-included agent toolkit with a built-in coding agent CLI | command-code, aider, opencode, oh-my-pi |
