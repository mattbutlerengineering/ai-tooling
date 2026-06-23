# Evaluation: SkillSpector

**Repo:** [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector)
**Stars:** 9,432 | **Last updated:** 2026-06-22 | **License:** Apache-2.0
**Last verified:** 2026-06-22
**Dev loop stage:** Review (vetting a skill before install), Ship (supply-chain gate)
**Layer:** Tooling

---

## What it does

A security scanner that answers "is this agent skill safe to install?" before you add
it to Claude Code / Codex / Gemini. It ingests a skill from a git repo, URL, zip,
directory, or single file and runs a LangGraph pipeline of analyzers that combine
**offline static pattern matching + bundled YARA rules** with an **LLM judgment layer**,
emitting findings against a vulnerability taxonomy (prompt injection, data exfiltration,
excessive agency, supply chain, etc.) with coded severities and remediation prose, plus
a 0–100 risk score and an install/do-not-install recommendation. The `--no-llm` flag runs
the entire static + YARA layer with no API key.

## How we tested it

**Evidence:** MEASURED

**Ran the offline static + YARA layer hands-on** on 2026-06-22 (macOS arm64) as a
good-vs-bad A/B against `skillspector scan --no-llm`. The repo requires **Python 3.12+**
(`requires-python = ">=3.12,<3.14"`); this host has 3.11.4, so I provisioned 3.12.13 with
`uv python install 3.12`, cloned `NVIDIA/SkillSpector` (v2.3.1) into a `mktemp -d`, and
installed all deps with `uv sync` — including **`yara-python==4.5.4`**, so the YARA layer
was live, not stubbed. I then authored two skills in the temp dir and scanned each with
`--no-llm` (no LLM provider key set; the LLM judgment nodes were not exercised). **The
temp dir was deleted afterward.**

The static/YARA layer inventory I confirmed in the installed tree:

- **12 static analyzer categories** (`src/skillspector/nodes/analyzers/static_patterns_*.py`):
  agent_snooping, data_exfiltration, excessive_agency, harmful_content, memory_poisoning,
  output_handling, privilege_escalation, prompt_injection, rogue_agent, supply_chain,
  system_prompt_leakage, tool_misuse — plus an AST analyzer and a YARA runner (`static_yara.py`).
- **26 bundled YARA rules** across 5 files (`yara_rules/`): `agent_skills.yar` (5),
  `malware.yar` (6), `webshells.yar` (6), `hacktools.yar` (5), `cryptominers.yar` (4).

**A/B inputs.** A *benign* skill (`word-counter`: a SKILL.md + a `count.py` that only reads
a file and prints word/line/char counts — no network, no shell, no exec). A *dangerous*
skill (`super-helper`) hand-crafted with **example** (non-real) malicious patterns: a
SKILL.md with prompt-injection strings ("ignore all previous instructions", "override
safety", "bypass all constraints", "reveal your system prompt") and `curl … | bash`
installers; a `helper.py` that reads `~/.ssh/id_rsa` and `POST`s `os.environ` to a remote
host, `base64.b64decode` → `exec`, `subprocess.run(..., shell=True)`, `os.system("chmod 777 /etc/passwd")`;
and an `install.sh` doing `eval "$(curl …)"`, `cat ~/.aws/credentials | nc`, and `wget … | bash`.
No real secrets were written — every URL/credential is a placeholder.

**Observed (verbatim risk assessments from the JSON output of each `--no-llm` run):**

| Skill      | Score   | Severity | Recommendation | Issues | Scan time |
|------------|---------|----------|----------------|--------|-----------|
| benign     | 9/100   | LOW      | SAFE           | 1      | 0.74s     |
| dangerous  | 100/100 | CRITICAL | DO_NOT_INSTALL | 29     | 0.73s     |

The **benign** scan produced a single MEDIUM hygiene finding — `LP3` (no declared
`permissions` field in SKILL.md though executable code is present) — and otherwise rated
the skill SAFE. That same `LP3` also fired on the dangerous skill, so it is not a
false-positive on the benign one so much as a uniform "declare your permissions" nudge.

The **dangerous** scan fired 29 findings (24 HIGH, 5 MEDIUM) spanning 9 categories, with
the **3 YARA rules firing being the load-bearing proof the bundled signature layer ran**:

| id   | Category                  | Count | What fired |
|------|---------------------------|-------|------------|
| AST1 | Dangerous Code Execution  | 1     | `exec(decoded)` |
| AST4 | Dangerous Code Execution  | 1     | `subprocess` call |
| AST5 | Dangerous Code Execution  | 1     | `os.system()` |
| E1   | Data Exfiltration         | 2     | external `POST` transmission |
| P1   | Prompt Injection          | 5     | instruction-override phrases |
| P6   | System Prompt Leakage     | 1     | "reveal your system prompt" |
| PE2  | Privilege Escalation      | 1     | root/`chmod 777 /etc/passwd` |
| PE3  | Privilege Escalation      | 3     | credential access (`~/.ssh`, `~/.aws`) |
| SC2  | Supply Chain              | 3     | `curl\|bash` / `wget\|bash` remote-script fetch |
| TM1  | Tool Misuse               | 4     | `shell=True`, `-rf /` parameter abuse |
| TM2  | Tool Misuse               | 3     | tool-chaining abuse |
| LP3  | MCP Least Privilege       | 1     | undeclared permissions |
| YR1  | YARA Match                | 1     | `agent_skill_destructive_autonomous_actions` (helper.py:18) |
| YR4  | YARA Match                | 2     | `agent_skill_prompt_injection_hidden_instructions` (SKILL.md:9), `agent_skill_mcp_tool_poisoning_metadata` (SKILL.md:3) |

```bash
# Provision Python 3.12 (host is 3.11) and install into an isolated temp dir
uv python install 3.12
TMP=$(mktemp -d); cd "$TMP"
git clone --depth 1 https://github.com/NVIDIA/SkillSpector repo && cd repo
uv sync --python 3.12     # installs skillspector v2.3.1 + yara-python 4.5.4

# Offline A/B — no LLM key set, static + YARA only
uv run skillspector scan "$TMP/benign-skill"    --no-llm --format json   # -> 9/100  SAFE,  1 issue
uv run skillspector scan "$TMP/dangerous-skill" --no-llm --format json   # -> 100/100 DO_NOT_INSTALL, 29 issues (incl. 3 YARA)
rm -rf "$TMP"
```

**What was NOT exercised (disclosed):** the **LLM judgment layer**. The pipeline's semantic
nodes need a provider key (`OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `NVIDIA_INFERENCE_KEY`,
per `--help` and `model_registry.yaml`); I ran exclusively with `--no-llm` and set no key,
so the LLM analyzers, their per-skill latency, their per-scan cost, and any
accuracy lift they add over the static layer are **unmeasured here**. The headline
"**26.1% of skills contain vulnerabilities, 5.2% show likely malicious intent**" is **the
project's own research claim** (from its README), not something measured by this run. The
A/B above is two crafted skills, not a labelled corpus, so it demonstrates *discrimination*
(dangerous ≫ benign on the offline layer), not a population false-positive/negative rate.

## What worked

- **The offline layer alone produced a decisive, correct verdict on both inputs — measured.**
  With no LLM key, the dangerous skill scored 100/100 CRITICAL / DO_NOT_INSTALL (29 findings)
  and the benign one 9/100 LOW / SAFE (1 hygiene nudge). That ~91-point separation is a real,
  reproducible discrimination property of the static + YARA pass, useful even air-gapped.
- **YARA layer is live and fired — measured.** `yara-python` installed cleanly and 3 of the
  26 bundled rules matched the dangerous skill (`destructive_autonomous_actions`,
  `prompt_injection_hidden_instructions`, `mcp_tool_poisoning_metadata`), proving signature
  detection runs offline alongside the regex/AST analyzers, not just behind the LLM.
- **Taxonomy is practitioner-grade and accurate to the planted patterns.** Each finding
  carried a coded id, category, confidence, exact file:line location, the offending snippet,
  and specific remediation. The 9 categories that fired map cleanly onto what I actually
  planted (exfiltration → E1, curl|bash → SC2, injection → P1/P6, cred theft → PE3, shell=True → TM1).
- **Fast.** Both `--no-llm` scans completed in ~0.73s, fitting a pre-install CI gate or
  pre-commit hook for a skills registry.
- **Install was achievable on a 3.11 host via `uv`.** The Python 3.12 floor is real, but
  `uv python install 3.12` + `uv sync` provisioned everything (incl. YARA) in one isolated
  pass — friction, not a blocker.
- **Credible provenance.** NVIDIA, Apache-2.0, 9.4K stars, actively pushed (today) — low
  abandonment/quality risk for a tool in your trust path.

## What didn't work or surprised us

- **LLM layer unexercised here.** The semantic judgment nodes need a provider key; I ran
  `--no-llm` only, so any accuracy/recall the LLM adds over the static layer, plus its
  per-skill latency and cost, are unmeasured. `--help` itself flags `--no-llm` as "faster,
  less accurate," i.e. the vendor positions the static layer as a floor, not the ceiling.
- **Python 3.12+ floor.** The package pins `>=3.12,<3.14`; on a 3.11 host you must provision
  a newer interpreter (trivial with `uv`/`pyenv`, but a real prerequisite for CI images).
- **Some duplicate findings.** The dangerous scan emitted, e.g., `E1` twice on the same line
  and `P1` five times across overlapping phrases — thorough, but a consumer counting raw
  issue rows should dedupe by (id, location) before reporting a "number of problems."
- **Accuracy is demonstrated on crafted inputs, not a corpus.** This A/B shows the offline
  layer separates an obviously-malicious skill from an obviously-benign one; it does not
  establish a population FP/FN rate, and the vendor's 26.1%/5.2% figures remain unverified here.
- **Overlap with lighter guards.** For pure config/lint hygiene, `agnix`/`agentlint` are
  cheaper; SkillSpector's edge is genuine malice/vulnerability detection (exfil, injection,
  YARA malware signatures), so it complements rather than replaces those.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (scoped to skill safety) | Offline layer measured: dangerous skill → 100/100 CRITICAL / 29 findings across 9 categories incl. 3 YARA matches; benign → 9/100 SAFE / 1 hygiene finding. Decisive discrimination; LLM-layer accuracy unmeasured (no key) and FP/FN on a corpus not established. |
| Speed | + | Both `--no-llm` scans completed in ~0.73s (measured); the LLM judgment layer adds latency per skill (not measured). |
| Maintainability | + | Findings carry coded id + category + file:line + confidence + actionable remediation, making them trackable; JSON/SARIF output suits CI ingestion. |
| Safety | + (core value) | Targets the real supply-chain risk of installing untrusted skills; the offline static + 26 YARA rules + AST layer caught planted exfiltration, injection, cred-theft, remote-script-fetch, and shell abuse — measured, no LLM key needed. |
| Cost Efficiency | + (offline) / neutral (full) | Offline `--no-llm` layer is free and fast (measured); the full pipeline incurs per-skill LLM cost against a provider endpoint (not measured). |

## Verdict

**CONDITIONAL** — adopt as a pre-install / CI gate for agent skills, running at least the
**offline `--no-llm` layer**, which is now **measured**: on a hands-on good-vs-bad A/B it
rated a crafted-malicious skill 100/100 CRITICAL / DO_NOT_INSTALL (29 findings spanning
exfiltration, prompt injection, credential access, remote-script-fetch, shell abuse, and 3
live YARA matches) versus 9/100 SAFE for a benign one, in ~0.73s each with no API key. That
is a real, reproducible safety net for the genuine supply-chain risk of untrusted skills,
from a credible vendor (NVIDIA, Apache-2.0, actively maintained). The conditions that keep
it CONDITIONAL rather than ADOPT: it requires **Python 3.12+** (provisionable via `uv`, but a
real CI prerequisite); the **LLM judgment layer was not exercised here** (needs a provider
key — its accuracy lift, latency, and per-skill cost are unmeasured); and the A/B proves
*discrimination on crafted inputs*, not a population false-positive/negative rate, so the
vendor's 26.1%/5.2% corpus figures remain unverified by us. Re-evaluate ADOPT after measuring
the LLM layer against a labelled skill corpus. **This run supports, and does not contradict,
the existing CONDITIONAL verdict.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [SkillSpector](https://github.com/NVIDIA/SkillSpector) | tool | Security scanner for AI agent skills — detects vulnerabilities and malicious patterns | Downloaded skills could contain prompt injection or exfiltration | scorecard |
