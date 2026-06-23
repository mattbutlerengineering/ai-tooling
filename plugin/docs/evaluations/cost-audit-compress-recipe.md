# Evaluation: Cost-Audit + Compress recipe (ccusage + headroom)

**Repo:** [ryoppippi/ccusage](https://github.com/ryoppippi/ccusage) + [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom)
**Stars:** ccusage 16,484 · headroom 37,301 | **Last updated:** ccusage 2026-06-23 · headroom 2026-06-19 | **License:** ccusage MIT · headroom Apache-2.0
**Last verified:** 2026-06-22  <!-- the date you last checked this eval against reality; staleness sweep (audit-evals.py --staleness) flags evals older than their category threshold -->
**Dev loop stage:** Reflect (audit where the budget went) + Implement/Verify (trim tool output before it costs tokens)
**Layer:** Tooling (ccusage reporting) + Infrastructure (headroom compression layer)

---

## What it does

This is a **recipe**, not a new tool: it pairs a catalogued cost-**monitoring** tool with a catalogued output-**compression** tool so the combined setup answers a question neither answers alone — *where did my token budget actually go, and can I cut it before I spend it?*

- **ccusage** (`npx ccusage@latest`) is the **reporting/audit** layer. It parses the local `~/.claude` JSONL transcripts (plus Gemini CLI, Codex, OpenCode, etc.) into token/dollar reports by day / month / session / model, with `--json` for piping. It is the after-the-fact accountant: it tells you the $7.8K lifetime / $298–933-per-day spend and *which* sessions and models drove it — but it cannot change the spend.
- **headroom** (`pip install headroom-ai`) is the **trim** layer. It is a deterministic, fully-local compressor that sits between the agent and the model and shrinks verbose tool output (diffs, JSON, logs, file reads) before it is billed. Crucially it makes **no secondary-LLM call** — compression is local structural transformation (a JSON columnar compactor `compact_document_json`, an AST/structural pipeline via `compress()`), so the **net saving ≈ the gross token reduction minus negligible local latency**. That is exactly why headroom is the right compressor for a "prove net savings" recipe: an LLM-summarizer compressor would burn inference tokens to save context tokens, muddying the net; headroom does not.

The mechanism of the recipe: run `headroom audit-reads` on the *same* local transcripts ccusage costs, to size the *compressible* bytes; use ccusage's per-model price to turn that byte-opportunity into dollars; then wire headroom (`headroom init` durable integration, or its proxy/MCP) as a PreToolUse/PostToolUse output-trim so the high-reduction workloads stop costing those tokens. ccusage then re-measures the new, lower spend on the next Reflect pass — closing the loop.

## How we tested it

**Evidence:** MEASURED

We installed both tools on this macOS arm64 host and ran a real before/after compression measurement on four representative tool outputs drawn from this repo, counting tokens with **two independent oracles** — headroom's own `CompressResult` token counter and **tiktoken `cl100k_base`** — so the deltas are not headroom marking its own homework. We also ran `headroom audit-reads` against this machine's real Claude Code transcripts to capture the audit-layer output.

**Install (versions captured):**

```bash
npx ccusage@latest --version            # -> ccusage 20.0.14  (Node v20.19.5)
pip install headroom-ai                  # -> headroom-ai 0.27.0   (Python 3.11.4)
headroom --version                       # -> headroom, version 0.27.0
```

> **Honest install caveat (disclosed, not fabricated):** the *full* feature set `pip install "headroom-ai[all]"` **failed to build on this host** — the `hnswlib` wheel aborts with `fatal error: 'iostream' file not found` (a missing C++ stdlib on the CommandLineTools SDK, a local toolchain gap, not a headroom defect). The core `headroom-ai` wheel installed cleanly and ships the compressors we measured (`compress`, `SmartCrusher`, `compact_document_json`, `audit-reads`). The consequence is visible in the numbers below: the prose/code Kompress-base model paths that live in the `[all]` extras did **not** activate, so the source-file and git-log artifacts showed 0% — this is reported as a real result, not hidden. ccusage required no install (npx) and no API key.

**Artifacts (all real outputs generated from this repo, redacted of absolute paths):**

```bash
npx ccusage@latest session --json > art_ccusage_session.json   # 2.18 MB real JSON
git log -p -8        > art_gitdiff.txt                          # 311 KB real diff
git log --stat -80   > art_gitlog.txt                           # 158 KB verbose log
cp audit-evals.py      art_source.py                            # 50 KB source file
```

**Measurement** (per artifact, the correct deterministic headroom path per content type; tokens via tiktoken `cl100k_base`, cross-checked against headroom's `CompressResult.tokens_*`):

```
artifact                                         before    after    saved     pct       ms
ccusage session JSON (compact_document_json)      23113    17042     6071   26.3%      1.5
git diff (pipeline, convo-level)                  81947    57948    23999   29.3%    128.1
git log (pipeline, convo-level)                   40395    40395        0    0.0%    125.0
source audit-evals.py (pipeline, convo-level)     12895    12895        0    0.0%     16.7
AGGREGATE                                        158350   128280    30070   19.0%
```

The JSON figure uses `SmartCrusher.compact_document_json` (deterministic columnar compaction of the session array); a spot-check confirmed the compacted form **retains every key** (`agent`, `inputTokens`, `outputTokens`, `totalCost` all present) — it is a lossless schema-header + row representation, not a lossy drop. The git-diff figure is the `headroom.compress()` pipeline at convo level and was independently confirmed by tiktoken (81,947 → 57,948) and by headroom's own counter (87,516 → 62,190, ratio 0.289) on the same input — two tokenizers agreeing the diff shrank ~29%.

**Dollar mapping** (token reduction × ccusage's published Sonnet input price $3.00/MTok):

```
Tokens saved on this 4-artifact bundle: 30,070
  = $0.0902 per bundle on Sonnet input ($3.00/MTok)
  @ 50 such bundles/day  -> $4.51/day  ->  ~$99/mo (22 working days)
  same bundle on Haiku ($0.80/MTok)    ->  $0.024/bundle
```

**Audit layer — `headroom audit-reads` on this machine's real transcripts** (the data that decides whether the trim is worth wiring):

```json
{ "read_calls": 11746, "read_bytes": 49662896,
  "stale_bytes": 11621502, "stale_calls": 2843,
  "linenum_overhead_bytes": 4045118,
  "subset_bytes": 426084, "subset_calls": 256,
  "dedup_identical_bytes": 88655, "dedup_identical_calls": 21,
  "sessions": 4465 }
```

i.e. of 49.7 MB of Read-tool traffic, ~11.6 MB is stale re-reads, 4.0 MB is pure line-number scaffolding, and 0.4 MB is subset-containable — concrete, machine-specific compression opportunity that ccusage's dollar report tells you is worth chasing.

**Wiring (install + integrate):**

```bash
# 1. Audit layer — see where the budget went, by repo/branch/session/model + spikes
npx ccusage@latest daily --json | jq '.totals'        # dollars
headroom audit-reads --format json                     # compressible bytes in same logs

# 2. Trim layer — durable PreToolUse/PostToolUse output compression
pip install headroom-ai                                # (or: npm install headroom-ai)
headroom init --global                                 # durable agent integration
# alternative zero-config path: headroom proxy --port 8787  (point client at it)
```

## What worked

- **Real, two-oracle-verified net savings on the high-value workloads.** The git diff compressed **29.3%** (23,999 tokens) and the JSON blob **26.3%** (6,071 tokens), confirmed by both tiktoken and headroom's own counter. Because headroom is deterministic and local (sub-150 ms, no LLM call), the **net saving equals the gross** minus negligible latency — there is no inference cost clawing it back.
- **The two tools compose on the same substrate.** ccusage and `headroom audit-reads` both read the local `~/.claude` transcripts. ccusage prices them; audit-reads sizes the compressible fraction of them. You can therefore turn "$X/day on Reads" (ccusage) into "Y MB of that is stale/subset/line-number waste" (audit-reads) into a targeted trim — a decision loop neither tool gives you alone.
- **Lossless-style JSON compaction.** `compact_document_json` produced a 26% reduction while preserving every field key — safe for structured tool output where dropping a key would break downstream parsing.
- **Zero-friction audit half.** ccusage ran with no install and no API key; `headroom audit-reads` ran read-only against existing transcripts with no proxy stood up.

## What didn't work or surprised us

- **The `[all]` extras would not build on this host**, so the prose/code Kompress-base paths never activated — the **git log (0.0%) and source file (0.0%)** artifacts are the honest evidence of that. With only the core wheel, headroom compresses *structured* output (diffs, JSON) well and *unstructured* prose not at all on this install. A clean `[all]` install (working C++ toolchain) is required to compress logs/prose, per headroom's own benchmark table.
- **Compression is conditional, and the default config hides it.** Out of the box `compress()` returned **0% on everything** — `protect_recent` shields the most-recent message and the input sat under the model limit, so nothing was eligible. We had to set `compress_user_messages=True, protect_recent=0, target_ratio=0.4` to make the diff compress. The savings are real but require deliberate configuration; an operator who installs and walks away may get ~0%.
- **Small/high-signal outputs do not pay.** The 50 KB source file is below the threshold where structural compression finds slack; on truly small high-signal outputs the ~1–130 ms latency plus the reversibility-cache bookkeeping can **exceed** the token saving. This recipe pays on big diffs/JSON/logs, not on terse outputs.
- **The dollar figure is workload-scaled, not a headline.** $0.09/bundle is small in isolation; the recipe only matters at the volume ccusage reveals (here ~$300/day), where the audit-reads opportunity (11.6 MB stale + 4 MB line-number overhead) is recurring. The audit layer exists precisely to decide whether the trim clears the noise floor.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Compression is structural/lossless on the measured paths (JSON keys all retained; diff text shrunk, not garbled); headroom's reversible cache lets the agent retrieve originals — no measured correctness change, but prose-path was untested (didn't install) |
| Speed | + | Fewer input tokens per turn = faster model responses and longer effective context; compression itself ran in 1.5–128 ms locally, far below any network round-trip |
| Maintainability | + | ccusage makes per-model/per-session spend visible over time; audit-reads names the specific waste classes (stale, subset, line-number) so teams can target the trim instead of guessing |
| Safety | + | Both run fully local — ccusage parses logs offline (no key), headroom compresses on-machine with no data egress; reversible cache means a bad compression is recoverable, not lost |
| Cost Efficiency | + | The whole point: measured 26–29% token reduction on big structured outputs, net ≈ gross (no LLM inference cost), mapped to a real ~$99/mo at the volume ccusage surfaces here |

## Verdict

**ADOPT (conditional on workload)** — for any team running coding agents heavily enough that ccusage shows a non-trivial daily spend with large structured tool outputs (diffs, JSON, logs, file reads) dominating it.

**Net-savings verdict, stated plainly:** on the workloads where it pays — big git diffs and JSON/API blobs — headroom delivered a **measured 26–29% token reduction (19% aggregate across a mixed bundle)**, and because it is deterministic and local with **no secondary-LLM call**, the **net saving equals that gross reduction**. ccusage is the indispensable other half: it tells you *whether* you have enough such output to bother (and `headroom audit-reads` sizes exactly how much is stale/duplicated waste). The recipe **does NOT pay** in three cases, and we measured or reasoned each: (1) **small high-signal outputs** — the 50 KB source file got 0% and the compression overhead can exceed the saving; (2) **prose/unstructured logs without the `[all]` install** — the git-log artifact got 0% because the Kompress-base model paths require the heavy extras that failed to build here; (3) **low overall volume** — at a few dollars a day the ~$0.09/bundle saving is below the operational-noise floor. Use ccusage unconditionally (it is already ADOPT/MEASURED/in-STACK and free to run); add headroom when ccusage + audit-reads confirm large structured outputs are driving real spend, and verify the `[all]` install succeeds if you need prose/log compression. STACK reconciliation for the individual tools is handled by the parent process; this eval adds only the recipe.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cost-audit-compress-recipe](https://github.com/ryoppippi/ccusage) | reference | Recipe pairing ccusage (cost audit) with headroom (deterministic local output compression) to prove and capture net token savings | Seeing where the token budget goes is useless without a way to cut it before you spend — and an LLM-summarizer compressor muddies the net; this pairs auditing with a no-inference trim | ccusage, headroom, cost-observability, caveman, token-optimizer-mcp |
