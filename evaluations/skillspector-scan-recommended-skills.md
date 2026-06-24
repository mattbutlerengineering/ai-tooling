# SkillSpector scan of the recommended skills

**Evidence:** MEASURED
**Last verified:** 2026-06-24
**Tool used:** [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) v2.3.5 ([eval](skillspector.md))
**Dev loop stage:** Review / Ship (supply-chain vetting)

A hands-on run of the SkillSpector security scanner against the **skill** entries in
[STACK.md](../STACK.md), in response to issue #132 ("run security skill on recommended
skills"). This is a *scan report*, not a tool evaluation — SkillSpector itself is evaluated
in [skillspector.md](skillspector.md).

## What this checks

SkillSpector answers "is this skill safe to install?" by combining offline static pattern
matching + bundled YARA rules with an optional LLM judgment layer, emitting findings against
a vulnerability taxonomy (prompt injection, data exfiltration, privilege escalation, supply
chain, etc.) with a 0–100 risk score, a severity, and an install recommendation.

## How we tested it

Ran the offline static + YARA layer **hands-on** on 2026-06-24 (macOS arm64). SkillSpector
requires Python 3.12+ (`requires-python = ">=3.12,<3.14"`); this host's default is 3.11, so
Python 3.12 was provisioned with `uv python install 3.12`, `NVIDIA/SkillSpector` **v2.3.5**
was cloned into a temp dir, and deps installed with `uv sync` — including `yara-python==4.5.4`,
so the YARA layer was live. (The tool eval [skillspector.md](skillspector.md) measured v2.3.1;
this scan ran v2.3.5 — newer, in case static-layer behavior has since shifted.) Each recommended skill's **canonical GitHub repo** was cloned
(`git clone --depth 1`) and scanned with:

```
uv run skillspector scan <repo-dir> --no-llm --format json --output <name>.json
```

**`--no-llm` runs the static + YARA layer only — no API key.** This is a deliberate scope
limit (no LLM provider key was available), and it is the central caveat for reading the
results below: SkillSpector's own output marks every `--no-llm` run `is_complete: false`,
`llm_analysis: "skipped"`, `filtering_mode: "heuristic"`. The LLM layer is what adjudicates
*intent* and suppresses pattern false positives; without it, findings are raw pattern hits.
Each repo was scanned whole-directory; the temp dir (cloned external repos + the SkillSpector
install) was deleted afterward.

## Results (static `--no-llm` layer)

| Skill (repo) | Score | Severity | Recommendation | Findings (by severity) | Top categories |
|---|---|---|---|---|---|
| [caveman](https://github.com/JuliusBrussee/caveman) | 100 | CRITICAL | DO_NOT_INSTALL | 142 (HIGH 52, MED 88, LOW 2) | Agent Snooping (66), Privilege Escalation (25), Rogue Agent (10) |
| [trailofbits/skills](https://github.com/trailofbits/skills) | 100 | CRITICAL | DO_NOT_INSTALL | 338 (CRIT 6, HIGH 161, MED 170, LOW 1) | Dangerous Code Execution (52), Memory Poisoning (44), Output Handling (42) |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 100 | CRITICAL | DO_NOT_INSTALL | 12 (HIGH 5, MED 4, LOW 3) | Excessive Agency (3), Memory Poisoning (3), Supply Chain (2) |
| [agent-skills](https://github.com/addyosmani/agent-skills) | 100 | CRITICAL | DO_NOT_INSTALL | 59 (HIGH 32, MED 25, LOW 2) | Tool Misuse (21), Agent Snooping (18), Excessive Agency (9) |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | 100 | CRITICAL | DO_NOT_INSTALL | 498 (CRIT 1, HIGH 337, MED 157, LOW 3) | Privilege Escalation (270), Data Exfiltration (72), Dangerous Code Execution (39) |
| [web-quality-skills](https://github.com/addyosmani/web-quality-skills) | 45 | MEDIUM | CAUTION | 7 (HIGH 6, LOW 1) | Prompt Injection (5), Agent Snooping (1), Excessive Agency (1) |

Scan times: trailofbits 35s, last30days 23s, the rest 2–5s. `documentation-and-adrs` and
`resolving-merge-conflicts` are sub-skills of `agent-skills` and `mattpocock/skills`
respectively and are covered by those repo scans. `--recursive` did not split the bundles
into per-skill reports here (it scans immediate `SKILL.md` subdirectories; these repos nest
deeper), so each row is the whole-repo aggregate.

## Reading the results: the static layer is high-recall, low-precision

**Five of six trusted, widely-used skills scored 100 / CRITICAL / DO_NOT_INSTALL** — including
Trail of Bits' own security-skills repo. Taken at face value that would condemn the entire
recommended stack, which is not credible. Spot-checking the findings shows why: the static
layer matches patterns in **documentation, examples, CI config, and benchmark files**, with
no LLM to judge intent. Representative hits:

- **caveman → "Privilege Escalation / Credential Access" (HIGH, conf 0.6):** the string
  `.env.local` in `benchmarks/run.py` — a benchmark harness, not the skill.
- **caveman → "Agent Snooping / Skill Enumeration" (MED, conf 0.8):** the path
  `skills/caveman/SKILL.md` inside a `.github/workflows/sync-skill.yml` CI file.
- **last30days → "Data Exfiltration / External Transmission" (MED, conf 0.5):** a
  `https://api.star-history.com/` star-history badge URL in `README.md`.
- **last30days → "Privilege Escalation / Credential Access" (HIGH, conf 0.7):** the words
  "access tokens" in `AGENTS.md` prose.
- **web-quality → "Prompt Injection / Hidden Instructions" (HIGH, conf 0.7):** an HTML
  comment `<!-- ✅ Language specified -->` in an accessibility code example.

These are false positives for the question "is the skill malicious?" The `last30days`
Privilege-Escalation count (270) is inflated precisely because the skill legitimately talks
about web APIs and tokens — exactly the vocabulary the static patterns key on.

**One finding is genuinely worth noting**, not a false positive:

- **trailofbits → "Supply Chain / Known Vulnerable Dependency" (CRITICAL, conf 0.9):**
  `numpy` in `plugins/culture-index/skills/interpreting-culture-index/scripts/pyproject.toml`,
  flagged against 10 advisories (e.g. CVE-2021-41495). This is a real dependency advisory in a
  bundled script — a supply-chain note for anyone running that one script, though it is not the
  skill's instruction logic. The other 5 CRITICALs in that repo are similar dependency advisories.

## Bottom line

- **No static-layer evidence of genuine malice** in any recommended skill. The CRITICAL
  verdicts are dominated by pattern matches on prose, examples, CI, and benchmark files — the
  expected behavior of a high-recall pre-filter run **without** its LLM adjudication layer
  (`is_complete: false`).
- **`skillspector --no-llm` is not a usable gate for vetting *known-good* skills** — it will
  flag almost all of them. Its value is the opposite direction: catching a *malicious* skill
  (low false-negative), as the good-vs-bad A/B in [skillspector.md](skillspector.md) showed.
  To triage trusted skills, run the **LLM layer** (set a provider key and drop `--no-llm`),
  which suppresses these intent-less pattern hits.
- **Actionable follow-ups:** (1) the `numpy`/dependency advisories in `trailofbits/skills`
  bundled scripts are a real (if peripheral) supply-chain note; (2) re-running this scan with
  the LLM layer would convert these raw counts into an adjudicated verdict — a candidate for a
  future MEASURED pass if an API key is provisioned.
