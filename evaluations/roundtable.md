# Evaluation: roundtable

**Repo:** [Kostakurta8/roundtable](https://github.com/Kostakurta8/roundtable)
**Stars:** 14 | **Last updated:** 2026-08-10 (pushed) | **License:** MIT
**Last verified:** 2026-11-12
**Last triaged:** 2026-11-12  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Watches Claude Code agents work as a pixel-art office — replays any second of a
session exactly and shows per-agent cost. Read-only, 100% local, never calls an API.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured.** Installed it via the packed release (`npm i https://github.com/Kostakurta8/roundtable/releases/latest/download/roundtable.tgz`, v0.4.0, Node 22.23) and ran `roundtable --stats` against a synthetic `~/.claude` root I generated with a script, so every expected number is known by construction. The fixture holds one main session (4 assistant responses written as 8 lines, 2 tool calls, 2 hook firings written as 4 records), two subagent transcripts (3 responses, 4 lines) and a workflow `journal.jsonl` carrying a decoy `output_tokens: 99999`. The baseline arm is the naive per-line sum of `usage.output_tokens`, which is what a quick `jq` over the transcripts gives you.

```
python3 mk.py root                         # fixture generator, 6 files
roundtable --stats --root root
  children wrote 50.8% of the output ... (650 vs 630 written in main transcripts)
  cold start: 4,000 cache-creation tokens per child
  usage blocks: 12 lines describe 7 responses - summing per line reports 2,560 output tokens against 1,280 real (+100%)
    main transcripts +139.7%, subagent transcripts +61.5%
  hooks: 4 records = 2 firings (+100% if you count lines)
roundtable --card --bare --root root --out card.png   # 1200x630 PNG, 1.8 s
  2 subagents (2 at once), 16.3k tokens, 1m 20s - est $0.05
roundtable --gif --bare --root root --out s.gif       # 960x562 GIF, 0.6 MB, 24.1 s
roundtable --root root --no-open -p 7499              # GET / -> HTTP 200
```

Checked against the fixture's known truth:

| Quantity | Truth by construction | Naive per-line sum | roundtable `--stats` |
|---|---|---|---|
| Output tokens, all transcripts | 1,280 (630 main + 650 children) | 2,560 (+100%) | 1,280, and it also prints the naive 2,560 |
| Main-only / child-only output | 630 / 650 | 1,510 / 1,050 | 630 / 650 (+139.7% / +61.5% reported for the naive sums, matching 1510/630 and 1050/650) |
| Responses vs usage lines | 7 vs 12 | 12 | 7 vs 12 |
| Hook firings | 2 | 4 | 2 |
| Cold-start cache-creation per child | 4,000 (mean of 5,000 and 3,000) | n/a | 4,000 |
| Decoy `journal.jsonl` (99,999) | excluded | included by a glob | excluded |
| Card token total | 16,280 output+cache (+35 input) = 16.3k | n/a | 16.3k |

Seven of seven checkable quantities matched exactly. The card, GIF and server paths all produced output against the fixture with no network and no API key.

## Test design

- **Task/corpus:** a generated fixture (`mk.py`, below), one session with two subagents, multi-line responses sharing one `message.id`, duplicate hook records and a decoy workflow journal. Disclosed in full in the table above.
- **Baseline:** summing `usage.output_tokens` over every line of every `.jsonl` (the naive count), plus counting hook records as firings.
- **Metric:** exact agreement with the known totals (k/N quantities matched), plus whether the tool reports the naive over-count itself.
- **Reproduce:** write the fixture generator that emits the files described above, then run `roundtable --stats --root <dir>`; all expected numbers follow from the message ids and usage values chosen in the generator.

## What worked

- **Deduplicates by message id correctly.** All seven checkable quantities matched the planted truth, including the 2x over-count a per-line sum produces on multi-block responses.
- **Reports the over-count itself.** The stats output prints the naive figure beside the real one, so the correction is verifiable from its own output.
- **Skips the workflow journal.** The decoy 99,999 never entered a total.
- **Zero-config and offline.** One `npm i` of a release tarball; stats, card, GIF and the web server all ran with no key, no hook install and no write to the observed directory.

## What didn't work or surprised us

- **Median rounding.** With two children whose tool calls were 1 and 0 and whose spans were about 10 s and 0 s, it printed `median child: 1 tool calls over 10 s`, which is the upper of the two middle values rather than the mean; harmless but a median over an even count is not what a reader assumes.
- **Cost figure is an estimate** (`est $0.05`); it depends on a price table inside the tool and I have no independent oracle for it, so it is unverified here.
- **Fixture is synthetic.** It matches the schema the repo's own fixtures use (Claude Code v2.1.220 era), not a live multi-agent session, so real transcript variations (compaction, resumed sessions) are untested.
- **Maturity.** Repo shows a single commit in the clone, 14 stars, v0.4.0, and the README says the npm package name is not yet published; install is from a GitHub release tarball.
- **Browser office view not exercised.** I confirmed the server answers HTTP 200 but did not drive the pixel-art UI or replay scrubbing, so the headline replay feature is unmeasured.
- **README's windows-first note:** the author says Windows is the platform actually watched; this run was Linux.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Seven of seven token/hook/response quantities matched a known-by-construction fixture; the naive per-line sum was off by 100%. |
| Speed | neutral | `--stats` and `--card` returned in about 2 s on a small root; larger corpora not timed. |
| Maintainability | neutral | A read-only observer; it changes nothing in your repo. |
| Safety | + | Read-only, no hooks, no outbound calls claimed; the fixture root was unmodified and `--bare` strips transcript text from GIF/card. |
| Cost Efficiency | + | Shows per-child cold-start cache cost and the child share of output, which is the input for fan-out cost decisions. |
| Verifiability | + | Prints the naive and deduplicated counts side by side, so a reader can check its correction against the raw files. |

## Verdict

**discovery-log — measured; promotion candidate** — its transcript accounting reproduced every planted quantity exactly (1,280 real vs 2,560 naive output tokens), and it is differentiated from `abtop` by `--stats`, replay and card output; would read ADOPT or CONDITIONAL on human confirmation, with the caveats above (14 stars, unpublished to npm, UI replay not exercised, synthetic fixture).

## Triage note

Triage banded this as a P2 challenger against `abtop` (both are local session
observability tools), but the presentation and interaction model are genuinely
different — an exact, scrubbable visual replay with per-agent cost attribution is
not what `abtop`'s real-time TUI offers, and none of the catalog's other
observability tools (`claude-fleet`, `peek`, `claude-devtools`) provide a replay
view either. Too early (14 stars, 6 days old) to call redundant; left at
discovery-log for a real hands-on eval rather than a mechanical SKIP.

_Triaged 2026-08-10 by the P2 challenger band._

**Re-triaged 2026-10-01 by the P2 challenger band (daily discovery pass):** no change — the
replay/cost-attribution differentiation from `abtop` still holds, no new adoption or measurement
signal surfaced. Left at `discovery-log`.

**Re-triaged 2026-10-14 by the P2 challenger band (5-oldest-untriaged pass):** no change — the
replay/cost-attribution differentiation from `abtop` still holds. Left at `discovery-log`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [roundtable](https://github.com/Kostakurta8/roundtable) | tool | Pixel-art visual replay of Claude Code agent sessions (MIT) — replay any second exactly, see per-agent cost; read-only, 100% local | Agent progress is a scrolling transcript with no visual replay or per-agent cost breakdown, and no local-only option | claude-fleet, peek, abtop, claude-devtools |
