# Single entrypoint for the catalog integrity gates (#114).
#
#   make check   verify mode — runs exactly what .github/workflows/integrity.yml
#                enforces, in --check order, exiting non-zero on the first failure.
#   make fix     apply mode — runs the apply-mode fixers in dependency order, then
#                re-runs `check` so a clean exit means the tree is actually green.
#   make check-offline
#                `check` minus the network install resolver — the fast local loop.
#                NOT the canonical gate: it cannot catch a broken install command,
#                so CI runs the full `check` and so should you before pushing.
#
# CI's `audit` job calls `make check`, so the two cannot drift. Keep this target in
# lockstep with the gate set: a gate added to integrity.yml must be added here (and
# test_automation.py's TestIntegrityMakefile pins that they stay in sync).
#
# `check`'s install resolver (audit-evals.py --installs) hits the network and uses
# `gh`, so it needs gh auth / GH_TOKEN. `fix`'s fixers are offline, but its trailing
# `check` re-run inherits that same network/gh requirement. The final `-`-prefixed
# staleness lines are report-only trailers (both offline) — the `-` prefix keeps a
# stale eval or a stale metadata cache from failing the gate. Only **Last verified:**
# field presence is gated; L (evals) and R (repo-metadata.json) age on the calendar,
# and their only fix needs the network CI must not depend on.
#
# `check-stars.py --check` is the one gate with no counterpart in `fix`, and that is
# deliberate (#377): a missing **Stars:** value cannot be generated, only declared — the
# author knows whether the file has one subject, several contenders, or none. Dropping
# `--check` there turns it report-only in one word, which is how the gate-vs-report call
# stays reversible; TestStarConvention pins both modes regardless of which is wired.
#
# `verify-installs.py --check` is the second such gate, for the same shape of reason
# (#382/ADR-0006): it validates that every ADOPT/KEEP ledger row DECLARES a well-formed
# `Install evidence` value, never that the value is still true. The apply side
# (`--record`) reads one laptop's install records, so it is deliberately absent from
# `fix` — CI has no lockfile, and a build that failed because a machine changed would be
# worse than the drift it caught.
#
# ruff and mypy (#388) are the ONLY gates that are not pure stdlib — every other one runs
# on python3 + gh + node. They are pinned in requirements-dev.txt, because an unpinned
# linter turns an upstream rule addition into a red build on an unrelated PR. Install
# them once:
#
#   python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
#
# and either put .venv/bin on PATH or point the two variables below at it:
#
#   make check RUFF=.venv/bin/ruff MYPY=.venv/bin/mypy
#
# They run FIRST in both check targets: a syntax error should surface before twelve
# data gates parse the tree with it.
RUFF ?= ruff
MYPY ?= mypy

.PHONY: check check-offline fix lint lint-preflight

# A missing linter must say what to install, not "command not found: ruff".
lint-preflight:
	@command -v $(RUFF) >/dev/null 2>&1 || { \
	  echo "ruff not found. Install the dev pins:"; \
	  echo "  python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt"; \
	  echo "  make check RUFF=.venv/bin/ruff MYPY=.venv/bin/mypy"; exit 1; }
	@command -v $(MYPY) >/dev/null 2>&1 || { \
	  echo "mypy not found — see requirements-dev.txt"; exit 1; }

# Runnable alone while iterating on a script.
lint: lint-preflight
	$(RUFF) check
	$(MYPY)

check: lint-preflight
	$(RUFF) check
	$(MYPY)
	python3 audit-evals.py --offline
	python3 audit-evals.py --selftest
	python3 -m unittest -q test_automation
	python3 reconcile-counts.py --check
	python3 backfill-evidence.py --check
	python3 backfill-lastverified.py --check
	python3 check-stars.py --check
	python3 verify-installs.py --check
	python3 tier-stack.py --check
	python3 triage.py --check
	python3 watchlist.py --check
	./sync-plugin-docs.sh --check
	python3 audit-evals.py --installs
	-python3 audit-evals.py --staleness
	-python3 audit-evals.py --metadata-staleness

# Everything in `check` except the network install resolver (A) — the fast local loop.
# `check` remains the canonical gate; this is for iterating without paying ~22s of
# network round trips per run. CI always runs the full `check`.
# TestIntegrityMakefile pins that this stays `check` minus exactly that one line.
check-offline: lint-preflight
	$(RUFF) check
	$(MYPY)
	python3 audit-evals.py --offline
	python3 audit-evals.py --selftest
	python3 -m unittest -q test_automation
	python3 reconcile-counts.py --check
	python3 backfill-evidence.py --check
	python3 backfill-lastverified.py --check
	python3 check-stars.py --check
	python3 verify-installs.py --check
	python3 tier-stack.py --check
	python3 triage.py --check
	python3 watchlist.py --check
	./sync-plugin-docs.sh --check
	-python3 audit-evals.py --staleness
	-python3 audit-evals.py --metadata-staleness

fix: lint-preflight
	$(RUFF) check --fix
	python3 reconcile-counts.py
	python3 backfill-evidence.py
	python3 backfill-lastverified.py
	python3 tier-stack.py
	python3 triage.py
	python3 watchlist.py
	./sync-plugin-docs.sh
	@$(MAKE) check
