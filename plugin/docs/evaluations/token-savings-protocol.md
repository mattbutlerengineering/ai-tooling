# Evaluation: Token-savings verification protocol

**Repo:** _(methodology — not a third-party tool; the harness lives in this repo)_
**Last verified:** 2026-06-26
**Dev loop stage:** Reflect
**Layer:** Process

---

## What it does

A repeatable A/B method for verifying the "% token savings" headline that nearly
every Optimize-cluster entry in `CATALOG.md` advertises (headroom 60–95%, context-mode
96%, token-optimizer-mcp 95%+, semble ~98%, gortex 50×). Those numbers are vendor
self-reports measured against undisclosed best-case corpora; this repo's evidence
standard is that a strong claim is **reproduced**, not quoted.

The protocol fixes the two variables a headline hides — the **corpus** and the
**transform** — and measures `tokens_in(corpus)` with the tool off vs. on:

1. **Fix a corpus.** A real, disclosed artifact of the kind that actually fills an
   agent's context: verbose tool output, a JSON API response, a log, a wide
   markdown table. Disclose exactly what it is so the run is reproducible.
2. **Fix the tokenizer.** `tiktoken` `cl100k_base`, so counts are deterministic and
   comparable across tools rather than each vendor counting its own way.
3. **Measure with/without.** Tokens-in of the raw corpus (baseline) vs. the
   tool-processed corpus. Report the delta as a percentage **and** absolute tokens.
4. **Record honestly.** Claimed X% vs. measured Y% on the named corpus. A tool that
   underdelivers is recorded as such (claimed 96%, measured 2%) — the catalog stays
   trustworthy even when a tool disappoints.

A passing verification (measured savings materially present on a realistic corpus,
without accuracy loss) graduates that tool's eval **REVIEW → MEASURED** and lets
`tier-stack.py` promote it toward STACK Tier 1. The companion detector
`audit-evals.py --savings-claims` lists every unverified claim so the backlog is a
number to shrink.

## How we tested it

**Evidence:** MEASURED

We ran the harness end-to-end **hands-on** to prove it produces real, reproducible
token deltas — a measured A/B, not a description of one. The transform used here is a
deterministic **reference stand-in** (intra-line whitespace collapse + adjacent
duplicate-line removal — the conservative, lossless class of reduction a Layer-1
compressor performs); it is *not* any specific catalogued tool. Each tool's own eval
substitutes the real tool at the transform step and reuses everything else.

Tokenizer: `tiktoken` `cl100k_base` (v0.13.0). We measured three real corpora drawn
from this repo's own workflow:

```
# reference transform: collapse whitespace + drop adjacent dup lines; count with tiktoken
$ python3 protocol_demo.py corpus.txt      # verbose `unittest -v` output (245 lines)
tokens (in):  8741 -> 8680   reduction:  0.7%  (61 tokens saved)
$ python3 protocol_demo.py corpusB.json    # gh-api issues JSON, pretty-printed (86 lines)
tokens (in):  4034 -> 3949   reduction:  2.1%  (85 tokens saved)
$ python3 protocol_demo.py COMPARISON.md   # wide whitespace-padded markdown table (634 lines)
tokens (in):  9628 -> 9628   reduction:  0.0%  (0 tokens saved)
```

The measured result is the point: a conservative, lossless transform reproducibly
saves **0–2%** on real corpora — one to two orders of magnitude below the 60–96%
headlines the same cluster advertises. Those headlines are achievable only with
aggressive, often lossy compression against hand-picked best-case inputs. The
protocol makes that gap measurable per-tool instead of taking the headline on faith.

`caveman` is the worked exemplar of the graduated state: its eval reports a *measured*
49–59% on a prose corpus (using exactly this tiktoken method, see `caveman.md`) against
a looser vendor headline — which is why it sits in STACK while the REVIEW-only
compressors do not.

> This protocol is itself a methodology eval, **intentionally not added to
> `CATALOG.md`/`COMPARISON.md`** — it is the measuring instrument, not a tool in the
> inventory. No catalog count changes.

## What worked

- Deterministic and reproducible: same corpus + `cl100k_base` → identical counts on
  every run, so a regression (a tool's savings shrinking) is detectable.
- Discriminating: a 0% result on the markdown table immediately exposes that "savings"
  are entirely corpus-dependent — the single most important thing a headline omits.
- Zero-cost and offline: no API key, no model inference; `tiktoken` counts locally.

## What didn't work or surprised us

- The reference transform is deliberately weak; it must not be read as a verdict on
  any catalogued compressor — it only validates the harness. A real tool's eval will
  show its own (likely larger, possibly lossy) number.
- Token deltas alone are insufficient: an aggressive compressor can post a huge % while
  dropping information the agent needed. Every verification must pair the delta with an
  accuracy/fidelity check, not just celebrate the percentage.
- A single corpus is not enough to generalize; report the corpus alongside the number
  and prefer measuring two or three of different shapes.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | The protocol measures cost, not code correctness; but it mandates an accuracy check so a lossy compressor can't hide behind a % |
| Speed | neutral | Verification is a one-off offline measurement, not a hot path |
| Maintainability | + | Replaces scattered, incomparable vendor claims with one comparable, reproducible number per tool |
| Safety | neutral | No execution of untrusted tool logic required for the baseline; tool-side runs inherit that tool's risk |
| Cost Efficiency | + | Turns the catalog's loudest, softest cost claims into verified evidence and prioritizes which compressors actually pay off |

## Verdict

**ADOPT** (as the standard verification method)

This is the canonical A/B method for any catalog entry advertising a numeric token
savings. It is cheap, offline, deterministic, and directly feeds the existing
Evidence-tier and `--savings-claims` machinery. Adopt it as the required path to
graduate an Optimize-cluster eval from REVIEW to MEASURED; the headline numbers in
that cluster are not adoptable evidence until reproduced this way.

## Catalog entry

_Intentionally none._ This is a methodology eval (the measuring instrument), not a
third-party tool, so it has no `CATALOG.md`/`COMPARISON.md` row and does not change
the catalog count. Tools verified **with** this protocol keep their existing catalog
rows; running it only graduates their eval's `**Evidence:**` field.
