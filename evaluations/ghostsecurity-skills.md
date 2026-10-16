# Evaluation: ghostsecurity/skills

**Repo:** [ghostsecurity/skills](https://github.com/ghostsecurity/skills)
**Stars:** 396 | **Last updated:** 2026-03-11 | **License:** Apache-2.0
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Claude Code plugin providing 7 skills for application security scanning, covering the full AppSec pipeline: repository context mapping (`ghost-repo-context`), static code analysis (`ghost-scan-code`), dependency vulnerability scanning (`ghost-scan-deps`), secrets detection (`ghost-scan-secrets`), finding validation (`ghost-validate`), HTTP proxy for live testing (`ghost-proxy`), and combined reporting (`ghost-report`). Each skill is a multi-step orchestrator that spawns subagents for planning, scanning, verifying, and summarizing — not just a prompt that tells the agent to "look for vulnerabilities."

The scan-code skill alone covers 103 vulnerability vectors across 4 project types (backend, frontend, mobile, library), organized by OWASP category (injection, authz, authn, crypto, data exposure, etc.). Each vector has per-severity thresholds, CWE mappings, file-candidate heuristics, and multi-criteria validation rules. The verifier agent independently re-checks every finding against the source code before it reaches the report.

Update from the 2026-10-16 run: the repo is now a two-plugin marketplace (`ghost` and `exo`), the scan-code index lists **102** vectors (the 103 above is the older figure), and the three helper binaries are published as open-source Apache-2.0 repos (`ghostsecurity/poltergeist`, `ghostsecurity/wraith`, plus Reaper). The earlier note that the scanners are closed-source no longer holds.

## How we tested it

**Evidence:** RUN

**Hands-on** — cloned `ghostsecurity/skills` @ `25fdf06`, built the two scanner binaries the skills shell out to from source (`ghostsecurity/poltergeist` @ `20d3fa3`, `ghostsecurity/wraith` @ `1c5f44c`), and ran each against a disclosed planted-defect fixture under `/tmp`, next to an incumbent scanner and a naive baseline. Ran `claude plugin validate` on the plugin and parsed all 7 SKILL.md frontmatters and the scan-code criteria index. The LLM-driven layer (the skills' subagent orchestration) was out of reach without model credentials; see "What didn't work".

```
# build (installer's version lookup is walled here; GitHub release assets unreachable)
apt-get install -y libhyperscan-dev
(cd poltergeist && CGO_ENABLED=1 go build -o bin/poltergeist ./cmd/poltergeist)
(cd wraith && go build -o bin/wraith ./cmd/wraith)
go install github.com/google/osv-scanner/v2/cmd/osv-scanner@v2.0.2   # wraith shells out to it
go install github.com/zricethezav/gitleaks/v8@v8.18.4               # incumbent baseline
pip install pip-audit                                                # incumbent baseline

# secrets: 10 planted secrets (S1-S10) + a decoys file, scored by file:line
poltergeist -format json -output pg.json secrets/
gitleaks detect --no-git -s secrets -f json -r gl.json
grep -rniE 'password|secret|api[_-]?key|token|BEGIN .*PRIVATE' secrets/
python3 score.py
poltergeist: planted caught 8/10 [2, 3, 5, 6, 7, 8, 9, 10]  missed [1, 4]  total flagged lines 8  decoy-file hits 0
gitleaks:    planted caught 8/10 [1, 2, 3, 4, 5, 6, 8, 9]  missed [7, 10] total flagged lines 9  decoy-file hits 1
grep:        planted caught 6/10 [2, 3, 5, 6, 8, 9]       missed [1, 4, 7, 10] total flagged lines 11 decoy-file hits 5

# deps: requirements.txt with 5 known-vulnerable pins + 2 clean pins
wraith scan --format json --output wr.json requirements.txt     # 5 packages, 123 vulnerabilities
osv-scanner scan source -L requirements.txt --format json       # django 75, flask 8, pyyaml 4, requests 10, urllib3 26 = 123
pip-audit -r requirements.txt --no-deps --disable-pip           # 120 vulnerabilities in 5 packages
# clean pins (requests-toolbelt==1.0.0, certifi==2024.8.30): 0 findings in all three

# plugin package + scan-code criteria index
claude plugin validate plugins/ghost    # Validation passed
python3 count_vectors.py                # backend 47, frontend 15, library 14, mobile 26 = 102 indexed, 0 missing from the criteria files
```

Wall-clock on the fixture: poltergeist 1.5 s (163 rules, Hyperscan engine), gitleaks 0.05 s; wraith 1.5 s, pip-audit 1.3 s.

## Test design

- **Task/corpus:** `/tmp/eval-ghostsecurity-skills/fx/secrets` — 10 synthetic secrets in 9 files (S1 AWS access key id, S2 AWS secret key, S3 GitHub PAT, S4 OpenAI-shaped key without the `T3BlbkFJ` marker, S5 Stripe live key, S6 Slack bot token, S7 Postgres URL with password, S8 RSA private key block, S9 hex `api_key`, S10 OpenAI `sk-proj-` key with the marker and 74+74 chars) plus a `decoys.py` of placeholders, the documented AWS example key id, an env lookup and a sha256 hash. `fx/deps/requirements.txt` — django==2.2.0, requests==2.19.0, pyyaml==5.3, flask==0.12.2, urllib3==1.24.1 (vulnerable) and requests-toolbelt==1.0.0, certifi==2024.8.30 (clean). The values are random strings generated with a fixed seed; none is a live credential.
- **Baseline:** a keyword `grep` (no tool), and the incumbents `gitleaks` v8.18.4 (secrets) and `osv-scanner` v2.0.2 / `pip-audit` 2.10.1 (deps).
- **Metric:** planted secrets caught (k/10) by file:line, hits inside the decoys file; vulnerable packages found (k/5), clean packages flagged (k/2), vulnerability count.
- **Reproduce:** the command block above. Fixture generator and scorer were throwaway scripts under `/tmp`; the planted-line convention is a `S<n>` comment on the line before each secret.

### Test design — skills

- **Triggering:** not measured. Firing is decided by the model reading each SKILL.md `description`; with no model credentials there is no deterministic score to report. What was checked mechanically: all 7 skills parse with a `name` and a `description` (232-518 chars), and two of them (`ghost-proxy`, `ghost-validate`) declare no `allowed-tools`.
- **Output A/B:** not measured for the same reason. The part of the pipeline that is deterministic (the binaries) is what the secrets and deps comparisons above measure; the AI analysis layered on top (exploitability, context assessment, the verifier agent, `ghost-scan-code` SAST) was not exercised.
- **Not run:** `ghost-scan-code`, `ghost-validate`, `ghost-proxy`, the Reaper proxy and the subagent orchestration.

## What worked

- **Poltergeist is a credible secrets scanner.** On the fixture it caught 8 of 10 planted secrets with zero hits on the decoys file, against 6 of 10 and 5 decoy hits for keyword grep. It is on par with gitleaks by count (8 of 10 each) with a different miss set: poltergeist alone caught the Postgres URL (S7) and the full-length OpenAI key (S10); gitleaks alone caught the AWS access key id (S1) and the marker-less OpenAI-shaped string (S4).
- **Redaction and entropy filtering are on by default** — the JSON output carries `redacted` values and per-rule entropy thresholds, so scan output is safe to paste into a report.
- **Wraith matches the incumbent exactly.** It found 5 of 5 vulnerable pins, 0 of 2 clean pins flagged, and 123 vulnerabilities — identical to `osv-scanner` run directly (75+8+4+10+26). `pip-audit` found 120 in the same 5 packages.
- **Package hygiene:** `claude plugin validate` passes; the scan-code criteria index lists 102 vectors and every indexed vector has an entry in its platform criteria file.
- **The binaries are now open source (Apache-2.0)** and built from source here in under a minute each, which removes the closed-binary trust objection the earlier review raised.

## What didn't work or surprised us

- **The skills themselves were not exercised.** Triggering, the subagent pipeline, the verifier agent and the DAST validation all need a model; the verdict below rests on the tool layer only. The headline claim (AI judgment on top of deterministic tools produces better findings) is untested here.
- **Poltergeist needs CGO and Hyperscan to build** (`libhyperscan-dev`); a `CGO_ENABLED=0` build fails. The skills install the prebuilt release binary instead, so this only matters when building from source.
- **Wraith is a thin wrapper over osv-scanner** and fails at runtime with "osv-scanner not found" unless that binary is on `PATH`. The tool layer adds no detection beyond the incumbent osv-scanner; any value is in the skill layer's exploitability analysis.
- **Poltergeist does not flag a bare AWS access key id** (S1) and its OpenAI rule requires the exact `T3BlbkFJ` shape with 74 characters each side, so S4 is a fixture-shape miss rather than a detector bug. Gitleaks flags the documented AWS example key (`AKIAIOSFODNN7EXAMPLE`) in the decoys file; poltergeist does not.
- **Fixture caveat:** secrets are synthetic and the rules are pattern-based, so recall on real leaked credentials may differ; n=10 planted secrets and 5 vulnerable pins is a smoke-test sample, not a benchmark.
- **Install path:** the installer scripts the skills run (`curl ... | bash` against `updates.ghostsecurity.ai`) could not resolve a version in this sandbox, so the shipped binaries were not the ones tested.
- **Tool restrictions are still inconsistent** across skills (see the `allowed-tools` note under Test design).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Secrets: poltergeist 8/10 vs gitleaks 8/10 vs grep 6/10 with 0/1/5 decoy hits; deps: wraith 5/5 vulnerable, 0/2 false flags, 123 vulns, identical to osv-scanner. The AI verifier's effect on false positives was not measured |
| Speed | neutral | Scanners finish in 1.5 s on the fixture; the multi-agent skill pipeline was not timed |
| Maintainability | neutral | Findings feed review; no direct effect on code structure |
| Safety | + | Real scanners with redaction on by default and now open-source binaries; no better than gitleaks/osv-scanner on detection by count |
| Cost Efficiency | neutral | The scanners are free and local; Wraith queries the OSV API. The subagent orchestration's token cost was not measured |
| Verifiability | + | Scanner output is structured JSON with rule IDs, entropy and file:line, so each finding can be checked against the source mechanically; the AI-verified layer was not assessed |

## Verdict

**discovery-log — tentative read** — the tool layer works and is on par with the incumbents (poltergeist 8/10 planted secrets with 0 decoy hits vs gitleaks 8/10 with 1; wraith identical to osv-scanner at 123/123 vulnerabilities), but the skills that make this a catalog entry (SAST, verifier, DAST, orchestration) need a model to exercise and were not measured, so there is no evidence yet that the package beats `gitleaks` + `osv-scanner` + `security-guidance`. A human or credentialed run of `ghost-scan-code` against a planted-vulnerability app is what a real read needs.

## Triage note

Left at `discovery-log` — no SKIP: the tools work, the repo is active (last commit 2026-09-28) and not redundant at the skill layer. Earlier triage (2026-08-04) left it for the P0/eval-runner lane; this pass reached RUN evidence on the scanner binaries only.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ghostsecurity/skills](https://github.com/ghostsecurity/skills) | skill | AppSec skills for AI coding agents — OWASP, threat modeling, secure defaults | Need security-focused skills that catch vulnerabilities during development, not just review | SkillSpector, security-guidance |
