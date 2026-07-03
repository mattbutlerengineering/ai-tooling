# Single entrypoint for the catalog integrity gates (#114).
#
#   make check   verify mode — runs exactly what .github/workflows/integrity.yml
#                enforces, in --check order, exiting non-zero on the first failure.
#   make fix     apply mode — runs the apply-mode fixers in dependency order, then
#                re-runs `check` so a clean exit means the tree is actually green.
#
# CI's `audit` job calls `make check`, so the two cannot drift. Keep this target in
# lockstep with the gate set: a gate added to integrity.yml must be added here (and
# test_automation.py's TestIntegrityMakefile pins that they stay in sync).
#
# `check`'s last step (audit-evals.py --installs) hits the network and uses `gh`,
# so it needs gh auth / GH_TOKEN. `fix`'s fixers are offline, but its trailing
# `check` re-run inherits that same network/gh requirement.

.PHONY: check fix

check:
	python3 audit-evals.py --offline
	python3 audit-evals.py --selftest
	python3 -m unittest -q test_automation
	python3 reconcile-counts.py --check
	python3 backfill-evidence.py --check
	python3 tier-stack.py --check
	./sync-plugin-docs.sh --check
	python3 audit-evals.py --installs

fix:
	python3 reconcile-counts.py
	python3 backfill-evidence.py
	python3 tier-stack.py
	./sync-plugin-docs.sh
	@$(MAKE) check
