# Source qualification preparation RCA

The first run stopped at host-skills because the new isolated workspace lacked the existing immutable legacy checkouts. Those exact clean checkouts were linked under the new ignored .local directory; no legacy lock or source changed.

The second run passed 18 checks, then correctly rejected the old Desktop Host-build input manifest. The new Host code had been locally committed, but its derived Desktop build manifest had not yet been frozen. The canonical --freeze-commit entry generated that manifest; no manual generated edit was used.

The third invocation overlapped the tail of the freeze/commit operation because the command had yielded a running session. All 19 checks exited zero, but it recorded Desktop 3219113 while the final input lock was committed as 841f7c7. That result is retained as SOURCE_METADATA_STALE and is not current qualification. It is an orchestration/provenance error, not a product failure or evidence of Runtime incompatibility.

Correction: finish and join the commit operation first, freeze all six clean source identities, then run exactly one read-only qualification and compare every identity/status after completion. Do not modify sources or start a build while that check runs. No product, Runtime, database, service, model or paid verification is added by this source-only check. Earlier failure/raw logs remain unchanged.
