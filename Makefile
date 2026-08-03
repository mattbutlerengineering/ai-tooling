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
# staleness line is a report-only trailer (offline) — its `-` prefix keeps a stale
# eval from failing the gate; only **Last verified:** field presence is gated.

.PHONY: check check-offline fix

check:
	python3 audit-evals.py --offline
	python3 audit-evals.py --selftest
	python3 -m unittest -q test_automation
	python3 reconcile-counts.py --check
	python3 backfill-evidence.py --check
	python3 backfill-lastverified.py --check
	python3 tier-stack.py --check
	python3 triage.py --check
	python3 watchlist.py --check
	./sync-plugin-docs.sh --check
	python3 audit-evals.py --installs
	-python3 audit-evals.py --staleness

# Everything in `check` except the network install resolver (A) — the fast local loop.
# `check` remains the canonical gate; this is for iterating without paying ~22s of
# network round trips per run. CI always runs the full `check`.
# TestIntegrityMakefile pins that this stays `check` minus exactly that one line.
check-offline:
	python3 audit-evals.py --offline
	python3 audit-evals.py --selftest
	python3 -m unittest -q test_automation
	python3 reconcile-counts.py --check
	python3 backfill-evidence.py --check
	python3 backfill-lastverified.py --check
	python3 tier-stack.py --check
	python3 triage.py --check
	python3 watchlist.py --check
	./sync-plugin-docs.sh --check
	-python3 audit-evals.py --staleness

fix:
	python3 reconcile-counts.py
	python3 backfill-evidence.py
	python3 backfill-lastverified.py
	python3 tier-stack.py
	python3 triage.py
	python3 watchlist.py
	./sync-plugin-docs.sh
	@$(MAKE) check
