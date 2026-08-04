# Evaluation: command-code

**Repo:** [CommandCodeAI/command-code](https://github.com/CommandCodeAI/command-code)
**Stars:** 3,606 | **Last updated:** 2026-08-04 (pushed) | **License:** **none declared**
**Dev loop stage:** Implement (terminal coding agent)
**Layer:** Harness
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A terminal coding agent in the same category as `aider`, `opencode`, `grok-cli` and `pi`. The
repository description is the bare string "Command Code AI"; no further capability detail was
available without installing it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the `CATALOG.md` one-liner and "Overlaps with" cell. Enough to place and band it; not enough for a
positive verdict, and none is offered.

The license was checked directly rather than taken from the cached snapshot, since the disposal turns
on it:

```
gh api repos/CommandCodeAI/command-code --jq '.license.spdx_id'   # null
gh api repos/CommandCodeAI/command-code/contents/LICENSE          # 404 Not Found
```

## Verdict

**SKIP** — no declared license, confirmed against a live fetch on 2026-08-04: `license` is `null` and
there is no `LICENSE` file in the repository at all (HTTP 404). Under this repo's adoption bar an
entry with no license grant is not adoptable — not because of what the terms say, but because there
are none.

**The freshness of that check is the point.** Earlier in this same triage pass, `vercel-labs/skills`
was queued for elimination on a cached `license_spdx: NONE` and survived: a live fetch showed upstream
had since added an MIT LICENSE. So a cached `NONE` is not evidence. This one was re-fetched today and
the absence is current, which is what makes it usable as a ground.

Note also what is *not* being claimed. `NOASSERTION` — GitHub's "could not parse the LICENSE file" —
would mean nothing here; two rows in this same lane show it hiding a permissive Apache-2.0
(`terraform-skill`) and a blocking CC BY-NC (`academic-research-skills`). This is the different case:
a confirmed absence, not a parse failure.

The category context makes the SKIP cheap rather than costly. This is one of ~20 catalog rows
answering "which terminal coding agent do I run?" (see the cluster note on
[`gemini-cli`](./gemini-cli.md)), its own `Overlaps with` cell names `aider`, `opencode`, `grok-cli`
and `pi` as alternatives, and nothing in the repository description distinguishes it from them.
Removing an unlicensed, undifferentiated member of a saturated cluster costs the catalog nothing it
does not already have licensed.

Re-open the moment a LICENSE lands — that is exactly what happened to `vercel-labs/skills`, and this
row should get the same second look rather than staying SKIPped on a stale fact.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [command-code](https://github.com/CommandCodeAI/command-code) | harness | Multi-provider AI coding agent CLI — Claude, DeepSeek, GLM, Kimi, OpenAI (★3.4K; ⚠️ no license) | Want a coding agent CLI that works across multiple LLM providers without vendor lock-in | aider, opencode, grok-cli, pi |
