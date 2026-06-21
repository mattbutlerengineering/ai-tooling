# Evaluation: SkillSpector

**Repo:** [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector)
**Stars:** ~8.6K | **Last updated:** 2026-06 | **License:** Apache-2.0
**Dev loop stage:** Review (vetting a skill before install), Ship (supply-chain gate)
**Layer:** Tooling

---

## What it does

A security scanner that answers "is this agent skill safe to install?" before you add
it to Claude Code / Codex / Gemini. It ingests a skill from a git repo, URL, zip,
directory, or single file and runs a LangGraph pipeline of analyzers that combine
**offline static pattern matching + bundled YARA rules** with an **LLM judgment layer**,
emitting findings against a vulnerability taxonomy (prompt injection, data exfiltration,
excessive agency, supply chain, etc.) with severity codes.

## How we tested it

**Source-grounded review — not run hands-on.** SkillSpector requires **Python 3.12+**
(this machine has 3.11.4, so `make install` / the `skillspector` CLI won't run cleanly)
and its full pipeline needs an **LLM API key** (OpenAI-compatible or NVIDIA NIM, per
`model_registry.yaml`) for the judgment nodes. Rather than fake a run, I cloned the repo
and read the analyzer source — the static layer is concrete and verifiable without
executing it. I did **not** install it, run the CLI, or scan a real skill; no scores or
example outputs below are from a run.

```bash
git clone --depth 1 https://github.com/NVIDIA/SkillSpector   # reviewed; NOT run
# blocked: needs Python 3.12+ (have 3.11) and an LLM key for the full pipeline
# evidence below is read from src/skillspector/nodes/analyzers/ and yara_rules/
```

Verifiable facts from the source tree:

- **11 static analyzer categories** (`static_patterns_*.py`): data_exfiltration,
  prompt_injection, excessive_agency, harmful_content, memory_poisoning,
  output_handling, privilege_escalation, rogue_agent, supply_chain,
  system_prompt_leakage, tool_misuse.
- **Real regex patterns** (offline, no LLM): exfiltration matches `requests.post(...)`,
  `httpx.post`, `urllib...urlopen(data=)`, `curl --data`, and `fetch(...method:POST)`;
  prompt injection matches "ignore (all) previous instructions", "override
  safety/security", "bypass restrictions/constraints", "disregard previous".
- **Bundled YARA rules** (`yara_rules/`): `malware.yar`, `webshells.yar`,
  `cryptominers.yar`, `hacktools.yar` — binary-threat detection beyond text regex.
- **Severity taxonomy** (`pattern_defaults.py`): coded findings with remediation prose,
  e.g. `P5` (CRITICAL — content could cause physical harm), `SC1` (deps lack version
  pinning), `EA2` (autonomous high-impact actions without human-in-the-loop), `EA4`
  (unbounded resource consumption → DoS/cost), `OH2` (cross-trust-boundary output flow).

The headline "**26.1% of skills contain vulnerabilities, 5.2% show likely malicious
intent**" is **the project's own research claim** (from its README), not something
measured here.

## What worked

- **Offline static layer is real and substantial.** The 11 categories + concrete regex
  + YARA rules mean a meaningful chunk of detection (exfiltration calls, injection
  phrases, known malware signatures) runs without any LLM — useful even air-gapped.
- **Taxonomy is practitioner-grade.** Severity codes map to specific, actionable
  remediation text (pin deps, add human-in-the-loop, bound resource use), not vague
  "this looks risky" output.
- **Multi-format input** (repo/URL/zip/dir/file) fits a pre-install gate in CI or a
  pre-commit hook for a skills registry.
- **Credible provenance.** NVIDIA, Apache-2.0, ~8.6K stars — low abandonment/quality risk
  for a security tool you'd put in the trust path.

## What didn't work or surprised us

- **Could not run it here.** Python 3.12+ and an LLM key are hard prerequisites for the
  full pipeline; the static layer is offline but extracting it standalone wasn't
  attempted. So detection *accuracy* (false-positive/negative rate) is unmeasured — the
  vendor's 26.1%/5.2% figures are unverified by us.
- **LLM dependency for the full verdict.** The judgment nodes mean reproducibility and
  cost depend on a model endpoint; two runs may not agree, and scanning many skills has
  a per-skill LLM cost.
- **Overlap with lighter guards.** For pure config/lint hygiene, `agnix`/`agentlint`
  are cheaper; SkillSpector's edge is genuine malice/vulnerability detection, so it
  complements rather than replaces those.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Detection accuracy not measured here (not run); static patterns are concrete but FP/FN rate unknown |
| Speed | neutral | Static layer is fast; the LLM judgment layer adds latency per skill (not measured) |
| Maintainability | + | Severity taxonomy with coded, actionable remediation makes findings trackable |
| Safety | + | Targets the real supply-chain risk of installing untrusted skills — 11 threat categories + YARA malware rules (source-verified) |
| Cost Efficiency | neutral | Static layer free; full pipeline incurs per-skill LLM cost (needs a model endpoint) |

## Verdict

**CONDITIONAL** — adopt as a pre-install / CI gate for agent skills when you can meet
the prerequisites (Python 3.12+ and an LLM endpoint for the full pipeline). The
source-verified static layer (11 categories of regex + YARA malware rules + a coded
severity taxonomy) is a real, offline-capable safety net for the genuine supply-chain
risk of installing untrusted skills, from a credible vendor. The conditions: this review
is source-grounded, not a measured run, so detection accuracy is unverified here; and the
full verdict depends on an LLM endpoint (cost + reproducibility). Re-evaluate with a
hands-on run on Python 3.12+ to measure FP/FN against planted-malicious skill files.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [SkillSpector](https://github.com/NVIDIA/SkillSpector) | tool | Security scanner for AI agent skills — detects vulnerabilities and malicious patterns | Downloaded skills could contain prompt injection or exfiltration | scorecard |
